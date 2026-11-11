from contextlib import closing
import sqlite3
from urllib.parse import quote

import pytest

from app import create_app
from quest_manager import create_quest
from storage import insert_quest, load_progress, load_quests


@pytest.fixture
def database(tmp_path):
    return tmp_path / "quests.db"


@pytest.fixture
def client(database):
    app = create_app(database)
    app.config["TESTING"] = True
    return app.test_client()


@pytest.fixture
def saved_quests(client, database):
    for quest_id, title, minutes in [
        ("q1", "Study math", 60),
        ("q2", "Do laundry", 20),
        ("q3", "Go swimming", 30),
    ]:
        quest = create_quest([], title, minutes)[0]
        quest["id"] = quest_id
        insert_quest(database, quest)

    with closing(sqlite3.connect(database)) as connection:
        connection.execute(
            "UPDATE quests SET status = 'completed', completedAt = ? WHERE id = ?",
            ("2026-11-10T15:00:00Z", "q2"),
        )
        connection.execute("UPDATE progress SET totalXP = 90 WHERE id = 1")
        connection.commit()

    return load_quests(database)


def test_empty_list(client):
    response = client.get("/quests")

    assert response.status_code == 200
    assert response.is_json
    assert response.get_json() == []


def test_list_returns_all_saved_fields(client, saved_quests):
    response = client.get("/quests")

    assert response.status_code == 200
    assert response.get_json() == saved_quests
    assert [quest["id"] for quest in response.get_json()] == ["q1", "q2", "q3"]


@pytest.mark.parametrize(
    "status, expected_ids",
    [("pending", ["q1", "q3"]), ("completed", ["q2"])],
)
def test_filter_by_status(client, saved_quests, status, expected_ids):
    response = client.get("/quests", query_string={"status": status})

    assert response.status_code == 200
    assert [quest["id"] for quest in response.get_json()] == expected_ids


@pytest.mark.parametrize("status", ["pending", "completed"])
def test_filter_with_no_matches(client, status):
    response = client.get("/quests", query_string={"status": status})

    assert response.status_code == 200
    assert response.get_json() == []


@pytest.mark.parametrize("status", ["done", "Pending", "", "null", "pending' OR 1=1 --"])
def test_invalid_status_returns_json_error(client, database, saved_quests, status):
    response = client.get("/quests", query_string={"status": status})

    assert response.status_code == 400
    assert response.is_json
    assert response.get_json()["error"]
    assert load_quests(database) == saved_quests
    assert load_progress(database) == {"totalXP": 90}


@pytest.mark.parametrize("index", [0, 1])
def test_detail_for_pending_and_completed_quests(client, saved_quests, index):
    quest = saved_quests[index]
    response = client.get(f"/quests/{quest['id']}")

    assert response.status_code == 200
    assert response.is_json
    assert response.get_json() == quest


@pytest.mark.parametrize("quest_id", ["missing", "q1' OR '1'='1"])
def test_unknown_id_returns_json_error(client, saved_quests, quest_id):
    response = client.get("/quests/" + quote(quest_id, safe=""))

    assert response.status_code == 404
    assert response.get_json() == {"error": "Quest not found."}


@pytest.mark.parametrize("quest_id", [" ", "\t"])
def test_blank_id_returns_json_error(client, quest_id):
    response = client.get("/quests/" + quote(quest_id, safe=""))

    assert response.status_code == 400
    assert response.is_json
    assert response.get_json()["error"]


def test_created_quest_can_be_read(client):
    created = client.post(
        "/quests", json={"title": "Read history", "durationMinutes": 45}
    )
    assert created.status_code == 201
    quest = created.get_json()

    assert client.get("/quests").get_json() == [quest]
    assert client.get(f"/quests/{quest['id']}").get_json() == quest


def test_quests_can_be_read_after_app_recreation(database, saved_quests):
    reopened = create_app(database).test_client()

    assert reopened.get("/quests").get_json() == saved_quests
    assert reopened.get("/quests/q2").get_json() == saved_quests[1]
    assert load_progress(database) == {"totalXP": 90}


def test_reads_do_not_change_quests_or_xp(client, database, saved_quests):
    assert client.get("/quests").status_code == 200
    assert client.get("/quests?status=completed").status_code == 200
    assert client.get("/quests/q1").status_code == 200
    assert client.get("/quests/q2").status_code == 200
    assert client.get("/quests/missing").status_code == 404

    assert load_quests(database) == saved_quests
    assert load_progress(database) == {"totalXP": 90}


@pytest.mark.parametrize("path", ["/quests", "/quests/q1"])
def test_database_errors_return_generic_json(client, database, path):
    with closing(sqlite3.connect(database)) as connection:
        connection.execute("DROP TABLE quests")
        connection.commit()

    response = client.get(path)

    assert response.status_code == 500
    assert response.is_json
    assert response.get_json() == {"error": "Could not load quests."}
    assert str(database) not in response.get_data(as_text=True)
    assert "no such table" not in response.get_data(as_text=True)


@pytest.mark.parametrize("path", ["/quests", "/quests/q1"])
def test_missing_database_is_not_recreated_by_get(client, database, path):
    database.unlink()

    response = client.get(path)

    assert response.status_code == 500
    assert response.is_json
    assert not database.exists()
