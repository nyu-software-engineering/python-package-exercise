"""Exercise browser actions against the real app and a temporary database."""

from contextlib import closing, contextmanager
import sqlite3
from threading import Thread

import pytest
from playwright.sync_api import expect
from werkzeug.serving import make_server

from app import create_app
from storage import initialize_database, load_progress, load_quests


@pytest.fixture
def database(tmp_path):
    path = tmp_path / "planner.db"
    initialize_database(path)

    with closing(sqlite3.connect(path)) as connection:
        connection.execute("UPDATE progress SET totalXP = 90 WHERE id = 1")
        connection.commit()

    return path


@contextmanager
def running_planner(database):
    app = create_app(database)
    server = make_server("127.0.0.1", 0, app, threaded=True)
    thread = Thread(
        target=server.serve_forever,
        kwargs={"poll_interval": 0.05},
        daemon=True,
    )
    thread.start()

    try:
        yield f"http://127.0.0.1:{server.server_port}"
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()
        assert not thread.is_alive(), "The test server did not stop."


@contextmanager
def browser_page(browser, url):
    context = browser.new_context()
    try:
        page = context.new_page()
        page.goto(url)
        yield page
    finally:
        context.close()


@pytest.fixture
def planner(page, database):
    with running_planner(database) as url:
        page.goto(url)
        expect(page.locator("#progress-summary")).to_have_text(
            "90 XP | Level 1"
        )
        expect(page.locator("#quest-list li")).to_have_count(0)
        yield url


def create_from_form(page, title, minutes):
    page.get_by_label("Title", exact=True).fill(title)
    page.get_by_label("Minutes", exact=True).fill(str(minutes))

    with page.expect_response(
        lambda response: response.url.endswith("/quests")
        and response.request.method == "POST"
    ) as saved:
        page.get_by_role("button", name="Create Quest", exact=True).click()

    response = saved.value
    assert response.status == 201
    quest = response.json()

    expect(
        page.get_by_role(
            "button",
            name=f"View details for {title}",
            exact=True,
        )
    ).to_be_visible()

    return quest


def open_details(page, quest):
    page.get_by_role(
        "button",
        name=f"View details for {quest['title']}",
        exact=True,
    ).click()
    expect(page.locator("#detail-id")).to_have_text(quest["id"])
    expect(page.locator("#quest-detail")).to_be_visible()


def complete_from_page(page):
    quest_id = page.locator("#detail-id").inner_text()

    with page.expect_response(
        lambda response: response.url.endswith(
            f"/quests/{quest_id}/complete"
        )
        and response.request.method == "POST"
    ) as completed:
        page.get_by_role(
            "button", name="Complete quest", exact=True
        ).click()

    response = completed.value
    assert response.status == 200
    expect(page.locator("#detail-status")).to_have_text("Completed")
    expect(page.locator("#refresh-quests")).to_be_enabled()

    return response.json()


def test_browser_completion_saves_xp_and_retry_awards_nothing(
    page, planner, database
):
    quest = create_from_form(page, "Study math", 60)

    assert quest["status"] == "pending"
    assert load_quests(database) == [quest]
    assert load_progress(database) == {"totalXP": 90}
    expect(page.locator("#progress-summary")).to_have_text(
        "90 XP | Level 1"
    )

    open_details(page, quest)
    result = complete_from_page(page)

    assert result["awardedXP"] == 60
    assert result["totalXP"] == 150
    assert result["level"] == 2
    assert result["quest"]["completedAt"]
    assert load_quests(database) == [result["quest"]]
    assert load_progress(database) == {"totalXP": 150}
    expect(page.locator("#progress-summary")).to_have_text(
        "150 XP | Level 2"
    )
    expect(page.locator("#completed-note")).to_be_visible()
    expect(page.locator("#quest-actions")).to_be_hidden()

    # Use the browser's session for a real repeated completion request.
    token_response = page.request.get(f"{planner}/csrf-token")
    assert token_response.status == 200
    token = token_response.json()["csrfToken"]

    retry_response = page.request.post(
        f"{planner}/quests/{quest['id']}/complete",
        headers={"X-CSRF-Token": token},
    )

    assert retry_response.status == 200
    assert retry_response.json() == {**result, "awardedXP": 0}
    assert load_progress(database) == {"totalXP": 150}
    assert load_quests(database) == [result["quest"]]

    page.reload()
    expect(page.locator("#progress-summary")).to_have_text(
        "150 XP | Level 2"
    )
    page.get_by_label("Show quests").select_option("completed")
    expect(page.locator("#quest-list li")).to_have_count(1)

    open_details(page, result["quest"])
    expect(page.locator("#completed-note")).to_be_visible()
    expect(page.locator("#detail-completed time")).to_have_attribute(
        "datetime", result["quest"]["completedAt"]
    )


@pytest.mark.parametrize(
    "minutes, expected_xp, expected_level",
    [
        (10, 100, 2),
        (250, 340, 4),
    ],
)
def test_browser_edits_change_the_saved_completion_reward(
    page, planner, database, minutes, expected_xp, expected_level
):
    quest = create_from_form(page, "Study math", 60)
    open_details(page, quest)

    page.get_by_role("button", name="Edit quest", exact=True).click()
    page.get_by_label("Edit title", exact=True).fill("Read a chapter")
    page.get_by_label("Edit minutes", exact=True).fill(str(minutes))

    with page.expect_response(
        lambda response: response.url.endswith(f"/quests/{quest['id']}")
        and response.request.method == "PATCH"
    ) as edited:
        page.get_by_role(
            "button", name="Save changes", exact=True
        ).click()

    assert edited.value.status == 200
    updated = edited.value.json()

    expect(page.locator("#detail-title")).to_have_text("Read a chapter")
    expect(page.locator("#detail-duration")).to_have_text(
        f"{minutes} minutes"
    )
    expect(page.locator("#detail-reward")).to_have_text(f"{minutes} XP")
    expect(page.locator("#detail-description")).to_have_text(
        updated["fantasyDescription"]
    )
    expect(page.locator("#refresh-quests")).to_be_enabled()

    assert updated["id"] == quest["id"]
    assert updated["title"] == "Read a chapter"
    assert updated["durationMinutes"] == minutes
    assert updated["xpReward"] == minutes
    assert updated["status"] == "pending"
    assert load_quests(database) == [updated]
    assert load_progress(database) == {"totalXP": 90}

    result = complete_from_page(page)

    assert result["awardedXP"] == minutes
    assert result["totalXP"] == expected_xp
    assert result["level"] == expected_level
    assert load_quests(database) == [result["quest"]]
    assert load_progress(database) == {"totalXP": expected_xp}
    expect(page.locator("#progress-summary")).to_have_text(
        f"{expected_xp} XP | Level {expected_level}"
    )


def test_restart_and_pending_deletion_preserve_completed_progress(
    browser, database
):
    with running_planner(database) as url:
        with browser_page(browser, url) as page:
            expect(page.locator("#progress-summary")).to_have_text(
                "90 XP | Level 1"
            )

            quest = create_from_form(page, "Study math", 60)
            open_details(page, quest)
            completed = complete_from_page(page)

            assert completed["totalXP"] == 150
            assert completed["awardedXP"] == 60

            pending = create_from_form(page, "Water plants", 20)
            saved = load_quests(database)

            assert saved == [completed["quest"], pending]
            assert load_progress(database) == {"totalXP": 150}

    # Both the first server and its browser session have now been closed.
    with running_planner(database) as url:
        with browser_page(browser, url) as page:
            expect(page.locator("#progress-summary")).to_have_text(
                "150 XP | Level 2"
            )
            expect(page.locator("#quest-list li")).to_have_count(2)

            open_details(page, completed["quest"])
            expect(page.locator("#completed-note")).to_be_visible()
            expect(page.locator("#quest-actions")).to_be_hidden()
            expect(page.locator("#detail-completed time")).to_have_attribute(
                "datetime", completed["quest"]["completedAt"]
            )
            assert load_quests(database) == saved

            page.get_by_label("Show quests").select_option("pending")
            expect(page.locator("#quest-list li")).to_have_count(1)
            open_details(page, pending)

            page.get_by_role(
                "button", name="Delete quest", exact=True
            ).click()
            expect(page.locator("#delete-confirmation")).to_be_visible()
            page.get_by_role(
                "button", name="Cancel delete", exact=True
            ).click()

            expect(page.locator("#delete-confirmation")).to_be_hidden()
            assert load_quests(database) == saved
            assert load_progress(database) == {"totalXP": 150}

            page.get_by_role(
                "button", name="Delete quest", exact=True
            ).click()

            with page.expect_response(
                lambda response: response.url.endswith(
                    f"/quests/{pending['id']}"
                )
                and response.request.method == "DELETE"
            ) as deleted:
                page.get_by_role(
                    "button", name="Confirm delete", exact=True
                ).click()

            assert deleted.value.status == 200
            expect(page.locator("#quest-list li")).to_have_count(0)
            expect(page.locator("#progress-summary")).to_have_text(
                "150 XP | Level 2"
            )
            assert load_quests(database) == [completed["quest"]]
            assert load_progress(database) == {"totalXP": 150}

            page.get_by_label("Show quests").select_option("completed")
            expect(page.locator("#quest-list li")).to_have_count(1)
            open_details(page, completed["quest"])
            expect(page.locator("#completed-note")).to_be_visible()