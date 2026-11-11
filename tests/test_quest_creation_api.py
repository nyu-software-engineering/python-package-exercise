from contextlib import closing
import sqlite3

import pytest

from app import create_app
from storage import load_progress, load_quests


@pytest.fixture
def database(tmp_path):
    return tmp_path / "quests.db"


@pytest.fixture
def client(database):
    app = create_app(database)
    app.config["TESTING"] = True
    return app.test_client()


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