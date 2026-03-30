"""Session and scan agent database operations."""

from __future__ import annotations
import json
import uuid
from datetime import datetime, timezone

from .connection import get_conn
from .models import Session, ScanAgent


def now() -> str:
    """Get current UTC timestamp in ISO format."""
    return datetime.now(timezone.utc).isoformat()


# ── Sessions ──────────────────────────────────────────────────

def create_session(
    target: str,
    target_type: str,
    config: dict,
    lang_info: dict | None = None,
) -> Session:
    """Create a new scan session.
    
    Args:
        target: Target path or URL
        target_type: Type of target ('filesystem', 'url', 'mixed')
        config: Configuration dict (model, provider, agents, etc.)
        lang_info: Optional language detection info
        
    Returns:
        Created Session instance
    """
    session = Session(
        id=str(uuid.uuid4()),
        target=target,
        target_type=target_type,
        config_json=config,
        lang_info_json=lang_info or {},
        started_at=now(),
    )
    with get_conn() as conn:
        conn.execute("""
            INSERT INTO sessions
            (id, target, target_type, status, config_json,
             lang_info_json, finding_count, started_at)
            VALUES (?,?,?,?,?,?,?,?)
        """, (
            session.id, session.target, session.target_type,
            session.status, json.dumps(session.config_json),
            json.dumps(session.lang_info_json),
            0, session.started_at,
        ))
    return session


def get_session(session_id: str) -> Session | None:
    """Get session by ID.
    
    Args:
        session_id: Session UUID
        
    Returns:
        Session instance or None if not found
    """
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM sessions WHERE id = ?", (session_id,)
        ).fetchone()
    if not row:
        return None
    d = dict(row)
    d["config_json"] = json.loads(d["config_json"] or "{}")
    d["lang_info_json"] = json.loads(d["lang_info_json"] or "{}")
    return Session(**d)


def list_sessions(limit: int = 20) -> list[Session]:
    """List recent sessions.
    
    Args:
        limit: Maximum number of sessions to return
        
    Returns:
        List of Session instances
    """
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM sessions ORDER BY started_at DESC LIMIT ?",
            (limit,)
        ).fetchall()
    result = []
    for row in rows:
        d = dict(row)
        d["config_json"] = json.loads(d["config_json"] or "{}")
        d["lang_info_json"] = json.loads(d["lang_info_json"] or "{}")
        result.append(Session(**d))
    return result


def finish_session(session_id: str, status: str = "completed") -> None:
    """Mark session as finished.
    
    Args:
        session_id: Session UUID
        status: Final status ('completed', 'failed', 'cancelled')
    """
    with get_conn() as conn:
        conn.execute(
            "UPDATE sessions SET status=?, finished_at=? WHERE id=?",
            (status, now(), session_id)
        )


def get_summary(session_id: str) -> dict | None:
    """Get session summary from view.
    
    Args:
        session_id: Session UUID
        
    Returns:
        Dict with summary data or None
    """
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM v_session_summary WHERE id=?", (session_id,)
        ).fetchone()
    return dict(row) if row else None


# ── Scan agents ───────────────────────────────────────────────

def register_agent(session_id: str, name: str) -> ScanAgent:
    """Register a new scan agent.
    
    Args:
        session_id: Parent session UUID
        name: Agent name (e.g., 'SAST', 'DAST')
        
    Returns:
        Created ScanAgent instance
    """
    agent = ScanAgent(
        id=str(uuid.uuid4()),
        session_id=session_id,
        name=name,
    )
    with get_conn() as conn:
        conn.execute("""
            INSERT INTO scan_agents (id, session_id, name, status, progress)
            VALUES (?,?,?,?,?)
        """, (agent.id, agent.session_id, agent.name, agent.status, agent.progress))
    return agent


def update_agent(
    agent_id: str,
    status: str | None = None,
    progress: float | None = None,
    error: str | None = None,
) -> None:
    """Update agent status and progress.
    
    Args:
        agent_id: Agent UUID
        status: New status (pending, running, completed, failed, skipped)
        progress: Progress value 0.0-1.0
        error: Error message if failed
    """
    fields, values = [], []
    if status is not None:
        fields.append("status=?")
        values.append(status)
        if status == "running":
            fields.append("started_at=?")
            values.append(now())
        elif status in ("completed", "failed", "skipped"):
            fields.append("finished_at=?")
            values.append(now())
    if progress is not None:
        fields.append("progress=?")
        values.append(progress)
    if error is not None:
        fields.append("error=?")
        values.append(error)
    if not fields:
        return
    values.append(agent_id)
    with get_conn() as conn:
        conn.execute(
            f"UPDATE scan_agents SET {', '.join(fields)} WHERE id=?",
            values
        )


def get_agent(session_id: str, name: str) -> ScanAgent | None:
    """Get agent by session and name.
    
    Args:
        session_id: Parent session UUID
        name: Agent name
        
    Returns:
        ScanAgent instance or None
    """
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM scan_agents WHERE session_id=? AND name=?",
            (session_id, name)
        ).fetchone()
    return ScanAgent(**dict(row)) if row else None


def get_all_agents(session_id: str) -> list[ScanAgent]:
    """Get all agents for a session.
    
    Args:
        session_id: Parent session UUID
        
    Returns:
        List of ScanAgent instances
    """
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM scan_agents WHERE session_id=? ORDER BY started_at",
            (session_id,)
        ).fetchall()
    return [ScanAgent(**dict(r)) for r in rows]
