from contextlib import closing
from datetime import datetime, timezone
from os import PathLike, fspath
from pathlib import Path
import sqlite3

from progression import award_xp, calculate_level


_QUEST_COLUMNS = (
    "id", "title", "durationMinutes", "fantasyDescription",
    "status", "xpReward", "completedAt",
)
_SELECT_QUESTS = "SELECT " + ", ".join(_QUEST_COLUMNS) + " FROM quests"


_CREATE_QUESTS = """
CREATE TABLE IF NOT EXISTS quests (
    id TEXT PRIMARY KEY NOT NULL CHECK (length(trim(id)) > 0),
    title TEXT NOT NULL CHECK (length(trim(title)) > 0),
    durationMinutes INTEGER NOT NULL
        CHECK (typeof(durationMinutes) = 'integer' AND durationMinutes > 0),
    fantasyDescription TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending'
        CHECK (status IN ('pending', 'completed')),
    xpReward INTEGER NOT NULL
        CHECK (typeof(xpReward) = 'integer' AND xpReward = durationMinutes),
    completedAt TEXT,
    CHECK (
        (status = 'pending' AND completedAt IS NULL)
        OR (status = 'completed' AND completedAt IS NOT NULL)
    )
)
"""

_CREATE_PROGRESS = """
CREATE TABLE IF NOT EXISTS progress (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    totalXP INTEGER NOT NULL DEFAULT 0
        CHECK (typeof(totalXP) = 'integer' AND totalXP >= 0)
)
"""


def initialize_database(database_path: str | PathLike[str]) -> None:
    path = _validate_database_path(database_path)
    with closing(sqlite3.connect(path, isolation_level=None)) as connection:
        with connection:
            connection.execute("BEGIN IMMEDIATE")
            connection.execute(_CREATE_QUESTS)
            connection.execute(_CREATE_PROGRESS)
            connection.execute(
                "INSERT INTO progress (id, totalXP) SELECT 1, 0 "
                "WHERE NOT EXISTS (SELECT 1 FROM progress WHERE id = 1)"
            )


def insert_quest(database_path: str | PathLike[str], quest: dict) -> None:
    _validate_pending_quest(quest)
    values = tuple(quest[field] for field in _QUEST_COLUMNS)
    with closing(_connect_existing(database_path)) as connection:
        with connection:
            connection.execute(
                "INSERT INTO quests (" + ", ".join(_QUEST_COLUMNS)
                + ") VALUES (?, ?, ?, ?, ?, ?, ?)", values,
            )


def update_pending_quest(
    database_path: str | PathLike[str], quest: dict, *, expected_quest: dict | None = None,
) -> None:
    """Save a pending quest, optionally rejecting changes to an outdated copy."""
    _validate_pending_quest(quest)
    if expected_quest is not None:
        _validate_pending_quest(expected_quest)
        if expected_quest["id"] != quest["id"]:
            raise ValueError("expected quest must have the same ID")
    with closing(_connect_existing(database_path)) as connection:
        with connection:
            connection.execute("BEGIN IMMEDIATE")
            _require_pending_quest(connection, quest["id"])
            if expected_quest is not None:
                current = connection.execute(
                    _SELECT_QUESTS + " WHERE id = ?", (quest["id"],),
                ).fetchone()
                if current != tuple(expected_quest[field] for field in _QUEST_COLUMNS):
                    raise ValueError("quest has changed; reload before editing")
            connection.execute(
                "UPDATE quests SET title = ?, fantasyDescription = ?, "
                "durationMinutes = ?, xpReward = ? WHERE id = ? AND status = 'pending'",
                (quest["title"], quest["fantasyDescription"], quest["durationMinutes"],
                 quest["xpReward"], quest["id"]),
            )


def delete_pending_quest(database_path: str | PathLike[str], quest_id: str) -> None:
    if not isinstance(quest_id, str):
        raise TypeError("quest_id must be a string")
    if not quest_id.strip():
        raise ValueError("quest_id must not be blank")
    with closing(_connect_existing(database_path)) as connection:
        with connection:
            connection.execute("BEGIN IMMEDIATE")
            _require_pending_quest(connection, quest_id)
            connection.execute(
                "DELETE FROM quests WHERE id = ? AND status = 'pending'", (quest_id,),
            )


def complete_quest(database_path: str | PathLike[str], quest_id: str) -> dict:
    """Complete a saved quest and award XP once, in the same transaction."""
    if not isinstance(quest_id, str):
        raise TypeError("quest_id must be a string")
    if not quest_id.strip():
        raise ValueError("quest_id must not be blank")
    with closing(_connect_existing(database_path)) as connection:
        connection.row_factory = sqlite3.Row
        with connection:
            # Read after taking the write lock, so another completion cannot race us.
            connection.execute("BEGIN IMMEDIATE")
            row = connection.execute(
                _SELECT_QUESTS + " WHERE id = ?", (quest_id,),
            ).fetchone()
            if row is None:
                raise KeyError(f"quest not found: {quest_id}")
            quest = dict(row)
            progress = connection.execute(
                "SELECT totalXP FROM progress WHERE id = 1",
            ).fetchone()
            if progress is None:
                raise ValueError("progress is not initialized; call initialize_database first")
            total_xp = progress["totalXP"]
            awarded_xp = 0

            if quest["status"] == "pending":
                updated = award_xp(total_xp, quest["durationMinutes"])
                if updated["totalXP"] > 2**63 - 1:
                    raise ValueError("totalXP exceeds the SQLite integer limit")
                quest["status"] = "completed"
                quest["completedAt"] = datetime.now(timezone.utc).isoformat()
                saved_quest = connection.execute(
                    "UPDATE quests SET status = 'completed', completedAt = ? "
                    "WHERE id = ? AND status = 'pending'",
                    (quest["completedAt"], quest_id),
                )
                saved_progress = connection.execute(
                    "UPDATE progress SET totalXP = ? WHERE id = 1",
                    (updated["totalXP"],),
                )
                if saved_quest.rowcount != 1 or saved_progress.rowcount != 1:
                    raise sqlite3.IntegrityError("quest completion could not be saved")
                total_xp = updated["totalXP"]
                awarded_xp = quest["xpReward"]

            return {
                "quest": quest, "totalXP": total_xp,
                "level": calculate_level(total_xp), "awardedXP": awarded_xp,
            }


def load_quests(database_path: str | PathLike[str], status: str | None = None) -> list[dict]:
    if status not in (None, "pending", "completed"):
        raise ValueError("status must be pending, completed, or None")
    query = _SELECT_QUESTS
    parameters = ()
    if status is not None:
        query += " WHERE status = ?"
        parameters = (status,)
    with closing(_connect_existing(database_path, readonly=True)) as connection:
        connection.row_factory = sqlite3.Row
        return [dict(row) for row in connection.execute(query + " ORDER BY rowid", parameters)]


def load_progress(database_path: str | PathLike[str]) -> dict:
    with closing(_connect_existing(database_path, readonly=True)) as connection:
        row = connection.execute("SELECT totalXP FROM progress WHERE id = 1").fetchone()
    if row is None:
        raise ValueError("progress is not initialized; call initialize_database first")
    return {"totalXP": row[0]}


def _validate_pending_quest(quest):
    if not isinstance(quest, dict):
        raise TypeError("quest must be a dictionary")
    if set(quest) != set(_QUEST_COLUMNS):
        raise ValueError("quest must contain exactly the seven standard fields")
    for field in ("id", "title", "fantasyDescription"):
        if not isinstance(quest[field], str):
            raise TypeError(f"{field} must be a string")
        if not quest[field].strip():
            raise ValueError(f"{field} must not be blank")
    for field in ("durationMinutes", "xpReward"):
        if type(quest[field]) is not int:
            raise TypeError(f"{field} must be an integer")
    if not 1 <= quest["durationMinutes"] <= 2**63 - 1:
        raise ValueError("durationMinutes must be a positive SQLite integer")
    if quest["xpReward"] != quest["durationMinutes"]:
        raise ValueError("xpReward must equal durationMinutes")
    if quest["status"] != "pending" or quest["completedAt"] is not None:
        raise ValueError("quest must be pending without a completion time")


def _require_pending_quest(connection, quest_id):
    row = connection.execute("SELECT status FROM quests WHERE id = ?", (quest_id,)).fetchone()
    if row is None:
        raise KeyError(f"quest not found: {quest_id}")
    if row[0] != "pending":
        raise ValueError("only pending quests can be changed")


def _validate_database_path(database_path):
    if not isinstance(database_path, (str, PathLike)):
        raise TypeError("database_path must be a string or a text path-like object")
    path = fspath(database_path)
    if not isinstance(path, str):
        raise TypeError("database_path must be a string or a text path-like object")
    if not path.strip() or path == ":memory:" or path.startswith("file:"):
        raise ValueError("database_path must name a file, not a temporary database or URI")
    return path


def _connect_existing(database_path, *, readonly=False):
    path = Path(_validate_database_path(database_path)).resolve().as_uri()
    return sqlite3.connect(path + ("?mode=ro" if readonly else "?mode=rw"), uri=True)
