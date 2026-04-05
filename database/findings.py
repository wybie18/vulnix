"""Finding, tag, PoC, and patch database operations."""

from __future__ import annotations
import json
import uuid
from datetime import datetime, timezone

from .connection import get_conn
from .models import Finding, Poc, Patch


def now() -> str:
    """Get current UTC timestamp in ISO format."""
    return datetime.now(timezone.utc).isoformat()


# ── Findings ──────────────────────────────────────────────────

def insert_finding(session_id: str, finding: Finding) -> str:
    """Insert a new finding with deduplication.
    
    Args:
        session_id: Parent session UUID
        finding: Finding instance to insert
        
    Returns:
        Finding ID or empty string if duplicate
    """
    finding.id = finding.id or str(uuid.uuid4())
    finding.session_id = session_id
    finding.created_at = finding.created_at or now()

    with get_conn() as conn:
        # Deduplicate — skip if same dedup_key already exists in this session
        exists = conn.execute(
            "SELECT 1 FROM findings WHERE session_id=? AND dedup_key=?",
            (session_id, finding.dedup_key)
        ).fetchone()
        if exists:
            return ""

        conn.execute("""
            INSERT INTO findings
            (id, session_id, agent, title, severity, cwe, cvss,
             file, line, detail, remediation, confidence,
             dedup_key, references_json, raw_json, created_at)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            finding.id, finding.session_id, finding.agent,
            finding.title, finding.severity, finding.cwe, finding.cvss,
            finding.file, finding.line, finding.detail,
            finding.remediation, finding.confidence,
            finding.dedup_key,
            json.dumps(finding.references_json),
            json.dumps(finding.raw_json),
            finding.created_at,
        ))
    return finding.id


def get_findings(
    session_id: str,
    severity: str | None = None,
    agent: str | None = None,
    cwe: str | None = None,
) -> list[Finding]:
    """Get findings with optional filters.
    
    Args:
        session_id: Parent session UUID
        severity: Filter by severity level
        agent: Filter by agent name
        cwe: Filter by CWE identifier
        
    Returns:
        List of Finding instances sorted by severity
    """
    query = "SELECT * FROM findings WHERE session_id=?"
    params: list = [session_id]
    if severity:
        query += " AND severity=?"
        params.append(severity)
    if agent:
        query += " AND agent=?"
        params.append(agent)
    if cwe:
        query += " AND cwe=?"
        params.append(cwe)
    query += """ ORDER BY CASE severity
        WHEN 'critical' THEN 0 WHEN 'high' THEN 1
        WHEN 'medium' THEN 2 WHEN 'low' THEN 3 ELSE 4 END"""

    with get_conn() as conn:
        rows = conn.execute(query, params).fetchall()
    return [_row_to_finding(r) for r in rows]


def get_finding(finding_id: str) -> Finding | None:
    """Get finding by ID.
    
    Args:
        finding_id: Finding UUID
        
    Returns:
        Finding instance or None
    """
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM findings WHERE id=?", (finding_id,)
        ).fetchone()
    return _row_to_finding(row) if row else None


def get_enriched_findings(session_id: str) -> list[dict]:
    """Get findings with tags, PoC, and patch status.
    
    Args:
        session_id: Parent session UUID
        
    Returns:
        List of dicts from v_findings_enriched view
    """
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM v_findings_enriched WHERE session_id=?",
            (session_id,)
        ).fetchall()
    return [dict(row) for row in rows]


def _row_to_finding(row) -> Finding:
    """Convert database row to Finding instance."""
    d = dict(row)
    d["references_json"] = json.loads(d.get("references_json") or "[]")
    d["raw_json"] = json.loads(d.get("raw_json") or "{}")
    return Finding(**d)


# ── Tags ──────────────────────────────────────────────────────

def tag_finding(finding_id: str, tag: str) -> None:
    """Add a tag to a finding.
    
    Args:
        finding_id: Finding UUID
        tag: Tag string (e.g., 'owasp:a03', 'false-positive')
    """
    with get_conn() as conn:
        conn.execute(
            "INSERT OR IGNORE INTO finding_tags (finding_id, tag) VALUES (?,?)",
            (finding_id, tag)
        )


def get_tags(finding_id: str) -> list[str]:
    """Get all tags for a finding.
    
    Args:
        finding_id: Finding UUID
        
    Returns:
        List of tag strings
    """
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT tag FROM finding_tags WHERE finding_id=?", (finding_id,)
        ).fetchall()
    return [r["tag"] for r in rows]


# ── PoCs ──────────────────────────────────────────────────────

def insert_poc(poc: Poc) -> None:
    """Insert a proof-of-concept.
    
    Args:
        poc: Poc instance to insert
    """
    poc.id = poc.id or str(uuid.uuid4())
    poc.created_at = poc.created_at or now()
    with get_conn() as conn:
        conn.execute("""
            INSERT INTO pocs
            (id, finding_id, language, code,
             run_instructions, expected_output, risk_note, created_at)
            VALUES (?,?,?,?,?,?,?,?)
        """, (
            poc.id, poc.finding_id, poc.language, poc.code,
            poc.run_instructions, poc.expected_output,
            poc.risk_note, poc.created_at,
        ))


def get_poc(finding_id: str) -> Poc | None:
    """Get PoC for a finding.
    
    Args:
        finding_id: Finding UUID
        
    Returns:
        Poc instance or None
    """
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM pocs WHERE finding_id=?", (finding_id,)
        ).fetchone()
    return Poc(**dict(row)) if row else None


# ── Patches ───────────────────────────────────────────────────

def insert_patch(patch: Patch) -> None:
    """Insert a remediation patch.
    
    Args:
        patch: Patch instance to insert
    """
    patch.id = patch.id or str(uuid.uuid4())
    patch.created_at = patch.created_at or now()
    with get_conn() as conn:
        conn.execute("""
            INSERT INTO patches
            (id, finding_id, original_code, fixed_code,
             explanation, breaking_change, references_json, created_at)
            VALUES (?,?,?,?,?,?,?,?)
        """, (
            patch.id, patch.finding_id, patch.original_code,
            patch.fixed_code, patch.explanation,
            1 if patch.breaking_change else 0,
            json.dumps(patch.references_json),
            patch.created_at,
        ))


def get_patch(finding_id: str) -> Patch | None:
    """Get patch for a finding.
    
    Args:
        finding_id: Finding UUID
        
    Returns:
        Patch instance or None
    """
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM patches WHERE finding_id=?", (finding_id,)
        ).fetchone()
    if not row:
        return None
    d = dict(row)
    d["references_json"] = json.loads(d.get("references_json") or "[]")
    d["breaking_change"] = bool(d["breaking_change"])
    return Patch(**d)
