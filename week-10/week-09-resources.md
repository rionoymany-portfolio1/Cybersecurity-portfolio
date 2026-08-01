# Resources: Week 9 — File Upload Vulnerabilities

---

## PortSwigger Web Security Academy Labs

| Lab | Difficulty | URL |
|-----|-----------|-----|
| RCE via web shell upload | Apprentice | https://portswigger.net/web-security/file-upload/lab-file-upload-remote-code-execution-via-web-shell-upload |
| Content-Type restriction bypass | Apprentice | https://portswigger.net/web-security/file-upload/lab-file-upload-web-shell-upload-via-content-type-restriction-bypass |
| Path traversal | Practitioner | https://portswigger.net/web-security/file-upload/lab-file-upload-web-shell-upload-via-path-traversal |
| Race condition | Expert | https://portswigger.net/web-security/file-upload/lab-file-upload-web-shell-upload-via-race-condition |

**Theory:** https://portswigger.net/web-security/file-upload
**Race Conditions (background theory):** https://portswigger.net/web-security/race-conditions

---

## Tools

### Burp Suite
- **Community/Pro Download:** https://portswigger.net/burp/communitydownload
- **Send Group in Parallel / Group Send Options Documentation:** https://portswigger.net/burp/documentation/desktop/tools/repeater/send-group

---

## Standards & Weakness References

| Resource | URL |
|----------|-----|
| **CWE-434 (Unrestricted Upload)** | https://cwe.mitre.org/data/definitions/434.html |
| **CWE-862 (Missing Authorization)** — for context on CVE-2025-31324's access control gap; NVD officially classifies the CVE as CWE-434 | https://cwe.mitre.org/data/definitions/862.html |
| **CWE-367 (TOCTOU Race Condition)** | https://cwe.mitre.org/data/definitions/367.html |
| **CWE-22 (Path Traversal)** | https://cwe.mitre.org/data/definitions/22.html |
| **CWE-626 (Null Byte Interaction Error)** | https://cwe.mitre.org/data/definitions/626.html |
| **OWASP A04:2021 (Insecure Design)** | https://owasp.org/Top10/A04_2021-Insecure_Design/ |
| **OWASP File Upload Cheat Sheet** | https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html |

---

## Real-World CVEs Referenced This Week

| CVE | Software | URL |
|-----|----------|-----|
| **CVE-2025-31324** | SAP NetWeaver Visual Composer | https://nvd.nist.gov/vuln/detail/CVE-2025-31324 |
| **CVE-2021-24145** | WordPress Modern Events Calendar | https://wpscan.com/vulnerability/f42cc26b-9aab-4824-8168-b5b8571d1610/ |
| **CVE-2023-50164** | Apache Struts 2 | https://www.paloaltonetworks.com/blog/cloud-security/cve-2023-50164-custom-rules/ |
| **CVE-2017-5638** | Apache Struts 2 (Equifax breach) | https://archive.epic.org/privacy/data-breach/equifax/ |
| **CVE-2012-5653** | Drupal core | https://nvd.nist.gov/vuln/detail/CVE-2012-5653 |

---

## Null Byte — Fix Reference & Structural Context

| Resource | Detail |
|----------|--------|
| Fixed in PHP version | 5.3.4 (2010) |
| Relevant PHP bug tracker | https://bugs.php.net/bug.php?id=39863 |
| Structural context | The PHP fix closed the exposure within PHP's own string-handling layer. The underlying C null-terminator behavior persists as an architectural concern wherever modern code (Python, Node.js, Go) passes user-supplied strings to native C/C++ bindings or FFI without independent null-byte validation at that boundary. |

---

## Race Condition Research

| Resource | URL |
|----------|-----|
| James Kettle / PortSwigger Research — "Smashing the State Machine" | https://portswigger.net/research/smashing-the-state-machine |

---

## Real-World Data (Business Impact)

Full sourced breakdown by technique is in `business-impact-analysis.md`. Quick reference:

| Source | Statistic | URL |
|--------|-----------|-----|
| **IBM Cost of Breach 2023** | Global average: $4.45M; per-record: $165 | https://www.ibm.com/reports/data-breach |
| **Equifax Settlement (2019)** | $575M–$700M confirmed regulatory settlement | Oregon DOJ / FTC settlement records |
| **Equifax Total Cost** | $1.4B–$1.7B total breach-related expense | Multiple independent analyses |
| **Enterprise ERP downtime cost** | $300K–$1M+ per hour (relevant for manufacturing-sector SAP compromise) | Gartner / ITIC 2024 Hourly Cost of Downtime Survey — https://www.atlassian.com/incident-management/kpis/cost-of-downtime |

---

## Weekly Study Schedule

| Day | Activity | Resource |
|-----|----------|----------|
| **Mon** | Lab 1: No validation | PortSwigger |
| **Tue** | Lab 2: Content-Type bypass | PortSwigger |
| **Wed–Thu** | Lab 3: Path traversal | PortSwigger |
| **Fri–Sat** | Lab 4: Race condition (Expert — allow extra time) | PortSwigger + Burp Suite |
| **Sun** | Double extension / null byte theory review + write-up + commit | All files |

---

**Status:** Week 9 Resources | Complete Reference | Ready for Learning
