"""Database connection management."""

import pathlib
import sqlite3
from contextlib import contextmanager

from config.settings import DB_PATH

_SCHEMA = pathlib.Path(__file__).parent / "schema.sql"


def init_db() -> None:
    """Initialize database with schema."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with get_conn() as conn:
        conn.executescript(_SCHEMA.read_text())


@contextmanager
def get_conn():
    """Get database connection with proper configuration.
    
    Yields:
        sqlite3.Connection: Configured database connection
    """
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.execute("PRAGMA temp_store=MEMORY")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
