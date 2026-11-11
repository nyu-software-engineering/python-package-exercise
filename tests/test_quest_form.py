from pathlib import Path

import pytest
from playwright.sync_api import expect

ROOT = Path(__file__).resolve().parents[1]
PLANNER_URL = "https://planner.test/"
SAVED_QUEST = {
    "id": "q1",
    "title": "Study math",
    "durationMinutes": 60,
    "fantasyDescription": "Decipher an Ancient Scroll",
    "xpReward": 60,
}

@pytest.fixture
def planner(page):
    html = (ROOT / "templates" / "quest_form.html").read_text(encoding="utf-8")
    script = ROOT / "static" / "quest_form.js"

    page.route(
        PLANNER_URL,
        lambda route: route.fulfill(
            content_type="text/html", body="<!doctype html>\n" + html
        ),
    )
    page.route(
        "**/static/quest_form.js",
        lambda route: route.fulfill(path=script, content_type="text/javascript"),
    )
    page.goto(PLANNER_URL)
    return page


def fill_quest(page, title="Study math", minutes="60"):
    page.get_by_label("Title").fill(title)
    page.get_by_label("Minutes").fill(minutes)


def test_successful_submit_sends_one_request(planner):
    planner.route(
        "**/quests",
        lambda route: route.fulfill(status=201, json=SAVED_QUEST),
    )
    fill_quest(planner)

    with planner.expect_request("**/quests") as request:
        attempts = planner.locator("#quest-form").evaluate("""
            form => {
                const send = window.fetch.bind(window);
                let attempts = 0;
                window.fetch = (...args) => {
                    attempts += 1;
                    return send(...args);
                };

                form.addEventListener("quest:created", event => {
                    window.savedQuest = event.detail;
                });

                form.requestSubmit();
                form.requestSubmit();
                return attempts;
            }
        """)

    assert attempts == 1
    assert request.value.method == "POST"
    assert request.value.post_data_json == {
        "title": "Study math",
        "durationMinutes": 60,
    }
    expect(planner.get_by_role("status")).to_have_text(
        "Quest created: Study math — Decipher an Ancient Scroll "
        "(60 min, 60 planned XP)."
    )
    expect(planner.get_by_label("Title")).to_have_value("")
    assert planner.evaluate("window.savedQuest") == SAVED_QUEST


def test_invalid_inputs_show_field_errors(planner):
    fill_quest(planner, title="", minutes="2.5")
    planner.get_by_role("button", name="Create Quest").click()

    expect(planner.locator("#quest-title-error")).to_have_text(
        "Enter a quest title."
    )
    expect(planner.locator("#quest-minutes-error")).to_have_text(
        "Enter a positive whole number of minutes."
    )


def test_failed_save_keeps_inputs_and_allows_retry(planner):
    planner.route("**/quests", lambda route: route.fulfill(status=500))
    fill_quest(planner)
    button = planner.get_by_role("button", name="Create Quest")
    button.click()

    expect(planner.get_by_role("status")).to_have_text(
        "Could not save the quest. Try again."
    )
    expect(planner.get_by_label("Title")).to_have_value("Study math")
    expect(planner.get_by_label("Minutes")).to_have_value("60")
    expect(button).to_be_enabled()
