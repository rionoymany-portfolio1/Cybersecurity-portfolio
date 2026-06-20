# Resources: Week 5 - Active Reconnaissance & Network Scanning

---

## TryHackMe Rooms

### Room 1: Active Reconnaissance
- **URL:** https://tryhackme.com/room/activerecon
- **Time:** 2-3 hours
- **Difficulty:** Beginner
- **Topics:** Ping, traceroute, telnet, netcat, web browser
- **Key Skill:** When and how to use each tool

### Room 2: Nmap
- **URL:** https://tryhackme.com/room/furthernmap
- **Time:** 3-4 hours
- **Difficulty:** Beginner to Intermediate
- **Topics:** Scan types, version detection, NSE scripts, firewall evasion
- **Key Skill:** Comprehensive network reconnaissance

---

## Network Tools Documentation

### Ping (ICMP)

**Official Documentation:**
- RFC 792 (ICMP): https://tools.ietf.org/html/rfc792
- Linux man page: `man ping`
- Windows help: `ping /?`

**Common Flags:**
```bash
ping -c 4 target          # Linux: 4 packets
ping -n 4 target          # Windows: 4 packets
ping -s 1500 target       # Specify packet size
ping -i 0.1 target        # Interval between packets
ping -t target            # Continuous (Ctrl+C to stop)
ping -w 2000 target       # Wait time in milliseconds
```

**TTL Reference Values:**
| OS | Default TTL |
|----|------------|
| Windows | 128 |
| Linux | 64 |
| macOS | 64 |
| Cisco Router | 255 |
| Solaris | 256 |

### Traceroute

**Official Documentation:**
- RFC 1393 (Traceroute): https://tools.ietf.org/html/rfc1393
- Linux man page: `man traceroute`
- Windows: `tracert /?`

**Common Flags:**
```bash
traceroute target                    # Basic
traceroute -m 15 target              # Max hops
traceroute -w 2 target               # Wait time per probe
traceroute -T -p 80 target           # TCP-based (port 80)
traceroute -I target                 # ICMP-based
traceroute -U target                 # UDP-based (default)
```

**Tools:**
- mtr (better traceroute): `mtr target`
- tracepath (no root needed): `tracepath target`

### Telnet

**Official Documentation:**
- RFC 854 (TELNET): https://tools.ietf.org/html/rfc854
- Linux: `man telnet`
- Installation: `apt-get install telnet` (often removed for security)

**Usage:**
```bash
telnet target 21              # Connect to FTP
telnet target 80              # Connect to HTTP
telnet target 22              # Connect to SSH
telnet target 25              # Connect to SMTP
```

**Interactive Commands by Service:**
```
FTP:    USER, PASS, LIST, GET, PUT, QUIT
SMTP:   EHLO, MAIL FROM, RCPT TO, DATA
HTTP:   GET / HTTP/1.0 [ENTER][ENTER]
IMAP:   LOGIN, LIST, SELECT, FETCH
```

### Netcat / Ncat

**Official Documentation:**
- Netcat: https://nc110.sourceforge.io/
- Ncat (from Nmap): https://nmap.org/ncat/

**Installation:**
```bash
# Linux (Debian/Ubuntu)
apt-get install netcat-traditional

# Linux (Red Hat/CentOS)
yum install netcat

# macOS
brew install netcat

# Windows (from nmap package)
# Or download nc.exe separately
```

**Common Flags:**
```bash
nc target port                        # Basic connection
nc -v target port                     # Verbose
nc -w 5 target port                   # 5 second timeout
nc -u target port                     # UDP instead of TCP
nc -l -p port                         # Listen mode
nc -l -p port < file.txt              # Send file
cat file.txt | nc target port         # Pipe to nc
```

### Nmap

**Official Documentation:**
- Website: https://nmap.org/
- Man page: `man nmap`
- Book: "Nmap Network Scanning" by Gordon Lyon (free PDF)
- Official Guide: https://nmap.org/docs/

**Installation:**
```bash
# Linux (Debian/Ubuntu)
apt-get install nmap

# Linux (Red Hat/CentOS)
yum install nmap

# macOS
brew install nmap

# Windows
# Download from https://nmap.org/download.html
```

**Essential Flags:**
```bash
# Scan Types
-sS         # SYN scan (default, requires root)
-sT         # TCP Connect (no root needed)
-sU         # UDP scan
-sX         # Xmas scan (FIN, PSH, URG)
-sF         # FIN scan
-sN         # NULL scan

# Host Discovery
-Pn         # Skip ping (assume host up)
-PS port    # TCP SYN ping
-PE         # ICMP echo ping

# Port Specification
-p 80       # Specific port
-p 1-65535  # Range
-p U:53,111,137  # UDP ports

# Service Detection
-sV         # Version detection
-O          # OS detection
-A          # Aggressive (versions + OS + scripts)

# Scripts
--script=default      # Run default scripts
--script=ftp-anon     # Run specific script
--script-help=ftp*    # Get script help
-sC         # Run default scripts (same as --script=default)

# Output
-oN file.txt    # Normal output
-oX file.xml    # XML output
-oJ file.json   # JSON output
-oG file.gnmap  # Greppable output
-oA file        # All three formats

# Timing/Performance
-T0 through -T5     # Timing templates
--max-rate=100      # Max packets per second
--min-rate=10       # Min packets per second

# Evasion
-D 192.168.1.1,192.168.1.2  # Decoy scanning
-f                  # Fragment packets
--spoof-mac MAC     # Spoof MAC address
```

**Quick Command Reference:**
```bash
# Quick SYN scan (requires root)
sudo nmap -sS target

# TCP Connect (no root needed)
nmap -sT target

# Scan with versions and default scripts
nmap -sV -sC target

# Aggressive scan (lots of info)
nmap -A target

# Scan specific ports with versions
nmap -sV -p 80,443,21 target

# UDP scan (slow, requires root)
sudo nmap -sU target

# OS detection
sudo nmap -O target

# NSE vulnerability scan
nmap -p 21 --script=ftp-anon target

# Save results in multiple formats
nmap -A -oA results target
```

---

## Python Socket Documentation

### Python socket Module

**Official Documentation:**
- Python docs: https://docs.python.org/3/library/socket.html

**Common Functions:**
```python
socket.socket()              # Create socket
socket.connect_ex()          # Non-blocking connect
socket.recv()                # Receive data
socket.send()                # Send data
socket.close()               # Close socket
socket.settimeout()          # Set timeout
socket.getservbyport()       # Get service name from port

socket.AF_INET              # IPv4
socket.SOCK_STREAM          # TCP
socket.SOCK_DGRAM           # UDP
```

**Example: Port Scanning**
```python
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(1)
result = s.connect_ex(('target', 80))
if result == 0:
    print("Port open")
else:
    print("Port closed/filtered")
s.close()
```

### Python Threading

**Official Documentation:**
- Python docs: https://docs.python.org/3/library/threading.html
- Queue docs: https://docs.python.org/3/library/queue.html

**Common Classes:**
```python
threading.Thread()          # Create thread
threading.Lock()            # Mutual exclusion
Queue.Queue()              # Thread-safe queue
```

**Example: Multi-threaded Scanning**
```python
import threading
from queue import Queue

def worker(queue):
    while not queue.empty():
        port = queue.get()
        scan_port(port)
        queue.task_done()

port_queue = Queue()
for port in range(1, 1000):
    port_queue.put(port)

# Create and start threads
for _ in range(4):
    t = threading.Thread(target=worker, args=(port_queue,))
    t.start()

port_queue.join()  # Wait for all tasks done
```

---

## OWASP & Security References

### Network Security

**OWASP Resources:**
- Network Security: https://cheatsheetseries.owasp.org/cheatsheets/Network_Segmentation_Cheat_Sheet.html
- Port Security: https://cheatsheetseries.owasp.org/cheatsheets/Network_Security_Cheat_Sheet.html

### Reconnaissance

**OWASP Testing Guide:**
- https://owasp.org/www-project-web-security-testing-guide/
- Section: Information Gathering

### Common Vulnerabilities

**CWE References:**
- CWE-200: Information Exposure: https://cwe.mitre.org/data/definitions/200.html
- CWE-284: Improper Access Control: https://cwe.mitre.org/data/definitions/284.html

---

## RFCs & Standards

### Network Protocols

**Core RFCs:**
- RFC 791: IPv4 - https://tools.ietf.org/html/rfc791
- RFC 793: TCP - https://tools.ietf.org/html/rfc793
- RFC 768: UDP - https://tools.ietf.org/html/rfc768
- RFC 792: ICMP - https://tools.ietf.org/html/rfc792

### Services

**Service Ports (Well-Known Ports):**
- IANA Port Numbers: https://www.iana.org/assignments/service-names-port-numbers/
- Most common (1-1024) require root access to listen

---

## Online Tools (For Verification)

### Web-based Reconnaissance

**DNS & Network Tools:**
- MxToolbox: https://mxtoolbox.com/
- DNS Lookup: https://www.whatsmydns.net/
- IP Location: https://ip.majestic.com/
- Port Check: https://www.yougetsignal.com/tools/open-ports/

### Vulnerability Databases

**CVE Search:**
- NVD: https://nvd.nist.gov/
- CVEdetails: https://www.cvedetails.com/
- Exploit-DB: https://www.exploit-db.com/

---

## Practice Environments

### Free Hacking Labs

**HackTheBox:**
- Website: https://www.hackthebox.eu/
- Machines for practicing scanning and exploitation
- Retired machines available for free users

**OverTheWire:**
- Website: https://overthewire.org/wargames/
- Progressive challenges
- Covers networking, security concepts

**PentesterLab:**
- Website: https://pentesterlab.com/
- Practical exploits and challenges
- Network scanning exercises

---

## Command Quick Reference

### Common Scanning Scenarios

**Scenario 1: Quick port check (5 common ports)**
```bash
# Using netcat
for port in 21 22 80 443 3389; do
  echo "Testing port $port..."
  nc -zv target $port 2>&1 | grep -v refused
done
```

**Scenario 2: Full port range with Nmap**
```bash
# Comprehensive scan
sudo nmap -A -p- target
```

**Scenario 3: Service fingerprinting**
```bash
# Get versions + OS
nmap -sV -O target
```

**Scenario 4: Vulnerability detection**
```bash
# Run NSE scripts
nmap -A --script=default target
```

**Scenario 5: Firewall detection**
```bash
# Test firewall blocking
sudo nmap -sX target  # Xmas scan (blocked on Windows)
sudo nmap -sN target  # NULL scan (filtered on modern systems)
```

---

## Weekly Study Schedule

### Monday
- Install Nmap if needed
- Read: Ping basics
- Lab: Complete active-recon Task 2-3

### Tuesday
- Read: Traceroute & network paths
- Lab: Active-recon Task 4
- Install/test netcat and telnet

### Wednesday
- Read: Nmap scan types (Task 3-5)
- Lab: Nmap Room Tasks 1-9
- Understand -sS vs -sT vs -sX differences

### Thursday
- Write/test Python port scanner
- Modify scanner (different ports, threads)
- Compare speed with Nmap

### Friday
- Nmap version detection (-sV)
- NSE script usage
- Lab: Nmap Room Task 14 (Practical)

### Saturday
- Integration: Use all tools in sequence
- Document complete reconnaissance
- Write 6-part vulnerability report

### Sunday
- Review week's learning
- Practice command combinations
- Commit code to GitHub

---

## Useful Aliases for Bash

**Add to ~/.bashrc to make commands faster:**
```bash
# Quick port scanning
alias quickscan='nmap -sS -Pn'
alias versionscan='nmap -sV -Pn'
alias fullscan='nmap -A -p-'

# Python scanner quick run
alias pyscan='python3 simple-port-scanner.py'

# Common network tools
alias ports='sudo netstat -tulnp'
alias tcpdump80='sudo tcpdump -i any "port 80"'
alias monitor='watch -n 1 netstat -tulnp'
```

**Reload after editing:**
```bash
source ~/.bashrc
```

---

## Common Issues & Solutions

### "Permission Denied" for Nmap Scans
```bash
# Solution: Use sudo for raw packet scans
sudo nmap -sS target
```

### Python Socket Binding Issues
```bash
# Kill process on port
sudo lsof -i :8080
sudo kill -9 [PID]
```

### Timeout Errors in Python
```python
# Increase timeout if network is slow
s.settimeout(3.0)  # 3 seconds instead of 1.5
```

### Nmap Takes Too Long
```bash
# Use timing templates for speed
nmap -T4 target  # Aggressive timing

# Or limit port range
nmap -p 1-1000 target  # Only first 1000 ports
```

---

## Next Week Preview

**Week 6: Exploitation Preparation**
- Use Week 5 findings to plan attacks
- Identify vulnerable services
- Prepare exploit payloads
- Test on vulnerable VMs (not production!)

**Skills Needed from Week 5:**
- Know which ports are open
- Know which services are running
- Know software versions
- Know which services have known CVEs

---

**Status:** Week 5 Resources | Comprehensive Reference | Ready for Learning & Practice
