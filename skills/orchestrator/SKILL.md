---
name: orchestrator
description: 'Strategic phase planning, intelligent agent selection, target routing rules, and scope boundary enforcement. Use this skill as the master planner when initiating a full vulnerability assessment.'
---

# Orchestrator & Campaign Planning Skill

This skill enforces a methodological, scoped framework for managing an entire vulnerability assessment lifecycle. It acts as the command-and-control layer, dictating which specialized agents run, in what order, and keeping them strictly within the authorized Rules of Engagement (RoE).

## When to Activate
• Initiating a net-new vulnerability assessment, penetration test, or architecture review.
• Deciding which specialized agents (`sast`, `dast`, `fuzz`, `network`) are applicable to a given target list.
• Consolidating scattered discoveries and determining if a newly discovered asset (`Subdomain X`) should trigger a new agent lifecycle.
• Enforcing Scope and Rules of Engagement (RoE) before tests begin.

## Orchestration Checklist

### 1. Scope Definition & Boundary Enforcement
The most critical phase. An agent must never scan outside the defined rules.

#### ❌ NEVER Accept This
- A target scope like `*.company.com` without confirming if specific subdomains are explicitly out-of-bounds (OOB) or hosted by 3rd-party SaaS providers.
- Authorizing active exploitation (`exploit` agent) during a predefined "Read-Only/Reconnaissance" phase.
- Ignoring blacklisted URIs (e.g., automatically fuzzing an `/admin/delete_user` endpoint during an unauthenticated scan).

#### ✅ ALWAYS Verify This
- Build an explicit inclusion list (Targets) and exclusion list (Blacklist).
- Ensure network scanning/fuzzing is throttled to respect the environment (Staging vs. Production).

#### Verification Steps
- [ ] Explicit IP blocks, URIs, and Repositories documented.
- [ ] Production databases strictly excluded from write/delete load testing.
- [ ] Excluded 3rd-party SaaS explicitly filtered out of automated scans.

### 2. Phase Phasing & Agent Routing
Security testing is a linear, dependent process. Do not run out of order.

#### 🔄 Execution Pipeline
1. **Reconnaissance & Footprinting**: Route to `network` (Ports, Subdomains).
2. **Static & Composition Analysis**: Route to `dependency`, `secrets`, and `sast` if source code is provided.
3. **Dynamic Analysis**: Route to `dast` running against live applications.
4. **Deep Fuzzing**: Route to `fuzz` for complex binary/API inputs.
5. **Validation**: Route to `exploit` to confirm findings safely.
6. **Remediation**: Route to `fix` to generate code patches.
7. **Consolidation**: Route to `result_interpreter` and `report`.

#### Verification Steps
- [ ] Reconnaissance data fully processed before launching blind DAST attacks.
- [ ] Source code dependencies scanned prior to active fuzzing payloads.

### 3. Context Context Pivoting & Handoffs
Ensure data cleanly flows between disparate testing tools.

#### ✅ ALWAYS Do This
- When `network` discovers a new HTTP service on port 8443, automatically pipeline that IP:PORT combination down to the `dast` agent for validation.
- When `sast` discovers a SQL injection natively in the code, pipe the file constraint to the `exploit` agent to generate a reproduction PoC.

#### Verification Steps
- [ ] Raw outputs are passed through `result_interpreter` before advancing to `fix`.
- [ ] Duplicate findings from DAST and SAST are merged intelligently into a single vulnerability record.
