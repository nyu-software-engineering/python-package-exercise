from concurrent.futures import ThreadPoolExecutor
from contextlib import closing
from datetime import datetime, timedelta
import json
import sqlite3
from threading import Barrier

import pytest

from app import create_app
from quest_manager import create_quest
from storage import insert_quest, load_progress, load_quests


@pytest.fixture
def database(tmp_path):
    return tmp_path / "quests.db"


@pytest.fixture
def app(database):
    application = create_app(database)
    application.config.update(TESTING=True, SECRET_KEY="test-only-secret")
    return application


def session_client(app):
    client = app.test_client()
    token = client.get("/csrf-token").get_json()["csrfToken"]
    client.environ_base["HTTP_X_CSRF_TOKEN"] = token
    return client


@pytest.fixture
def client(app):
    return session_client(app)


@pytest.fixture
def saved_quests(app, database):
    for quest_id, title, minutes in [("q1", "Study math", 60), ("q2", "Do laundry", 50)]:
        quest = create_quest([], title, minutes)[0]
        quest["id"] = quest_id
        insert_quest(database, quest)
    with closing(sqlite3.connect(database)) as connection:
        connection.execute("UPDATE progress SET totalXP = 90 WHERE id = 1")
        connection.commit()
    return load_quests(database)


def test_initial_progress_is_readable_without_token(app, database):
    response = app.test_client().get("/progress")

    assert response.status_code == 200
    assert response.get_json() == {"totalXP": 0, "level": 1}
    assert "no-store" in response.headers["Cache-Control"]
    assert load_progress(database) == {"totalXP": 0}


def test_complete_returns_saved_quest_and_progress(client, database, saved_quests):
    response = client.post("/quests/q1/complete")

    assert response.status_code == 200
    result = response.get_json()
    timestamp = result["quest"]["completedAt"]
    expected = {**saved_quests[0], "status": "completed", "completedAt": timestamp}
    assert datetime.fromisoformat(timestamp).utcoffset() == timedelta(0)
    assert result == {"quest": expected, "totalXP": 150, "level": 2, "awardedXP": 60}
    assert "no-store" in response.headers["Cache-Control"]
    assert load_quests(database) == [expected, saved_quests[1]]
    assert client.get("/quests/q1").get_json() == expected
    assert client.get("/quests?status=completed").get_json() == [expected]
    assert client.get("/quests?status=pending").get_json() == [saved_quests[1]]
    assert client.get("/progress").get_json() == {"totalXP": 150, "level": 2}


def test_empty_json_object_is_allowed(client, saved_quests):
    response = client.post("/quests/q1/complete", json={})

    assert response.status_code == 200
    assert response.get_json()["awardedXP"] == 60


def test_retry_after_restart_keeps_timestamp_and_returns_current_progress(client, database, saved_quests):
    first = client.post("/quests/q1/complete").get_json()
    second = client.post("/quests/q2/complete")
    assert second.status_code == 200
    assert second.get_json()["totalXP"] == 200

    reopened = session_client(create_app(database))
    retry = reopened.post("/quests/q1/complete")

    assert retry.status_code == 200
    assert retry.get_json() == {**first, "totalXP": 200, "level": 3, "awardedXP": 0}
    assert reopened.get("/progress").get_json() == {"totalXP": 200, "level": 3}
    assert load_progress(database) == {"totalXP": 200}


def test_create_edit_complete_retry_and_delete_flow(client, database):
    created = client.post("/quests", json={"title": "Study math", "durationMinutes": 30})
    assert created.status_code == 201
    quest_id = created.get_json()["id"]
    assert client.get("/progress").get_json() == {"totalXP": 0, "level": 1}
    edited = client.patch(
        f"/quests/{quest_id}", json={"title": "Do laundry", "durationMinutes": 250},
    )
    assert edited.status_code == 200
    assert client.get("/progress").get_json() == {"totalXP": 0, "level": 1}
    first = client.post(f"/quests/{quest_id}/complete")
    assert first.status_code == 200
    result = first.get_json()
    assert result["quest"]["title"] == "Do laundry"
    assert result["quest"]["fantasyDescription"] == "Restore Order to the Kingdom"
    assert result["quest"]["durationMinutes"] == 250
    assert result["quest"]["xpReward"] == 250
    assert result["totalXP"] == 250
    assert result["level"] == 3
    assert result["awardedXP"] == 250
    assert client.post(f"/quests/{quest_id}/complete").get_json() == {**result, "awardedXP": 0}
    assert client.patch(f"/quests/{quest_id}", json={"durationMinutes": 1}).status_code == 409
    assert client.delete(f"/quests/{quest_id}").status_code == 409
    assert client.get(f"/quests/{quest_id}").get_json() == result["quest"]

    pending = client.post("/quests", json={"title": "Water plants", "durationMinutes": 10})
    assert pending.status_code == 201
    pending_id = pending.get_json()["id"]
    assert client.delete(f"/quests/{pending_id}").status_code == 200
    assert client.post(f"/quests/{pending_id}/complete").status_code == 404
    assert client.get("/progress").get_json() == {"totalXP": 250, "level": 3}
    assert load_progress(database) == {"totalXP": 250}


@pytest.mark.parametrize("ids, rewards, total", [(["q1", "q1"], [0, 60], 150), (["q1", "q2"], [50, 60], 200)])
def test_concurrent_http_completions(app, database, saved_quests, ids, rewards, total):
    clients = [session_client(app), session_client(app)]
    start = Barrier(2)

    def finish(index):
        start.wait(timeout=5)
        response = clients[index].post(f"/quests/{ids[index]}/complete")
        return response.status_code, response.get_json()

    with ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(finish, index) for index in range(2)]
        results = [future.result(timeout=10) for future in futures]

    assert [status for status, _ in results] == [200, 200]
    assert sorted(result["awardedXP"] for _, result in results) == rewards
    assert load_progress(database) == {"totalXP": total}
    assert app.test_client().get("/progress").get_json() == {"totalXP": total, "level": 1 + total // 100}


@pytest.mark.parametrize("payload", [None, [], "complete", True, 1, {"status": "completed"}, {"durationMinutes": 999}, {"xpReward": 999}, {"totalXP": 999}, {"completedAt": "now"}, {"id": "q2"}])
def test_body_cannot_set_quest_or_reward_fields(client, database, saved_quests, payload):
    # data='null' ensures an actual JSON null body rather than an absent body.
    response = client.post("/quests/q1/complete", data=json.dumps(payload), content_type="application/json")

    assert response.status_code == 400
    assert response.is_json
    assert load_quests(database) == saved_quests
    assert load_progress(database) == {"totalXP": 90}


@pytest.mark.parametrize("body, content_type", [("{", "application/json"), ("{}", "text/plain"), ("status=completed", "application/x-www-form-urlencoded")])
def test_malformed_or_non_json_body_is_rejected(client, database, saved_quests, body, content_type):
    response = client.post("/quests/q1/complete", data=body, content_type=content_type)

    assert response.status_code == 400
    assert response.is_json
    assert load_quests(database) == saved_quests
    assert load_progress(database) == {"totalXP": 90}


@pytest.mark.parametrize("quest_id, status", [("missing", 404), ("%20", 400), ("q1%27%20OR%20%271%27=%271", 404)])
def test_unknown_or_blank_id(client, database, saved_quests, quest_id, status):
    response = client.post(f"/quests/{quest_id}/complete")

    assert response.status_code == status
    assert response.is_json
    assert load_quests(database) == saved_quests
    assert load_progress(database) == {"totalXP": 90}


@pytest.mark.parametrize("token", [None, "", "wrong", "é"])
def test_completion_requires_session_token(client, database, saved_quests, token):
    client.environ_base.pop("HTTP_X_CSRF_TOKEN")
    response = client.post("/quests/q1/complete", headers={} if token is None else {"X-CSRF-Token": token})

    assert response.status_code == 403
    assert response.is_json
    assert load_quests(database) == saved_quests
    assert load_progress(database) == {"totalXP": 90}


def test_other_session_token_does_not_complete(app, database, saved_quests):
    first = app.test_client()
    token = first.get("/csrf-token").get_json()["csrfToken"]
    second = app.test_client()
    second.get("/csrf-token")

    assert second.post("/quests/q1/complete", headers={"X-CSRF-Token": token}).status_code == 403
    assert load_quests(database) == saved_quests
    assert load_progress(database) == {"totalXP": 90}


def test_cross_origin_completion_is_rejected(client, database, saved_quests):
    response = client.post("/quests/q1/complete", headers={"Origin": "https://other-site.test"})

    assert response.status_code == 403
    assert load_quests(database) == saved_quests
    assert load_progress(database) == {"totalXP": 90}


def test_same_origin_completion_is_allowed(client, saved_quests):
    assert client.post("/quests/q1/complete", headers={"Origin": "http://localhost"}).status_code == 200


@pytest.mark.parametrize("path", ["/progress", "/quests/q1/complete"])
def test_unavailable_database_is_not_recreated(client, database, path):
    database.unlink()
    response = client.get(path) if path == "/progress" else client.post(path)

    assert response.status_code == 500
    assert response.is_json
    assert str(database) not in response.get_data(as_text=True)
    assert not database.exists()


@pytest.mark.parametrize("path", ["/progress", "/quests/q1/complete"])
def test_missing_progress_returns_generic_error(client, database, saved_quests, path):
    with closing(sqlite3.connect(database)) as connection:
        connection.execute("DELETE FROM progress")
        connection.commit()
    response = client.get(path) if path == "/progress" else client.post(path)

    assert response.status_code == 500
    assert response.is_json
    assert "initialize_database" not in response.get_data(as_text=True)
    assert load_quests(database) == saved_quests


@pytest.mark.parametrize("table", ["quests", "progress"])
def test_failed_completion_rolls_back_and_can_be_retried(client, database, saved_quests, table):
    with closing(sqlite3.connect(database)) as connection:
        connection.execute(
            f"CREATE TRIGGER fail_completion AFTER UPDATE ON {table} "
            "BEGIN SELECT RAISE(ABORT, 'private storage failure'); END"
        )
        connection.commit()
    response = client.post("/quests/q1/complete")

    assert response.status_code == 500
    assert response.is_json
    assert "private storage failure" not in response.get_data(as_text=True)
    assert str(database) not in response.get_data(as_text=True)
    assert load_quests(database) == saved_quests
    assert client.get("/progress").get_json() == {"totalXP": 90, "level": 1}
    with closing(sqlite3.connect(database)) as connection:
        connection.execute("DROP TRIGGER fail_completion")
        connection.commit()
    assert client.post("/quests/q1/complete").get_json()["awardedXP"] == 60
    assert client.get("/progress").get_json() == {"totalXP": 150, "level": 2}


def test_xp_overflow_returns_error_without_completing(client, database, saved_quests):
    maximum = 2**63 - 1
    with closing(sqlite3.connect(database)) as connection:
        connection.execute("UPDATE progress SET totalXP = ? WHERE id = 1", (maximum,))
        connection.commit()

    response = client.post("/quests/q1/complete")

    assert response.status_code == 500
    assert response.is_json
    assert "SQLite" not in response.get_data(as_text=True)
    assert load_quests(database) == saved_quests
    assert load_progress(database) == {"totalXP": maximum}


def test_progress_read_does_not_award_xp_or_write(client, database, saved_quests):
    with closing(sqlite3.connect(database)) as connection:
        connection.execute(
            "CREATE TRIGGER block_progress BEFORE UPDATE ON progress "
            "BEGIN SELECT RAISE(ABORT, 'read must not write'); END"
        )
        connection.commit()

    for _ in range(2):
        assert client.get("/progress").get_json() == {"totalXP": 90, "level": 1}
    assert load_quests(database) == saved_quests
    assert load_progress(database) == {"totalXP": 90}


def test_get_completion_url_has_no_effect(client, database, saved_quests):
    assert client.get("/quests/q1/complete").status_code == 405
    assert load_quests(database) == saved_quests
    assert load_progress(database) == {"totalXP": 90}
