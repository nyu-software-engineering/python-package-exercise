from contextlib import closing
import sqlite3

import pytest

from app import create_app
from quest_descriptions import generate_fantasy_description
from storage import load_progress, load_quests


@pytest.fixture
def database(tmp_path):
    return tmp_path / "quests.db"


@pytest.fixture
def client(database):
    app = create_app(database)
    app.config["TESTING"] = True
    test_client = app.test_client()
    token = test_client.get("/csrf-token").get_json()["csrfToken"]
    test_client.environ_base["HTTP_X_CSRF_TOKEN"] = token
    return test_client


def test_create_quest_returns_and_saves_pending_quest(client, database):
    response = client.post(
        "/quests",
        json={"title": "Study math", "durationMinutes": 60},
    )

    assert response.status_code == 201
    quest = response.get_json()

    assert isinstance(quest["id"], str)
    assert quest["id"]
    assert quest["title"] == "Study math"
    assert quest["durationMinutes"] == 60
    assert quest["fantasyDescription"].strip()
    assert quest["status"] == "pending"
    assert quest["xpReward"] == 60
    assert quest["completedAt"] is None
    assert load_quests(database) == [quest]


def test_creating_quest_keeps_existing_xp(client, database):
    with closing(sqlite3.connect(database)) as connection:
        connection.execute("UPDATE progress SET totalXP = 90 WHERE id = 1")
        connection.commit()

    response = client.post(
        "/quests",
        json={"title": "Read history", "durationMinutes": 30},
    )

    assert response.status_code == 201
    assert load_progress(database) == {"totalXP": 90}
    assert load_quests(database)[0]["status"] == "pending"


def test_saved_quest_survives_app_recreation(client, database):
    response = client.post(
        "/quests",
        json={"title": "Clean kitchen", "durationMinutes": 20},
    )
    assert response.status_code == 201
    quest = response.get_json()

    create_app(database)

    assert load_quests(database) == [quest]
    assert load_progress(database) == {"totalXP": 0}


def test_web_creation_uses_template_variants_and_preserves_saved_descriptions(client, database, monkeypatch):
    seeds = iter([0, 1])
    monkeypatch.setattr("app.secrets.randbits", lambda bits: next(seeds))
    first = client.post("/quests", json={"title": "Read books", "durationMinutes": 30})
    second = client.post("/quests", json={"title": "Read books", "durationMinutes": 30})
    assert first.status_code == second.status_code == 201
    first_quest, second_quest = first.get_json(), second.get_json()
    assert first_quest["fantasyDescription"] == generate_fantasy_description("Read books", seed=0)
    assert second_quest["fantasyDescription"] == generate_fantasy_description("Read books", seed=1)
    assert first_quest["fantasyDescription"] != second_quest["fantasyDescription"]
    assert first_quest["id"] != second_quest["id"]
    expected = [first_quest, second_quest]
    assert client.get("/quests").get_json() == expected
    assert create_app(database).test_client().get("/quests").get_json() == expected
    assert load_quests(database) == expected
    assert load_progress(database) == {"totalXP": 0}
    edited = client.patch(f"/quests/{first_quest['id']}", json={"durationMinutes": 45})
    assert edited.status_code == 200
    assert edited.get_json()["fantasyDescription"] == first_quest["fantasyDescription"]
    assert edited.get_json()["xpReward"] == 45
