"""Initialize and access file-backed storage for one local quest-planner user."""

from contextlib import closing
from os import PathLike, fspath
from pathlib import Path
import sqlite3


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
    """Create missing quest/progress tables and seed 0 XP for a new user.

    Accept a text filesystem path (including pathlib.Path). Its parent directory
    must already exist. Blank paths, SQLite URIs, and ':memory:' are rejected
    because this helper closes its connection and promises file-backed storage.

    Repeated calls preserve existing quests, progress, and unrelated tables.
    Initialization is committed atomically and the connection is always closed.
    Existing table definitions are not migrated. SQLite errors propagate to the
    caller; invalid path types raise TypeError and invalid names raise ValueError.
    """
    path = _validate_database_path(database_path)
    with closing(sqlite3.connect(path, isolation_level=None)) as connection:
        with connection:
            # Explicitly include DDL and the initial row in the same transaction.
            connection.execute("BEGIN IMMEDIATE")
            connection.execute(_CREATE_QUESTS)
            connection.execute(_CREATE_PROGRESS)
            connection.execute(
                "INSERT INTO progress (id, totalXP) SELECT 1, 0 "
                "WHERE NOT EXISTS (SELECT 1 FROM progress WHERE id = 1)"
            )


def insert_quest(database_path: str | PathLike[str], quest: dict) -> None:
    """Commit one new pending quest without changing progress or the input dict.

    Call initialize_database first. The dictionary must have exactly the seven
    standard fields, with nonblank text ID/title/description, positive integer
    minutes, an equal integer XP reward, pending status, and no completion time.
    Minutes/reward must fit SQLite's signed 64-bit integer range. Extra metadata
    is rejected rather than silently discarded. Text formatting is preserved.

    Invalid field types raise TypeError; invalid fields/values raise ValueError.
    Duplicate IDs raise sqlite3.IntegrityError without overwriting any record.
    Other SQLite errors propagate. Failed inserts leave quests and XP unchanged.
    """
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
        raise ValueError("only new pending quests without a completion time can be inserted")

    values = tuple(quest[field] for field in _QUEST_COLUMNS)
    with closing(_connect_existing(database_path)) as connection:
        with connection:
            connection.execute(
                "INSERT INTO quests (" + ", ".join(_QUEST_COLUMNS)
                + ") VALUES (?, ?, ?, ?, ?, ?, ?)", values,
            )


def load_quests(database_path: str | PathLike[str], status: str | None = None) -> list[dict]:
    """Read independent quest dictionaries in insertion order, optionally filtered.

    status must be None, 'pending', or 'completed'; otherwise raise ValueError.
    An initialized empty database returns []. Reads never create a missing file
    or regenerate descriptions. Path rules match initialize_database; SQLite
    errors propagate for missing files/tables or other database problems.
    """
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
    """Read {'totalXP': saved_integer}; calculate the level with progression.

    Use an initialized database. A missing progress row raises ValueError;
    missing files/tables and other database errors propagate as SQLite errors.
    Path rules match initialize_database. No row is created or XP awarded, and
    the returned dictionary can be changed without changing stored progress.
    """
    with closing(_connect_existing(database_path, readonly=True)) as connection:
        row = connection.execute("SELECT totalXP FROM progress WHERE id = 1").fetchone()
    if row is None:
        raise ValueError("progress is not initialized; call initialize_database first")
    return {"totalXP": row[0]}


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
    # Encode URI-special characters in filenames, and never create a typo'd path.
    path = Path(_validate_database_path(database_path)).resolve().as_uri()
    return sqlite3.connect(path + ("?mode=ro" if readonly else "?mode=rw"), uri=True)
