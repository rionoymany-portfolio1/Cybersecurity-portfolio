# Resources: Week 3 - TryHackMe + Python Data Structures

---

## TryHackMe Resources

### Getting Started
- **TryHackMe Sign Up:** https://tryhackme.com/signup
- **TryHackMe Main:** https://tryhackme.com/
- **Network Fundamentals Module:** https://tryhackme.com/module/network-fundamentals

### Networking Topics to Learn (Find on TryHackMe)

Search TryHackMe for rooms covering these topics:

1. **Basic Networking Concepts** (30-45 min)
   - What is networking?
   - Client-server model
   - Network types
   
2. **Network Topologies & LAN** (45 min)
   - Local Area Networks (LAN)
   - DHCP basics
   - MAC addresses, ARP
   
3. **OSI Model** (1 hour)
   - 7 layers of networking
   - How data moves through layers
   - Each layer's responsibility
   
4. **Packets, Frames & Protocols** (45 min)
   - TCP vs UDP
   - Header structure
   - Payload understanding
   - Common ports
   
5. **Networking Tools** (1 hour)
   - Ping, traceroute, whois
   - DNS lookups
   - Basic network commands

### TryHackMe Tips
- **Do the labs:** Reading alone won't stick
- **Experiment:** Try modifying commands, see what breaks
- **Take notes:** Screenshot interesting findings
- **Join community:** Discord for questions
- **Track progress:** TryHackMe shows your completion %

### TryHackMe Time Commitment
- **Week 3 Goal:** Complete 2-3 networking rooms
- **Per room:** 1-2 hours (video + practice)
- **Total commitment:** 5-7 hours Week 3
- **Flexibility:** Rooms vary in length, choose ones that fit schedule

---

## Python Lists, Tuples, Dictionaries Documentation

### Official Python Docs
- **Lists:** https://docs.python.org/3/tutorial/datastructures.html#more-on-lists
- **Tuples:** https://docs.python.org/3/tutorial/datastructures.html#tuples-and-sequences
- **Dictionaries:** https://docs.python.org/3/tutorial/datastructures.html#dictionaries
- **Set Operations:** https://docs.python.org/3/tutorial/datastructures.html#sets

### Built-in Functions (Important)
- **len()** - Get length of collection
- **sorted()** - Create sorted copy
- **reversed()** - Reverse iteration
- **enumerate()** - Get index + value
- **zip()** - Combine multiple lists

### List Methods Reference
```python
list.append(x)      # Add to end
list.extend(list)   # Add multiple items
list.insert(i, x)   # Insert at position
list.remove(x)      # Remove first occurrence
list.pop([i])       # Remove and return item
list.clear()        # Remove all items
list.index(x)       # Find position
list.count(x)       # Count occurrences
list.sort()         # Sort in place
list.reverse()      # Reverse in place
list.copy()         # Shallow copy
```

### Dictionary Methods Reference
```python
dict.keys()         # Get all keys
dict.values()       # Get all values
dict.items()        # Get key-value pairs
dict.get(key, default)  # Get with default
dict.pop(key)       # Remove and return
dict.update(dict)   # Merge dictionaries
dict.clear()        # Remove all items
dict.copy()         # Shallow copy
```

---

## Learning Platforms

### Free Python Resources
- **W3Schools Python:** https://www.w3schools.com/python/
  - Lists: https://www.w3schools.com/python/python_lists.asp
  - Tuples: https://www.w3schools.com/python/python_tuples.asp
  - Dictionaries: https://www.w3schools.com/python/python_dictionaries.asp
  
- **Real Python:** https://realpython.com/
  - List article: https://realpython.com/list-manipulation-python/
  - Dicts article: https://realpython.com/python-dicts/
  
- **Python Official Tutorial:** https://docs.python.org/3/tutorial/

### Interactive Coding
- **Codecademy:** https://www.codecademy.com/learn/learn-python
  - Data structures modules
  - Immediate feedback
  
- **LeetCode Easy:** https://leetcode.com/
  - Practice with lists/dicts
  - Some free problems

---

## Red Team Specific Resources

### Security Data Structures
- **OWASP Data Storage:** https://owasp.org/www-community/attacks/Manipulating_User-Supplied_Data
- **Credential Storage:** https://cheatsheetseries.owasp.org/cheatsheets/Credential_Storage_Cheat_Sheet.html
- **JSON/YAML for configs:** Understand data format for scripts

### Reconnaissance Best Practices
- **Nmap output parsing** (Week 4+)
- **Organizing scan results** (Week 3 focus)
- **Credential management** (Week 3 focus)
- **Building reconnaissance databases** (Advanced)

---

## Networking Fundamentals References

### Networking Concepts (TryHackMe + Background)
- **IP Addresses:** 4 octets, 192.168.x.x for private networks
- **Ports:** 0-65535 range, <1024 = privileged, common: 22, 80, 443, 3306
- **Protocols:** TCP (reliable), UDP (fast), ICMP (ping)
- **OSI Model:** 7 layers from physical to application
- **DNS:** Domain → IP translation

### Networking Tools (Hands-On)
```bash
# Ping - test connectivity
ping 192.168.1.1

# Traceroute - trace path
traceroute 8.8.8.8

# Nslookup - DNS lookup
nslookup example.com

# Netstat - network statistics
netstat -an

# Whois - domain information
whois example.com
```

### Packet Analysis
- **Wireshark:** https://www.wireshark.org/
  - Packet sniffer
  - Visual network analysis
  - (Install but don't need Week 3)

---

## Cheat Sheets

### Python Data Structures Quick Reference

**Lists:**
```python
# Create
my_list = [1, 2, 3]
empty_list = []

# Access
my_list[0]      # First item
my_list[-1]     # Last item
my_list[1:3]    # Slice

# Modify
my_list.append(4)
my_list.remove(2)
my_list[0] = 10

# Iterate
for item in my_list:
    print(item)
```

**Tuples:**
```python
# Create (immutable)
my_tuple = (1, 2, 3)
single = (1,)       # Note comma!

# Access (same as list)
my_tuple[0]
my_tuple[1:2]

# Unpack
x, y, z = my_tuple

# Convert
list(my_tuple)
tuple(my_list)
```

**Dictionaries:**
```python
# Create
my_dict = {"key": "value", "port": 22}
empty_dict = {}

# Access
my_dict["key"]
my_dict.get("key", "default")

# Modify
my_dict["new_key"] = "new_value"
my_dict.update({"key2": "value2"})

# Iterate
for key in my_dict:          # Keys only
    print(key)

for key, value in my_dict.items():  # Key-value pairs
    print(f"{key}: {value}")

for value in my_dict.values():  # Values only
    print(value)
```

### Common Mistakes (Learn from these!)

**Mistake 1: Forgetting tuple comma**
```python
 WRONG:
single = (42)      # This is just 42 (int)

 CORRECT:
single = (42,)     # This is tuple with one element
```

**Mistake 2: Dictionary key error**
```python
 WRONG:
targets = {"192.168.1.1": "web-server"}
print(targets["192.168.1.2"])  # KeyError!

 CORRECT:
print(targets.get("192.168.1.2", "not found"))  # Safe
```

**Mistake 3: Modifying list while iterating**
```python
 PROBLEMATIC:
targets = ["192.168.1.1", "192.168.1.2", "192.168.1.3"]
for target in targets:
    if target == "192.168.1.2":
        targets.remove(target)  # Skips elements!

 BETTER:
targets = [t for t in targets if t != "192.168.1.2"]
```

**Mistake 4: Sharing mutable default (dicts/lists)**
```python
 PROBLEMATIC:
def scan_target(target, results=[]):  # Shared!
    results.append(target)
    return results

 PROBLEMATIC:
def store_data(data, cache={}):  # Shared!
    cache.update(data)
    return cache

 CORRECT:
def scan_target(target, results=None):
    if results is None:
        results = []
    results.append(target)
    return results
```

---

## Week 3 Study Schedule

### Monday
- Create TryHackMe account
- Start Pre-Security path intro
- Read Exercise 1.1-1.4 (Lists)

### Tuesday
- Complete TryHackMe "What is Networking"
- Complete TryHackMe "Intro to LAN"
- Practice Exercise 1.1-1.4 (write 3 list programs)

### Wednesday
- Complete TryHackMe "OSI Model"
- Complete TryHackMe "Packets & Frames"
- Practice Exercise 2.1-2.2 (tuples)

### Thursday
- Complete TryHackMe "Networking Tools"
- Practice Exercise 3.1-3.4 (dictionaries)
- Combine all data structures (Exercise 4.1-4.2)

### Friday
- Challenge: Build reconnaissance database
- Test all code with different inputs
- Write 6-part write-up

### Saturday
- Polish code and documentation
- Business impact analysis
- Review everything

### Sunday
- Commit to GitHub (week-03 folder)
- Reflect on TryHackMe learning
- Plan Week 4

---

## Integration Tips

### Applying TryHackMe + Python Together

**TryHackMe teaches:** Network basics (IPs, ports, protocols, OSI model)

**Python applies:** Store and organize what you learn

**Example workflow:**
1. TryHackMe: "Port 22 is SSH"
2. Python: `services = {22: "SSH", 80: "HTTP", ...}`
3. TryHackMe: "Scan target 192.168.1.1"
4. Python: `targets = [{"ip": "192.168.1.1", "ports": [22, 80]}]`
5. TryHackMe: "Learned 5 networking concepts"
6. Python: Store all 5 in organized dictionary

---

## Tools for Week 3

### Required
- Python 3.8+ (already have from Week 2)
- Code editor (VS Code or PyCharm)
- Internet connection (TryHackMe)

### Optional but Helpful
- Wireshark (packet analyzer, optional)
- Nmap (network mapper, install Week 4)
- Kali Linux VM (optional, use Windows/Mac fine)

### Installation
TryHackMe provides VMs in browser - no download needed!

---

## Next Week Preview

### Week 4 (Your planning needed)
- What will you focus on?
- Continue TryHackMe?
- More Python?
- Start actual exploitation?

**Likely progression:**
- Week 4: More TryHackMe + Python Functions
- Week 5: Web exploitation basics
- Week 6: Network scanning with Python
- Week 7: Privilege escalation introduction

---

## Resources Summary

 **TryHackMe:** Main platform (free + paid options)
 **Python Docs:** Official reference
 **W3Schools/Real Python:** Tutorials
 **Lab Guide:** This week's exercises
 **Write-Up:** Business context for learning

**Most important:** Do the TryHackMe labs! Watching ≠ understanding.

---

**Resources Updated:** Week 3 | TryHackMe + Python Data Structures  
**Next Review:** After Week 3 completion
