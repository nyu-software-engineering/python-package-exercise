"""Exercise real SQLite files, including reopen, repeat, and rollback behavior."""

from contextlib import closing
from pathlib import Path
import sqlite3

import pytest

from quest_manager import create_quest
from storage import initialize_database


QUEST_COLUMNS = (
    "id", "title", "durationMinutes", "fantasyDescription",
    "status", "xpReward", "completedAt",
)
INSERT_QUEST = "INSERT INTO quests VALUES (?, ?, ?, ?, ?, ?, ?)"


@pytest.mark.parametrize("path_type", [str, Path])
def test_initialization_creates_durable_schema_and_zero_xp(tmp_path, path_type):
    path = tmp_path / "quests.db"
    assert initialize_database(path_type(path)) is None
    assert path.is_file()

    # Read using a new connection: data must survive the initializer closing.
    with closing(sqlite3.connect(path)) as connection:
        tables = {row[0] for row in connection.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table'"
        )}
        assert tables == {"quests", "progress"}
        assert tuple(row[1] for row in connection.execute("PRAGMA table_info(quests)")) == QUEST_COLUMNS
        assert [row[1] for row in connection.execute("PRAGMA table_info(progress)")] == ["id", "totalXP"]
        assert connection.execute("SELECT * FROM quests").fetchall() == []
        assert connection.execute("SELECT id, totalXP FROM progress").fetchall() == [(1, 0)]


def test_repeated_initialization_preserves_quest_and_existing_xp(tmp_path):
    path = tmp_path / "quests.db"
    initialize_database(path)
    quest = create_quest([], "Study math", 60, seed=7)[0]
    with closing(sqlite3.connect(path)) as connection:
        connection.execute(INSERT_QUEST, tuple(quest[field] for field in QUEST_COLUMNS))
        connection.execute("UPDATE progress SET totalXP = 321 WHERE id = 1")
        connection.commit()

    initialize_database(path)
    initialize_database(path)

    with closing(sqlite3.connect(path)) as connection:
        connection.row_factory = sqlite3.Row
        assert [dict(row) for row in connection.execute("SELECT * FROM quests")] == [quest]
        assert [tuple(row) for row in connection.execute("SELECT id, totalXP FROM progress")] == [(1, 321)]


def test_initialization_preserves_unrelated_tables(tmp_path):
    path = tmp_path / "quests.db"
    with closing(sqlite3.connect(path)) as connection:
        connection.execute("CREATE TABLE notes (text TEXT)")
        connection.execute("INSERT INTO notes VALUES (?)", ("keep me",))
        connection.commit()

    initialize_database(path)

    with closing(sqlite3.connect(path)) as connection:
        assert connection.execute("SELECT text FROM notes").fetchall() == [("keep me",)]
        assert connection.execute("SELECT totalXP FROM progress").fetchone() == (0,)


def test_failed_initialization_rolls_back_schema_creation(tmp_path):
    path = tmp_path / "quests.db"
    with closing(sqlite3.connect(path)) as connection:
        # An incompatible existing table makes insertion of the initial 0 fail.
        connection.execute(
            "CREATE TABLE progress (id INTEGER PRIMARY KEY, totalXP INTEGER CHECK (totalXP > 0))"
        )

    with pytest.raises(sqlite3.IntegrityError):
        initialize_database(path)

    with closing(sqlite3.connect(path)) as connection:
        assert connection.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table'"
        ).fetchall() == [("progress",)]
        assert connection.execute("SELECT * FROM progress").fetchall() == []


@pytest.mark.parametrize("status, completed_at", [
    ("pending", None),
    ("completed", "2026-11-10T12:00:00Z"),
])
def test_schema_accepts_team_quest_records(tmp_path, status, completed_at):
    path = tmp_path / "quests.db"
    initialize_database(path)
    quest = create_quest([], "Study math", 60)[0]
    quest.update(status=status, completedAt=completed_at)
    with closing(sqlite3.connect(path)) as connection:
        connection.execute(INSERT_QUEST, tuple(quest[field] for field in QUEST_COLUMNS))
        connection.commit()
        assert connection.execute("SELECT status, completedAt FROM quests").fetchone() == (status, completed_at)


@pytest.mark.parametrize("invalid_fields", [
    {"id": None},
    {"title": " "},
    {"durationMinutes": 0, "xpReward": 0},
    {"durationMinutes": 1.5, "xpReward": 1.5},
    {"status": "done"},
    {"xpReward": 59},
    {"status": "completed", "completedAt": None},
    {"completedAt": "2026-11-10T12:00:00Z"},
])
def test_schema_rejects_invalid_quest_records(tmp_path, invalid_fields):
    path = tmp_path / "quests.db"
    initialize_database(path)
    quest = create_quest([], "Study math", 60)[0]
    quest.update(invalid_fields)
    with closing(sqlite3.connect(path)) as connection:
        with pytest.raises(sqlite3.IntegrityError):
            connection.execute(INSERT_QUEST, tuple(quest[field] for field in QUEST_COLUMNS))


@pytest.mark.parametrize("total_xp", [-1, 1.5, None])
def test_schema_rejects_invalid_progress(tmp_path, total_xp):
    path = tmp_path / "quests.db"
    initialize_database(path)
    with closing(sqlite3.connect(path)) as connection:
        with pytest.raises(sqlite3.IntegrityError):
            connection.execute("UPDATE progress SET totalXP = ? WHERE id = 1", (total_xp,))


def test_schema_allows_only_one_local_progress_record(tmp_path):
    path = tmp_path / "quests.db"
    initialize_database(path)
    with closing(sqlite3.connect(path)) as connection:
        with pytest.raises(sqlite3.IntegrityError):
            connection.execute("INSERT INTO progress (id, totalXP) VALUES (2, 0)")


@pytest.mark.parametrize("value", [None, True, False, 123, 1.5, b"quests.db", []])
def test_invalid_path_types_are_rejected(value):
    with pytest.raises(TypeError, match="database_path"):
        initialize_database(value)


@pytest.mark.parametrize("value", ["", " \t\n", ":memory:", "file::memory:?cache=shared", "file:quests.db"])
def test_temporary_or_blank_database_names_are_rejected(value):
    with pytest.raises(ValueError, match="database_path"):
        initialize_database(value)


def test_missing_parent_directory_is_not_created(tmp_path):
    path = tmp_path / "missing" / "quests.db"
    with pytest.raises(sqlite3.OperationalError):
        initialize_database(path)
    assert not path.parent.exists()


def test_directory_cannot_be_used_as_a_database_file(tmp_path):
    with pytest.raises(sqlite3.OperationalError):
        initialize_database(tmp_path)
