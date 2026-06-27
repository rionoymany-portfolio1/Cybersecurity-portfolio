# Week 6: Vulnerability Research & Web Exploitation

> **From Service Discovery to Confirmed Exploitation**

---

## Topics Covered This Week

### Room: Vulnerabilities 101
Understand how to research application flaws and locate them in vulnerability databases.

**URL:** https://tryhackme.com/room/vulnerabilities101

**Tasks:**
1. Introduction
2. Introduction to Vulnerabilities
3. Scoring Vulnerabilities (CVSS & VPR)
4. Vulnerability Databases
5. An Example of Finding a Vulnerability
6. Showcase: Exploiting Ackme's Application
7. Conclusion

### PortSwigger Web Security Lab: SQL Injection
**Lab:** SQL Injection Vulnerability in WHERE Clause — Retrieval of Hidden Data

**URL:** https://portswigger.net/web-security/sql-injection/lab-retrieve-hidden-data

**Difficulty:** Apprentice

### Python Development: Banner Grabbing Enhancement
Extended the Week 5 port scanner with active service banner retrieval.

**File:** `banner-grabbing-scanner.py`

---

## Learning Objectives

**By end of Week 6, you will:**
-  Understand vulnerability classification frameworks
-  Distinguish CVSS static scoring from VPR dynamic prioritization
-  Navigate NVD, CVE databases to find applicable vulnerabilities
-  Apply a discovered CVE profile to a real target
-  Understand SQL injection root cause at the query level
-  Execute a WHERE clause bypass using a tautology payload
-  Write a production-ready banner grabbing scanner
-  Connect service version discovery to CVE vulnerability research

---

## Attack Chain This Week

```
[Week 5 Output]
Banner grabbed: Apache Tomcat/9.0.41 (Java)
                vsftpd 3.0.3
                Microsoft Windows RPC
         |
         v
[Week 6 Step 1: Vulnerability Research]
Query NVD/CVE databases with exact version strings
Find: CVE-2021-44228 (Log4Shell) - CVSS 10.0
Find: Known SQL injection patterns
         |
         v
[Week 6 Step 2: Weaponization]
Craft exploit payload from CVE documentation
SQL Injection: Accessories'+OR+1=1--
         |
         v
[Week 6 Step 3: Exploitation]
Execute payload against target
Bypass AND released = 1 filter
Retrieve unreleased product catalog
         |
         v
[Week 6 Step 4: Documentation]
Record findings, business impact, remediation
Deliver professional assessment report
```
## Connection to Previous Weeks
 
**Week 5 → Week 6:**
- Port scanner grabbed `Server: Apache Tomcat/9.0.41 (Java)`
- This week: Search that version string in NVD → find CVEs → exploit
**This is the core Red Team loop:**
```
Scan → Fingerprint → Research → Exploit → Document → Repeat
```
---

## Files This Week

```
week-06/
├── README.md                        (this file)
├── write-up.md                      (6-part framework)
├── sql-injection-lab-report.md      (PortSwigger lab findings)
├── vulnerability-research-guide.md  (CVSS, VPR, NVD, CVE methodology)
├── banner-grabbing-scanner.py       (Python tool - enhanced Week 5 scanner)
├── lab-guide.md                     (TryHackMe + PortSwigger exercises)
└── resources.md                     (CVE databases, SQL injection references)
```

---

**Status:** Week 6 | Vulnerability Research + SQL Injection | Completed
