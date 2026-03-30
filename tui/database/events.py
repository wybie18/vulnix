"""Event logging database operations."""

from __future__ import annotations
import json
from datetime import datetime, timezone

from .connection import get_conn
from .models import Event


def now() -> str:
    """Get current UTC timestamp in ISO format."""
    return datetime.now(timezone.utc).isoformat()


def append(session_id: str, type: str, payload: dict, agent: str | None = None) -> None:
    """Append an event to the session log.
    
    Args:
        session_id: Parent session UUID
        type: Event type (log, progress, finding, error, done)
        payload: Event payload dict
        agent: Optional agent name that generated the event
    """
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO events (session_id, type, agent, payload_json, created_at) "
            "VALUES (?,?,?,?,?)",
            (session_id, type, agent, json.dumps(payload), now())
        )


def tail(session_id: str, since_id: int = 0, limit: int = 100) -> list[Event]:
    """Fetch recent events after a given ID.
    
    Used by TUI to poll for new log lines.
    
    Args:
        session_id: Parent session UUID
        since_id: Return events after this ID
        limit: Maximum number of events to return
        
    Returns:
        List of Event instances
    """
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM events WHERE session_id=? AND id>? ORDER BY id LIMIT ?",
            (session_id, since_id, limit)
        ).fetchall()
    result = []
    for row in rows:
        d = dict(row)
        d["payload_json"] = json.loads(d["payload_json"])
        result.append(Event(**d))
    return result


def get_all(session_id: str) -> list[Event]:
    """Get all events for a session.
    
    Used for bulk reads during report generation.
    
    Args:
        session_id: Parent session UUID
        
    Returns:
        List of Event instances
    """
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM events WHERE session_id=? ORDER BY id",
            (session_id,)
        ).fetchall()
    result = []
    for row in rows:
        d = dict(row)
        d["payload_json"] = json.loads(d["payload_json"])
        result.append(Event(**d))
    return result


def get_by_type(session_id: str, type: str) -> list[Event]:
    """Get events filtered by type.
    
    Args:
        session_id: Parent session UUID
        type: Event type to filter by
        
    Returns:
        List of Event instances
    """
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM events WHERE session_id=? AND type=? ORDER BY id",
            (session_id, type)
        ).fetchall()
    result = []
    for row in rows:
        d = dict(row)
        d["payload_json"] = json.loads(d["payload_json"])
        result.append(Event(**d))
    return result
