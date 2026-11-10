"""Initialize file-backed storage for one local quest-planner user."""

from contextlib import closing
from os import PathLike, fspath
import sqlite3


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
    if not isinstance(database_path, (str, PathLike)):
        raise TypeError("database_path must be a string or a text path-like object")
    path = fspath(database_path)
    if not isinstance(path, str):
        raise TypeError("database_path must be a string or a text path-like object")
    if not path.strip() or path == ":memory:" or path.startswith("file:"):
        raise ValueError("database_path must name a file, not a temporary database or URI")

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
