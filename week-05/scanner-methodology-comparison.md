# Scanner Methodology Comparison: Python Custom Tool vs Nmap

> **Understanding Trade-offs: Speed, Stealth, Accuracy, and Flexibility**

---

## Quick Comparison Table

| Aspect | Python Scanner | Nmap |
|--------|---|---|
| **Speed** | Very Fast (multi-threaded) | Moderate (more comprehensive) |
| **Stealth** | Moderate (Full handshake = logged) | Better (SYN scan = half-open) |
| **Accuracy** | Low-Moderate (port status only) | Very High (versions, OS, scripts) |
| **Customization** | Unlimited (you write code) | Limited (predefined options) |
| **Learning Curve** | Python basics | Nmap flag complexity |
| **Dependencies** | Python 3 only | Nmap binary + NSE Lua |
| **Vulnerability Detection** | None (just ports) | Comprehensive (NSE scripts) |
| **Firewall Evasion** | Difficult (TCP full connect) | Easier (SYN, fragmentation, timing) |
| **Knowledge Required** | Intermediate | Beginner to Advanced |

---

## Detailed Comparison

### 1. Architecture & How They Work

#### Python Socket Scanner

**Technology Stack:**
- Python `socket` module (system-level TCP)
- `threading.Queue` (concurrent execution)
- Standard TCP three-way handshake

**Execution Flow:**
```
1. Create socket for port
2. Set 1.5 second timeout
3. Attempt TCP connect_ex()
4. If result == 0: port open
5. Get service name from port database
6. Print result
7. Close socket
```

**Code Example:**
```python
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(1.5)
result = s.connect_ex((target_host, port))
if result == 0:
    print(f"{port} is open")
s.close()
```

**What Happens at Network Level:**
```
Attacker                          Target
   |                               |
   |------ SYN ----------->|        |
   |                       | (ACK)  |
   |<----- SYN-ACK --------|        |
   |                               |
   |------ ACK ----------->|        |
   | (Three-way complete!)         |
   |                               |
   |------ FIN/RST ------->|        |
   |                               |
   (Port recorded as OPEN)
```

**Evidence Left:**
- ✓ TCP connection logs on target
- ✓ Application logs (FTP, HTTP, etc.)
- ✓ Full connection in firewall logs
- ✗ No IDS signature for "nmap scan"

---

#### Nmap SYN Scan

**Technology Stack:**
- C language (raw packet manipulation)
- libpcap (packet capture)
- Raw sockets (packet-level control)

**Execution Flow:**
```
1. Send SYN packet to port
2. Wait for SYN-ACK response
3. Record port as OPEN
4. Send RST (don't complete handshake)
5. Port scanned without full connection
```

**What Happens at Network Level:**
```
Attacker                          Target
   |                               |
   |------ SYN ----------->|        |
   |                       | (ACK)  |
   |<----- SYN-ACK --------|        |
   |                               |
   |------ RST ----------->|        | (CLOSE - half-open!)
   |                               |
   (Port recorded as OPEN, but connection never completed!)
```

**Evidence Left:**
- ✗ No full connection logs (if target monitoring incomplete connections)
- ✓ Still visible in raw firewall logs
- ✗ Harder to detect by application logs (no actual login)
- ✓ IDS/IPS may detect port-sweep pattern

**Advantage:** Faster than Python (doesn't complete handshake), less likely to trigger application logs

---

### 2. Speed Comparison

#### Scenario: Scan 100 Ports

**Python Scanner (4 threads):**
```
- 100 ports ÷ 4 threads = 25 ports per thread
- Timeout per port: 1.5 seconds
- Expected time: 25 × 1.5 = 37.5 seconds (best case)
- Actual: 45-60 seconds (network variation)

Speed: Moderate (depends on timeout)
```

**Nmap SYN Scan:**
```
- No per-port timeout (waits for response, continues on silence)
- Parallel processing: Similar to Python
- No connection completion overhead
- Expected time: 5-15 seconds

Speed: 3-5x faster than Python
```

**Real-World Observation from Week 5:**
- Python scanner: 9 ports in ~2 seconds (local network)
- Nmap SYN: 4000 ports in ~60 seconds (with -sV detection)

**Winner:** Nmap SYN scan is significantly faster

---

### 3. Stealth & Detection Risk

#### Python Scanner Detection Risk

**What Leaves Traces:**

1. **Application Logs:**
   ```
   [FTP Server]
   NEW CONNECTION from 192.168.1.100
   ATTEMPTED USERNAME: (anonymous)
   
   [Detection] ✓ OBVIOUS
   ```

2. **Firewall Logs:**
   ```
   FLOW_CLOSE: 192.168.1.100 → 10.48.134.77:21 (TCP)
   BYTES_IN: 0, BYTES_OUT: 0
   DURATION: 0.5 seconds
   
   [Detection] ✓ Multiple rapid connections to different ports
   ```

3. **IDS/IPS Signature:**
   ```
   PYTHON_PORT_SCANNER_BEHAVIOR:
   - Rapid sequential connections
   - Short connection duration
   - Service version queries
   [Detection] ✗ Generic Python signature (low confidence)
   ```

**Stealth Score:** ⚠️ MEDIUM (leaves obvious connection logs)

---

#### Nmap SYN Scan Detection Risk

**What Leaves Traces:**

1. **Application Logs:**
   ```
   [FTP Server]
   NO ENTRY (connection never completed)
   
   [Detection] ✗ NO APPLICATION LOGS
   ```

2. **Firewall Logs:**
   ```
   FLOW_INCOMPLETE: 192.168.1.100 → 10.48.134.77:21 (SYN_RECEIVED, RST)
   BYTES_TRANSFERRED: 0
   
   [Detection] ⚠️ SYN without ACK is unusual
   ```

3. **IDS/IPS Signature:**
   ```
   NMAP_SIGNATURE_DETECTED:
   - Multiple SYNs without completions
   - Systematic port progression
   [Detection] ✓ Nmap has known signatures
   ```

**Stealth Score:** 🟡 MODERATE-HIGH (harder to detect than Python, but still identifiable)

---

#### Stealth Evasion Techniques

**Python Scanner Improvements:**
```python
import time
import random

# Add random delays between ports
time.sleep(random.uniform(0.1, 1.0))

# Randomize port order
random.shuffle(port_range)

# Spread across time (T-1 template equivalent)
# Result: Harder to detect as port scan
```

**Nmap Evasion:**
```bash
# Timing template (slower = stealthier)
nmap -T1 10.48.134.77  # Very slow, harder to detect

# Decoy scanning (confuse IDS)
nmap -D 192.168.1.1,192.168.1.2 10.48.134.77

# Fragment packets
nmap -f 10.48.134.77

# Idle zombie scan
nmap -sI zombie_host 10.48.134.77
```

---

### 4. Accuracy & Information Gathering

#### Python Scanner Output

**What It Tells You:**
```
PORT    STATE   SERVICE
21/tcp  open    ftp
80/tcp  open    http
443/tcp open    https
```

**What It Doesn't Tell You:**
- ❌ Software version
- ❌ OS information
- ❌ Service details
- ❌ Vulnerability status
- ❌ Exploit recommendations

**Accuracy:** LOW (port status only)

---

#### Nmap Output with Version Detection

**What It Tells You:**
```
PORT    STATE SERVICE      VERSION
21/tcp  open  ftp          vsftpd 3.0.3
80/tcp  open  http         Apache httpd 2.4.41
443/tcp open  https        Apache httpd 2.4.41
```

**With NSE Scripts:**
```
PORT    STATE SERVICE
21/tcp  open  ftp
|_ftp-anon: Anonymous login allowed
| -rwxrwxrwx confidential_data.txt
|_-rwxrwxrwx backup.sql
```

**With OS Detection:**
```
Service Info: OS: Linux
CPE: cpe:/o:linux:linux_kernel
Aggressive OS Guesses: Linux 5.4 (93%), Linux 4.15-5.6 (92%)
```

**Accuracy:** VERY HIGH (software versions, vulnerabilities, OS)

---

### 5. Customization & Flexibility

#### Python Scanner: Unlimited Flexibility

**Example 1: Custom Port Order**
```python
# Randomize port order to avoid IDS detection
random.shuffle(port_range)
for port in port_range:
    scan_port(port)
```

**Example 2: Conditional Logic**
```python
# If port 21 open, immediately banner grab
if result == 0 and port == 21:
    grab_ftp_banner(target_host)
    check_anonymous_access()
```

**Example 3: Output to Custom Format**
```python
# Write JSON instead of plain text
json_output = {
    "target": target_host,
    "ports": [21, 80, 443],
    "timestamp": datetime.now(),
    "next_step": "enumerate_ftp"
}
with open('results.json', 'w') as f:
    json.dump(json_output, f)
```

**Example 4: Integration with Other Tools**
```python
# Pass open ports directly to Nmap for detailed scan
open_ports = [21, 80, 443]
port_list = ','.join(map(str, open_ports))
os.system(f"nmap -sV -p {port_list} {target_host}")
```

**Flexibility:** UNLIMITED (you control everything)

---

#### Nmap: Predefined Options

**Limited to:**
- Pre-built scan types (-sS, -sT, -sU, -sX, etc.)
- Pre-written NSE scripts
- Pre-defined output formats (-oN, -oX, -oG)
- Pre-configured timing templates (-T0 to -T5)

**But:**
- Very robust for common use cases
- Extensive documentation
- Large NSE script library (600+ scripts)
- Mature, battle-tested tool

**Flexibility:** GOOD (covers 95% of scanning needs)

---

### 6. When to Use Each Tool

#### Use Python Scanner When:

✓ You need **custom logic** (conditional scanning)
✓ You want **stealthy, randomized** port sweeps
✓ You need **integration** with other Python tools
✓ You're **learning** network fundamentals
✓ Target environment **blocks** common Nmap signatures
✓ You need **simple, no-dependencies** scanning

**Example Scenario:**
```
"I need to scan ports 21, 80, 443 only on localhost
to test my firewall rules - Python scanner perfect"
```

---

#### Use Nmap When:

✓ You need **comprehensive** reconnaissance
✓ You want **software version detection** (-sV)
✓ You need **vulnerability confirmation** (NSE scripts)
✓ You're doing **professional** penetration testing
✓ You need **reliable, documented** results
✓ You want **fast scanning** of large ranges
✓ You need **OS detection** and fingerprinting

**Example Scenario:**
```
"I need to scan an entire network range (1-65535 ports),
detect software versions, and run NSE scripts
to find exploitable vulnerabilities - Nmap is best"
```

---

### 7. Attack Chain Integration

#### Recommended Workflow

```
WEEK 5: DISCOVERY PHASE
├─ Active Recon Tools (ping, traceroute, telnet, netcat)
│  └─ Goal: Confirm connectivity, basic service detection
│
├─ Python Scanner (focused, custom)
│  └─ Goal: Quick port sweep of well-known ports
│  └─ Advantage: Fast, customizable, less obvious
│
└─ Nmap SYN + NSE (comprehensive verification)
   └─ Goal: Confirm findings, detect vulnerabilities
   └─ Advantage: Detailed, reliable, professional

WEEK 6+: EXPLOITATION PHASE
├─ Use Nmap findings to prioritize targets
├─ Focus on highest-impact vulnerabilities
└─ Plan exploitation strategy
```

---

### 8. Real-World Decision Tree

```
START: Need to scan a target?

"Do I need software versions?"
├─ YES → Use Nmap (-sV)
└─ NO → Use Python (faster)

"Do I need vulnerability confirmation?"
├─ YES → Use Nmap (NSE scripts)
└─ NO → Use Python or quick Nmap

"Am I concerned about IDS detection?"
├─ YES → Use Python (randomized) or Nmap (-T1)
└─ NO → Use Nmap (default timing)

"Do I need custom automation?"
├─ YES → Use Python (as first pass)
└─ NO → Use Nmap (standalone)

"Is speed critical?"
├─ YES → Use Nmap SYN (faster)
└─ NO → Either tool works
```

---

## Summary: When Each Excels

### Python Scanner Excels At:
- Custom reconnaissance logic
- Learning network fundamentals
- Quick focused scans (10-20 ports)
- Stealthy, randomized sweeps
- Integration with Python workflows

### Nmap Excels At:
- Comprehensive network mapping
- Software version detection
- Vulnerability identification (NSE)
- Large scale scanning (1000+ ports)
- Professional assessments

### Best Practice:
**Combine both.** Use Python for initial, stealthy discovery. Use Nmap for deep, detailed verification.

---

## Code Quality Comparison

### Python Scanner - Production Ready
```python
✓ Multi-threading (4 concurrent)
✓ Error handling (OSError for service lookup)
✓ Timeout handling (1.5 second limit)
✓ Graceful exit (KeyboardInterrupt)
✓ Daemon threads (cleanup on exit)
✗ No output to file
✗ No resume capability
```

### Nmap - Enterprise Ready
```python
✓ Multiple output formats (-oX for XML, -oJ for JSON)
✓ Resume capability (--resume)
✓ Extensive logging
✓ Service detection
✓ Vulnerability detection
✓ OS fingerprinting
✓ Timing control
✓ Firewall evasion techniques
✓ Decoy options
```

---

## Conclusion

| Use Case | Recommended Tool | Reasoning |
|----------|---|---|
| Learning network scanning | Python | Understand fundamentals |
| Quick port sweep (10-100 ports) | Python | Speed + customization |
| Comprehensive assessment | Nmap | Depth + accuracy |
| Vulnerability detection | Nmap | NSE scripts essential |
| Stealthy reconnaissance | Python | Randomization easier |
| Professional pentesting | Nmap | Industry standard |
| Exploit development | Python | Integration with code |
| Red team engagement | Both | Python first, Nmap second |

**Week 5 Lesson:** Mastering both tools makes you a more effective Red Team operator than mastering just one.

---

**Status:** Week 5 Scanner Methodology | Understanding Trade-offs | Ready for Exploitation Phase
