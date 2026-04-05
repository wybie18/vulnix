"""LLM conversation history database operations."""

from __future__ import annotations
from datetime import datetime, timezone

from .connection import get_conn
from .models import Message


def now() -> str:
    """Get current UTC timestamp in ISO format."""
    return datetime.now(timezone.utc).isoformat()


def append(scan_agent_id: str, role: str, content: str, tokens: int | None = None) -> None:
    """Append a message to an agent's conversation history.
    
    Args:
        scan_agent_id: Agent UUID
        role: Message role (system, user, assistant)
        content: Message content
        tokens: Optional token count from API response
    """
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO messages (scan_agent_id, role, content, tokens, created_at) "
            "VALUES (?,?,?,?,?)",
            (scan_agent_id, role, content, tokens, now())
        )


def get_history(scan_agent_id: str) -> list[dict]:
    """Get conversation history for an agent.
    
    Returns messages in the format expected by LLM APIs: [{role, content}]
    
    Args:
        scan_agent_id: Agent UUID
        
    Returns:
        List of message dicts
    """
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT role, content FROM messages WHERE scan_agent_id=? ORDER BY id",
            (scan_agent_id,)
        ).fetchall()
    return [{"role": r["role"], "content": r["content"]} for r in rows]


def clear_history(scan_agent_id: str) -> None:
    """Clear all messages for an agent.
    
    Args:
        scan_agent_id: Agent UUID
    """
    with get_conn() as conn:
        conn.execute(
            "DELETE FROM messages WHERE scan_agent_id=?", (scan_agent_id,)
        )


def token_count(scan_agent_id: str) -> int:
    """Get total token count for an agent's conversation.
    
    Args:
        scan_agent_id: Agent UUID
        
    Returns:
        Total tokens used
    """
    with get_conn() as conn:
        row = conn.execute(
            "SELECT COALESCE(SUM(tokens), 0) FROM messages WHERE scan_agent_id=?",
            (scan_agent_id,)
        ).fetchone()
    return row[0]
