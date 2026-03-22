---
name: network
description: 'Strict infrastructure scanning methodology. Evaluates port exposures, TLS misconfigurations, exposed administrative panels, and subdomain takeovers. Use for network footprinting and risk profiling.'
---

# Network & Infrastructure Security Skill

This skill enforces a methodical approach to evaluating network infrastructure. It provides structured guidance on identifying risky service exposures, misconfigured protocols, and domain configuration weaknesses (such as subdomain takeovers) before engaging in active exploitation.

## When to Activate
• Performing port scanning and service fingerprinting against IP ranges or domains.
• Reviewing cloud infrastructure exposures (Security Groups/Firewall rules).
• Triaging open ports and unencrypted protocols reported by vulnerability scanners.
• Investigating DNS configurations for dangling CNAMEs (Subdomain Takeover risk).

## Infrastructure Evaluation Checklist

### 1. Port Exposure & Attack Surface
Identify exactly what services are listening and whether they should be public.

#### ❌ NEVER Accept This
- Administrative panels (SSH, RDP, Webmin, phpMyAdmin) exposed to the entire public internet (`0.0.0.0/0`) without strict source-IP whitelisting or VPN/Zero-Trust tunnels.
- Raw databases (MySQL, PostgreSQL, MongoDB, Redis) listening on public network interfaces.
- Unencrypted, plaintext legacy protocols handling credentials.

#### ✅ ALWAYS Verify This
- Compare open ports against the high-risk [Ports Dictionary](./ports.yaml).
- For every open port, attempt service banner grabbing to identify the underlying technology and version.
- Flag HTTP endpoints operating on non-standard ports (e.g., 8080, 8443, 9090) which often host internal administrative debugging tools.

#### Verification Steps
- [ ] Direct database exposures instantly flagged as Critical.
- [ ] Text-based legacy protocols (FTP, Telnet) flagged as High/Medium based on context.
- [ ] Nmap/masscan raw output parsed to identify OS and version footprints accurately.

### 2. TLS & Protocol Security
Evaluate encryption configurations for web-facing infrastructure.

#### ❌ NEVER Accept This
- Usage of deprecated protocols (SSLv3, TLS 1.0, TLS 1.1) unless supporting explicitly defined legacy hardware.
- Self-signed, expired, or massively broadly scoped wildcard certificates (`*.company.com`) utilized in isolated staging environments where compromise could leak the wildcard.

#### ✅ ALWAYS Verify This
- Ensure TLS 1.2+ is enforced.
- Verify certificates match the requested domain name correctly.

#### Verification Steps
- [ ] Certificate Subject Alternative Names (SANs) checked for hidden internal domains.
- [ ] Clear-text fallback vectors (port 80) strictly redirect to port 443.

### 3. DNS & Subdomain Takeovers
Identify infrastructure abandonment issues at the routing level.

#### ❌ NEVER Accept This
- "Dangling" DNS records (e.g., a `CNAME` pointing to `mycompany-staging.herokuapp.com` when the Heroku app has been deleted).
- Wildcard DNS records (`*.domain.com`) pointing to 3rd party cloud providers.

#### ✅ ALWAYS Do This
- Enumerate subdomains.
- For every CNAME alias targeting external cloud infrastructure (AWS S3, Azure Cloudapp, GitHub Pages, Pantheon, Fastly), verify the target bucket/service still exists and is claimed by the organization.

#### Verification Steps
- [ ] Resolve all identified subdomains to their A/CNAME records.
- [ ] Cross-reference NXDOMAIN or provider-specific "Not Found" HTTP errors with dangling CNAMEs.

---

## Output Parsing & Handoff
When reporting network issues to the `report` or `orchestrator` agents:
1. Provide the **Asset Identifier** (IP Address + Hostname).
2. Detail the **Exposed Service** (e.g., `TCP 3389 - Microsoft RDP`).
3. Define the **Access Requirement** (e.g., "Accessible via public internet, requires multi-factor authentication implementation via VPN").
