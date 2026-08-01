# Resources: Week 9 — XSS & Access Control

---

## TryHackMe Room

| Room | URL | Focus |
|------|-----|-------|
| **XSS (In-Depth)** | https://tryhackme.com/room/axss | All XSS types, root causes, real CVEs |

---

## Tools

### DVWA (Damn Vulnerable Web Application)
- **GitHub:** https://github.com/digininja/DVWA

### Browser Developer Tools
- Used to bypass client-side `maxlength` restrictions — built into every modern browser (F12 or right-click → Inspect Element)

---

## XSS References

### Official Standards

| Resource | URL |
|----------|-----|
| **CWE-79** | https://cwe.mitre.org/data/definitions/79.html |
| **OWASP A03:2021** | https://owasp.org/Top10/A03_2021-Injection/ |
| **OWASP XSS** | https://owasp.org/www-community/attacks/xss/ |
| **OWASP DOM-Based XSS** | https://owasp.org/www-community/attacks/DOM_Based_XSS |

### Prevention & Evasion Reference

| Resource | URL |
|----------|-----|
| **XSS Prevention Cheat Sheet** | https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html |
| **DOM-Based XSS Prevention Cheat Sheet** | https://cheatsheetseries.owasp.org/cheatsheets/DOM_based_XSS_Prevention_Cheat_Sheet.html |
| **XSS Filter Evasion Cheat Sheet** | https://owasp.org/www-community/xss-filter-evasion-cheatsheet |

---

## IDOR References

| Resource | URL |
|----------|-----|
| **CWE-639** | https://cwe.mitre.org/data/definitions/639.html |
| **OWASP IDOR** | https://owasp.org/www-community/attacks/Insecure_Direct_Object_References |

---

## BeEF (Browser Exploitation Framework)

| Resource | URL |
|----------|-----|
| **Official Project Site** | https://beefproject.com/ |
| **GitHub Repository** | https://github.com/beefproject/beef |

---

## Real-World CVEs Referenced This Week

| CVE | Software | URL |
|-----|----------|-----|
| **CVE-2023-38501** | copyparty | https://nvd.nist.gov/vuln/detail/CVE-2023-38501 |
| **CVE-2023-38501 Analysis** | Wiz Vulnerability DB | https://www.wiz.io/vulnerability-database/cve/cve-2023-38501 |
| **CVE-2021-38757** | Hospital Management System | https://www.cvedetails.com/cve/CVE-2021-38757/ |
| **CVE-2021-38757 Source** | GitHub Issue | https://github.com/kishan0725/Hospital-Management-System/issues/6 |

---

## CVSS Calculator (for reasoning through scores)

| Resource | URL |
|----------|-----|
| **FIRST.org CVSS 3.1 Calculator** | https://www.first.org/cvss/calculator/3.1 |
| **FIRST.org CVSS 4.0 Calculator** | https://www.first.org/cvss/calculator/4.0 |

---

## Content Security Policy (Defense Reference)

| Resource | URL |
|----------|-----|
| **MDN CSP Guide** | https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP |
| **CSP Evaluator (Google)** | https://csp-evaluator.withgoogle.com/ |

---

## Real-World Data (Business Impact)

Full sourced breakdown by vulnerability type — with confirmed regulatory fines, not estimates — is in `business-impact-analysis.md`. Quick reference:

| Source | Statistic | URL |
|--------|-----------|-----|
| **IBM Cost of Breach 2023** | Global average: $4.45M; stolen/compromised credentials vector: $4.62M | https://www.ibm.com/reports/data-breach |
| **British Airways GDPR Fine (2020)** | £20M confirmed penalty | https://en.wikipedia.org/wiki/British_Airways_data_breach |
| **First American Financial Corp (IDOR, 2019)** | ~$1.49M combined SEC + NY DFS settlement | https://www.dfs.ny.gov/reports_and_publications/press_releases/pr202311281 |

---

## Weekly Study Schedule

| Day | Activity | Resource |
|-----|----------|----------|
| **Mon** | XSS Room: Tasks 1-4 (fundamentals) | TryHackMe room |
| **Tue** | XSS Room: Task 5 (copyparty CVE) | TryHackMe room |
| **Wed** | XSS Room: Tasks 6-7 (Stored + Hospital CVE) | TryHackMe room |
| **Thu** | XSS Room: Tasks 8-10 (DOM, evasion, remediation) | TryHackMe room |
| **Fri** | DVWA: All 6 payloads (Reflected + Stored, L/M/H) | DVWA local |
| **Sat** | IDOR practice + write-up drafting | — |
| **Sun** | Finalize + commit to GitHub | All files |

---

**Status:** Week 8 Resources | Complete Reference | Ready for Learning
