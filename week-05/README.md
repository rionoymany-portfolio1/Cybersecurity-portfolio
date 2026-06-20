# Week 5: Active Reconnaissance & Network Scanning

> **From Basic Tools to Advanced Scanning - Building Custom Scanning Infrastructure**

---

##  Topics Covered This Week

### Room 1: Active Reconnaissance
Learn practical tools for gathering network information through direct probing.

**Tasks:**
1. Introduction
2. Web Browser reconnaissance
3. Ping - ICMP connectivity testing
4. Traceroute - Path mapping
5. Telnet - Service interaction
6. Netcat - Raw socket communication
7. Putting It All Together - Attack chain integration

### Room 2: Nmap - Further Network Mapping
In-depth exploration of the industry-standard network scanning tool.

**Tasks:**
1. Deploy
2. Introduction
3. Nmap Switches
4. Scan Types Overview
5. TCP Connect Scans
6. SYN Scans
7. UDP Scans
8. NULL, FIN, Xmas Scans
9. ICMP Network Scanning
10. NSE Scripts Overview
11. NSE Scripts - Working with scripts
12. NSE Scripts - Searching for scripts
13. Firewall Evasion
14. Practical (Real-world scanning)
15. Conclusion

### Custom Development: Simple Port Scanner
Build your own multi-threaded TCP port scanner in Python.

**Features:**
- Thread-Pool Queue Architecture (Concurrent Scanning Execution)
- Network Latency Handling via Non-blocking Socket Timeouts
- Service identification
- Graceful Shutdown via KeyboardInterrupt (Ctrl+C) Handling & Safe Resource Cleanup

---

##  Learning Objectives

**By end of Week 5, you will:**
-  Understand active reconnaissance methodology
-  Master ping, traceroute, telnet, netcat usage
-  Know when to use each tool
-  Detect OS via TTL fingerprinting
-  Understand scan types (TCP, SYN, UDP, NULL, FIN, Xmas, ICMP)
-  Write custom multi-threaded scanner
-  Use NSE scripts for vulnerability detection
-  Interpret scan results professionally
-  Integrate tools into attack chain

---

##  Why This Matters for Red Team

**Active Reconnaissance = Intelligence Gathering**

Professional attackers spend 70% of time on reconnaissance. This week shifts from **passive** (external queries) to **active** (direct probing):

| Week | Approach | Noise Level | Detection Risk |
|------|----------|------------|----------------|
| **Week 3-4** | Passive (Shodan, DNS, WHOIS) | Silent | Very Low (0%) |
| **Week 5** | Active (Ping, Nmap, Telnet) | Moderate | Moderate (30-50%) |
| **Week 6+** | Exploitation (Payload delivery) | Loud | High (70%+) |

**This Week's Advantage:**
- Direct confirmation of targets
- Service fingerprinting
- Version detection
- Vulnerability identification before exploit

**Real-World Impact:**
- Nmap + NSE scripts can identify 70%+ of vulnerabilities without exploitation
- Custom Python scanner enables stealthy, purpose-built scanning
- Understanding scan types = evading defensive tools

---


##  Attack Chain This Week

```
ACTIVE RECONNAISSANCE FLOW:

[Passive Recon Complete]
         ↓
PING (Connectivity check)
         ↓
[Blocked by Firewall? Yes→Infer OS via TTL, Continue]
         ↓
TRACEROUTE (Path mapping)
         ↓
[Identify gateway, determine network structure]
         ↓
TELNET/NETCAT (Banner grabbing)
         ↓
[Service identification, basic fingerprinting]
         ↓
PYTHON CUSTOM SCANNER (Quick port sweep)
         ↓
[Identify open ports, thread-based speed]
         ↓
NMAP COMPREHENSIVE SCAN (-sS -sV -p range)
         ↓
[Confirm ports, identify versions, service detection]
         ↓
NSE SCRIPTS (Vulnerability detection)
         ↓
[Confirm exploitability, find default configs]
         ↓
EVIDENCE COLLECTED FOR EXPLOITATION PHASE
```

---

##  TryHackMe Rooms

### Room 1: Active Reconnaissance
**URL:** https://tryhackme.com/room/activerecon
**Time:** 2-3 hours
**Difficulty:** Beginner
**Focus:** Practical tool usage

### Room 2: Nmap
**URL:** https://tryhackme.com/room/furthernmap
**Time:** 3-4 hours
**Difficulty:** Beginner to Intermediate
**Focus:** Comprehensive scanning methodology

---

##  Connection to Previous Weeks

**Week 1-3 Foundation:**
- Linux (Week 1) → Run Nmap, manage scripts
- Python (Week 2-3) → Build custom scanner, parse output

**Week 4 Context:**
- Passive Recon (Week 4) → Now we probe directly
- Web App attacks (Week 4) → Now we map network first

**Week 5 Application:**
- Network Intelligence → Foundation for Week 6 exploitation
- Service Fingerprinting → Know what to attack
- Custom Tools → Adapt to defensive measures

---

##  Unique This Week

**First Custom Tool:**
- This week you build actual working Python code
- Not just using commercial tools
- Demonstrates programming skill + network understanding

**Real Scanning:**
- Practical Nmap results (not simulated)
- Real findings (FTP misconfiguration example)
- Proof-of-concept vulnerability access

**Attack Chain Integration:**
- See how tools complement each other
- Understand when to use each
- Build methodology, not just tools

---

**Status:** Week 5 | Active Reconnaissance + Network Scanning | In Progress
