# Resources: Week 7 — Burp Suite Repeater & SQL Injection

---

## TryHackMe Rooms

| Room | URL | Focus |
| :--- | :--- | :--- |
| **Burp Suite: Repeater** | https://tryhackme.com/room/burpsuiterepeater | HTTP manipulation |
| **SQL Injection** | https://tryhackme.com/room/sqlinjectionlm | All SQLi categories |

---

## Tools

### Burp Suite Community Edition
- **Download:** https://portswigger.net/burp/communitydownload
- **Documentation:** https://portswigger.net/burp/documentation/desktop/tools/repeater
- **Repeater Guide:** https://portswigger.net/burp/documentation/desktop/tools/repeater/using

### DVWA (Damn Vulnerable Web Application)
- **GitHub:** https://github.com/digininja/DVWA
- **Setup Guide:** https://github.com/digininja/DVWA#installation

---

## SQL Injection References

### Official Standards

| Resource | URL |
|----------|-----|
| **CWE-89** | https://cwe.mitre.org/data/definitions/89.html |
| **OWASP A03:2021** | https://owasp.org/Top10/A03_2021-Injection/ |
| **OWASP SQLi** | https://owasp.org/www-community/attacks/SQL_Injection |
| **PortSwigger SQLi** | https://portswigger.net/web-security/sql-injection |

### Prevention

| Resource | URL |
|----------|-----|
| **SQLi Prevention Cheat Sheet** | https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html |
| **Query Parameterization Cheat Sheet** | https://cheatsheetseries.owasp.org/cheatsheets/Query_Parameterization_Cheat_Sheet.html |

### Testing Cheat Sheets

| Resource | URL |
|----------|-----|
| **PortSwigger SQLi Cheat Sheet** | https://portswigger.net/web-security/sql-injection/cheat-sheet |
| **PayloadsAllTheThings SQLi** | https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/SQL%20Injection |

---

## MySQL / MariaDB Documentation

| Resource | URL |
|----------|-----|
| **information_schema** | https://dev.mysql.com/doc/refman/8.0/en/information-schema.html |
| **UNION Syntax** | https://dev.mysql.com/doc/refman/8.0/en/union.html |
| **SLEEP()** | https://dev.mysql.com/doc/refman/8.0/en/miscellaneous-functions.html |
| **SUBSTRING()** | https://dev.mysql.com/doc/refman/8.0/en/string-functions.html |

---

## Hash Cracking Tools

| Tool | URL | Notes |
|------|-----|-------|
| **CrackStation** | https://crackstation.net/ | Free, large rainbow table |
| **Hashes.com** | https://hashes.com/en/decrypt/hash | Free online lookup |
| **hashcat** | https://hashcat.net/hashcat/ | Local GPU cracking |

**MD5 weakness reference:** https://www.kb.cert.org/vuls/id/836068

---

## Password Hashing Standards

| Algorithm | Recommendation | URL |
|-----------|---------------|-----|
| **bcrypt** | ✅ Approved (cost ≥ 12) | https://en.wikipedia.org/wiki/Bcrypt |
| **Argon2id** | ✅ Recommended (OWASP #1) | https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html |
| **scrypt** | ✅ Approved | https://www.tarsnap.com/scrypt.html |
| **MD5** | ❌ Never use for passwords | Broken since 2004 |
| **SHA1** | ❌ Never use for passwords | Broken since 2017 |

---

## Real-World Data (Business Impact)

| Source | Statistic | URL |
|--------|-----------|-----|
| **IBM Cost of Breach 2023** | Overall average breach: $4.45M; web application vector: $4.56M | https://www.ibm.com/reports/data-breach |
| **Verizon DBIR 2023** | SQLi in top 3 web attack patterns | https://www.verizon.com/business/resources/reports/dbir/ |
| **OWASP Top 10 2021** | Injection = #3 most critical | https://owasp.org/Top10/ |

---

## Weekly Study Schedule

| Day | Activity | Resource |
|-----|----------|----------|
| **Mon** | Burp Repeater: Tasks 1-5 | TryHackMe room |
| **Tue** | Burp Repeater: Tasks 6-8 (Challenges) | TryHackMe room |
| **Wed** | SQLi Room: Tasks 1-5 (In-Band) | TryHackMe room |
| **Thu** | SQLi Room: Tasks 6-9 (Blind + OOB) | TryHackMe room |
| **Fri** | DVWA: Full manual exploitation | DVWA local |
| **Sat** | Document all findings + hash cracking | CrackStation |
| **Sun** | Write-up + commit to GitHub | All files |

---

**Status:** Week 7 Resources | Complete Reference | Ready for Learning
