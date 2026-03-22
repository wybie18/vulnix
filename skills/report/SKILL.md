---
name: report
description: 'Report generation methodology. Enforces consistent risk ratings, actionable executive summaries, and standard output artifacts (SARIF, HTML, Markdown).'
---

# Vulnerability Reporting Skill

This skill enforces a professional, structured methodology for translating raw, technical vulnerability findings into actionable reports for both executive stakeholders and technical development teams.

## When to Activate
• Consolidating normalized vulnerability data from the `result_interpreter` into massive final reports.
• Applying risk rating frameworks (CVSS v3.1, OWASP Risk Rating) defensively to ensure consistency across findings.
• Generating standardized format templates (SARIF, Markdown, HTML).

## Reporting & Documentation Checklist

### 1. The Executive Summary
Executives don't care about a missing HttpOnly flag—they care about business impact.

#### ❌ NEVER Accept This
- Jargon-heavy summaries ("We found 4 XSS and 1 SQLi using AddressSanitizer over the REST API webhook").
- Raw lists of vulnerabilities without indicating strategic fixes.

#### ✅ ALWAYS Verify This
- Translate technical jargon into Business Risk (e.g., "Attackers could permanently delete production customer data via unauthenticated inputs").
- Highlight systemic issues (e.g., "The application lacks a centralized output-encoding mechanism, leading to 14 distinct cross-site scripting flaws").

#### Verification Steps
- [ ] Summary is understandable by a non-technical reader (CEO/CISO).
- [ ] Strategic, high-level remediation roadmap provided (e.g., "Implement a WAF, migrate to a modern ORM").

### 2. Risk Rating Consistency (CVSS Matrix)
Ensure 5 different scanners don't rate the same vulnerability 5 different ways.

#### ❌ NEVER Accept This
- An unexploitable "Theoretical" vulnerability marked as `Critical`.
- Inconsistent severity for the same bug class across the report.

#### ✅ ALWAYS Do This
- Enforce the chosen risk matrix strongly. If using CVSS v3.1, apply vectors accurately.
  - **Critical**: Remote Code Execution (RCE), Unauthenticated mass data exfiltration (SQLi).
  - **High**: Stored XSS mapped to Admin sessions, Subdomain Takeover.
  - **Medium**: Reflected XSS, CSRF, Misconfigured CORS (null).
  - **Low**: Missing security headers (CSP, HSTS).

#### Verification Steps
- [ ] All vulnerabilities contain an explicit Severity (Critical, High, Medium, Low).
- [ ] Verified PoCs appended to all High/Critical findings to prove exploitability.

### 3. Artifact Scaffolding (SARIF/HTML)
Deliver the generated report in requested structured formats.

#### ✅ ALWAYS Use Templates
Format technical deliverables seamlessly leveraging the built-in templates:
- [HTML Penetration Test Report](./templates/report.html.j2)
- [Executive Summary Markdown](./templates/report_executive.md.j2)
- [SARIF JSON Schema Output](./templates/sarif_template.json)

#### Verification Steps
- [ ] SARIF files strictly validate against the OASIS standard `2.1.0` schema.
- [ ] HTML outputs include embedded PoCs and clean markdown-to-HTML rendering.
