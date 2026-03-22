---
name: dependency
description: 'Strict Software Composition Analysis (SCA) methodology. Checks for CVEs, typosquatting, supply chain attacks, lockfile integrity, and abandoned package risks. Use for deep auditing of project dependencies.'
---

# Dependency & Supply Chain Security Skill

This skill enforces a strict, exhaustive methodology for examining project dependencies. It goes beyond simple CVE matching to evaluate supply chain risks, lifecycle scripts, and overall package hygiene.

## When to Activate
• Performing Software Composition Analysis (SCA) on lockfiles or manifests (e.g., `package.json`, `requirements.txt`, `Cargo.toml`, `pom.xml`).
• Triaging automated vulnerability scan alerts for 3rd-party libraries.
• Investigating potential supply chain attacks (e.g., typosquatting, malicious post-install scripts).
• Evaluating the maintenance status and takeover risk of upstream libraries.

## Security & Audit Checklist

### 1. Lockfile & Dependency Pinning
Evaluate how dependencies are resolved and fetched.

#### ❌ NEVER Accept This
- Manifests without an accompanying lockfile (e.g., `package.json` without `package-lock.json` or `yarn.lock`; `requirements.txt` without hashes).
- Broad version ranges (e.g., `*`, `>=1.0.0`, `^2.0`) in production builds.
- Fetching dependencies over unencrypted `http://` registries.

#### ✅ ALWAYS Verify This
- Ensure strict version pinning or deterministic lockfiles are present.
- Check if sub-dependencies (transitive dependencies) are explicitly tracked in the lockfile.
- Validate cryptographic hashes or checksums in lockfiles if supported by the package manager.

#### Verification Steps
- [ ] Lockfile exists and is perfectly in sync with the manifest.
- [ ] No wildcard or floating versions used in deployment constraints.
- [ ] All package registries used enforce HTTPS/TLS.

### 2. Known Vulnerabilities (CVE/GHSA Analysis)
Evaluate active vulnerabilities in the dependency tree.

#### ✅ ALWAYS Do This
- Cross-reference dependency versions against current CVE/GHSA databases.
- Verify if the vulnerability is actually reachable (e.g., is the vulnerable function actively imported and called in the source code?).
- Determine if a vulnerability is in a `devDependency` / `test` scope vs. `production` scope.

#### Verification Steps
- [ ] All high/critical CVEs mapped to exact component and version.
- [ ] Exploitability assessed based on actual usage context.
- [ ] Remediations specify exact target fix versions rather than generic "update".

### 3. Supply Chain Attack Indicators
Detect active tampering, typosquatting, and malicious scripts.

#### ❌ NEVER Accept This
- Packages that perfectly match known malicious databases or heavily typosquatted names.
- Obfuscated, heavily encoded, or dynamically downloaded payloads executing during install phases (e.g., `preinstall`, `postinstall`, `build.rs`, `setup.py`).

#### ✅ ALWAYS Check This
- Compare package names to [Known Malicious Patterns](./known_malicious.txt).
- Review custom install scripts in manifests for suspicious behavior:
  - Spawning unexpected shells (`sh -c`, `bash -c`).
  - Sending telemetry or environment variables to unknown external IPs using `curl` or `wget`.
  - Executing base64 or hex-encoded blobs.

#### Verification Steps
- [ ] No heavily obfuscated lifecycle/install scripts present.
- [ ] Package names manually checked for common typosquats (e.g., `request` vs `requests`, `env` vs `cross-env`).
- [ ] Review binary artifacts or sudden inclusion of compiled binaries in minor package updates.

### 4. Project Health & Abandonment Risk
Evaluate the socio-technical risk of dependency hijacking.

#### ✅ ALWAYS Do This
- Check the last commit/release date of critical external libraries.
- Check if the project is officially marked "Deprecated" or archived on GitHub/GitLab.
- Flag packages maintained by a single person with no succession plan.

#### Verification Steps
- [ ] No critical production dependency has been unmaintained for >2 years.
- [ ] No sudden, unexplained transfers of ownership of a highly-used repository without security audits.

---

## Analysis & Reporting Guide

When reporting vulnerabilities, include:
- **Dependency Name** & **Ecosystem** (npm, PyPI, Maven, Composer, etc.)
- **Vulnerable Version** vs. **Patched Version**
- **Transitive Path**: If the vulnerability is nested, provide the full inclusion path (e.g., `A -> B -> C (vulnerable)`).
- **Proof of Relevancy**: Explain if the vulnerable API is actually used within the project context.

## Rules of Engagement
- **Avoid Breaking Changes**: Always suggest the nearest non-breaking patch version (e.g., bump `1.2.3` to `1.2.4`) unless the major version is completely compromised.
- **False Positives**: Explicitly dismiss Dev/Test dependency CVEs if they do not impact the build pipeline or production runtime (e.g., a regex DoS in a local test framework that never touches user input).
