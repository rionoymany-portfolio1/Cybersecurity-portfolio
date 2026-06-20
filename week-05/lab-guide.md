# Lab Guide: Week 5 - Active Reconnaissance & Network Scanning

> **Hands-on Exercises Across TryHackMe, Python Development, and Real-world Scanning**

---

## Part 1: Active Reconnaissance Room
### https://tryhackme.com/room/activerecon

**Time:** 2-3 hours
**Difficulty:** Beginner
**Prerequisites:** Basic Linux command line

---

### Task 1: Introduction

**What to Learn:**
- Difference between passive and active reconnaissance
- Legal and ethical considerations
- Timeline of attack chain

**Exercise:**
1. Read intro material
2. Understand attack progression
3. Note key concepts

**Key Takeaway:**
Active recon = higher risk but higher accuracy than passive

---

### Task 2: Web Browser

**What to Learn:**
- Using browser for reconnaissance
- Developer tools inspection
- Source code analysis

**Hands-on Exercise:**
1. Open target website in browser
2. Press F12 (Developer Tools)
3. Check Network tab for requests
4. View page source (Ctrl+U)
5. Check for comments, scripts, headers
6. Document findings

**Things to Look For:**
```
- Server header: Apache? Nginx? IIS?
- X-Powered-By: What framework?
- Comments in HTML: Developer notes?
- JavaScript files: What libraries?
- Cookies: Session tokens? Admin indicators?
- Form fields: Hidden inputs? Comments?
```

**Task Completion:**
Answer questions about what you found in the page source

---

### Task 3: Ping

**What to Learn:**
- ICMP protocol basics
- TTL values and OS detection
- Connectivity testing

**Hands-on Exercise:**
```bash
# Basic ping
ping -c 4 [target]

# Continuous ping (Ctrl+C to stop)
ping [target]

# Ping with larger packets
ping -s 1500 [target]

# Fast ping (requires root)
sudo ping -i 0.1 [target]
```

**Observations to Make:**
1. Does target respond?
2. What TTL value do you see?
3. What OS can you infer?
4. Is response time consistent?
5. Is there packet loss?

**Document:**
```
Target: [IP]
Response: [Yes/No/Timeout]
TTL: [value]
Inferred OS: [Windows/Linux/Other]
Packet Loss: [0%/X%]
Response Time: [X ms average]
```

**Task Completion:**
Answer TTL-based questions about OS detection

---

### Task 4: Traceroute

**What to Learn:**
- Network path mapping
- Router identification
- Firewall detection

**Hands-on Exercise:**
```bash
# Basic traceroute
traceroute [target]

# Traceroute with max hops
traceroute -m 15 [target]

# TCP-based traceroute (harder to block)
sudo traceroute -T -p 80 [target]

# Verbose output
traceroute -v [target]
```

**Analysis:**
1. Count total hops
2. Identify responsive hops
3. Note timeout hops (*** ***)
4. Map network structure

**Document:**
```
Hop 1: [IP] - [Latency] ms - [ISP/Gateway]
Hop 2: [IP] - [Latency] ms - [Description]
Hop 3: *** - Timeout (Firewall?)
Hop 4: [Target IP] - [Latency] ms - REACHED

Total Hops: [N]
Firewalls Detected: [Y/N]
Network Structure: [Description]
```

**Task Completion:**
Answer questions about traceroute output interpretation

---

### Task 5: Telnet

**What to Learn:**
- Direct TCP service connection
- Banner grabbing
- Service version identification

**Hands-on Exercise:**
```bash
# Connect to FTP
telnet [target] 21

# Connect to HTTP
telnet [target] 80

# Connect to SSH
telnet [target] 22

# Try to issue commands
[After connection]
GET / HTTP/1.0
[Press Enter twice for HTTP]

USER anonymous
PASS guest
[For FTP]
```

**Services to Test:**
| Port | Service | Banner Expected |
|------|---------|-----------------|
| 21 | FTP | 220 vsFTPd... |
| 22 | SSH | SSH-2.0-OpenSSH... |
| 80 | HTTP | (none, wait for GET response) |
| 443 | HTTPS | (same as 80 but encrypted) |

**Document:**
```
Service: [FTP/SSH/HTTP]
Port: [N]
Connected: [Yes/No]
Banner: [Exact version string]
Commands Accepted: [USER/PASS/GET/etc]
Exploitable: [Yes/No/Maybe]
```

**Task Completion:**
Document banners for each service discovered

---

### Task 6: Netcat

**What to Learn:**
- Raw socket communication
- Interactive service testing
- More flexible than telnet

**Hands-on Exercise:**
```bash
# Basic connection
nc [target] 21

# Verbose connection
nc -v [target] 21

# Connection with timeout
nc -w 5 [target] 21

# Create script to send commands
echo -e "USER anonymous\nPASS guest\nLIST" | nc [target] 21
```

**Compare to Telnet:**
1. Does output differ?
2. Does connection feel different?
3. Which is easier to automate?

**Advantages of Netcat:**
- No telnet signature
- Easier to pipe commands
- Better for scripting
- Can listen on ports (netcat -l)

**Task Completion:**
Complete commands to access FTP via netcat

---

### Task 7: Putting It All Together

**What to Learn:**
- Attack chain workflow
- Tool selection logic
- Methodology thinking

**Hands-on Exercise:**

**Scenario:** You know a target IP but nothing else

**Complete This Workflow:**
```
Step 1: Ping [target]
→ Determine if host online
→ Get TTL for OS guess

Step 2: Traceroute [target]
→ Map network path
→ Confirm connectivity despite firewall

Step 3: Telnet/Netcat to ports 21, 22, 80, 443
→ Confirm services running
→ Grab service banners
→ Identify software versions

Step 4: Document Findings
Target IP: [X.X.X.X]
Open Ports: [21, 80, 443]
Services: [FTP vsftpd, HTTP Apache, HTTPS Apache]
OS Guess: [Windows based on TTL]
Exploitable: [FTP Anonymous likely based on version]

Step 5: Plan Next Steps
Next Phase: Run Python scanner on priority ports
Then: Use Nmap for comprehensive scan
Finally: Test for specific vulnerabilities
```

**Task Completion:**
Diagram the complete reconnaissance workflow

---

## Part 2: Nmap Room
### https://tryhackme.com/room/furthernmap

**Time:** 3-4 hours
**Difficulty:** Beginner to Intermediate

### Tasks 1-9: Nmap Fundamentals (Quick Summary)

**Task 1-2: Deploy & Introduction**
- Understand Nmap purpose
- Know when to use which scan

**Task 3: Nmap Switches**
- `-sS`: SYN scan (default)
- `-sT`: TCP Connect
- `-sU`: UDP scan
- `-sV`: Service version detection
- `-O`: OS detection
- `-p`: Port range
- `-Pn`: Skip ping

**Task 4-9: Scan Types**
Learn each scan type and when to use:
- TCP Connect: Reliable, logged
- SYN: Fast, semi-stealthy
- UDP: Slow, different protocol
- NULL/FIN/Xmas: Stealthy but unreliable on Windows
- ICMP: Network mapping

### Tasks 10-13: Advanced Nmap

**Task 10-12: NSE Scripts**
```bash
# List available scripts
nmap --script-help ftp-anon

# Run FTP anonymous check
nmap -p 21 --script=ftp-anon [target]

# Run all default scripts
nmap -p 21 --script=default [target]

# Search for scripts
nmap --script-help "ftp*"
```

**Task 13: Firewall Evasion**
```bash
# Slow scan (hard to detect)
nmap -T1 [target]

# Decoy scanning
nmap -D 192.168.1.1,192.168.1.2 [target]

# Fragment packets
nmap -f [target]

# Spoof MAC address
nmap --spoof-mac [target]
```

### Task 14: Practical

**Real Scanning Exercise:**
```bash
# Step 1: Quick SYN scan
sudo nmap -sS -Pn [target]

# Step 2: Version detection on open ports
sudo nmap -sS -sV -p [open ports] [target]

# Step 3: NSE vulnerability scan
sudo nmap -p 21 --script=ftp-anon -sV [target]

# Step 4: OS detection
sudo nmap -O -sV -Pn [target]
```

**Document Results:**
```
Target: [IP]
Open Ports: [21/tcp, 80/tcp, 445/tcp]
Services: [FTP vsftpd 3.0.3, HTTP Apache 2.4.41]
OS: [Windows 7-10 (guessed)]
Vulnerabilities: [FTP Anonymous Access Allowed]
Files Found: [confidential_data.txt, backup.sql]
```

---

## Part 3: Python Port Scanner Development

**Time:** 2 hours
**Requirements:** Python 3.6+, basic threading knowledge

### Exercise 1: Understand the Code

**Read through provided code:**
```python
# Study each section:
1. Import statements (socket, threading, queue)
2. Configuration (target_host, port_range)
3. scan_port() function (TCP connect logic)
4. thread_worker() function (queue management)
5. main() function (thread orchestration)
```

**Questions to Answer:**
1. Why use `socket.connect_ex()` instead of `socket.connect()`?
2. What does `settimeout(1.5)` accomplish?
3. How many threads run concurrently?
4. What happens if hostname can't be resolved?
5. What does task_done() do?

### Exercise 2: Run the Scanner

```bash
# Save code to file
nano port_scanner.py

# Copy and paste code from resources

# Run scanner
python3 port_scanner.py

# Expected output:
# Scanning Target: 10.48.134.77
# Time Started: [timestamp]
# PORT      STATE     SERVICE
# 21/tcp    open      ftp
# 80/tcp    open      http
# ...
# Scan Mission Accomplished Successfully
```

### Exercise 3: Modify the Scanner

**Modification 1: Change Target**
```python
# Line 5: Change target_host
target_host = "10.48.134.77"  # Change this to your target
```

**Modification 2: Change Port Range**
```python
# Line 6: Custom port range
port_range = [21, 22, 80, 443, 8080]  # Add/remove ports
```

**Modification 3: Change Thread Count**
```python
# Around line 80: Adjust concurrent threads
for _ in range(8):  # Change from 4 to 8
    t = threading.Thread(target=thread_worker, args=(port_queue,))
```

**Modification 4: Add Delay Between Scans**
```python
# In scan_port() function, add:
import time
time.sleep(0.1)  # 100ms delay between ports
```

### Exercise 4: Compare with Nmap

```bash
# Run Python scanner
time python3 port_scanner.py
# Note: execution time

# Run Nmap equivalent
time nmap -sS -p [ports] [target]
# Compare speed

# Run Nmap with version detection
nmap -sS -sV -p [ports] [target]
# Compare output detail
```

**Comparison Matrix:**
| Aspect | Python | Nmap |
|--------|--------|------|
| Speed | [X] sec | [Y] sec |
| Ports Found | [N] | [N] |
| Service Info | Names only | Names + versions |
| Vulnerabilities | None | [N] found |
| Output Format | Text | Multiple formats |

---

## Part 4: Integration Exercise

**Combine All Three Rooms into Real Attack Chain:**

**Scenario:** You have target IP 10.48.134.77, discover it from scratch

**Step 1: Active Recon (Task 2-7)**
```bash
ping -c 4 10.48.134.77
traceroute 10.48.134.77
telnet 10.48.134.77 21
nc -v 10.48.134.77 21
```
**Findings:** Host online, 3 hops, FTP service running

**Step 2: Python Scanner (Custom tool)**
```python
# Run port_scanner.py on well-known ports
target_host = "10.48.134.77"
port_range = [21, 22, 53, 80, 139, 443, 445, 3389, 8080]
# Execute and note open ports
```
**Findings:** Ports 21, 80, 135, 139, 445 open

**Step 3: Nmap Verification & Details (Task 14)**
```bash
# Comprehensive scan
sudo nmap -sS -sV -p 21,80,135,139,445 10.48.134.77
```
**Findings:** vsftpd 3.0.3, Apache 2.4.41, Windows RPC

**Step 4: Vulnerability Testing (Task 14 + NSE)**
```bash
# Test FTP anonymous
nmap -p 21 --script=ftp-anon -sV 10.48.134.77
```
**Findings:** Anonymous access allowed, sensitive files found

**Step 5: Document Complete Reconnaissance**
```
RECONNAISSANCE COMPLETE

Target: 10.48.134.77
Status: Online (3 hops from VPN gateway)

Open Ports:
- 21/tcp   ftp       vsftpd 3.0.3     [CRITICAL: Anonymous + world-readable files]
- 80/tcp   http      Apache 2.4.41    [MEDIUM: Outdated version]
- 135/tcp  msrpc     Windows RPC      [HIGH: Lateral movement vector]
- 139/tcp  netbios   Windows NetBIOS  [HIGH: SMB alternative]
- 445/tcp  smb       Windows 7-10     [HIGH: Exploitation target]

Next Steps:
1. Download sensitive files from FTP
2. Enumerate Apache web application
3. Test Windows RPC for exploits
4. Plan SMB exploitation
5. Establish persistence
```

---

## Lab Completion Checklist

### Active Reconnaissance Room
- [ ] Task 1: Intro completed
- [ ] Task 2: Web browser analysis done
- [ ] Task 3: Ping tests documented with TTL
- [ ] Task 4: Traceroute path mapped
- [ ] Task 5: Telnet banners collected
- [ ] Task 6: Netcat commands executed
- [ ] Task 7: Attack chain workflow documented

### Nmap Room
- [ ] Tasks 1-9: Fundamentals completed
- [ ] Tasks 10-12: NSE scripts practiced
- [ ] Task 13: Firewall evasion techniques understood
- [ ] Task 14: Practical scan completed
- [ ] Results documented in detail

### Python Scanner
- [ ] Code understood (each function)
- [ ] Scanner executed successfully
- [ ] Modifications tested (ports, threads)
- [ ] Speed comparison completed
- [ ] Output matches Nmap results

### Integration Exercise
- [ ] All 3 tools used in sequence
- [ ] Attack chain documented
- [ ] Vulnerability findings recorded
- [ ] Next exploitation steps planned

---

## Common Issues & Troubleshooting

### Python Scanner Issues

**Issue: "Permission Denied"**
```bash
# Solution: Bind to ports <1024 requires sudo
sudo python3 port_scanner.py
```

**Issue: "Connection refused" on all ports**
```bash
# Solution: Target is offline or IP wrong
# Verify with ping first
ping [target]
```

**Issue: Threads hanging (program stuck)**
```bash
# Solution: Increase timeout or reduce thread count
s.settimeout(0.5)  # Reduce timeout
# Or use: for _ in range(2): instead of range(4)
```

### Nmap Issues

**Issue: "You are not running nmap as root"**
```bash
# Solution: Use sudo for SYN and OS detection
sudo nmap -sS -O [target]
```

**Issue: "Port seems closed but I know it's open"**
```bash
# Solution: Use -Pn to skip ping (firewall may block)
nmap -Pn [target]
```

**Issue: NSE script says "Timeout"**
```bash
# Solution: Increase timeout
nmap -p 21 --script-timeout=10 --script=ftp-anon [target]
```

---

**Status:** Week 5 Lab Guide | All Exercises Included | Ready for Practice
