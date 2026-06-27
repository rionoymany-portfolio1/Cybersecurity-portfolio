# Resources: Week 6 — Vulnerability Research & SQL Injection

---

## TryHackMe Room

### Vulnerabilities 101
- **URL:** https://tryhackme.com/room/vulnerabilities101
- **Time:** 2-3 hours
- **Difficulty:** Beginner
- **Topics:** Vulnerability classification, CVSS, VPR, CVE databases, practical exploitation

---

## PortSwigger Web Security Academy

### SQL Injection Lab (This Week)
- **Lab URL:** https://portswigger.net/web-security/sql-injection/lab-retrieve-hidden-data
- **Theory:** https://portswigger.net/web-security/sql-injection
- **Cheat Sheet:** https://portswigger.net/web-security/sql-injection/cheat-sheet

### Burp Suite (Required Tool)
- **Download:** https://portswigger.net/burp/communitydownload
- **User Guide:** https://portswigger.net/burp/documentation
- **Community Edition:** Free, sufficient for all PortSwigger labs

---

## CVE & Vulnerability Databases

### Primary Sources

| Database | URL | Best For |
|----------|-----|----------|
| **NVD** | https://nvd.nist.gov/ | Official CVE details + CVSS scores |
| **CVE Details** | https://www.cvedetails.com/ | Browse by vendor, product, year |
| **Exploit-DB** | https://www.exploit-db.com/ | Working exploit code + Metasploit modules |
| **CISA KEV** | https://www.cisa.gov/known-exploited-vulnerabilities | Confirmed in-the-wild exploitation |
| **VulDB** | https://vuldb.com/ | VPR scoring context + threat intelligence |

### Command-Line Tools (Kali Linux)

```bash
# 1. Always install/update searchsploit database FIRST before researching
sudo apt-get install exploitdb
searchsploit -u               # Update local database with the latest CVEs

# 2. Execute local Exploit-DB queries
searchsploit vsftpd 3.0.3
searchsploit apache 2.4.41    # From our Port 80 banner discovery
searchsploit tomcat 9.0.41    # Matches our Log4Shell ecosystem focus
searchsploit --id tomcat       # Show CVE IDs only
```

---

## CVSS & VPR References

### CVSS

| Resource | URL |
|----------|-----|
| **CVSS 3.1 Calculator** | https://www.first.org/cvss/calculator/3.1 |
| **CVSS Specification** | https://www.first.org/cvss/specification-document |
| **Score Ranges Reference** | https://nvd.nist.gov/vuln-metrics/cvss |

### VPR

| Resource | URL |
|----------|-----|
| **Tenable VPR Documentation** | https://docs.tenable.com/vulnerability-management/Content/Settings/VPR.htm |
| **VPR vs CVSS Explained** | https://www.tenable.com/blog/what-is-vpr-and-how-is-it-different-from-cvss |

---

## SQL Injection References

### Official Standards

| Resource | URL |
|----------|-----|
| **CWE-89** | https://cwe.mitre.org/data/definitions/89.html |
| **OWASP SQL Injection** | https://owasp.org/www-community/attacks/SQL_Injection |
| **OWASP A03:2021 Injection** | https://owasp.org/Top10/A03_2021-Injection/ |

### Prevention

| Resource | URL |
|----------|-----|
| **SQLi Prevention Cheat Sheet** | https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html |
| **Query Parameterization** | https://cheatsheetseries.owasp.org/cheatsheets/Query_Parameterization_Cheat_Sheet.html |

---

## Case Study: CVE-2021-44228 (Log4Shell)

| Property | Value |
|----------|-------|
| **CVE ID** | CVE-2021-44228 |
| **NVD URL** | https://nvd.nist.gov/vuln/detail/CVE-2021-44228 |
| **CVSS Score** | 10.0 (Critical) |
| **Affected Software** | Apache Log4j 2.0-beta9 through 2.14.1 |
| **Attack Vector** | Network |
| **Authentication** | None required |
| **Impact** | Full Remote Code Execution |
| **Exploitation** | Confirmed in-the-wild within 2 hours of disclosure |
| **CISA KEV** | Listed |

---

## Python Socket Documentation

| Resource | URL |
|----------|-----|
| **socket module** | https://docs.python.org/3/library/socket.html |
| **threading module** | https://docs.python.org/3/library/threading.html |
| **connect_ex() docs** | https://docs.python.org/3/library/socket.html#socket.socket.connect_ex |

---

## Real-World Data Sources

The business impact figures in this week's write-up are derived from:

| Source | Data Used | URL |
|--------|-----------|-----|
| **IBM Cost of Data Breach 2023** | Average SQLi breach = $4.9M | https://www.ibm.com/reports/data-breach |
| **Verizon DBIR 2023** | SQLi in top 3 web attack patterns | https://www.verizon.com/business/resources/reports/dbir/ |
| **OWASP Top 10 2021** | Injection ranked #3 | https://owasp.org/Top10/ |

---

## Weekly Study Schedule

| Day | Activity | Resource |
|-----|----------|----------|
| **Mon** | Vulnerabilities 101: Tasks 1-3 | TryHackMe room |
| **Tue** | Vulnerabilities 101: Tasks 4-5 | NVD + Exploit-DB |
| **Wed** | Vulnerabilities 101: Task 6 | TryHackMe room |
| **Thu** | PortSwigger SQL Injection lab | Burp Suite + PortSwigger |
| **Fri** | Banner grabbing scanner testing | banner-grabbing-scanner.py |
| **Sat** | Connect banner → CVE research | NVD + searchsploit |
| **Sun** | Write-up + commit to GitHub | All files |

---

**Status:** Week 6 Resources | Complete Reference | Ready for Learning
