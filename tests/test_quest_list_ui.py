from pathlib import Path

import pytest
from jinja2 import Environment, FileSystemLoader
from playwright.sync_api import expect

ROOT = Path(__file__).resolve().parents[1]
URL = "https://planner.test/"
QUEST = {
    "id": "q1", "title": "Study math", "durationMinutes": 60,
    "fantasyDescription": "Decipher an Ancient Scroll", "status": "pending",
    "xpReward": 60, "completedAt": None,
}
COMPLETED = {
    **QUEST, "id": "q2", "title": "Do laundry", "durationMinutes": 50,
    "fantasyDescription": "Restore Order to the Kingdom", "xpReward": 50,
    "status": "completed", "completedAt": "2026-11-10T21:00:00+00:00",
}


@pytest.fixture
def planner(page):
    environment = Environment(loader=FileSystemLoader(ROOT / "templates"), autoescape=True)
    html = environment.get_template("planner.html").render(csrf_token="page-token")
    page.route(URL, lambda route: route.fulfill(content_type="text/html", body=html))

    def asset(route):
        name = route.request.url.rsplit("/", 1)[-1]
        content_type = "text/css" if name.endswith(".css") else "text/javascript"
        route.fulfill(path=ROOT / "static" / name, content_type=content_type)

    page.route("**/static/*", asset)
    page.route("**/progress", lambda route: route.fulfill(json={"totalXP": 150, "level": 2}))

    def quests(route):
        status = route.request.url.partition("?status=")[2]
        rows = [QUEST, COMPLETED]
        route.fulfill(json=[quest for quest in rows if not status or quest["status"] == status])

    page.route("**/quests*", quests)
    page.route("**/quests/q1", lambda route: route.fulfill(json=QUEST))
    page.route("**/quests/q2", lambda route: route.fulfill(json=COMPLETED))
    page.goto(URL)
    return page


def test_load_filter_and_show_all_detail_fields(planner):
    expect(planner.locator("#progress-summary")).to_have_text("150 XP | Level 2")
    expect(planner.locator("#quest-list li")).to_have_count(2)
    planner.get_by_label("Show quests").select_option("completed")
    expect(planner.locator("#quest-list li")).to_have_count(1)
    planner.get_by_role("button", name="View details for Do laundry").click()
    detail = planner.locator("#quest-detail")
    expect(detail).to_be_visible()
    expect(detail).to_contain_text("Do laundry")
    expect(detail).to_contain_text("Restore Order to the Kingdom")
    expect(detail).to_contain_text("50 minutes")
    expect(detail).to_contain_text("Completed")
    expect(detail).to_contain_text("50 XP")
    expect(detail).to_contain_text("q2")
    expect(detail.locator("time")).to_have_attribute("datetime", COMPLETED["completedAt"])


def test_empty_list_and_refresh(planner):
    planner.route("**/quests*", lambda route: route.fulfill(json=[]))
    planner.get_by_role("button", name="Refresh quests").click()
    expect(planner.locator("#list-message")).to_have_text("No quests yet. Create one to get started.")
    expect(planner.locator("#quest-list li")).to_have_count(0)


def test_failed_refresh_keeps_previous_data_and_can_retry(planner):
    expect(planner.locator("#quest-list li")).to_have_count(2)
    planner.route("**/quests*", lambda route: route.fulfill(status=500, json={"error": "Could not load quests."}))
    planner.get_by_role("button", name="Refresh quests").click()
    expect(planner.locator("#list-message")).to_contain_text("Could not load quests.")
    expect(planner.locator("#quest-list li")).to_have_count(2)
    planner.route("**/quests*", lambda route: route.fulfill(json=[QUEST]))
    planner.get_by_role("button", name="Refresh quests").click()
    expect(planner.locator("#quest-list li")).to_have_count(1)
    expect(planner.locator("#list-message")).to_have_text("1 quest shown.")


def test_deleted_detail_shows_error_without_stale_detail(planner):
    planner.route("**/quests/q1", lambda route: route.fulfill(status=404, json={"error": "Quest not found."}))
    planner.get_by_role("button", name="View details for Study math").click()
    expect(planner.locator("#detail-message")).to_have_text("Quest not found. Refresh the list and try again.")
    expect(planner.locator("#quest-detail")).to_be_hidden()


def test_creation_refreshes_saved_list(planner):
    expect(planner.locator("#quest-list li")).to_have_count(2)
    new_quest = {**QUEST, "id": "q3", "title": "Water plants"}

    def save_or_load(route):
        if route.request.method == "POST":
            assert route.request.headers["x-csrf-token"] == "page-token"
            route.fulfill(status=201, json=new_quest)
        else:
            route.fulfill(json=[QUEST, COMPLETED, new_quest])

    planner.route("**/quests", save_or_load)
    planner.get_by_label("Title", exact=True).fill("Water plants")
    planner.get_by_label("Minutes", exact=True).fill("60")
    planner.get_by_role("button", name="Create Quest").click()
    expect(planner.locator("#quest-status")).to_have_text("Quest created.")
    expect(planner.locator("#quest-list li")).to_have_count(3)
    expect(planner.get_by_role("button", name="View details for Water plants")).to_be_visible()


def test_untrusted_quest_text_is_not_html(planner):
    malicious = {**QUEST, "title": '<img src=x onerror="alert(1)">', "fantasyDescription": "<script>alert(1)</script>"}
    planner.route("**/quests", lambda route: route.fulfill(json=[malicious]))
    planner.route("**/quests/q1", lambda route: route.fulfill(json=malicious))
    planner.get_by_role("button", name="Refresh quests").click()
    planner.get_by_role("button", name="View details for " + malicious["title"]).click()
    expect(planner.locator("#quest-detail")).to_contain_text(malicious["fantasyDescription"])
    expect(planner.locator("#quest-list img, #quest-detail img, #quest-detail script")).to_have_count(0)


def test_narrow_layout_does_not_overflow(planner):
    planner.set_viewport_size({"width": 375, "height": 812})
    expect(planner.get_by_label("Title", exact=True)).to_be_visible()
    expect(planner.get_by_label("Show quests")).to_be_visible()
    assert planner.evaluate("document.documentElement.scrollWidth <= window.innerWidth")


def test_late_filter_response_does_not_replace_newer_results(planner):
    expect(planner.locator("#quest-list li")).to_have_count(2)
    planner.evaluate("""quest => {
        const send = window.fetch.bind(window);
        window.fetch = (...args) => {
            if (args[0] === '/quests?status=pending') {
                return new Promise(resolve => {
                    window.releasePending = () => resolve({
                        ok: true, status: 200,
                        json: async () => {
                            window.pendingRead = true;
                            return [quest];
                        },
                    });
                });
            }
            return send(...args);
        };
    }""", QUEST)
    planner.get_by_label("Show quests").select_option("pending")
    planner.wait_for_function("typeof window.releasePending === 'function'")
    planner.get_by_label("Show quests").select_option("completed")
    expect(planner.locator("#quest-list h3")).to_have_text(["Do laundry"])
    planner.evaluate("window.releasePending()")
    planner.wait_for_function("window.pendingRead === true")
    expect(planner.locator("#quest-list h3")).to_have_text(["Do laundry"])
    expect(planner.get_by_label("Show quests")).to_have_value("completed")


def test_progress_error_keeps_last_total_and_allows_refresh(planner):
    expect(planner.locator("#progress-summary")).to_have_text("150 XP | Level 2")
    planner.route("**/progress", lambda route: route.fulfill(status=500))
    planner.get_by_role("button", name="Refresh quests").click()
    expect(planner.locator("#progress-message")).to_have_text("Could not update progress. Try Refresh quests.")
    expect(planner.locator("#progress-summary")).to_have_text("150 XP | Level 2")
    planner.route("**/progress", lambda route: route.fulfill(json={"totalXP": 200, "level": 3}))
    planner.get_by_role("button", name="Refresh quests").click()
    expect(planner.locator("#progress-summary")).to_have_text("200 XP | Level 3")
    expect(planner.locator("#progress-message")).to_have_text("")


def test_detail_buttons_wait_for_refresh_then_allow_retry(planner):
    expect(planner.locator("#quest-list li")).to_have_count(2)
    planner.evaluate("""() => {
        const send = window.fetch.bind(window);
        window.fetch = (...args) => {
            if (args[0] === '/quests') {
                return new Promise(resolve => {
                    window.failRefresh = () => resolve(new Response('', { status: 500 }));
                });
            }
            return send(...args);
        };
    }""")
    planner.get_by_role("button", name="Refresh quests").click()
    view = planner.get_by_role("button", name="View details for Study math")
    expect(view).to_be_disabled()
    planner.evaluate("window.failRefresh()")
    expect(view).to_be_enabled()
    view.click()
    expect(planner.locator("#quest-detail")).to_be_visible()
