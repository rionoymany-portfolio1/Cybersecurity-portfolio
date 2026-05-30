# Resources: Week 4 - Web Security & Reconnaissance

---

## TryHackMe Rooms (Week 4)

### Room 1: Guided Pentest: Web
- **URL:** https://tryhackme.com/room/guidedpentestweb
- **Time:** 2-3 hours
- **Difficulty:** Beginner to Intermediate
- **Topics:** IDOR, password reset, RCE, attack chains

### Room 2: Passive Reconnaissance
- **URL:** https://tryhackme.com/room/passiverecon
- **Time:** 1-2 hours
- **Difficulty:** Beginner
- **Topics:** Whois, DNS, DNSDumpster, Shodan

---

## Reconnaissance Tools

### Whois

**Official Documentation:**
- https://www.whois.net/

**Command Usage:**
```bash
whois example.com
whois -h whois.arin.net 192.168.1.1  # IP lookup
```

**Online Tools:**
- https://www.whois.net/
- https://whois.domaintools.com/
- https://www.whoisology.com/

**What to look for:**
- Registrant organization name
- Registrant email address
- Phone number
- Physical address
- Admin contact details
- Registration and expiration dates

---

### DNS Enumeration Tools

#### nslookup

**Official:**
- https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/nslookup

**Common queries:**
```bash
nslookup example.com                 # A records (IPv4)
nslookup -type=AAAA example.com      # AAAA records (IPv6)
nslookup -type=MX example.com        # Mail servers
nslookup -type=NS example.com        # Name servers
nslookup -type=TXT example.com       # Text records
nslookup -type=CNAME example.com     # Aliases
```

#### dig

**Official:**
- https://linux.die.net/man/1/dig
- https://www.isc.org/bind/

**Common queries:**
```bash
dig example.com                      # A record
dig example.com +short               # Short output
dig example.com @8.8.8.8            # Query Google DNS
dig example.com +trace              # Trace DNS path
dig example.com ANY                 # All records
dig -x 192.168.1.1                  # Reverse lookup
```

**Red Team tip:** Use `+trace` to see entire DNS hierarchy

---

### DNSDumpster

**Official Website:**
- https://dnsdumpster.com/

**What it does:**
- Performs passive DNS lookups
- Aggregates data from multiple sources
- Creates visual maps of infrastructure
- Free and no registration required

**How to use:**
1. Visit https://dnsdumpster.com/
2. Enter domain name
3. Click "Search"
4. Review results
5. Download report/screenshot

**Information revealed:**
- All known subdomains
- IP addresses
- Hosting providers
- DNS servers
- Mail servers
- Organizational structure

---

### Shodan.io

**Official Website:**
- https://www.shodan.io/

**Account:**
- Free account: 1 search, limited credits
- Shodan+ (paid): Unlimited searches, advanced filters

**Common searches:**
```
"example.com"              # Search company domain
org:"Company Name"         # Search by organization
city:"New York"           # Geolocation
port:3306                 # Specific port (MySQL)
product:"Apache"          # Specific product
"200 OK"                  # Specific HTTP response
ssl:"example.com"         # SSL certificate search
```

**Red Team Intelligence:**
- Find IP ranges used by company
- Discover exposed services
- Identify software versions
- Find vulnerable devices
- Map entire infrastructure

**Example findings:**
- Port 3306 MySQL exposed = database accessible
- Port 22 SSH with OpenSSH 7.4 = known vulnerability
- Port 8080 with Java = possible web application

---

## Web Security Resources

### OWASP (Open Web Application Security Project)

**Official:** https://owasp.org/

**Must-read resources:**
- **OWASP Top 10:** https://owasp.org/www-project-top-ten/
  - A01: Broken Access Control (includes IDOR)
  - A02: Cryptographic Failures
  - A07: Identification and Authentication Failures

- **OWASP Testing Guide:** https://owasp.org/www-project-web-security-testing-guide/
  - Methodical approach to web testing
  - Testing techniques for each vulnerability

- **OWASP Cheat Sheets:** https://cheatsheetseries.owasp.org/
  - Authentication Cheat Sheet
  - Authorization Cheat Sheet
  - Secure File Upload Cheat Sheet

### IDOR (Insecure Direct Object Reference)

**Understanding IDOR:**
- https://owasp.org/www-community/attacks/Insecure_Direct_Object_References
- https://cwe.mitre.org/data/definitions/639.html

**IDOR Prevention:**
- Always check authorization
- Use indirect references (not sequential IDs)
- Implement access control checks
- Log and monitor access patterns

**Testing for IDOR:**
```
1. Identify parameter with object reference
2. Change parameter value incrementally
3. Check if you can access unauthorized data
4. Document findings
5. Test with different user roles
```

### Weak Password Reset

**CWE Reference:**
- https://cwe.mitre.org/data/definitions/640.html (password recovery mechanism)

**Common weaknesses:**
- Predictable tokens
- Tokens visible in email
- No expiration time
- No rate limiting
- Questions can be guessed

**Prevention:**
- Cryptographically random tokens
- Short expiration (1 hour)
- Rate limiting (5 attempts/hour)
- Use established libraries
- Never put password in email

---

## Code Examples & References

### Vulnerable Code (What to Avoid)

```python
# IDOR - No authorization check
@app.route('/api/user/<user_id>')
def get_user(user_id):
    user = User.query.get(user_id)
    return user.to_json()  # Anyone can access any user!

# Weak password reset
def reset_password(email):
    token = str(user.id) + str(int(time.time()))  # Predictable!
    send_reset_email(email, token)

# Unsafe file upload
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    file.save(f'uploads/{file.filename}')  # Not randomized!
    return f'File saved: uploads/{file.filename}'
```

### Secure Code (Best Practices)

```python
# IDOR - Check authorization
@app.route('/api/user/<user_id>')
@login_required
def get_user(user_id):
    current_user = get_current_user()
    
    # Check if authorized
    if user_id != current_user.id and not current_user.is_admin:
        abort(403, 'Unauthorized')
    
    user = User.query.get(user_id)
    return user.to_json()

# Secure password reset
import secrets
def reset_password(email):
    token = secrets.token_urlsafe(32)  # Cryptographically random
    token_expires = datetime.now() + timedelta(hours=1)
    save_reset_token(email, token, token_expires)
    send_reset_email(email, token)

# Safe file upload
import secrets
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    
    # Validate extension
    allowed = {'jpg', 'png', 'gif'}
    ext = file.filename.rsplit('.', 1)[1].lower()
    if ext not in allowed:
        abort(400, 'File type not allowed')
    
    # Save with random name
    filename = secrets.token_hex(16) + '.' + ext
    file.save(f'uploads/{filename}')
    return {'status': 'success', 'file': filename}
```

---

## Tools for Week 4

### Browser-based (No install needed)
- **Burp Suite Community:** https://portswigger.net/burp/communitydownload
  - Free version sufficient for Week 4
  - Proxy and intercept requests
  - Repeat and modify requests

- **OWASP ZAP:** https://www.zaproxy.org/
  - Free alternative to Burp
  - Same functionality
  - Easier learning curve

### Command-line (Already have)
- **whois** - Built-in on Linux/Mac, available on Windows
- **nslookup** - Built-in on all systems
- **dig** - Linux/Mac, can install on Windows

### Online (No install)
- **DNSDumpster:** https://dnsdumpster.com/
- **Shodan:** https://www.shodan.io/
- **Whois lookup:** https://www.whois.net/

---

## Learning Path by Topic

### If you want to understand IDOR deeper:
1. Read: https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html
2. Watch: "IDOR" section of Burp Academy
3. Practice: Try IDOR challenges on HackTheBox
4. Code: Write both vulnerable and secure versions

### If you want to understand password reset exploitation:
1. Read: CWE-640 Password Recovery Mechanism
2. Research: Real password reset bypasses (CVE database)
3. Understand: Cryptographic randomness requirements
4. Code: Implement secure token generation

### If you want to master reconnaissance:
1. Use: Each tool on multiple domains
2. Document: What each tool reveals
3. Combine: Use multiple tools on same target
4. Analyze: Look for patterns and connections

---

## Practice Resources

### HackTheBox (After Week 4)
- https://www.hackthebox.eu/
- Has IDOR-focused machines
- Has web exploitation machines
- Free machines available

### PentesterLab
- https://pentesterlab.com/
- IDOR course (free tier available)
- Web exploitation exercises
- Real vulnerability practice

### PortSwigger Web Security Academy
- https://portswigger.net/web-security
- Free online training
- Interactive labs (browser-based)
- Covers IDOR, authentication, file upload

---

## Real-World CVEs (Examples)

### IDOR Vulnerabilities
- **Capital One Breach (2019):** IDOR + misconfiguration
  - 100M records exposed
  - https://en.wikipedia.org/wiki/2019_Capital_One_data_breach

- **Facebook Messenger Kids:** IDOR allowed access to other children's accounts
  - https://www.facebook.com/security/

### RCE Vulnerabilities
- **Struts2 RCE (CVE-2017-5645):** Remote code execution
- **Log4j RCE (CVE-2021-44228):** Critical RCE vulnerability
- **WordPress Plugin RCE:** Multiple plugins with file upload RCE

---

## Red Team Resources

### Methodology
- **Lockheed Martin Cyber Kill Chain:** https://www.lockheedmartin.com/en-us/capabilities/cyber/cyber-kill-chain.html
  - Reconnaissance
  - Weaponization
  - Delivery
  - Exploitation
  - Installation
  - Command & Control
  - Actions on Objectives

- **MITRE ATT&CK Framework:** https://attack.mitre.org/
  - Comprehensive adversary tactics
  - Real-world attack patterns
  - Defense evasion techniques

### Tools
- **Nmap:** https://nmap.org/ (Week 5+)
- **Metasploit:** https://www.metasploit.com/ (Week 6+)
- **Burp Suite Professional:** (Paid, comprehensive)

---

## Quick Reference Commands

### Whois
```bash
whois example.com
whois -h whois.arin.net 192.168.1.1  # IP whois
```

### DNS (dig preferred)
```bash
dig example.com                      # A record
dig example.com MX                   # Mail servers
dig example.com NS                   # Name servers
dig example.com +trace              # Full trace
dig -x 192.168.1.1                  # Reverse lookup
```

### DNS (nslookup)
```bash
nslookup example.com
nslookup -type=MX example.com
nslookup -type=NS example.com
```

### Online searches
- Whois: https://www.whois.net/
- DNS: https://dnsdumpster.com/
- Shodan: https://www.shodan.io/

---

## Important Reminders

 **DO:**
- Use these tools only on authorized targets
- Document everything you find
- Follow TryHackMe ethical guidelines
- Practice on lab environments first
- Take detailed notes

 **DON'T:**
- Use reconnaissance tools on real companies without permission
- Share offensive findings publicly
- Use discovered credentials for unauthorized access
- Assume passive recon is "safe" legally (still need permission)
- Forget that these skills are for defensive purposes too

---

## Next Week Preview

### Week 5 (Your planning needed)
Based on current progression:
- **Likely:** Network scanning with Nmap
- **Or:** More web exploitation (HackTheBox)
- **Or:** Continue TryHackMe rooms

What would you like to focus on?

---

**Resources Updated:** Week 4 | Web Security & Reconnaissance  
**Next Review:** After Week 4 completion
