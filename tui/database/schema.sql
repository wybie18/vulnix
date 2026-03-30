-- ─────────────────────────────────────────────────────────────
-- vulnix.db  —  full SQLite schema
-- ─────────────────────────────────────────────────────────────

-- ─────────────────────────────────────────────────────────────
-- 1. SESSIONS
--    One row per vulnix scan invocation.
-- ─────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS sessions (
    id              TEXT    PRIMARY KEY,
    target          TEXT    NOT NULL,
    target_type     TEXT    NOT NULL
                    CHECK (target_type IN ('filesystem', 'url', 'mixed')),
    status          TEXT    NOT NULL DEFAULT 'running'
                    CHECK (status IN ('running', 'completed', 'failed', 'cancelled')),
    config_json     TEXT,
    lang_info_json  TEXT,
    finding_count   INTEGER NOT NULL DEFAULT 0,
    started_at      TEXT    NOT NULL,
    finished_at     TEXT
);


-- ─────────────────────────────────────────────────────────────
-- 2. SCAN_AGENTS
--    One row per agent per session. Tracks lifecycle + progress.
-- ─────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS scan_agents (
    id              TEXT    PRIMARY KEY,
    session_id      TEXT    NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
    name            TEXT    NOT NULL,
    status          TEXT    NOT NULL DEFAULT 'pending'
                    CHECK (status IN ('pending', 'running', 'completed', 'failed', 'skipped')),
    progress        REAL    NOT NULL DEFAULT 0.0
                    CHECK (progress BETWEEN 0.0 AND 1.0),
    error           TEXT,
    started_at      TEXT,
    finished_at     TEXT,
    UNIQUE (session_id, name)
);


-- ─────────────────────────────────────────────────────────────
-- 3. FINDINGS
--    Every security / QA finding from every agent.
-- ─────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS findings (
    id              TEXT    PRIMARY KEY,
    session_id      TEXT    NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
    agent           TEXT    NOT NULL,
    title           TEXT    NOT NULL,
    severity        TEXT    NOT NULL
                    CHECK (severity IN ('critical', 'high', 'medium', 'low', 'info')),
    cwe             TEXT,
    cvss            REAL    CHECK (cvss IS NULL OR cvss BETWEEN 0.0 AND 10.0),
    file            TEXT,
    line            INTEGER CHECK (line IS NULL OR line > 0),
    detail          TEXT,
    remediation     TEXT,
    confidence      TEXT    NOT NULL DEFAULT 'medium'
                    CHECK (confidence IN ('high', 'medium', 'low')),
    dedup_key       TEXT,
    references_json TEXT,
    raw_json        TEXT,
    created_at      TEXT    NOT NULL
);


-- ─────────────────────────────────────────────────────────────
-- 4. MESSAGES
--    Full AI conversation history per agent per session.
--    Enables resumable context — feed back to the LLM on retry.
-- ─────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS messages (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    scan_agent_id   TEXT    NOT NULL REFERENCES scan_agents(id) ON DELETE CASCADE,
    role            TEXT    NOT NULL
                    CHECK (role IN ('system', 'user', 'assistant')),
    content         TEXT    NOT NULL,
    tokens          INTEGER,
    created_at      TEXT    NOT NULL
);


-- ─────────────────────────────────────────────────────────────
-- 5. EVENTS
--    Append-only log of everything that happened during a scan.
--    Feeds the RichLog pane in the TUI. Survives agent crashes.
-- ─────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS events (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id      TEXT    NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
    type            TEXT    NOT NULL
                    CHECK (type IN ('log', 'progress', 'finding', 'error', 'done')),
    agent           TEXT,
    payload_json    TEXT    NOT NULL,
    created_at      TEXT    NOT NULL
);


-- ─────────────────────────────────────────────────────────────
-- 6. AGENT_RUNS
--    Every subprocess/CLI tool invocation by any agent.
--    Used for debugging: "what exact command did semgrep run?"
-- ─────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS agent_runs (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    scan_agent_id   TEXT    NOT NULL REFERENCES scan_agents(id) ON DELETE CASCADE,
    tool            TEXT    NOT NULL,
    command         TEXT,
    exit_code       INTEGER,
    stdout          TEXT,
    stderr          TEXT,
    duration_ms     INTEGER,
    ran_at          TEXT    NOT NULL
);


-- ─────────────────────────────────────────────────────────────
-- 7. FINDING_TAGS
--    Flexible label system: OWASP categories, custom tags, etc.
-- ─────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS finding_tags (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    finding_id      TEXT    NOT NULL REFERENCES findings(id) ON DELETE CASCADE,
    tag             TEXT    NOT NULL,
    UNIQUE (finding_id, tag)
);


-- ─────────────────────────────────────────────────────────────
-- 8. POCS
--    Proof-of-concept code generated by the exploit agent.
-- ─────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS pocs (
    id              TEXT    PRIMARY KEY,
    finding_id      TEXT    NOT NULL REFERENCES findings(id) ON DELETE CASCADE,
    language        TEXT    NOT NULL,
    code            TEXT    NOT NULL,
    run_instructions TEXT,
    expected_output TEXT,
    risk_note       TEXT,
    created_at      TEXT    NOT NULL
);


-- ─────────────────────────────────────────────────────────────
-- 9. PATCHES
--    Remediation patches generated by the fix agent.
-- ─────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS patches (
    id              TEXT    PRIMARY KEY,
    finding_id      TEXT    NOT NULL REFERENCES findings(id) ON DELETE CASCADE,
    original_code   TEXT    NOT NULL,
    fixed_code      TEXT    NOT NULL,
    explanation     TEXT,
    breaking_change INTEGER NOT NULL DEFAULT 0
                    CHECK (breaking_change IN (0, 1)),
    references_json TEXT,
    created_at      TEXT    NOT NULL
);


-- ─────────────────────────────────────────────────────────────
-- 10. REPORTS
--     Output files generated by the report agent.
-- ─────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS reports (
    id              TEXT    PRIMARY KEY,
    session_id      TEXT    NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
    format          TEXT    NOT NULL
                    CHECK (format IN ('json', 'html', 'pdf', 'sarif', 'markdown')),
    file_path       TEXT    NOT NULL,
    summary_json    TEXT,
    created_at      TEXT    NOT NULL
);


-- ─────────────────────────────────────────────────────────────
-- INDEXES
-- ─────────────────────────────────────────────────────────────

CREATE INDEX IF NOT EXISTS idx_findings_session
    ON findings (session_id);
CREATE INDEX IF NOT EXISTS idx_findings_severity
    ON findings (session_id, severity);
CREATE INDEX IF NOT EXISTS idx_findings_agent
    ON findings (session_id, agent);
CREATE INDEX IF NOT EXISTS idx_findings_dedup
    ON findings (dedup_key);
CREATE INDEX IF NOT EXISTS idx_findings_cwe
    ON findings (cwe);

CREATE INDEX IF NOT EXISTS idx_messages_agent
    ON messages (scan_agent_id);

CREATE INDEX IF NOT EXISTS idx_events_session
    ON events (session_id, id);
CREATE INDEX IF NOT EXISTS idx_events_type
    ON events (session_id, type);

CREATE INDEX IF NOT EXISTS idx_runs_agent
    ON agent_runs (scan_agent_id);
CREATE INDEX IF NOT EXISTS idx_runs_tool
    ON agent_runs (tool);

CREATE INDEX IF NOT EXISTS idx_scan_agents_session
    ON scan_agents (session_id);


-- ─────────────────────────────────────────────────────────────
-- TRIGGERS
-- ─────────────────────────────────────────────────────────────

CREATE TRIGGER IF NOT EXISTS trg_finding_count_insert
AFTER INSERT ON findings
BEGIN
    UPDATE sessions
    SET finding_count = finding_count + 1
    WHERE id = NEW.session_id;
END;

CREATE TRIGGER IF NOT EXISTS trg_finding_count_delete
AFTER DELETE ON findings
BEGIN
    UPDATE sessions
    SET finding_count = finding_count - 1
    WHERE id = OLD.session_id;
END;

CREATE TRIGGER IF NOT EXISTS trg_session_complete
AFTER UPDATE OF status ON scan_agents
WHEN NEW.status IN ('completed', 'failed', 'skipped')
BEGIN
    UPDATE sessions
    SET status = 'completed',
        finished_at = datetime('now')
    WHERE id = NEW.session_id
      AND NOT EXISTS (
          SELECT 1 FROM scan_agents
          WHERE session_id = NEW.session_id
            AND status IN ('pending', 'running')
      );
END;


-- ─────────────────────────────────────────────────────────────
-- VIEWS
-- ─────────────────────────────────────────────────────────────

CREATE VIEW IF NOT EXISTS v_session_summary AS
SELECT
    s.id,
    s.target,
    s.target_type,
    s.status,
    s.started_at,
    s.finished_at,
    s.finding_count,
    SUM(CASE WHEN f.severity = 'critical' THEN 1 ELSE 0 END) AS critical,
    SUM(CASE WHEN f.severity = 'high'     THEN 1 ELSE 0 END) AS high,
    SUM(CASE WHEN f.severity = 'medium'   THEN 1 ELSE 0 END) AS medium,
    SUM(CASE WHEN f.severity = 'low'      THEN 1 ELSE 0 END) AS low,
    SUM(CASE WHEN f.severity = 'info'     THEN 1 ELSE 0 END) AS info
FROM sessions s
LEFT JOIN findings f ON f.session_id = s.id
GROUP BY s.id;

CREATE VIEW IF NOT EXISTS v_findings_enriched AS
SELECT
    f.*,
    ft.tags,
    CASE WHEN p.id IS NOT NULL THEN 1 ELSE 0 END AS has_poc,
    CASE WHEN pa.id IS NOT NULL THEN 1 ELSE 0 END AS has_patch
FROM findings f
LEFT JOIN (
    SELECT finding_id, GROUP_CONCAT(tag, ', ') AS tags
    FROM finding_tags
    GROUP BY finding_id
) ft ON ft.finding_id = f.id
LEFT JOIN pocs p ON p.finding_id = f.id
LEFT JOIN patches pa ON pa.finding_id = f.id;

CREATE VIEW IF NOT EXISTS v_agent_performance AS
SELECT
    sa.session_id,
    sa.name          AS agent,
    sa.status,
    sa.started_at,
    sa.finished_at,
    ROUND(
        (JULIANDAY(sa.finished_at) - JULIANDAY(sa.started_at)) * 86400
    )                AS duration_seconds,
    COUNT(f.id)      AS findings_produced,
    COUNT(ar.id)     AS tool_runs
FROM scan_agents sa
LEFT JOIN findings f  ON f.agent = sa.name AND f.session_id = sa.session_id
LEFT JOIN agent_runs ar ON ar.scan_agent_id = sa.id
GROUP BY sa.id;
