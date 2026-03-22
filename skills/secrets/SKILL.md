---
name: secrets
description: 'Strict secrets detection methodology, composite entropy heuristics, explicit redaction bounds, and false-positive filtering for hardcoded credentials analysis.'
---

# Secrets Detection Skill

This skill enforces a strict, context-aware workflow for locating exposed credentials and high-entropy API keys across source code, configurations, and git histories.

## When to Activate
• Scanning local repositories, config files, and `.env` templates for hardcoded credentials
• Reviewing pull requests and code diffs for accidental key exposure
• Validating suspected token formats (e.g., AWS, Stripe, GitHub, Slack)
• Filtering false positives like dummy credentials in unit tests or mock datasets

## Security & Pattern Checklist

### 1. Composite Detection & Entropy Analysis
Pure regex leads to massive false-positive inflation. Always correlate entropy with context.

#### ✅ ALWAYS Verify This
- Rely on [Secrets Patterns](./patterns.yaml) to identify well-known programmatic key structures (e.g., `AKIA...` for AWS).
- Pair high-Shannon entropy mathematical checks with contextual anchors nearby (e.g., `client_secret`, `bearer`, `api_token`, `authorization`).
- Check base64 strings and encoded blobs inside `.yaml` or `.json` payloads specifically deployed by orchestration (like Kubernetes Secrets).

#### Verification Steps
- [ ] Confirmed format matches against known provider signatures.
- [ ] Nearby variables or assignments analyzed to verify contextual intent.
- [ ] Surrounding codebase examined for testing namespaces.

### 2. Contextual Nullification (False Positives)
Do not flag intentionally public or dummy data as critical vulnerabilities.

#### ❌ NEVER Accept This
- Reporting obvious placeholder values (`"your_api_key_here"`, `"password123"`, `<INSERT_TOKEN>`) as Critical exposures.
- Flagging UUIDs, long numeric IDs, or standard configuration dictionaries just because they match string length heuristics.
- Reporting "Public" keys explicitly intended for client-side inclusion (e.g., `pk_live_...` for Stripe, Firebase public init vars) with identical severity to a secret key.

#### Verification Steps
- [ ] File path validated; not currently analyzing a `tests/`, `fixtures/`, or `/mock` directory.
- [ ] Key type explicitly identified (e.g., Public Key vs. Private Key).
- [ ] Variable context checked—ensure the variable isn't resolving from the environment, e.g., `const API_KEY = process.env.API_KEY`.

### 3. Masking & Output Bounds
Secrets MUST be sanitized before transmission or reporting out of the agent boundary.

#### ✅ ALWAYS Verify This
- Redact secrets using a recognizable format (e.g., `<PROVIDER>_SECRET[REDACTED]`, or showing only the first 4 and last 4 characters: `AKIA**********ABCD`).
- Provide precise repository, file, block/line number, and git commit origins.

#### Verification Steps
- [ ] Full plaintext secret is completely stripped from the final markdown/JSON response.
- [ ] Mapping is assigned to CWE-798 (Use of Hard-coded Credentials).

---

## Analysis & Reporting Guide

### Multi-Line Secret Validation
Look out for PEM/RSA keys:
- Validate header/footer constructs (`-----BEGIN PRIVATE KEY-----`).
- Reject the finding if it is explicitly noted as a generic test fixture in the comments.

## Rules of Engagement
- **No Verification Transmissions**: NEVER attempt to `curl` or authenticate against live provider APIs using the discovered keys. Your testing bound is completely passive.
- **Reporting Fidelity**: Provide redacted traces emphasizing the immediate variable context and origin line to aid developers in immediate rotation.
