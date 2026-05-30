# Write-Up: Web Application Attack Chains & Passive Reconnaissance

---

## 1. VULNERABILITY: Web Applications Without Security Controls

**What's "broken":**
Web applications often have multiple vulnerabilities that work together:

1. **Poor Reconnaissance Protection**
   - Public data exposed (whois, DNS, Shodan)
   - No effort to hide infrastructure

2. **IDOR (Insecure Direct Object Reference)**
   - Users can access resources they shouldn't
   - No authorization checks (user 1 can view user 2's profile)
   - Example: `/api/user/123` shows any user by changing ID

3. **Weak Password Reset**
   - Predictable reset tokens
   - No rate limiting on attempts
   - Tokens don't expire quickly

4. **Admin Panel Exposure**
   - Default credentials still active
   - Admin panel at predictable URL (/admin, /administrator)
   - No MFA protection

5. **Code Execution**
   - Ability to upload files and execute them
   - No input validation on code/commands
   - Server runs web app as privileged user

**Why it matters:**
These aren't new vulnerabilities. They're **chain vulnerabilities** - individually bad, together they're catastrophic.

---

## 2. EXPLOITATION: The Complete Attack Chain

**How attackers leverage reconnaissance + vulnerabilities:**

### Phase 1: Passive Reconnaissance (No Detection Risk)

```python
# Week 4 skills: Gather intelligence without touching target

# Whois - Get company information
whois targetcompany.com
# Returns: Registrant name, email, company, address

# DNS enumeration - Find subdomains
dig targetcompany.com
nslookup -type=MX targetcompany.com
# Returns: web, mail, api, admin subdomains

# Shodan - Find exposed services
# Search: "targetcompany.com" on Shodan.io
# Returns: IP addresses, ports, services, versions, software

# DNSDumpster - Map infrastructure
# Visit: https://dnsdumpster.com
# Returns: All known subdomains, IP ranges, MX records
```

**Result:** Complete map of target with ZERO detection risk
- All subdomains identified
- All public IPs discovered
- Service versions known
- No security alerts triggered

### Phase 2: IDOR Exploitation

```
Target has: /api/user/profile?id=123

Attacker tries: /api/user/profile?id=124 → Gets user 124's data
Attacker tries: /api/user/profile?id=125 → Gets user 125's data
...
Attacker collects: All user profiles + emails + personal data

Result: Extract sensitive user information without login
```

### Phase 3: Weak Password Reset Exploitation

```
Target password reset flow:
1. User enters email
2. Server sends reset token via email
3. Token format: predictable (e.g., user_id + timestamp)
4. No rate limiting on attempts

Attacker exploits:
- Intercepts reset email (or guesses token pattern)
- Resets admin password to known value
- Logs in as admin

Result: Account takeover
```

### Phase 4: Admin Panel Access

```
Now as admin:
- Access to all user data
- Configuration files
- Database connection strings
- API keys and secrets
- File upload functionality

Attacker gains: Administrative control
```

### Phase 5: Remote Code Execution

```
Admin panel has file upload:
- Upload PHP shell: shell.php
- Or upload image with embedded code
- Web server executes uploaded file

Then attacker can:
- Read system files: /etc/passwd
- Execute commands: ls -la /
- Create backdoors for persistence
- Download entire database

Result: Complete server compromise
```

**The Complete Chain:**

```
Whois/DNS/Shodan (passive, silent)
         ↓
Discover vulnerable endpoints
         ↓
IDOR to access user data
         ↓
Find password reset logic
         ↓
Reset admin password
         ↓
Log in as admin
         ↓
Upload malicious file
         ↓
Execute code on server
         ↓
FULL COMPROMISE
```

**Timeline:** 2-4 hours total, completely undetected

---

## 3. BUSINESS IMPACT: Why This Attack Chain Matters

### Financial Impact

**Scenario: SaaS Company (500 customers, $5M annual revenue)**

**Stage 1: IDOR Data Extraction**
- Attacker extracts all customer data
- 50K customer records exposed
- Contains: credit cards, personal info, usage data
- Value: $2.4M (50K × $48 per record)

**Stage 2: Password Reset + Admin Access**
- Attacker gains admin account
- Accesses billing system
- Accesses customer communication logs
- Additional exposure: $1M

**Stage 3: RCE + Persistence**
- Attacker downloads entire database
- Installs backdoor for future access
- Can shut down service at will
- Ransom demand: $500K

**Stage 4: Discovery + Cleanup**
- Company discovers breach after 14 days (typical)
- Incident response: 30 days cleanup
- Downtime costs: $100K/day × 14 days = $1.4M
- Notification + legal: $300K
- Customer churn: 20% × $5M revenue = $1M/year impact

**Total Cost:**
- Data breach fines: $2.4M-$5M (GDPR, other regulations)
- Incident response: $500K
- Downtime: $1.4M
- Lost revenue: $1M+ (first year)
- **TOTAL FIRST YEAR: $5.3M-$7.9M**

### Organizational Risk

**Why organizations are vulnerable:**

1. **Reconnaissance data is public** - Can't prevent whois/DNS queries
2. **Developer shortcuts** - IDOR happens when devs forget authorization checks
3. **Legacy systems** - Password reset code never updated since 2010
4. **Admin panels too accessible** - Shouldn't be on main web server
5. **File upload naive** - Developers assume uploaded files are always images

**Detection difficulty:**
- Passive recon: 0% chance of detection (external queries)
- IDOR access: Low chance (looks like normal user browsing)
- Password reset: Low chance (legitimate password reset)
- Admin access: Low chance (admin account is expected)
- RCE: Finally detected, but too late

---

## 4. TECHNICAL FIX: Prevent the Attack Chain

### Fix 1: Reconnaissance Hardening
```
Not much you can do (whois/DNS are public):
- Don't expose admin subdomains publicly
- Use generic DNS names (not admin.company.com)
- Monitor what's in Shodan (request removal if needed)
- Use private registrar (hide whois info)
- Don't put company info in DNS comments
```

### Fix 2: IDOR Prevention
```python
# VULNERABLE CODE (what attackers exploit)
@app.route('/api/user/<user_id>')
def get_user(user_id):
    user = User.query.get(user_id)
    return user.to_json()  # Returns any user!

# SECURE CODE (what you should do)
@app.route('/api/user/<user_id>')
@login_required  # Must be logged in
def get_user(user_id):
    current_user = get_current_user()
    
    # Check authorization
    if user_id != current_user.id and not current_user.is_admin:
        return {"error": "Unauthorized"}, 403
    
    user = User.query.get(user_id)
    return user.to_json()
```

### Fix 3: Secure Password Reset
```python
# VULNERABLE: Predictable token
token = str(user.id) + str(timestamp)  # Too predictable

# SECURE: Random, short-lived token
import secrets
token = secrets.token_urlsafe(32)  # Cryptographically random
token_expires = datetime.now() + timedelta(hours=1)  # Expires in 1 hour
# Rate limit: Max 5 reset attempts per hour
```

### Fix 4: Admin Panel Security
```
- Move admin panel to separate domain
- Require VPN access to admin panel
- Require MFA for admin login
- Use custom URL paths (not /admin)
- IP whitelist if possible
```

### Fix 5: Secure File Upload
```python
# VULNERABLE: Upload anything
file.save(f"uploads/{filename}")

# SECURE: Validate + rename
import secrets
allowed_extensions = {'jpg', 'png', 'gif'}
filename = secure_filename(file.filename)
extension = filename.split('.')[-1].lower()

if extension not in allowed_extensions:
    return {"error": "File type not allowed"}, 400

# Save with random name, not user-provided name
new_filename = secrets.token_hex(16) + "." + extension
file.save(f"uploads/{new_filename}")

# Important: Don't execute uploaded files
# Don't store in web-accessible directory
```

---

## 5. POLICY FIX: Organizational Controls

### Security Policies Required

**Policy 1: Code Review Mandatory**
- All code must be reviewed before deployment
- Reviewer checks: Authorization, input validation, file handling
- IDOR prevention is non-negotiable checklist item

**Policy 2: Security Testing Requirements**
- Every new feature must include security tests
- OWASP Top 10 tests required
- Manual penetration testing quarterly

**Policy 3: Admin Access Control**
- No admin panel on production internet
- VPN required for admin access
- MFA mandatory for all admin accounts
- Audit log: Who accessed admin panel when

**Policy 4: File Upload Security**
- Whitelist allowed file types
- Store outside web directory
- Never execute uploaded files
- Scan uploads for malware

**Policy 5: Password Reset Security**
- Tokens must be cryptographically random
- Tokens expire after 1 hour
- Rate limit: 5 attempts per hour
- Notify user of reset attempt

### Training Requirements

**Developer Training:**
- OWASP Top 10 (especially IDOR)
- Secure coding practices
- Authentication/authorization patterns
- Quarterly security training

**Security Team:**
- Understand attack chains
- Threat modeling
- Penetration testing methodology
- Incident response procedures

---

## 6. DETECTION RULE: Identify Attack Chain

### Sigma Rule: IDOR Exploitation Detection

```yaml
title: Potential IDOR Exploitation - Multiple User ID Access
description: Detect when single user rapidly accesses different user resources
logsource:
  service: web_application
  product: any
detection:
  selection:
    http_status: 200
    request_uri|contains: '/api/user/'
  timeframe: 5m
  condition: selection | count > 20  # 20+ different user IDs in 5 minutes
falsepositives:
  - Admin user bulk operations
  - System maintenance scripts
level: high
```

### SIEM Detection: Password Reset Chain

```
Alert if:
1. Multiple password reset requests (3+ in 30 min)
2. Reset tokens from same IP but different users
3. Successful reset followed immediately by login from same IP
4. Admin account password reset from unexpected location

Example sequence:
- 14:32 - Reset password request for user_123
- 14:35 - Reset password request for user_456
- 14:37 - Reset password request for admin (matches pattern)
- 14:40 - Admin login from same IP as resets
- [ALERT] "Possible password reset attack chain"
```

### WAF Rule: File Upload Exploitation

```
Alert if:
1. File upload to admin panel
2. Uploaded file type is .php, .jsp, .asp, .py, etc.
3. Followed by immediate HTTP request to uploaded file
4. Followed by system commands in request parameters

Example:
- 15:45 POST /admin/upload → uploads shell.php
- 15:46 GET /uploads/shell.php?cmd=ls
- [ALERT] "Possible RCE attempt - PHP shell uploaded and executed"
```

---

## 7. WEEK 4 SUMMARY

**What We Learned:**

**From Passive Reconnaissance Room:**
- Whois = company + registrant info
- DNS = subdomains, mail servers
- Shodan = exposed services and metadata
- DNSDumpster = infrastructure mapping
- **Key insight:** Most reconnaissance is PUBLIC and undetectable

**From Web Pentesting Room:**
- IDOR = authorization bypass
- Weak password reset = account takeover
- Admin panel access = privilege escalation
- RCE = full compromise
- **Key insight:** Vulnerabilities chain together for complete attack

**Why It Matters:**
- Professional attackers spend 70% on recon
- Single vulnerabilities are exploitable
- Chains of vulnerabilities are devastating
- Detection difficulty increases with each step

**Red Team Application:**
- Week 1-3: Tools and fundamentals
- **Week 4: Real attack methodology (this is how real attacks work)**
- Week 5+: Advanced techniques, evasion, persistence

---

## Sources & References

### Official Standards (Verified)
- OWASP IDOR: https://owasp.org/www-community/attacks/Insecure_Direct_Object_References
- CWE-639: https://cwe.mitre.org/data/definitions/639.html
- CWE-640: https://cwe.mitre.org/data/definitions/640.html
- OWASP File Upload: https://owasp.org/www-community/vulnerabilities/Unrestricted_File_Upload

### Methodology (Verified)
- Lockheed Martin Cyber Kill Chain: https://www.lockheedmartin.com/en-us/capabilities/cyber/cyber-kill-chain.html
- MITRE ATT&CK Framework: https://attack.mitre.org/

### Best Practices
- OWASP Cheat Sheets: https://cheatsheetseries.owasp.org/
  - Authentication Cheat Sheet
  - Authorization Cheat Sheet
  - Secure File Upload Cheat Sheet

### Detection Rules
- Sigma Rule Format: https://github.com/SigmaHQ/sigma
- Based on industry-standard SIEM patterns

---
**Status:** Week 4 Complete | Web Pentesting + Passive Recon Mastered | 6-Part Framework Applied
