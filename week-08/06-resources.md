# Resources: Week 8 — UNION SQLi, SQLmap, and Python Automation

---

## SQL Injection References

| Resource | URL |
|----------|-----|
| **PortSwigger UNION Attacks** | https://portswigger.net/web-security/sql-injection/union-attacks |
| **PortSwigger SQLi Cheat Sheet** | https://portswigger.net/web-security/sql-injection/cheat-sheet |
| **OWASP SQLi** | https://owasp.org/www-community/attacks/SQL_Injection |
| **CWE-89** | https://cwe.mitre.org/data/definitions/89.html |
| **SQLi Prevention Cheat Sheet** | https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html |

---

## SQLmap

| Resource | URL |
|----------|-----|
| **Official Website** | https://sqlmap.org/ |
| **GitHub Repository** | https://github.com/sqlmapproject/sqlmap |
| **Usage Documentation** | https://github.com/sqlmapproject/sqlmap/wiki/Usage |
| **Tamper Scripts List** | https://github.com/sqlmapproject/sqlmap/tree/master/tamper |

**Installation:**
```bash
# Kali Linux (pre-installed)
sqlmap --version

# Manual install
git clone https://github.com/sqlmapproject/sqlmap.git
python3 sqlmap/sqlmap.py --version

# pip (not recommended, use git clone)
pip install sqlmap
```

---

## Python `requests` Library

| Resource | URL |
|----------|-----|
| **Official Documentation** | https://docs.python-requests.org/ |
| **Quickstart Guide** | https://docs.python-requests.org/en/latest/user/quickstart/ |
| **Session Objects** | https://docs.python-requests.org/en/latest/user/advanced/#session-objects |

**Installation:**
```bash
pip install requests
pip3 install requests
```

**Core usage:**
```python
import requests

# GET request with parameters
response = requests.get(url, params={"id": "1"}, cookies={"session": "abc"})

# POST request with body
response = requests.post(url, data={"username": "admin", "password": "pass"})

# Session object (auto-handles cookies)
session = requests.Session()
session.get(url)  # Cookies from this response saved automatically
session.get(url2) # Previous cookies sent automatically
```

---

## Python `re` (Regular Expressions)

| Resource | URL |
|----------|-----|
| **Python re Documentation** | https://docs.python.org/3/library/re.html |
| **Regex101 (test patterns)** | https://regex101.com/ |

**Patterns used in this week's script:**
```python
import re

# Match "First name: VALUE<br" — VALUE is our extracted data
re.findall(r"First name:\s*(.*?)<br", html)

# Match "Surname: VALUE</pre>" — VALUE is our extracted data
re.findall(r"Surname:\s*(.*?)</pre>", html)

# Key: r"" raw string prevents \s from being interpreted as escape sequence
# .*? is non-greedy — stops at first match, not last
```

---

## MySQL / MariaDB `information_schema`

| Resource | URL |
|----------|-----|
| **information_schema Overview** | https://dev.mysql.com/doc/refman/8.0/en/information-schema.html |
| **TABLES Table** | https://dev.mysql.com/doc/refman/8.0/en/information-schema-tables-table.html |
| **COLUMNS Table** | https://dev.mysql.com/doc/refman/8.0/en/information-schema-columns-table.html |

**Key tables for SQL injection enumeration:**
```sql
-- All tables in current database
SELECT table_name FROM information_schema.tables WHERE table_schema=database()

-- All columns in a specific table
SELECT column_name FROM information_schema.columns WHERE table_name='users'

-- All databases accessible to current user
SELECT schema_name FROM information_schema.schemata
```

---

## Hash Cracking

| Tool | URL | Use |
|------|-----|-----|
| **CrackStation** | https://crackstation.net/ | Free MD5/SHA1/SHA256 lookup |
| **Hashes.com** | https://hashes.com/en/decrypt/hash | Free online lookup |
| **hashcat** | https://hashcat.net/hashcat/ | Local GPU cracking |

**Identifying hash types:**
```
32 hex chars = MD5
40 hex chars = SHA1
64 hex chars = SHA256
60 chars starting with $2b$ = bcrypt
```

---

## DVWA

| Resource | URL |
|----------|-----|
| **GitHub Repository** | https://github.com/digininja/DVWA |
| **Installation Guide** | https://github.com/digininja/DVWA#installation |

---

## Business Impact Data (Verified)

| Source | Statistic | URL |
|--------|-----------|-----|
| **IBM Cost of Breach 2023** | Overall average: $4.45M; Web app vector: $4.56M | https://www.ibm.com/reports/data-breach |
| **OWASP Top 10 2021** | Injection ranked #3 | https://owasp.org/Top10/ |
| **Verizon DBIR 2023** | Injection in top web attack patterns | https://www.verizon.com/business/resources/reports/dbir/ |

---

## Weekly Study Schedule

| Day | Activity | Tool/Resource |
|-----|----------|---------------|
| **Mon** | UNION payload sequence — Payloads 1-4 | DVWA |
| **Tue** | UNION payload sequence — Payloads 5-8 | DVWA |
| **Wed** | SQLmap staged commands | sqlmap + DVWA |
| **Thu** | Python script — setup and run | dvwa-sqli-extractor.py |
| **Fri** | Python script — extend and modify | Python |
| **Sat** | Comparison exercise + write-up | All tools |
| **Sun** | Commit week-08 to GitHub | GitHub |

---

**Status:** Week 8 Resources | Complete Reference
