---
name: dast
description: 'Strict dynamic testing methodology, header checks, CORS evaluation, XSS/SSRF/SQLi/SSTI/LFI analysis guide, and comprehensive web vulnerability probing payloads. Use for authoritative DAST testing and black-box application fuzzing.'
---

# Dynamic Application Security Testing (DAST) Skill

This skill enforces a strict, multi-step methodology for Dynamic Application Security Testing (DAST). It ensures that all testing covers required security boundaries without skipping critical details.

## When to Activate
• Running Dynamic Application Security Testing against live web applications or APIs
• Performing active penetration testing / fuzzing of application inputs
• Evaluating HTTP Security Headers, CORS, and Cookie security flags
• Mapping and probing attack surfaces for XSS, SQLi, SSRF, SSTI, LFI, and other runtime vulnerabilities
• Verifying automated scan findings or investigating undocumented API endpoints

## Security & Penetration Checklist

### 1. HTTP Security Headers & TLS Configuration
Evaluate default platform defenses before attacking business logic.

#### ✅ ALWAYS Verify This
- Check for `Strict-Transport-Security` (HSTS) protecting against downgrade attacks.
- Verify `Content-Security-Policy` (CSP) is explicitly defined, not relying on 'unsafe-inline' or 'unsafe-eval'.
- Ensure `X-Frame-Options` is set to `DENY` or `SAMEORIGIN`.
- Ensure `X-Content-Type-Options: nosniff`.
- Check Cookie flags: `HttpOnly`, `Secure`, and `SameSite` must be enforced.

#### Verification Steps
- [ ] No missing security headers on sensitive endpoints.
- [ ] Cookies initiating state/sessions are heavily restricted.
- [ ] TLS endpoints enforce strong ciphers and drop outdated protocols (TLS 1.0/1.1).

### 2. Cross-Origin Resource Sharing (CORS) Misconfigurations
Evaluate how APIs handle origin requests.

#### ❌ NEVER Accept This
- `Access-Control-Allow-Origin: *` mixed with `Access-Control-Allow-Credentials: true`.
- Dynamic reflection of the explicit `Origin` header without strict whitelisting.
- Acceptance of `null` origin.

#### Verification Steps
- [ ] Send `Origin: https://evil.com` and observe reflection.
- [ ] Send `Origin: null` and observe response.
- [ ] Ensure credentials/cookies aren't permitted on wildcards.

### 3. Fuzzing & Input Reflection (XSS, SQLi, SSTI, LFI)
Do not assume client-side protections map to server-side security. 

#### ✅ ALWAYS Test Multiple Contexts
- Load appropriate payload references:
  - `[XSS Payloads](./payloads/xss.txt)`
  - `[SQLi Payloads](./payloads/sqli.txt)`
  - `[SSTI Payloads](./payloads/ssti.txt)`
  - `[LFI Payloads](./payloads/lfi.txt)`
- Send payloads via JSON bodies, XML elements, Query Params, Path variables, and HTTP Headers (e.g., `User-Agent`, `X-Forwarded-For`).
- Check for asynchronous reflections (e.g., payloads firing in an admin dashboard, not just directly in the immediate response).

#### Verification Steps
- [ ] All input vectors fuzzed.
- [ ] Output encoding verified on reflected inputs (XSS).
- [ ] Time-based analysis performed for blind SQLi and Command Injection.
- [ ] Application does not bleed server internals (Stack traces, versions) on malformed requests.

### 4. Authentication, Session & Access Controls (IDOR)
Business logic flaws cannot be entirely automated.

#### ❌ NEVER Do This
- Trust sequential numeric IDs without authorization checks.
- Proceed without testing Parameter Pollution or HTTP Verb Tampering.

#### ✅ ALWAYS Do This
- Attempt unauthenticated access on protected endpoints.
- Attempt B-User access on A-User resources (Horizontal Privilege Escalation).
- Attempt lower-privileged user access on admin endpoints (Vertical Privilege Escalation).

#### Verification Steps
- [ ] Insecure Direct Object References (IDOR) mapped and tested.
- [ ] Session tokens are invalidated properly on logout.
- [ ] Reusing old session tokens yields `401 Unauthorized`.

---

## Analysis & Reporting Guide

### Cross-Site Scripting (XSS)
Validate the *exact* reflection context:
- Inside HTML tags (`<div>REFLECTED</div>`)
- Inside HTML attributes (`<input value="REFLECTED">`)
- Inside JavaScript blocks (`<script>var x = 'REFLECTED';</script>`)
- Use context-breaking payloads before standard test strings depending on the reflection point.

### Server-Side Request Forgery (SSRF)
Identify endpoints capable of fetching external resources (webhooks, import features, PDF generators):
- Probe with internal, non-routable IPs (e.g., `127.0.0.1`, `localhost`, `169.254.169.254`).
- Utilize alternative wrappers (`file://`, `dict://`, `gopher://`).
- Check for blind SSRF utilizing out-of-band (OOB) techniques.

## Rules of Engagement
- **Non-Destructive Active Testing**: NEVER run `DROP`, `DELETE`, or `UPDATE` queries during blind SQL attacks. Use harmless operations (e.g., `SELECT 1`, `SLEEP`).
- **No Persistence**: NEVER upload permanent webshells on production environments.
- **Reporting Fidelity**: Provide verbatim HTTP Request/Response pairs verifying the exploit to reduce false positives.
