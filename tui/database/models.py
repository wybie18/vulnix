"""Pydantic models for VULNIX database."""

from __future__ import annotations
import hashlib
from typing import Any
from pydantic import BaseModel, Field


class Session(BaseModel):
    """Vulnerability scan session."""
    id: str
    target: str
    target_type: str  # 'filesystem' | 'url' | 'mixed'
    status: str = "running"
    config_json: dict = Field(default_factory=dict)
    lang_info_json: dict = Field(default_factory=dict)
    finding_count: int = 0
    started_at: str
    finished_at: str | None = None


class ScanAgent(BaseModel):
    """Individual scan agent instance."""
    id: str
    session_id: str
    name: str
    status: str = "pending"
    progress: float = 0.0
    error: str | None = None
    started_at: str | None = None
    finished_at: str | None = None


class Finding(BaseModel):
    """Security or QA finding."""
    id: str
    session_id: str
    agent: str
    title: str
    severity: str  # critical | high | medium | low | info
    cwe: str | None = None
    cvss: float | None = None
    file: str | None = None
    line: int | None = None
    detail: str = ""
    remediation: str | None = None
    confidence: str = "medium"
    references_json: list[str] = Field(default_factory=list)
    raw_json: dict = Field(default_factory=dict)
    created_at: str = ""

    @property
    def dedup_key(self) -> str:
        """Generate deduplication key."""
        raw = f"{self.title}:{self.cwe}:{self.line}:{self.file}"
        return hashlib.sha1(raw.encode()).hexdigest()[:16]

    @property
    def severity_rank(self) -> int:
        """Get numeric severity rank for sorting."""
        return {"critical": 0, "high": 1, "medium": 2,
                "low": 3, "info": 4}.get(self.severity, 5)


class Message(BaseModel):
    """LLM conversation message."""
    id: int | None = None
    scan_agent_id: str
    role: str  # system | user | assistant
    content: str
    tokens: int | None = None
    created_at: str = ""


class Event(BaseModel):
    """System event log entry."""
    id: int | None = None
    session_id: str
    type: str  # log | progress | finding | error | done
    agent: str | None = None
    payload_json: dict = Field(default_factory=dict)
    created_at: str = ""


class AgentRun(BaseModel):
    """Tool execution record."""
    id: int | None = None
    scan_agent_id: str
    tool: str
    command: str | None = None
    exit_code: int | None = None
    stdout: str | None = None
    stderr: str | None = None
    duration_ms: int | None = None
    ran_at: str = ""


class Poc(BaseModel):
    """Proof-of-concept exploit code."""
    id: str
    finding_id: str
    language: str
    code: str
    run_instructions: str | None = None
    expected_output: str | None = None
    risk_note: str | None = None
    created_at: str = ""


class Patch(BaseModel):
    """Remediation patch."""
    id: str
    finding_id: str
    original_code: str
    fixed_code: str
    explanation: str | None = None
    breaking_change: bool = False
    references_json: list[str] = Field(default_factory=list)
    created_at: str = ""


class Report(BaseModel):
    """Generated report file."""
    id: str
    session_id: str
    format: str  # json | html | pdf | sarif | markdown
    file_path: str
    summary_json: dict = Field(default_factory=dict)
    created_at: str = ""
