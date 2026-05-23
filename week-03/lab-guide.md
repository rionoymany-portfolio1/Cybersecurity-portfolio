# Lab Guide: Python Data Structures - Week 3

---

## Part 1: Lists - Ordered, Mutable Collections

### Exercise 1.1: Creating and Accessing Lists

**Objective:** Work with list basics

**Task:**
```python
# Create lists
target_ips = ["192.168.1.1", "192.168.1.2", "192.168.1.3"]
open_ports = [22, 80, 443, 3306]
services = ["SSH", "HTTP", "HTTPS", "MySQL"]

# Access by index
print(target_ips[0])        # First IP: 192.168.1.1
print(target_ips[-1])       # Last IP: 192.168.1.3
print(open_ports[1:3])      # Slice: [80, 443]

# Check length
print(f"Targets: {len(target_ips)}")
print(f"Open ports: {len(open_ports)}")

# Check if item in list
if 22 in open_ports:
    print("[+] SSH port found")

# Find index
ssh_index = open_ports.index(22)
print(f"SSH is at index {ssh_index}")
```

**Expected Output:**
```
192.168.1.1
192.168.1.3
[80, 443]
Targets: 3
Open ports: 4
[+] SSH port found
SSH is at index 0
```

---

### Exercise 1.2: List Methods - Adding and Removing

**Objective:** Modify lists dynamically

**Task:**
```python
# Create initial list
discovered_hosts = ["192.168.1.1", "192.168.1.2"]

# Add items
discovered_hosts.append("192.168.1.3")
discovered_hosts.extend(["192.168.1.4", "192.168.1.5"])
discovered_hosts.insert(1, "192.168.1.99")  # Insert at position 1

print("After additions:", discovered_hosts)

# Remove items
discovered_hosts.remove("192.168.1.99")     # Remove by value
print("After remove:", discovered_hosts)

# Pop (remove and get value)
last_host = discovered_hosts.pop()
print(f"Removed: {last_host}")
print("After pop:", discovered_hosts)

# Clear entire list
backup = discovered_hosts.copy()  # Make backup first!
discovered_hosts.clear()
print("After clear:", discovered_hosts)
print("Backup:", backup)
```

**Expected Output:**
```
After additions: ['192.168.1.1', '192.168.1.99', '192.168.1.2', '192.168.1.3', '192.168.1.4', '192.168.1.5']
After remove: ['192.168.1.1', '192.168.1.2', '192.168.1.3', '192.168.1.4', '192.168.1.5']
Removed: 192.168.1.5
After pop: ['192.168.1.1', '192.168.1.2', '192.168.1.3', '192.168.1.4']
After clear: []
Backup: ['192.168.1.1', '192.168.1.2', '192.168.1.3', '192.168.1.4']
```

---

### Exercise 1.3: List Operations - Sorting and Sorting

**Objective:** Organize list data

**Task:**
```python
# Unsorted ports
ports = [443, 22, 80, 3306, 22, 80, 443]

# Sort
ports.sort()
print("Sorted:", ports)

# Sort descending
ports.sort(reverse=True)
print("Reverse:", ports)

# Count duplicates
print(f"Port 22 appears {ports.count(22)} times")
print(f"Port 443 appears {ports.count(443)} times")

# Remove duplicates (convert to set)
unique_ports = list(set(ports))
print("Unique ports:", sorted(unique_ports))

# Reverse order
targets = ["192.168.1.1", "192.168.1.2", "192.168.1.3"]
targets.reverse()
print("Reversed targets:", targets)
```

**Expected Output:**
```
Sorted: [22, 22, 80, 80, 443, 443, 3306]
Reverse: [3306, 443, 443, 80, 80, 22, 22]
Port 22 appears 2 times
Port 443 appears 2 times
Unique ports: [22, 80, 443, 3306]
Reversed targets: ['192.168.1.3', '192.168.1.2', '192.168.1.1']
```

---

### Exercise 1.4: List Comprehension (Filtering)

**Objective:** Create filtered lists efficiently

**Task:**
```python
# Original data
all_ports = [20, 21, 22, 23, 25, 53, 80, 443, 3306, 5432]

# Filter common ports (simple comprehension)
common_ports = [p for p in all_ports if p in [22, 80, 443]]
print("Common ports:", common_ports)

# Filter ports > 100
high_ports = [p for p in all_ports if p > 100]
print("Ports > 100:", high_ports)

# Transform during filtering
ports_with_names = [f"{p}/tcp" for p in [22, 80, 443]]
print("With protocol:", ports_with_names)

# Nested filtering
services = ["SSH", "HTTP", "HTTPS", "MySQL", "PostgreSQL"]
interesting = [s for s in services if len(s) > 4]
print("Long service names:", interesting)
```

**Expected Output:**
```
Common ports: [22, 80, 443]
Ports > 100: [443, 3306, 5432]
With protocol: ['22/tcp', '80/tcp', '443/tcp']
Long service names: ['HTTPS', 'MySQL', 'PostgreSQL']
```

---

## Part 2: Tuples - Immutable Collections

### Exercise 2.1: Creating and Using Tuples

**Objective:** Understand immutable data

**Task:**
```python
# Create tuples
scan_result = ("192.168.1.1", 22, "SSH", "OpenSSH_7.4")
location = (40.7128, -74.0060)  # Latitude, Longitude (example)
version = (1, 2, 3)  # Version number

# Access by index
print(f"IP: {scan_result[0]}")
print(f"Port: {scan_result[1]}")
print(f"Service: {scan_result[2]}")

# Unpacking
ip, port, service, version = scan_result
print(f"\nUnpacked: {ip}:{port} -> {service} {version}")

# Tuples in sets (can't use lists in sets!)
scanned_services = {
    ("192.168.1.1", 22, "SSH"),
    ("192.168.1.2", 3306, "MySQL"),
    ("192.168.1.1", 22, "SSH")  # Duplicate
}
print(f"\nScanned services (set): {scanned_services}")
print(f"Unique scans: {len(scanned_services)}")

# Try to modify (will error)
try:
    scan_result[1] = 23  # Try to change port
except TypeError as e:
    print(f"\nError (expected): {e}")
```

**Expected Output:**
```
IP: 192.168.1.1
Port: 22
Service: SSH

Unpacked: 192.168.1.1:22 -> SSH OpenSSH_7.4

Scanned services (set): {('192.168.1.1', 22, 'SSH'), ('192.168.1.2', 3306, 'MySQL')}
Unique scans: 2

Error (expected): 'tuple' object does not support item assignment
```

---

### Exercise 2.2: Tuple Operations

**Objective:** Work with tuple data

**Task:**
```python
# Combine tuples
scan1 = ("192.168.1.1", 22)
scan2 = ("SSH", "OpenSSH_7.4")
full_result = scan1 + scan2
print("Combined:", full_result)

# Repeat tuples
pattern = ("192.168.1.", 10)
repeated = pattern * 3
print("Repeated:", repeated)

# Get tuple info
result = ("192.168.1.1", 22, "SSH", "OpenSSH")
print(f"Length: {len(result)}")
print(f"Index of 'SSH': {result.index('SSH')}")
print(f"Count of 'SSH': {result.count('SSH')}")

# Convert to/from list
ports_list = [22, 80, 443]
ports_tuple = tuple(ports_list)
print(f"Tuple from list: {ports_tuple}")

back_to_list = list(ports_tuple)
print(f"List from tuple: {back_to_list}")
```

**Expected Output:**
```
Combined: ('192.168.1.1', 22, 'SSH', 'OpenSSH_7.4')
Repeated: ('192.168.1.', 10, '192.168.1.', 10, '192.168.1.', 10)
Length: 4
Index of 'SSH': 2
Count of 'SSH': 1
Tuple from list: (22, 80, 443)
List from tuple: [22, 80, 443]
```

---

## Part 3: Dictionaries - Key-Value Pairs

### Exercise 3.1: Creating and Accessing Dictionaries

**Objective:** Store related information together

**Task:**
```python
# Create dictionary (target information)
target = {
    "ip": "192.168.1.1",
    "hostname": "web-server",
    "ports": [22, 80, 443],
    "services": ["SSH", "HTTP", "HTTPS"],
    "os": "Linux",
    "vulnerable": True
}

# Access by key
print(f"IP: {target['ip']}")
print(f"Ports: {target['ports']}")
print(f"OS: {target['os']}")

# Get with default
user = target.get('user', 'unknown')  # Returns 'unknown' if not found
print(f"User: {user}")

# Check if key exists
if 'vulnerable' in target:
    print(f"Vulnerability status: {target['vulnerable']}")

# Get all keys
print(f"\nAll keys: {list(target.keys())}")

# Get all values
print(f"All values: {list(target.values())}")

# Iterate
print("\nIterating:")
for key, value in target.items():
    print(f"  {key}: {value}")
```

**Expected Output:**
```
IP: 192.168.1.1
Ports: [22, 80, 443]
OS: Linux
User: unknown
Vulnerability status: True

All keys: ['ip', 'hostname', 'ports', 'services', 'os', 'vulnerable']
All values: ['192.168.1.1', 'web-server', [22, 80, 443], ['SSH', 'HTTP', 'HTTPS'], 'Linux', True]

Iterating:
  ip: 192.168.1.1
  hostname: web-server
  ports: [22, 80, 443]
  services: ['SSH', 'HTTP', 'HTTPS']
  os: Linux
  vulnerable: True
```

---

### Exercise 3.2: Modifying Dictionaries

**Objective:** Update dictionary data

**Task:**
```python
# Create credentials dictionary
credentials = {
    "admin": "password123",
    "root": "toor"
}

# Add new credential
credentials["user"] = "user123"
credentials.update({"guest": "guest"})
print("After additions:", credentials)

# Modify existing
credentials["admin"] = "newpassword456"
print("After modification:", credentials)

# Remove
del credentials["guest"]  # Delete specific key
print("After del:", credentials)

removed_value = credentials.pop("root")  # Remove and get value
print(f"Removed 'root': {removed_value}")
print("After pop:", credentials)

# Clear all
backup = credentials.copy()
credentials.clear()
print("After clear:", credentials)
print("Backup:", backup)
```

**Expected Output:**
```
After additions: {'admin': 'password123', 'root': 'toor', 'user': 'user123', 'guest': 'guest'}
After modification: {'admin': 'newpassword456', 'root': 'toor', 'user': 'user123', 'guest': 'guest'}
After del: {'admin': 'newpassword456', 'root': 'toor', 'user': 'user123'}
Removed 'root': toor
After pop: {'admin': 'newpassword456', 'user': 'user123'}
After clear: {}
Backup: {'admin': 'newpassword456', 'user': 'user123'}
```

---

### Exercise 3.3: Nested Dictionaries (Complex Structures)

**Objective:** Store hierarchical data (most useful for Red Team)

**Task:**
```python
# Reconnaissance database
network = {
    "192.168.1.1": {
        "hostname": "web-server",
        "ports": {
            22: "SSH",
            80: "HTTP",
            443: "HTTPS"
        },
        "credentials": ["admin:pass123", "root:toor"],
        "vulnerable": True
    },
    "192.168.1.2": {
        "hostname": "db-server",
        "ports": {
            3306: "MySQL",
            5432: "PostgreSQL"
        },
        "credentials": [],
        "vulnerable": False
    },
    "192.168.1.3": {
        "hostname": "dns-server",
        "ports": {
            53: "DNS"
        },
        "credentials": ["admin:admin123"],
        "vulnerable": True
    }
}

# Access nested data
print(f"Web server: {network['192.168.1.1']['hostname']}")
print(f"Web server SSH port: {network['192.168.1.1']['ports'][22]}")
print(f"Web server creds: {network['192.168.1.1']['credentials']}")

# Find vulnerable targets
print("\nVulnerable targets:")
for ip, data in network.items():
    if data['vulnerable']:
        print(f"  [{ip}] {data['hostname']} - Ports: {list(data['ports'].keys())}")

# Add new target
network["192.168.1.4"] = {
    "hostname": "mail-server",
    "ports": {25: "SMTP", 143: "IMAP"},
    "credentials": [],
    "vulnerable": False
}

print(f"\nTotal targets: {len(network)}")
```

**Expected Output:**
```
Web server: web-server
Web server SSH port: SSH
Web server creds: ['admin:pass123', 'root:toor']

Vulnerable targets:
  [192.168.1.1] web-server - Ports: [22, 80, 443]
  [192.168.1.3] dns-server - Ports: [53]

Total targets: 4
```

---

### Exercise 3.4: Dictionary Comprehension (Building from data)

**Objective:** Create dictionaries efficiently

**Task:**
```python
# Create port-to-service mapping
ports = [22, 80, 443, 3306, 5432]
services = ["SSH", "HTTP", "HTTPS", "MySQL", "PostgreSQL"]

# Dictionary comprehension
port_map = {port: service for port, service in zip(ports, services)}
print("Port mapping:", port_map)

# From lists
ips = ["192.168.1.1", "192.168.1.2", "192.168.1.3"]
targets = {ip: {"scanned": False, "ports": []} for ip in ips}
print("\nTarget template:", targets)

# Filter during creation
all_ports = [20, 21, 22, 23, 80, 443, 3306]
common_ports = {p: "common" for p in all_ports if p in [22, 80, 443]}
print("\nCommon ports dict:", common_ports)

# Transform keys/values
port_strings = {f"port_{p}": str(p) for p in [22, 80, 443]}
print("\nWith prefixes:", port_strings)
```

**Expected Output:**
```
Port mapping: {22: 'SSH', 80: 'HTTP', 443: 'HTTPS', 3306: 'MySQL', 5432: 'PostgreSQL'}

Target template: {'192.168.1.1': {'scanned': False, 'ports': []}, '192.168.1.2': {'scanned': False, 'ports': []}, '192.168.1.3': {'scanned': False, 'ports': []}}

Common ports dict: {22: 'common', 80: 'common', 443: 'common'}

With prefixes: {'port_22': '22', 'port_80': '80', 'port_443': '443'}
```

---

## Part 4: Combining Data Structures

### Exercise 4.1: Lists of Dictionaries (Common pattern)

**Objective:** Store multiple items with related data

**Task:**
```python
# List of target dictionaries
targets = [
    {
        "ip": "192.168.1.1",
        "hostname": "web-server",
        "status": "online",
        "open_ports": [80, 443]
    },
    {
        "ip": "192.168.1.2",
        "hostname": "db-server",
        "status": "online",
        "open_ports": [3306]
    },
    {
        "ip": "192.168.1.3",
        "hostname": "dns-server",
        "status": "offline",
        "open_ports": []
    }
]

# Access specific target
print(f"First target: {targets[0]['hostname']}")

# Loop through targets
print("\nOnline targets:")
for target in targets:
    if target['status'] == 'online':
        print(f"  {target['ip']} ({target['hostname']}) - Ports: {target['open_ports']}")

# Find target by IP
target_ip = "192.168.1.2"
for target in targets:
    if target['ip'] == target_ip:
        print(f"\nFound: {target['hostname']} on {target['ip']}")
        break

# Add new target
targets.append({
    "ip": "192.168.1.4",
    "hostname": "mail-server",
    "status": "online",
    "open_ports": [25, 143]
})

print(f"\nTotal targets: {len(targets)}")
```

**Expected Output:**
```
First target: web-server

Online targets:
  192.168.1.1 (web-server) - Ports: [80, 443]
  192.168.1.2 (db-server) - Ports: [3306]

Found: db-server on 192.168.1.2

Total targets: 4
```

---

### Exercise 4.2: Dictionary of Lists (Grouping)

**Objective:** Organize related items by category

**Task:**
```python
# Group services by target
services_by_host = {
    "web-server": ["HTTP", "HTTPS", "SSH"],
    "db-server": ["MySQL", "PostgreSQL", "SSH"],
    "dns-server": ["DNS"],
    "mail-server": ["SMTP", "IMAP", "POP3"]
}

# Find hosts with specific service
service_to_find = "SSH"
print(f"Hosts with {service_to_find}:")
for host, services in services_by_host.items():
    if service_to_find in services:
        print(f"  {host}: {services}")

# Add service to host
services_by_host["db-server"].append("Redis")
print(f"\ndb-server services: {services_by_host['db-server']}")

# Count services per host
print("\nService counts:")
for host, services in services_by_host.items():
    print(f"  {host}: {len(services)} services")

# Get all unique services
all_services = set()
for services_list in services_by_host.values():
    all_services.update(services_list)
print(f"\nUnique services found: {sorted(all_services)}")
```

**Expected Output:**
```
Hosts with SSH:
  web-server: ['HTTP', 'HTTPS', 'SSH']
  db-server: ['MySQL', 'PostgreSQL', 'SSH']

db-server services: ['MySQL', 'PostgreSQL', 'SSH', 'Redis']

Service counts:
  web-server: 3 services
  db-server: 4 services
  dns-server: 1 services
  mail-server: 3 services

Unique services found: ['DNS', 'HTTP', 'HTTPS', 'IMAP', 'MySQL', 'POP3', 'PostgreSQL', 'SMTP', 'SSH', 'Redis']
```

---

## Challenge Exercise: Red Team Reconnaissance Database

**Build a reconnaissance data structure**

```python
# Week 3 Challenge: Network Reconnaissance Database

reconnaissance = {
    "targets": [
        {
            "ip": "192.168.1.1",
            "hostname": "web-prod",
            "open_ports": {
                22: "SSH",
                80: "HTTP",
                443: "HTTPS"
            },
            "found_credentials": [
                ("admin", "password123"),
                ("www-data", "webpass")
            ],
            "vulnerability": "OpenSSH 7.4 (CVE-2018-15473)"
        },
        {
            "ip": "192.168.1.2",
            "hostname": "db-prod",
            "open_ports": {
                3306: "MySQL",
                22: "SSH"
            },
            "found_credentials": [
                ("root", "rootpass"),
                ("app_user", "apppass123")
            ],
            "vulnerability": "MySQL 5.7 (default credentials)"
        },
        {
            "ip": "192.168.1.3",
            "hostname": "dns-prod",
            "open_ports": {
                53: "DNS"
            },
            "found_credentials": [],
            "vulnerability": None
        }
    ]
}

# Analysis
print("=" * 50)
print("RECONNAISSANCE SUMMARY")
print("=" * 50)

for target in reconnaissance['targets']:
    print(f"\n[*] {target['hostname']} ({target['ip']})")
    print(f"    Open ports: {list(target['open_ports'].keys())}")
    print(f"    Credentials found: {len(target['found_credentials'])}")
    if target['found_credentials']:
        for username, password in target['found_credentials']:
            print(f"      - {username}:{password}")
    if target['vulnerability']:
        print(f"    Vulnerability: {target['vulnerability']}")
    else:
        print(f"    Vulnerability: None detected")

# Find targets with credentials
print("\n" + "=" * 50)
print("TARGETS WITH CREDENTIALS:")
print("=" * 50)
for target in reconnaissance['targets']:
    if target['found_credentials']:
        print(f"{target['hostname']}: {len(target['found_credentials'])} credentials")

# List all vulnerabilities
print("\n" + "=" * 50)
print("VULNERABILITIES:")
print("=" * 50)
for target in reconnaissance['targets']:
    if target['vulnerability']:
        print(f"{target['hostname']}: {target['vulnerability']}")
```

---

## Your Assignment: Write These 4 Programs

**Due by end of Week 3:**

1. **lists-basics.py** - Create, access, modify lists
2. **tuples.py** - Create tuples, understand immutability
3. **dictionaries.py** - Create dicts, nested structures
4. **combined-program.py** - Use lists + dicts + tuples together

**Challenge:** Add the reconnaissance database program to your code examples

---

## TryHackMe Integration

**As you complete TryHackMe modules, practice:**
- Parse TryHackMe output using lists/dicts
- Store network information (IPs, ports, services) in structured format
- Use data structures to organize findings

---

**Status:** Lab Guide Complete | Ready for Week 3 Practice
