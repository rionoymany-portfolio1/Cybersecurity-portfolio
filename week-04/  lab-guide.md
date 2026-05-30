# Lab Guide: Week 4 - Web Pentesting & Passive Recon

---

## Part 1: Passive Reconnaissance Room
### https://tryhackme.com/room/passiverecon

**Expected Time:** 1 hour
**Difficulty:** Beginner
**Goal:** Learn passive intelligence gathering tools

---

### Task 1: Introduction

**What to learn:**
- Passive reconnaissance definition
- Why it's important for Red Team
- Legal and ethical considerations

**Key concepts:**
- Reconnaissance is 70% of attack time
- Passive = no direct contact with target
- Active = direct probing (alerts defenses)

---

### Task 2: Passive Versus Active Recon

**Understanding the difference:**

| Aspect | Passive | Active |
|--------|---------|--------|
| **Detection Risk** | None (external queries) | High (target logs it) |
| **Tools** | whois, DNS, Shodan | nmap, nessus, nikto |
| **Time** | Quick (hours) | Longer (days) |
| **Legal** | Legal (public info) | Risky (direct probing) |

**Task:** Understand why passive comes first
- Answer the questions about passive vs active
- Document key differences

**Notes to take:**
- Passive = external research
- Active = internal testing
- Always start with passive
- Active confirms what passive revealed

---

### Task 3: Whois

**What is Whois:**
- Database of domain registrations
- Public information about domain owners
- Contains: Registrant name, email, organization, address, phone

**How to use:**
```bash
whois example.com
```

**What you'll get:**
- Domain creation date
- Registrant contact info
- Registrant organization
- Admin contact email
- Technical contact

**Why Red Team cares:**
- Find company location
- Identify key contacts
- Discover other domains by same registrant
- Find email patterns for phishing

**Task Instructions:**
1. Run `whois` on provided target
2. Identify registrant information
3. Find date domain was registered
4. Note down answers to questions

**Example output analysis:**
```
Registrant Organization: ACME Corp
Registrant Email: admin@acmecorp.com
Admin Email: admin@acmecorp.com
Name Servers: ns1.acmecorp.com, ns2.acmecorp.com
```

**Red Team Intelligence:**
- ACME Corp = target organization
- admin@acmecorp.com = potential account
- ns1, ns2 = DNS servers (worth investigating)

---

### Task 4: nslookup and dig

**What is DNS:**
- Domain Name System
- Translates domain names to IP addresses
- Contains records: A (IPv4), AAAA (IPv6), MX (mail), TXT, CNAME

**Tool 1: nslookup**
```bash
nslookup example.com              # Basic lookup
nslookup -type=MX example.com     # Mail servers
nslookup -type=TXT example.com    # Text records
```

**Tool 2: dig (preferred)**
```bash
dig example.com                   # A records
dig example.com @8.8.8.8         # Query specific DNS server
dig example.com +short            # Short output
dig example.com ANY               # All records
```

**Task Instructions:**
1. Perform DNS lookup on target
2. Find A records (IP addresses)
3. Find MX records (mail servers)
4. Find any subdomains mentioned
5. Document all discovered IPs

**Red Team Intelligence:**
- A records = IP addresses of servers
- MX records = mail servers (sometimes on different IP)
- Subdomains found = other services to attack
- TXT records = sometimes contain security info or clues

**Example:**
```
example.com A record: 192.168.1.1
example.com MX: mail.example.com
mail.example.com A: 192.168.1.10
```

**Findings:**
- Main website: 192.168.1.1
- Mail server: 192.168.1.10
- Two different systems identified!

---

### Task 5: DNSDumpster

**What is DNSDumpster:**
- Online tool for passive DNS enumeration
- Aggregates DNS data from multiple sources
- Maps complete domain infrastructure

**How to use:**
1. Visit: https://dnsdumpster.com/
2. Enter domain name
3. Tool performs passive queries
4. Visualizes entire DNS structure

**What you'll see:**
- All known subdomains
- IP addresses and locations
- DNS servers
- Mail servers
- Organizational structure

**Task Instructions:**
1. Use DNSDumpster on target domain
2. Screenshot the DNS map
3. Identify subdomains (web, mail, api, admin, etc.)
4. Note IP addresses and ISP information
5. Answer questions about infrastructure

**Red Team Intelligence:**
- web.example.com = main web server
- api.example.com = API endpoint
- admin.example.com = potential admin panel (valuable!)
- mail.example.com = email infrastructure
- Each has separate IP = separate attack surface

---

### Task 6: Shodan.io

**What is Shodan:**
- "Internet's camera"
- Searches for internet-connected devices
- Finds: Servers, routers, cameras, printers, anything with IP
- Indexes open ports and services

**How to use:**
1. Go to: https://www.shodan.io/
2. Create free account
3. Search: `"example.com"` (with quotes)
4. View results: IPs, ports, services, software versions

**What you'll find:**
- Servers running company applications
- Exposed services (FTP, Telnet, SSH)
- Web servers with known vulnerabilities
- Database servers exposed to internet
- Version information (very valuable!)

**Example Search Results:**
```
192.168.1.1
  Port 22 (SSH): OpenSSH 7.4 (outdated, vulnerable!)
  Port 80 (HTTP): Apache 2.4.6
  Port 443 (HTTPS): Apache 2.4.6
  
192.168.1.10
  Port 3306 (MySQL): 5.7.31
  Port 3389 (RDP): Windows Server 2016
```

**Red Team Intelligence:**
- OpenSSH 7.4 = CVE-2018-15473 exists
- MySQL 5.7.31 = default credentials might work
- RDP exposed = Windows access point
- Each version = specific exploits available

**Task Instructions:**
1. Search target company on Shodan
2. Find all exposed IPs
3. Identify services and versions
4. Document findings
5. Note which services have known CVEs

**IMPORTANT:** Free account is limited. Premium has more data.

---

### Task 7: Summary

**What you've learned:**
1. Whois = Company information
2. DNS = IP addresses and subdomains
3. DNSDumpster = Infrastructure mapping
4. Shodan = Service discovery and versions

**Passive Recon Complete Map:**

```
Company Name (Whois)
    ↓
Domain registrants, contact emails
    ↓
DNS Enumeration (nslookup, dig)
    ↓
Subdomains, IP addresses, mail servers
    ↓
DNSDumpster visualization
    ↓
Complete infrastructure map
    ↓
Shodan search
    ↓
Service versions, known vulnerabilities
    ↓
READY FOR EXPLOITATION
```

**No alarms triggered. No detection. Complete intelligence.**

---

## Part 2: Guided Pentest: Web Room
### https://tryhackme.com/room/guidedpentestweb

**Expected Time:** 1 hour
**Difficulty:** Beginner
**Goal:** Complete attack chain from recon to RCE

---

### Task 1: Introduction

**What you'll learn:**
- Vulnerable web application setup
- How to approach exploitation methodically
- Attack chain thinking
- Why chaining vulnerabilities matters

**Important note:**
- This is a lab environment
- Application intentionally vulnerable
- These are real vulnerabilities
- Real companies have these same issues

---

### Task 2: Reconnaissance and Enumeration

**Goal:** Gather information about the target application

**Steps to follow:**
1. Access the web application
2. View page source (Ctrl+U)
3. Check for comments, hidden fields
4. Test basic input validation
5. Look for error messages (tell tales)
6. Identify all pages and endpoints
7. Note technology stack (PHP, Python, JavaScript versions)

**Tools to use:**
- Browser developer tools (F12)
- Burp Suite Community (free)
- OWASP ZAP (free)

**What to document:**
- All discovered pages
- All forms and inputs
- Technology detected
- Error messages revealed
- Hidden endpoints found

**Task answers:**
- Complete enumeration questions
- Identify the vulnerable parameter
- Note the technology stack

**Red Team Note:** This stage should take 20-30 minutes. Don't rush.

---

### Task 3: IDOR (Insecure Direct Object Reference)

**What is IDOR:**
- Users can access resources they shouldn't
- Authorization not properly checked
- Example: `/profile?id=123` returns user 123, try `/profile?id=124`

**Exploitation steps:**
1. Find a URL with ID parameter (user/product/profile)
2. Change the ID number incrementally
3. See if you get different user's data
4. Document what data you can access
5. Try accessing admin profile

**Common patterns:**
- `/user/123` → Change to `/user/124`
- `/api/profile?id=1` → Change to `/api/profile?id=2`
- `/account.php?account_id=100` → Change to `/account_id=101`

**Task instructions:**
1. Find the IDOR vulnerability in application
2. Access profile with different IDs
3. Find admin user profile
4. Extract required information

**Success indicators:**
- You can access other users' data
- You found admin account
- Task marks completed
- You can use every tool in the room efficiently 

---

### Task 4: Weak Password Reset

**What is weak password reset:**
- Reset token is predictable
- Token doesn't expire
- No rate limiting
- Token visible in URL or easily guessed

**Exploitation steps:**
1. Find password reset function
2. Request password reset for admin account
3. Look for reset token (email, URL, form)
4. Analyze token pattern (is it predictable?)
5. Try guessing other reset tokens
6. Reset admin password if possible

**Common patterns:**
- Token = timestamp + user_id
- Token = sequential numbers
- Token = hash of email
- Token visible in reset URL

**Task instructions:**
1. Trigger password reset for admin
2. Analyze the reset token
3. Determine if it's predictable
4. Exploit weakness
5. Reset admin password

**Success indicators:**
- You obtained valid reset token
- You reset admin password
- You can now log in as admin

---

### Task 5: Admin Panel Access

**Goal:** Now that you're admin, explore what's available

**What to do:**
1. Log in as admin (from Task 4)
2. Browse all admin features
3. Document what you can do
4. Look for file upload functionality
5. Find any interesting configuration

**Admin panel typically contains:**
- User management
- Site configuration
- Content management
- File management
- Settings/system info

**Task instructions:**
1. Log in as admin
2. Answer questions about admin panel
3. Identify file upload location
4. Note system information revealed

**Red Team Note:** Admin panel usually reveals software versions, system paths, installed plugins.

---

### Task 6: Remote Code Execution (RCE)

**What is RCE:**
- Upload file to server
- Server executes that file
- Attacker can run commands

**Exploitation steps:**
1. Go to file upload function (admin panel)
2. Create malicious file (usually PHP, JSP, or ASP)
3. Upload it
4. Access the uploaded file
5. Execute commands through it

**Simple PHP webshell:**
```php
<?php
system($_GET['cmd']);
?>
```

**How it works:**
- Save as `shell.php`
- Upload through admin panel
- Access: `/uploads/shell.php?cmd=ls`
- Server executes `ls` command
- Output returned to you

**Task instructions:**
1. Create appropriate webshell for application
2. Upload through admin panel
3. Find uploaded file location
4. Execute commands
5. Complete required objectives

**Success indicators:**
- Uploaded file successfully
- Can access uploaded file
- Can execute system commands
- Answer task questions

---

### Task 7: The Attack Chain

**Putting it all together:**

```
1. RECONNAISSANCE (Task 2)
   ↓
   Find vulnerable parameter
   
2. IDOR EXPLOITATION (Task 3)
   ↓
   Access admin profile without authentication
   
3. PASSWORD RESET WEAKNESS (Task 4)
   ↓
   Reset admin password with weak token
   
4. ADMIN ACCESS (Task 5)
   ↓
   Log in as admin
   
5. REMOTE CODE EXECUTION (Task 6)
   ↓
   Upload webshell, execute commands
   
6. FULL COMPROMISE
   ↓
   Complete system access achieved
```

**Timeline:** 30-60 minutes total attack

**Detection risk:** Low (50% or less detected)

**Task instructions:**
1. Review attack progression
2. Answer questions about each phase
3. Explain why each vulnerability matters
4. Understand why chain is more dangerous than individual vulns

---

### Task 8: Conclusion

**What you've learned:**
- Real vulnerabilities exist in real applications
- They're easy to exploit
- Detection is difficult
- Professional attackers use this exact methodology
- These vulnerabilities are preventable

**Key takeaways:**
- Always perform authorization checks
- Use cryptographic random tokens
- Validate file uploads
- Monitor for IDOR patterns
- Implement rate limiting

**Next steps:**
- Practice on HackTheBox
- Understand secure coding principles
- Learn how to prevent these vulnerabilities
- Think like attacker, code like defender

---

## Integration: Passive Recon + Web Pentesting

**Week 4 combines two perspectives:**

**Passive Recon Room teaches:**
- How much information is publicly available
- Why reconnaissance matters
- What attackers find before attacking

**Web Pentesting Room teaches:**
- How to exploit those discoveries
- Real attack methodology
- Why each vulnerability matters
- How fast compromise happens

**Together, they show:**
```
Public info (Whois, DNS, Shodan)
    ↓
Target web application
    ↓
Find vulnerabilities (IDOR, weak reset)
    ↓
Exploit chain
    ↓
Full compromise
```

---

## Hands-On Practice Notes

### For Passive Recon:
- Run commands yourself (don't just read output)
- Try different query variations
- Search Shodan for multiple variations
- Try Shodan search filters
- Document everything you find

### For Web Pentesting:
- Don't skip enumeration (Task 2)
- Test every single ID number
- Document all found parameters
- Try multiple password reset flows
- Explore entire admin panel before moving on
- Don't give up if something doesn't work first try

---

## Key Concepts to Master

1. **IDOR vulnerability pattern:**
   - Find ID parameter
   - Change value
   - Check authorization

2. **Weak password reset pattern:**
   - Predictable tokens
   - No expiration
   - No rate limiting
   - = account takeover

3. **File upload exploitation:**
   - No type validation
   - No name randomization
   - Stored in web directory
   - Can be executed
   - = RCE

4. **Attack chain thinking:**
   - Each step builds on previous
   - Early discovery → later exploitation
   - One vulnerability alone is bad
   - Many vulnerabilities together = catastrophic

---

**Status:** Lab Guide Complete | Ready for Week 4 Hands-On Practice
