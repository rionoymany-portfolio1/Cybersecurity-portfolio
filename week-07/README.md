# Week 7: Burp Suite Repeater & SQL Injection Deep Dive

> **Manual Exploitation Methodology — Understanding Before Automating**

---

## Topics Covered This Week

### Room 1: Burp Suite Repeater
Learn to craft, modify, and resend raw HTTP requests for precise vulnerability testing.

**URL:** https://tryhackme.com/room/burpsuiterepeater

**Tasks:**
1. Introduction
2. What is Repeater?
3. Basic Usage
4. Message Analysis Toolbar
5. Inspector
6. Practical Example
7. Challenge
8. Extra-mile Challenge
9. Conclusion

### Room 2: SQL Injection
Understand and exploit all major SQL injection categories.

**URL:** https://tryhackme.com/room/sqlinjectionlm

**Tasks:**
1. Brief
2. What is a Database?
3. What is SQL?
4. What is SQL Injection?
5. In-Band SQLi
6. Blind SQLi — Authentication Bypass
7. Blind SQLi — Boolean Based
8. Blind SQLi — Time Based
9. Out-of-Band SQLi
10. Remediation

### DVWA Practice: Manual SQL Injection
Full database extraction on DVWA (Damn Vulnerable Web Application) using 100% manual payloads.

**Difficulty:** Low
**Approach:** Zero automated tools — enforces deep comprehension of SQL syntax and backend mechanics

---

## Learning Objectives

**By end of Week 7, you will:**
- ✅ Use Burp Suite Repeater to intercept, modify, and replay HTTP requests
- ✅ Understand why Repeater is superior to direct browser manipulation for exploitation
- ✅ Distinguish all four SQL injection categories: In-Band, Blind Boolean, Blind Time-Based, Out-of-Band
- ✅ Execute Union-based SQLi to extract structured database data
- ✅ Enumerate database schema: tables, columns, and data manually
- ✅ Extract and identify MD5-hashed credentials from a live database
- ✅ Understand the difference between a systematic attacker and a script kiddie

---

## The Anti-Script-Kiddie Principle

This week deliberately avoids automated tools like SQLmap. The reason is fundamental to professional Red Team consulting:

```
Script Kiddie:
  Run sqlmap → Get results → Report numbers
  Understanding: Zero

Professional Red Team Operator:
  Craft payload manually → Understand the SQL query → Infer database structure
  Explain to client exactly WHY their input sanitization failed
  Understanding: Complete
```

A Red Team consultant who cannot explain the exact query modification behind a finding cannot defend the report under client questioning. Manual exploitation forces that understanding.

---

## Attack Chain This Week

```
[Burp Suite Repeater]
Intercept HTTP request containing user parameter
         │
         ▼
Send to Repeater ──> Modify ──> Replay ──> Observe
         │
         ▼
[SQL Injection Discovery]
Inject ' ──> SQL error confirms injection point
         │
         ▼
[Column Enumeration]
ORDER BY 2 (ok) ──> ORDER BY 3 (error) = 2 columns confirmed
         │
         ▼
[Database Reconnaissance]
UNION SELECT database(), user() ──> dvwa / app@localhost
         │
         ▼
[Schema Mapping]
information_schema ──> tables: guestbook, users
                   ──> columns: user_id, user, password...
         │
         ▼
[Credential Extraction]
UNION SELECT user, password FROM users
         │
         ▼
[Hash Cracking]
MD5 hashes ──> plaintext passwords recovered
         │
         ▼
[Full Database Compromise]
```

---

## Files This Week

```
week-07/
├── README.md                           (this file)
├── write-up.md                         (6-part framework)
├── dvwa-sqli-exploitation-report.md    (complete DVWA walkthrough)
├── sqli-types-reference.md             (all 4 SQLi categories explained)
├── burp-repeater-methodology.md        (Repeater workflow guide)
├── lab-guide.md                        (TryHackMe + DVWA exercises)
└── resources.md                        (references and tools)
```

---

**Status:** Week 7 | Burp Suite Repeater + SQL Injection | Complete
