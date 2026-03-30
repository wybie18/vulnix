"""Report generation database operations."""

from __future__ import annotations
import json
import uuid
from datetime import datetime, timezone

from .connection import get_conn
from .models import Report


def now() -> str:
    """Get current UTC timestamp in ISO format."""
    return datetime.now(timezone.utc).isoformat()


def insert_report(report: Report) -> None:
    """Insert a generated report.
    
    Args:
        report: Report instance to insert
    """
    report.id = report.id or str(uuid.uuid4())
    report.created_at = report.created_at or now()
    with get_conn() as conn:
        conn.execute("""
            INSERT INTO reports
            (id, session_id, format, file_path, summary_json, created_at)
            VALUES (?,?,?,?,?,?)
        """, (
            report.id, report.session_id, report.format,
            report.file_path, json.dumps(report.summary_json),
            report.created_at,
        ))


def get_reports(session_id: str) -> list[Report]:
    """Get all reports for a session.
    
    Args:
        session_id: Parent session UUID
        
    Returns:
        List of Report instances
    """
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM reports WHERE session_id=? ORDER BY created_at DESC",
            (session_id,)
        ).fetchall()
    result = []
    for row in rows:
        d = dict(row)
        d["summary_json"] = json.loads(d.get("summary_json") or "{}")
        result.append(Report(**d))
    return result


def get_report(report_id: str) -> Report | None:
    """Get report by ID.
    
    Args:
        report_id: Report UUID
        
    Returns:
        Report instance or None
    """
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM reports WHERE id=?", (report_id,)
        ).fetchone()
    if not row:
        return None
    d = dict(row)
    d["summary_json"] = json.loads(d.get("summary_json") or "{}")
    return Report(**d)
