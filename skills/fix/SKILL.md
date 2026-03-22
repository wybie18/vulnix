---
name: fix
description: 'Strict patch generation rules emphasizing minimal invasiveness, breaking-change detection, and idiomatic remediation styles. Use for prescribing exact fixes to discovered vulnerabilities.'
---

# Remediation and Fix Skill

This skill enforces a rigorous, minimally invasive methodology for fixing vulnerabilities identified by QA/VA testing. The objective is to patch the vulnerability with exact, idiomatic code changes while actively preventing functional breakage.

## When to Activate
• Generating direct source code patches for vulnerabilities (SAST/DAST/Fuzzing findings).
• Suggesting dependency update paths (SCA findings).
• Designing defensive configurations or WAF rules when source code cannot be easily modified.
• Evaluating another developer's fix for completeness and regression risk.

## Patch Generation Checklist

### 1. Root Cause & Context Verification
Evaluate the defect within its surrounding architectural context.

#### ❌ NEVER Do This
- Blindly escape input without checking where the data is ultimately rendered (e.g., HTML escaping data that goes into a SQL query).
- Rewrite entire functions or refactor architecture if a simple one-line fix achieves security.

#### ✅ ALWAYS Verify This
- Check the exact type of injection/flaw before deciding the mitigation (e.g., parameterization for SQLi, output encoding for XSS).
- Adopt the existing coding style (naming conventions, error handling, spacing) of the surrounding file.

#### Verification Steps
- [ ] Root cause specifically identified (e.g., "concatenated SQL string").
- [ ] Included context: 3-5 lines of code above and below the vulnerable segment.
- [ ] Selected fix aligns directly with [Remediation References](./remediation_refs.yaml).

### 2. The Patch: Minimal & Idiomatic Security
Apply fixes using native framework protections rather than custom, homegrown filters.

#### ❌ NEVER Accept This
- "Blacklisting" bad characters (e.g., `input.replace("<script>", "")` or `input.replace("'", "")`).
- Replacing standard framework features with overly complex regexes.

#### ✅ ALWAYS Do This
- Use parameterized queries, ORMs, or Prepared Statements for Database operations.
- Use context-aware rendering functions (e.g., React `dangerouslySetInnerHTML` elimination, DOMPurify, standard Flask templates).
- Use strict "Allowlisting" (Whitelisting) for input validation (e.g., ensuring an ID is strictly numeric, not just stripping `-` or `*`).

#### Verification Steps
- [ ] Fix introduces NO custom cryptography or proprietary sanitization algorithms.
- [ ] Validation is strictly "Allowlist" based.
- [ ] Dependency updates strictly target the nearest patched semantic version (e.g., moving from `1.4.1` to `1.4.2`, NOT `1.4.1` to `3.0.0` unless explicitly requested).

### 3. Detecting Breaking Changes (Regression Prevention)
Ensure the patch does not disable legitimate workflows.

#### ❌ NEVER Accept This
- Enforcing aggressive input validation that breaks documented API schemas.
- Adding hard authentication blocks on endpoints explicitly designed to be public (e.g., webhooks, callbacks).
- Removing problematic features entirely unless authorized by the product owner.

#### ✅ ALWAYS Do This
- Document what perfectly valid data might accidentally be caught by the new fix.
- Ensure the fix handles `null` or explicit typing gracefully depending on the language (e.g., TypeScript explicit checks, Python `None` handling).

#### Verification Steps
- [ ] Check if the modified API response schema changed.
- [ ] Verify error states handled securely without leaking stacks.
- [ ] Confirm no legitimate edge-case inputs are blocked by the new allowlist.

### 4. Alternative Mitigations
If a source patch is prohibited, provide environmental configurations.

#### ✅ ALWAYS Include (if applicable)
- WAF (Web Application Firewall) rule stubs.
- Nginx/Apache configuration directives removing vulnerable endpoints.
- Database permission scoping (e.g., downgrading the service account from `dbo` to `read-only`).

---

## Output Format
Always present the fix using standard Markdown Diff blocks, followed by the breaking change analysis.

```diff
-  query = f"SELECT * FROM users WHERE id = {user_id}"
-  cursor.execute(query)
+  query = "SELECT * FROM users WHERE id = %s"
+  cursor.execute(query, (user_id,))
```
