from contextlib import closing
from concurrent.futures import ThreadPoolExecutor
import re
import sqlite3
from threading import Barrier

import pytest

from app import create_app
from quest_manager import create_quest
from quest_validation import MAX_SAFE_MINUTES
from storage import insert_quest, load_progress, load_quests


@pytest.fixture
def database(tmp_path):
    return tmp_path / "quests.db"


@pytest.fixture
def app(database):
    application = create_app(database)
    application.config.update(TESTING=True, SECRET_KEY="test-only-secret")
    return application


@pytest.fixture
def client(app):
    test_client = app.test_client()
    with test_client.session_transaction() as session:
        session["csrf_token"] = "test-token"
    test_client.environ_base["HTTP_X_CSRF_TOKEN"] = "test-token"
    return test_client


@pytest.fixture
def saved_quests(app, database):
    for quest_id, title, minutes in [
        ("q1", "Study math", 60),
        ("q2", "Do laundry", 20),
        ("q3", "Water the plants", 30),
    ]:
        quest = create_quest([], title, minutes)[0]
        quest["id"] = quest_id
        if quest_id == "q1":
            quest["fantasyDescription"] = "A saved custom scroll"
        insert_quest(database, quest)

    with closing(sqlite3.connect(database)) as connection:
        connection.execute(
            "UPDATE quests SET status = 'completed', completedAt = ? WHERE id = ?",
            ("2026-11-10T15:00:00Z", "q2"),
        )
        connection.execute("UPDATE progress SET totalXP = 90 WHERE id = 1")
        connection.commit()
    return load_quests(database)


def test_patch_title_updates_description(client, database, saved_quests):
    response = client.patch("/quests/q1", json={"title": "  Go swimming  "})

    assert response.status_code == 200
    expected = {
        **saved_quests[0],
        "title": "Go swimming",
        "fantasyDescription": "Train for the Royal Tournament",
    }
    assert response.get_json() == expected
    assert load_quests(database) == [expected, *saved_quests[1:]]
    assert load_progress(database) == {"totalXP": 90}


def test_patch_duration_updates_reward_only(client, database, saved_quests):
    response = client.patch("/quests/q1", json={"durationMinutes": 45})

    assert response.status_code == 200
    expected = {**saved_quests[0], "durationMinutes": 45, "xpReward": 45}
    assert response.get_json() == expected
    assert load_quests(database) == [expected, *saved_quests[1:]]
    assert load_progress(database) == {"totalXP": 90}


def test_patch_both_fields_survives_reopening(client, database, saved_quests):
    response = client.patch(
        "/quests/q1", json={"title": "Do laundry", "durationMinutes": 15}
    )

    assert response.status_code == 200
    expected = {
        **saved_quests[0], "title": "Do laundry", "durationMinutes": 15,
        "xpReward": 15, "fantasyDescription": "Restore Order to the Kingdom",
    }
    reopened = create_app(database).test_client()
    assert reopened.get("/quests/q1").get_json() == expected
    assert reopened.get("/quests").get_json() == [expected, *saved_quests[1:]]
    assert load_progress(database) == {"totalXP": 90}


def test_duration_edit_preserves_original_title_formatting(client, database, saved_quests):
    with closing(sqlite3.connect(database)) as connection:
        connection.execute("UPDATE quests SET title = ? WHERE id = ?", ("  Study math  ", "q1"))
        connection.commit()

    response = client.patch("/quests/q1", json={"durationMinutes": 45})

    assert response.status_code == 200
    assert response.get_json()["title"] == "  Study math  "
    assert response.get_json()["fantasyDescription"] == "A saved custom scroll"


def test_delete_survives_reopening(client, database, saved_quests):
    response = client.delete("/quests/q1")

    assert response.status_code == 200
    assert response.get_json() == {"deleted": "q1"}
    reopened = create_app(database).test_client()
    assert reopened.get("/quests").get_json() == saved_quests[1:]
    assert reopened.get("/quests/q1").status_code == 404
    assert load_progress(database) == {"totalXP": 90}


def test_repeated_delete_does_not_change_other_quests(client, database, saved_quests):
    assert client.delete("/quests/q1").status_code == 200
    response = client.delete("/quests/q1")

    assert response.status_code == 404
    assert load_quests(database) == saved_quests[1:]
    assert load_progress(database) == {"totalXP": 90}


@pytest.mark.parametrize("method", ["patch", "delete"])
def test_completed_quest_is_protected(client, database, saved_quests, method):
    response = getattr(client, method)("/quests/q2", json={"title": "Read a book"})

    assert response.status_code == 409
    assert response.is_json
    assert load_quests(database) == saved_quests
    assert load_progress(database) == {"totalXP": 90}


@pytest.mark.parametrize("method", ["patch", "delete"])
def test_missing_id(client, database, saved_quests, method):
    response = getattr(client, method)("/quests/missing", json={"title": "Read a book"})

    assert response.status_code == 404
    assert response.get_json() == {"error": "Quest not found."}
    assert load_quests(database) == saved_quests


@pytest.mark.parametrize("method", ["patch", "delete"])
def test_blank_id(client, method):
    response = getattr(client, method)("/quests/%20", json={"title": "Read a book"})

    assert response.status_code == 400
    assert response.is_json


@pytest.mark.parametrize(
    "payload",
    [None, [], "title", {}, {"status": "completed"}, {"xpReward": 999},
     {"title": "Read a book", "completedAt": "now"}],
)
def test_patch_rejects_invalid_payload(client, database, saved_quests, payload):
    response = client.patch("/quests/q1", json=payload)

    assert response.status_code == 400
    assert response.is_json
    assert load_quests(database) == saved_quests


@pytest.mark.parametrize("title", [None, "", "  ", 30, True, [], {}])
def test_invalid_title_does_not_save(client, database, saved_quests, title):
    response = client.patch("/quests/q1", json={"title": title})

    assert response.status_code == 400
    assert load_quests(database) == saved_quests


@pytest.mark.parametrize("minutes", [None, 0, -1, 1.5, 30.0, "30", True, False, MAX_SAFE_MINUTES + 1])
def test_invalid_duration_does_not_save(client, database, saved_quests, minutes):
    response = client.patch(
        "/quests/q1", json={"title": "Go swimming", "durationMinutes": minutes}
    )

    assert response.status_code == 400
    assert load_quests(database) == saved_quests
    assert load_progress(database) == {"totalXP": 90}


@pytest.mark.parametrize("method, event", [("patch", "UPDATE"), ("delete", "DELETE")])
def test_failed_write_rolls_back(client, database, saved_quests, method, event):
    with closing(sqlite3.connect(database)) as connection:
        connection.execute(
            f"CREATE TRIGGER fail_write AFTER {event} ON quests "
            "BEGIN SELECT RAISE(ABORT, 'forced write failure'); END"
        )
        connection.commit()

    response = getattr(client, method)(
        "/quests/q1", json={"title": "Go swimming", "durationMinutes": 45}
    )

    assert response.status_code == 500
    assert response.is_json
    assert "forced write failure" not in response.get_data(as_text=True)
    assert str(database) not in response.get_data(as_text=True)
    assert load_quests(database) == saved_quests
    assert load_progress(database) == {"totalXP": 90}


@pytest.mark.parametrize("method", ["patch", "delete"])
def test_missing_database_is_not_recreated(client, database, method):
    database.unlink()

    response = getattr(client, method)("/quests/q1", json={"title": "Go swimming"})

    assert response.status_code == 500
    assert response.is_json
    assert not database.exists()


def test_completed_between_lookup_and_save_is_protected(client, database, saved_quests, monkeypatch):
    import app as app_module

    original_update = app_module.update_pending_quest

    def complete_then_update(path, quest, *, expected_quest=None):
        with closing(sqlite3.connect(path)) as connection:
            connection.execute(
                "UPDATE quests SET status = 'completed', completedAt = ? WHERE id = ?",
                ("2026-11-10T16:00:00Z", "q1"),
            )
            connection.execute("UPDATE progress SET totalXP = 150 WHERE id = 1")
            connection.commit()
        original_update(path, quest, expected_quest=expected_quest)

    monkeypatch.setattr(app_module, "update_pending_quest", complete_then_update)
    response = client.patch("/quests/q1", json={"title": "Go swimming"})

    assert response.status_code == 409
    stored = load_quests(database)[0]
    assert stored["status"] == "completed"
    assert stored["title"] == saved_quests[0]["title"]
    assert stored["fantasyDescription"] == saved_quests[0]["fantasyDescription"]
    assert load_progress(database) == {"totalXP": 150}


def test_overlapping_edits_return_a_conflict_instead_of_losing_data(app, client, database, saved_quests, monkeypatch):
    import app as app_module

    original_load = app_module.load_quests
    reads_finished = Barrier(2)

    def load_together(path, status=None):
        quests = original_load(path, status)
        reads_finished.wait(timeout=5)
        return quests

    def edit(payload):
        separate_client = app.test_client()
        with separate_client.session_transaction() as session:
            session["csrf_token"] = "parallel-token"
        response = separate_client.patch(
            "/quests/q1", json=payload, headers={"X-CSRF-Token": "parallel-token"}
        )
        return payload, response.status_code, response.get_json()

    monkeypatch.setattr(app_module, "load_quests", load_together)
    with ThreadPoolExecutor(max_workers=2) as pool:
        first = pool.submit(edit, {"title": "Go swimming"})
        second = pool.submit(edit, {"durationMinutes": 45})
        results = [first.result(timeout=10), second.result(timeout=10)]

    assert sorted(result[1] for result in results) == [200, 409]
    accepted = next(result for result in results if result[1] == 200)
    rejected = next(result for result in results if result[1] == 409)
    assert load_quests(database) == [accepted[2], *saved_quests[1:]]
    assert load_progress(database) == {"totalXP": 90}

    monkeypatch.setattr(app_module, "load_quests", original_load)
    retry = client.patch("/quests/q1", json=rejected[0])
    assert retry.status_code == 200
    stored = load_quests(database)[0]
    assert stored["title"] == "Go swimming"
    assert stored["durationMinutes"] == 45
    assert stored["xpReward"] == 45


@pytest.mark.parametrize("method, path", [("post", "/quests"), ("patch", "/quests/q1"), ("delete", "/quests/q1")])
@pytest.mark.parametrize("token", [None, "", "wrong-token", "é"])
def test_invalid_csrf_is_rejected(client, database, saved_quests, method, path, token):
    client.environ_base.pop("HTTP_X_CSRF_TOKEN")
    headers = {} if token is None else {"X-CSRF-Token": token}
    response = getattr(client, method)(
        path, json={"title": "Go swimming", "durationMinutes": 45}, headers=headers
    )

    assert response.status_code == 403
    assert response.is_json
    assert load_quests(database) == saved_quests
    assert load_progress(database) == {"totalXP": 90}


@pytest.mark.parametrize("method, path", [("post", "/quests"), ("patch", "/quests/q1"), ("delete", "/quests/q1")])
def test_cross_origin_change_is_rejected(client, database, saved_quests, method, path):
    response = getattr(client, method)(
        path, json={"title": "Go swimming", "durationMinutes": 45},
        headers={"Origin": "https://other-site.test"},
    )

    assert response.status_code == 403
    assert load_quests(database) == saved_quests


def test_same_origin_change_is_allowed(client, saved_quests):
    response = client.patch(
        "/quests/q1", json={"title": "Go swimming"}, headers={"Origin": "http://localhost"}
    )

    assert response.status_code == 200


def test_csrf_token_is_stable_and_not_cached(app):
    client = app.test_client()
    first = client.get("/csrf-token")
    assert first.status_code == 200
    token = first.get_json()["csrfToken"]

    assert isinstance(token, str) and token
    assert "no-store" in first.headers["Cache-Control"]
    assert "HttpOnly" in first.headers["Set-Cookie"]
    assert "SameSite=Strict" in first.headers["Set-Cookie"]
    assert client.get("/csrf-token").get_json()["csrfToken"] == token


def test_token_from_another_session_is_rejected(app, database, saved_quests):
    first = app.test_client()
    second = app.test_client()
    response = first.get("/csrf-token")
    assert response.status_code == 200
    token = response.get_json()["csrfToken"]
    assert second.get("/csrf-token").status_code == 200

    response = second.delete("/quests/q1", headers={"X-CSRF-Token": token})

    assert response.status_code == 403
    assert load_quests(database) == saved_quests


def test_rendered_creation_form_has_working_token(app, database):
    client = app.test_client()
    page = client.get("/")
    match = re.search(r'data-csrf-token="([^"]+)"', page.get_data(as_text=True))
    assert match is not None

    response = client.post(
        "/quests", json={"title": "Study math", "durationMinutes": 60},
        headers={"X-CSRF-Token": match.group(1)},
    )

    assert response.status_code == 201
    assert load_quests(database) == [response.get_json()]
