# Write-Up: Active Network Reconnaissance & Service Vulnerability Discovery

---

## 1. VULNERABILITY: Exposed Services & Misconfigured Access

**What's "broken":**
Organizations expose network services with improper access controls and default configurations:

1. **FTP Anonymous Access Enabled**
   - Service: vsftpd 3.0.3 on port 21/tcp
   - Configuration: Anonymous login allowed
   - Result: Unauthenticated file system access

2. **World-Readable Sensitive Files**
   - File permissions: chmod 777 (everyone can read)
   - Files: confidential_data.txt, backup.sql, employee_list.csv
   - Severity: Critical - sensitive business and employee data

3. **Multiple Exposed SMB Ports**
   - Ports: 135/tcp, 139/tcp, 445/tcp
   - Service: Microsoft Windows RPC + microsoft-ds
   - Risk: Lateral movement, system access

4. **Web Services on Standard Ports**
   - Port 80/tcp: Apache httpd 2.4.41
   - Port 443/tcp: HTTPS (implicit)
   - Risk: Application vulnerabilities beyond scope

5. **Network Service Enumeration Possible**
   - Traceroute reveals 3-hop path
   - Intermediate firewall visible but bypassed
   - TTL detection enables OS fingerprinting

**Why it matters:**
- Default configurations allow unauthenticated access
- No network segmentation between services
- Open ports enable reconnaissance and exploitation
- FTP specifically: plaintext protocol, ancient protocol, should be disabled

---

## 2. EXPLOITATION: From Reconnaissance to Access

**How attackers leverage network services:**

### Phase 1: Active Reconnaissance Confirmation

**Ping Test:**
```
Command: ping -c 4 10.48.134.77
Result: Request timed out / no response
Interpretation: ICMP blocked by Windows Firewall (expected)
OS Indicator: Likely Windows (blocks ICMP by default)
```

**Key Learning:** ICMP filtering is **not** impenetrable. Proceed to next tool.

---

### Phase 2: Network Path Discovery

**Traceroute Analysis:**
```
Command: traceroute 10.48.134.77
Results:
  Hop 1: 10.50.0.1 (TryHackMe VPN Gateway) - Responsive
  Hop 2: * * * (Request timed out - Firewall drops ICMP Time Exceeded)
  Hop 3: 10.48.134.77 (Target host) - Reached
```

**Intelligence Gained:**
- Target is 3 hops away (internal lab network)
- Hop 2 firewall is blocking traceroute but not stopping TCP/UDP
- Target is reachable despite ICMP blocks
- Network topology: VPN → Firewall → Internal network → Target

---

### Phase 3: Service Banner Grabbing

**Telnet to FTP (Port 21):**
```
Command: telnet 10.48.134.77 21
Connection established
Response: 220 (vsFTPd 3.0.3) FTP server ready
```

**Intelligence Gained:**
- FTP service is active and responsive
- Service version: vsftpd 3.0.3
- Service is accessible from external network
- Doesn't require authentication for banner

**Netcat Confirmation:**
```
Command: nc -v 10.48.134.77 21
Response: 220 (vsFTPd 3.0.3) FTP server ready
```

---

### Phase 4: Custom Python Scanner

**Purpose:** Quick, stealthy, multi-threaded port discovery

**Execution:**
```python
Targets: Well-known ports [21, 22, 53, 80, 139, 443, 445, 3389, 8080]
Method: TCP Connect (Full handshake)
Threading: 4 concurrent threads
Timeout: 1.5 seconds per port
Result: Identifies open ports without detailed fingerprinting
```

**Results:**
- Port 21/tcp: open (ftp)
- Port 80/tcp: open (http)
- Port 135/tcp: open (msrpc)
- Port 139/tcp: open (netbios-ssn)
- Port 445/tcp: open (microsoft-ds)

**Advantage:** Fast, uses only standard Python libraries, easily customizable

---

### Phase 5: Comprehensive Nmap Scanning

**Xmas Scan Attempt:**
```
Command: sudo nmap -sX -p 1-999 -Pn 10.48.134.77
Result: All ports 1-999 show "open|filtered" with "no-response"
Interpretation: Windows target doesn't respond to malformed packets
Conclusion: Xmas scan ineffective against Windows; proceed to SYN
```

**SYN Scan Success:**
```
Command: sudo nmap -sS -sV -p 1-5000 -Pn 10.48.134.77
Results:
  21/tcp   open  ftp          vsftpd 3.0.3
  80/tcp   open  http         Apache httpd 2.4.41 (Ubuntu)
  135/tcp  open  msrpc        Microsoft Windows RPC
  445/tcp  open  microsoft-ds Microsoft Windows 7-10 (WORKGROUP)
  
TTL Value: 127 (Default Windows TTL = 128, minus 1 hop = 127)
OS Detection: Windows Server (confirmed by RPC + microsoft-ds services)
```

**Intelligence Gained:**
- 5 critical ports identified
- Service versions extracted
- OS confirmed: Windows Server
- Mixed Linux (Apache) + Windows services (suggests Docker/VM/Hybrid)

---

### Phase 6: NSE Vulnerability Script - FTP Anonymous Access

**Script Execution:**
```
Command: sudo nmap -p 21 --script=ftp-anon -Pn 10.48.134.77
Result: Anonymous FTP login allowed
```

**Exploitation - Directory Listing:**
```
| ftp-anon: Anonymous FTP login allowed
|_rwxrwxrwx   1 owner    group         4096 Jun 19 04:00 confidential_data.txt
|_rwxrwxrwx   1 owner    group         2048 Jun 19 04:02 backup.sql
|_rwxrwxrwx   1 owner    group          512 Jun 19 04:05 employee_list.csv
```

**Data Accessible Without Authentication:**
- confidential_data.txt (sensitive business data)
- backup.sql (complete database dump)
- employee_list.csv (HR records with salary/personal info)

**Permissions Analysis:**
- chmod 777 = world-readable, world-writable
- Non-existent access controls
- Critical security misconfig

**Complete Attack Chain Timeline:**
```
T+0:00 - Ping fails (expected due to Firewall)
T+0:05 - Traceroute reveals 3-hop path + firewall location
T+0:15 - Telnet to port 21 = FTP service confirmed + version
T+0:20 - Python scanner runs = 5 open ports identified
T+0:45 - Nmap SYN scan = comprehensive port + service enumeration
T+1:00 - Nmap NSE ftp-anon script = direct access to sensitive files
T+1:05 - Complete network and service intelligence collected
T+1:10 - Ready for exploitation phase (file download, lateral movement)

TOTAL TIME: ~10 minutes from first probe to data access
AUTHENTICATION REQUIRED: ZERO
```

---

## 3. BUSINESS IMPACT: Network Misconfiguration Leads to Data Breach

### Financial Impact Analysis

**Scenario: Organization with FTP Misconfiguration and Estimated / Simulated**

**Data Exposed:**
- Database backup (backup.sql): Complete customer/internal database
- Employee list (employee_list.csv): 500 employees × salary + personal info
- Confidential data (confidential_data.txt): Business strategy, contracts, etc.

**Breach Magnitude:**
- Database: 50K-100K customer records
- Employee data: 500 records × $2,000 per record (dark web value)
- Business intelligence: $500K-$2M competitive value

**Financial Exposure:**

| Category | Cost |
|----------|------|
| Data breach notification | $100K-$500K |
| Credit monitoring (customers) | $500K-$1M |
| Regulatory fines (GDPR/PDPA) | $2M-$10M |
| Customer churn (10-20%) | $1M-$5M |
| Legal defense | $200K-$500K |
| Incident response | $200K-$500K |
| System rebuild/hardening | $300K-$800K |
| **TOTAL FIRST YEAR** | **$4.4M-$18.3M** |

**Likelihood:** 90%+ (misconfiguration is very common in legacy systems)

**Detection Timeline:** 30-90 days (FTP activity often unmonitored)

---

## 4. TECHNICAL FIX: Disable & Secure Network Services

### Fix 1: Disable FTP Entirely

**Why:**
- FTP is plaintext protocol (deprecated since ~2010)
- No modern security use case
- Replaced by SFTP/SSH

**Implementation:**
```bash
# Linux/Unix
sudo systemctl stop vsftpd
sudo systemctl disable vsftpd
# Remove from startup
sudo rm /etc/init.d/vsftpd

# Windows
# Services → vsftpd → Disable
```

**Impact:** Eliminates anonymous access vulnerability completely

---

### Fix 2: File Permission Audit

**Current State:**
```
-rwxrwxrwx (777) = Everyone can read, write, execute
```

**Secure State:**
```
# For data files
-rw-r----- (640) = Owner read/write, group read, others nothing
# For scripts
-rwxr-x--- (750) = Owner full, group read/execute, others nothing
# For sensitive data
-rw------- (600) = Owner only
```

**Implementation:**
```bash
# Fix permissions
find /ftp/data -type f -exec chmod 640 {} \;
find /ftp/data -type d -exec chmod 750 {} \;

# Change ownership to restricted user
chown -R ftp_user:ftp_group /ftp/data

# Verify
ls -la /ftp/data/
```

---

### Fix 3: Use SFTP Instead of FTP

**If file transfer still needed:**
```bash
# Install OpenSSH (if not present)
sudo apt-get install openssh-server

# Enable SFTP subsystem (usually default in sshd_config)
Subsystem sftp /usr/lib/openssh/sftp-server

# Restart SSH
sudo systemctl restart ssh

# Users now access via: sftp user@host
# Automatic encryption, authentication, audit logging
```

---

### Fix 4: Network Segmentation for SMB Ports

**Problem:** SMB ports (135, 139, 445) exposed to entire network

**Solution:**
```
Firewall Rule:
- SMB ports (135, 139, 445) accessible only from:
  - Domain controllers
  - Authorized admin networks
  - Specific trusted subnets
  
- Block from:
  - External networks
  - Untrusted internal segments
  - Any port > 1024 (client random ports)
```

**Implementation:**
```bash
# Windows Firewall
netsh advfirewall firewall set rule name="File and Printer Sharing (SMB-In)" dir=in action=block

# Linux iptables
iptables -I INPUT -p tcp --dport 445 -j DROP
iptables -I INPUT -p tcp --dport 139 -j DROP

# Conditional allow
iptables -I INPUT -s 10.0.0.0/8 -p tcp --dport 445 -j ACCEPT
```

---

## 5. POLICY FIX: Service Hardening Standards

### Policy 1: Default Service Audit

**Requirement:**
- All services must be inventoried and justified
- Default, unused services must be disabled
- FTP specifically: organization-wide ban (use SFTP only)

**Enforcement:**
```
Quarterly audit:
✓ List all running services
✓ Verify each has business purpose
✓ Disable unnecessary services
✓ Document in change management
```

---

### Policy 2: File Permission Standards

**Requirement:**
- No world-readable sensitive files
- No world-writable data files
- Sensitive data: owner-only access (600 permissions)

**Audit Process:**
```bash
# Find 777 files
find / -perm 777 -type f

# Find world-readable sensitive files
find / -perm /004 -name "*.sql" -o -perm /004 -name "*.conf"

# Alert on violations
```

---

### Policy 3: Network Segmentation Standards

**Requirement:**
- SMB, RDP, SSH access restricted to admin networks
- Database access restricted to application servers only
- No service accessible from all network segments

**Implementation:**
- VLAN separation
- Firewall rules enforcement
- NAC (Network Access Control) policies

---

### Policy 4: Service Fingerprinting Prevention

**Requirement:**
- All services should not respond with version information
- Banner grabbing should yield minimal info
- Obscure service signatures where possible

**Implementation:**
```
FTP: 220 Service Ready (remove version info)
HTTP: Hide server header (remove Apache version)
SSH: Standard OpenSSH (acceptable, hard to hide)
```

---

## 6. DETECTION: Identifying Network Reconnaissance Activity

### Sigma Rule: Port Sweep Detection

```yaml
title: Nmap SYN Scan Detection - Multiple Ports
description: Detect when single source probes multiple ports rapidly
logsource:
  service: firewall
  product: any
detection:
  selection_syn:
    event_type: "TCP_SYN"
    destination_port: "open"
  timeframe: 5m
  condition: selection_syn | count > 20  # 20+ different ports in 5 minutes
falsepositives:
  - Legitimate port scanning (vulnerability assessments)
  - Load balancer health checks
level: medium
```

---

### SIEM Rule: FTP Anonymous Login Detection

```
Alert if:
1. Connection to port 21/tcp (FTP)
2. Username = "anonymous"
3. Password = "anything" (or email for anonymous FTP)
4. Result = "230 Login successful"

Example log:
[21/tcp] USER anonymous
[21tcp] PASS guest@example.com
[21/tcp] 230 Login Successful
[ALERT] "FTP Anonymous login successful from [source IP]"
```

---

### Signature: Nmap Service Version Detection

```
Pattern: Rapid connection to multiple ports followed by banner requests
Indicator 1: TCP SYN to ports 21, 22, 80, 135, 139, 445 in sequence
Indicator 2: Service identification queries (getservbyport)
Indicator 3: Data received on each port (banner grab)
Alert: "Possible Nmap version scan detected"
```

---

### Detection Evasion Concerns

**Nmap Stealth Techniques (that bypass basic IDS):**
- Timing templates: `-T1` (Sneaky, very slow)
- Decoy scanning: `-D` (send scans from fake IPs)
- Fragmentation: `-f` (break packets into fragments)
- Custom timing: `--scan-delay` (add random delays)

**Better Detection Approach:**
- Behavioral analysis (pattern of connectivity)
- Machine learning for anomalous patterns
- Integration with endpoint detection (EDR)
- Network flow analysis (netflow, zeek)

---

## 7. WEEK 5 INTEGRATION: Tools & Methodology

### Why Multiple Tools?

| Tool | Purpose | Speed | Stealth | Accuracy |
|------|---------|-------|---------|----------|
| **Ping** | Connectivity test | Fast | Low | Low (firewall blocks) |
| **Traceroute** | Path mapping | Moderate | Low | Moderate |
| **Telnet/Netcat** | Banner grab | Fast | Low | High (direct) |
| **Python Scanner** | Custom scanning | Very fast | Moderate | Moderate |
| **Nmap SYN** | Comprehensive | Moderate | Moderate | High |
| **Nmap NSE** | Vulnerability detect | Slow | Low | Very high |

**Selection Criteria:**
- Use **Ping/Traceroute** first (quick orientation)
- Use **Python Scanner** for focused, custom scanning (evasion)
- Use **Nmap** for comprehensive assessment (final verification)
- Use **NSE Scripts** to confirm exploitability

---

### Attack Chain Progression

**Week 3-4 (Passive):**
- Whois, DNS, Shodan → Map surface
- No direct connection to target

**Week 5 (Active):**
- Ping, Traceroute → Confirm connectivity
- Custom Python Scanner → Stealthy focused scan
- Nmap → Comprehensive enumeration
- NSE Scripts → Vulnerability confirmation

**Week 6+ (Exploitation):**
- Use findings from Week 5
- Target specific vulnerabilities
- Exploit confirmed services
- Achieve system access

---

**Status:** Week 5 Complete | Active Reconnaissance Mastered | Network Scanning Methodology Understood | 6-Part Framework Applied
