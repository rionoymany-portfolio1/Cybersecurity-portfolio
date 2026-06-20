# Active Reconnaissance Toolkit: Practical Guide

> **Direct Probing Tools - Understanding Network Responsiveness & Service Discovery**

---

## Overview: Active vs Passive Reconnaissance

| Aspect | Passive | Active |
|--------|---------|--------|
| **Method** | External queries (Shodan, DNS, WHOIS) | Direct connection to target |
| **Detection Risk** | 0% (queries are external) | 30-50% (target logs connection) |
| **Tools** | DNS, Shodan, WHOIS, traceroute | Ping, telnet, netcat, nmap |
| **Timeline** | Minutes to hours | Seconds to minutes |
| **Accuracy** | Moderate (third-party data) | High (direct confirmation) |
| **Legal Status** | Safe (public information) | Risky (direct access attempt) |

**Key Insight:** Active reconnaissance is faster and more accurate, but generates logs and potentially alerts defensive systems.

---

## Tool 1: Ping (ICMP Echo)

### Purpose
Confirm target host is online and reachable using ICMP protocol.

### Usage

**Basic ping:**
```bash
ping 10.48.134.77
ping google.com
```

**Limited attempts (recommended in offensive context):**
```bash
# Linux/Mac
ping -c 4 10.48.134.77

# Windows
ping -n 4 10.48.134.77
```

**Specify packet size:**
```bash
ping -s 1500 10.48.134.77
```

### Output Interpretation

```
PING 10.48.134.77 (10.48.134.77) 56(84) bytes of data.
64 bytes from 10.48.134.77: icmp_seq=1 ttl=127 time=1.5ms
64 bytes from 10.48.134.77: icmp_seq=2 ttl=127 time=1.6ms
64 bytes from 10.48.134.77: icmp_seq=3 ttl=127 time=1.4ms
64 bytes from 10.48.134.77: icmp_seq=4 ttl=127 time=1.7ms

--- 10.48.134.77 statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3004ms
rtt min/avg/max/stddev = 1.4/1.55/1.7/0.11 ms
```

**What Each Value Means:**

| Value | Meaning | Red Team Use |
|-------|---------|-------------|
| **TTL = 127** | Time To Live (hops remaining) | OS detection (Windows default = 128) |
| **time = 1.5ms** | Round trip time | Network proximity (fast = local) |
| **0% loss** | All packets returned | Host is online and responsive |
| **Request timeout** | No response to ICMP | Firewall blocks ICMP, host sleeping, or offline |

### OS Detection via TTL

```
Received TTL = 127 or 128  → Windows Server (decrement by 0-1)
Received TTL = 63 or 64    → Linux/Unix (decrement by 0-1)
Received TTL = 31 or 32    → Router/Network device
Received TTL = 255         → Embedded device

Default TTL values (before decrement):
- Windows: 128
- Linux/Unix: 64
- Router/Switch: 255
- iOS/Apple: 64
```

### In Week 5 Lab

**Actual Result:**
```
Command: ping -c 4 10.48.134.77
Result: Request timed out / No response
Interpretation: Windows Firewall blocking ICMP
Conclusion: Target is likely online but ICMP-blocked

Next Step: Use traceroute (uses ICMP but different) or TCP probes
```

### Detection & Evasion

**Detected by:**
- Firewall logs (ICMP Request blocked)
- IDS (sudden ICMP activity)
- Host-based detection (Windows Event Viewer)

**Evasion:**
- Expect it to fail against hardened systems
- Combine with other tools (ping alone is not conclusive)
- Slow down pings (`-i` flag) to avoid pattern detection

---

## Tool 2: Traceroute / Tracert

### Purpose
Map network path from your machine to target. Identify routers, hops, and potential firewall locations.

### Usage

**Linux/Mac:**
```bash
traceroute 10.48.134.77
traceroute -m 15 10.48.134.77  # Set max hops to 15
```

**Windows:**
```bash
tracert 10.48.134.77
```

**With specified port (TCP-based, harder to block):**
```bash
# Modern traceroute (most systems)
traceroute -T -p 80 10.48.134.77
```

### Output Interpretation

```
traceroute to 10.48.134.77 (10.48.134.77), 30 hops max, 60 byte packets

1  10.50.0.1 (10.50.0.1)  0.5 ms  0.4 ms  0.5 ms
   ├─ Hop 1: Local gateway (responds)
   ├─ IP: 10.50.0.1 (TryHackMe VPN gateway)
   └─ Response time: <1ms (local network)

2  * * *
   ├─ Hop 2: Firewall or intermediate device
   ├─ Reason: Drops ICMP Time Exceeded messages
   └─ Conclusion: Filtering happening here (intentional security measure)

3  10.48.134.77 (10.48.134.77)  1.5 ms  1.6 ms  1.4 ms
   ├─ Hop 3: Target reached
   ├─ Response time: 1.5ms (local network)
   └─ Conclusion: Target is online and responds to traceroute
```

### Red Team Intelligence from Traceroute

| Finding | Intelligence |
|---------|-------------|
| 3 total hops | Target is close (internal network) |
| Hop 1 = 10.50.0.1 | VPN/Gateway infrastructure (TryHackMe lab) |
| Hop 2 = *** | Intermediate firewall blocking ICMP responses |
| Hop 3 = Target | Target found and responsive |
| Response times <2ms | Local network (not internet-routed) |

### Week 5 Lab Result

```
Traceroute confirms:
- 3-hop path to target
- Gateway is VPN endpoint (10.50.0.1)
- Firewall at hop 2 blocks traceroute but allows TCP/UDP
- Target is reachable despite ICMP blocks

Conclusion: Proceed to TCP-based tools (telnet, nmap)
```

### Detection & Evasion

**Detected by:**
- Firewall logs (ICMP Time Exceeded dropped)
- IDS (hop sweep patterns)
- NetFlow/sFlow analysis

**Evasion:**
- Expect intermediate devices to not respond
- Combine with other reconnaissance tools
- Use TCP-based traceroute (harder to block)

---

## Tool 3: Telnet

### Purpose
Direct TCP connection to specific port and service to grab banners and identify service versions.

### Usage

**Connect to FTP (port 21):**
```bash
telnet 10.48.134.77 21
```

**Connect to HTTP (port 80):**
```bash
telnet 10.48.134.77 80
# Then type: GET / HTTP/1.0
# Press Enter twice
```

**Connect to SSH (port 22):**
```bash
telnet 10.48.134.77 22
# SSH responds with version banner automatically
```

### Output Interpretation

```bash
$ telnet 10.48.134.77 21
Trying 10.48.134.77...
Connected to 10.48.134.77.
Escape character is '^]'.
220 (vsFTPd 3.0.3)
```

**What This Tells Us:**

| Information | Red Team Use |
|------------|-------------|
| **Connected** | Port 21/tcp is open |
| **220 Response Code** | FTP server ready for login |
| **vsFTPd 3.0.3** | Service name and version |
| **No authentication yet** | Banner doesn't require login (good for us) |

### Real-World Example from Week 5

```
$ telnet 10.48.134.77 21
Connected to 10.48.134.77
220 (vsFTPd 3.0.3) FTP server ready.
```

**Red Team Analysis:**
- Service: Very old FTP implementation (vsftpd 3.0.3)
- Default configuration: Probably misconfigured
- Next step: Try FTP anonymous login
- Success: Anonymous access likely enabled

### Interactive Use

**FTP Example:**
```
telnet 10.48.134.77 21
220 (vsFTPd 3.0.3) FTP server ready
user anonymous       ← Type this
331 Please specify the password
password              ← Type this (press enter, any value works)
230 Login successful
ls                   ← List files
-rwxrwxrwx ... confidential_data.txt
-rwxrwxrwx ... backup.sql
quit
```

### Detection & Evasion

**Detected by:**
- FTP server logs (login attempts)
- Firewall logs (connection to port 21)
- IDS (FTP command patterns)

**Evasion:**
- Use netcat instead (no login prompt history)
- Combine multiple tools to avoid patterns
- Expect FTP to be logged

---

## Tool 4: Netcat (nc) / ncat

### Purpose
Raw socket communication - like telnet but more flexible, no interactive prompt history.

### Installation

```bash
# Linux (Debian/Ubuntu)
sudo apt-get install netcat-traditional

# Linux (Red Hat/CentOS)
sudo yum install netcat

# Mac
brew install netcat

# Windows
# Use ncat (from nmap package) or download nc.exe
```

### Usage

**Basic connection:**
```bash
nc 10.48.134.77 21
```

**Connect with timeout:**
```bash
nc -w 5 10.48.134.77 21
# Timeout after 5 seconds
```

**Verbose mode (show connection details):**
```bash
nc -v 10.48.134.77 21
```

**Send custom commands:**
```bash
# Create file with commands
echo "USER anonymous" > commands.txt
echo "PASS guest" >> commands.txt
cat commands.txt | nc 10.48.134.77 21
```

### Output Interpretation

```bash
$ nc -v 10.48.134.77 21
10.48.134.77 port 21 (ftp) open

220 (vsFTPd 3.0.3) FTP server ready
```

### Advantages Over Telnet

| Aspect | Telnet | Netcat |
|--------|--------|--------|
| **Interaction** | Interactive prompt | No history, direct I/O |
| **Detection** | Telnet client signature | Generic socket (harder to detect) |
| **Piping** | Limited | Full shell piping support |
| **Port Listen** | Send only | Can listen on ports (`-l`) |
| **Timeout** | Hard to set | Easy (`-w` flag) |

### Week 5 Lab Usage

```bash
$ nc -v 10.48.134.77 21
10.48.134.77 port 21 (ftp) open
220 (vsFTPd 3.0.3) FTP server ready
USER anonymous
331 Please specify the password
PASS guest@example.com
230 Login successful
TYPE I
200 Switching to Binary mode
LIST
drwxrwxrwx ... confidential_data.txt
drwxrwxrwx ... backup.sql
drwxrwxrwx ... employee_list.csv
QUIT
```

### Detection & Evasion

**Detected by:**
- Service logs (connection + commands)
- Firewall logs (port access)
- IDS (FTP command patterns)

**Evasion:**
- Netcat leaves less client-side evidence
- Combine with other tools
- Expect service to be logged regardless

---

## Putting It All Together: Attack Chain

### Workflow Example

**Step 1: Ping (Connectivity Check)**
```bash
ping -c 4 10.48.134.77
# Result: Request timed out → ICMP blocked, continue
```

**Step 2: Traceroute (Path Mapping)**
```bash
traceroute 10.48.134.77
# Result: 3 hops, Hop 2 blocked, target reachable
```

**Step 3: Python Scanner (Quick Port Discovery)**
```bash
python3 simple-port-scanner.py
# Result: Ports 21, 80, 135, 139, 445 open
```

**Step 4: Telnet (Banner Grabbing)**
```bash
telnet 10.48.134.77 21
# Result: vsFTPd 3.0.3 identified
```

**Step 5: Netcat (Interactive Testing)**
```bash
nc -v 10.48.134.77 21
# Result: Anonymous FTP login successful
```

**Step 6: Nmap (Comprehensive Scan)**
```bash
nmap -sS -sV -p 1-5000 10.48.134.77
# Result: 5 services enumerated with versions
```

**Step 7: NSE Scripts (Vulnerability Confirmation)**
```bash
nmap -p 21 --script=ftp-anon 10.48.134.77
# Result: Anonymous FTP access confirmed with file listing
```

**Step 8: Data Access**
```
Files available:
- confidential_data.txt
- backup.sql
- employee_list.csv
```

---

## Quick Reference

### When to Use Each Tool

| Situation | Tool | Reason |
|-----------|------|--------|
| "Is host online?" | Ping | Fast, simple yes/no |
| "What's the network path?" | Traceroute | Identify gateways, firewalls |
| "What service on port 21?" | Telnet | Direct connection, banner |
| "Try FTP commands?" | Netcat | Interactive, no client logs |
| "All ports + versions?" | Nmap | Comprehensive, automated |
| "Does FTP allow anon?" | NSE ftp-anon | Specific vulnerability check |

---

**Status:** Week 5 Active Reconnaissance | Tools Mastered | Ready for Network Scanning Phase
