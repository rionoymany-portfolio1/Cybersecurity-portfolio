# Week 3: TryHackMe Pre-Security + Python Data Structures

> **Real Platform Learning + Python Collections**

---

##  Topics Covered This Week

### Part 1: TryHackMe Pre-Security Path
- Account creation and profile setup
- Pre-Security learning path introduction
- Networking Fundamentals module:
  - What is Networking?
  - Intro to LAN
  - Networking tools (ping, traceroute, whois)
  - OSI model basics
  - Understanding packets

### Part 2: Python Data Structures
- Lists: creation, indexing, slicing, methods
- Tuples: immutable sequences, unpacking
- Dictionaries: key-value pairs, nested structures
- When to use each data structure
- Working with collections in Red Team context

---

##  Learning Objectives

**By end of Week 3, you will:**
-  Have TryHackMe account with Pre-Security path started
-  Understand networking fundamentals (packets, IP, DNS)
-  Be comfortable with Python lists, tuples, and dictionaries
-  Know when/how to use each data structure
-  Apply collections to Red Team scenarios (storing targets, credentials, results)

---

##  Why This Matters for Red Team

**TryHackMe Connection:**
- Pre-Security path = foundation for Red Team work
- Networking fundamentals = understand what you're attacking
- Hands-on labs = practice in safe environment
- TryHackMe reputation = industry-recognized credential

**Python Collections Connection:**
| Data Structure | Red Team Use |
|---|---|
| **Lists** | Store targets, ports, discovered hosts, results |
| **Tuples** | Immutable data (coordinates, fixed results) |
| **Dictionaries** | Store credentials (user:pass), service:port mappings |

**Example:** Reconnaissance automation
```python
# Week 2 (basic loop)
for target in ["192.168.1.1", "192.168.1.2"]:
    print(f"Target: {target}")

# Week 3 (with data structures)
targets = {
    "web_server": {"ip": "192.168.1.1", "ports": [80, 443]},
    "db_server": {"ip": "192.168.1.2", "ports": [3306, 5432]}
}
for server_name, details in targets.items():
    print(f"[*] {server_name}: {details['ip']} ports {details['ports']}")
```

---

##  Weekly Schedule

| Day | Focus | Deliverable |
|-----|-------|-------------|
| **Mon-Tue** | TryHackMe signup + Pre-Security intro | Complete Pre-Security intro room |
| **Tue-Wed** | Networking Fundamentals path | Complete 5 Networking modules |
| **Wed-Thu** | Python Lists, Tuples, Dicts | Write 6 Python programs |
| **Thu** | Integrate TryHackMe learning + Python | Combined practical script |
| **Fri** | Write 6-part write-up | Complete analysis |
| **Sat** | Business impact analysis | Executive brief |
| **Sun** | Commit to GitHub | week-03 folder live |

---

##  TryHackMe Learning

### Network Fundamentals Module
- **Start:** https://tryhackme.com/module/network-fundamentals
- **Expected time:** 5-7 hours
- **Week 3 focus:** Complete this module's rooms
- **Types:** Mix of video + hands-on labs

### Networking Fundamentals (Priority This Week)
1. **What is Networking?** (30 min)
   - Definitions, client-server model, network types

2. **Intro to LAN** (45 min)
   - Local Area Network concepts
   - DHCP, MAC addresses, ARP

3. **OSI Model** (1 hour)
   - 7 layers of networking
   - Each layer's role in communication

4. **Packets & Frames** (45 min)
   - How data travels
   - Headers and payloads
   - TCP/UDP basics

5. **Networking Tools** (1 hour)
   - Ping, traceroute, whois
   - DNS lookups
   - Netstat basics

---

##  Python Data Structures

### Lists
- Ordered, mutable collections
- Access by index
- Methods: append, remove, pop, sort, reverse

### Tuples
- Ordered, immutable collections
- More memory efficient
- Can be dictionary keys
- Unpacking syntax

### Dictionaries
- Unordered (Python 3.7+: ordered), mutable
- Key-value pairs
- Fast lookups by key
- Nested structures possible

---

##  What's Included in week-03/

```
week-03/
├── README.md (this file)
├── write-up.md (6-part framework)
├── business-impact-analysis.md
├── lab-guide.md
├── resources.md
└── code-examples/
    ├── 01-lists-basics.py
    ├── 02-lists-methods.py
    ├── 03-tuples.py
    ├── 04-dictionaries.py
    ├── 05-nested-structures.py
    └── 06-combined-program.py
```

---

##  Next Steps

1. **Create TryHackMe account:** https://tryhackme.com/signup
2. **Start Pre-Security path**
3. **Work through Networking Fundamentals** (estimate: 3-4 hours this week)
4. **Study lab-guide.md** for Python collections
5. **Write code examples** and test them
6. **Complete 6-part write-up**

---

**Status:** Week 3 | TryHackMe + Python Data Structures | In Progress
