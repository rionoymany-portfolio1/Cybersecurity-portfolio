# Lab Guide: Python Fundamentals - Week 2

---

## Part 1: Variables, Print, Input, String Operations

### Exercise 1.1: Variables and Print

**Objective:** Understand variable declaration and different data types

**Task:**
```python
# Create variables with different data types
name = "Rio"
age = 14
height = 5.7
is_student = True

# Print each variable
print(name)
print(age)
print(height)
print(is_student)

# Print with formatting
print(f"Name: {name}, Age: {age}")
print(f"Height: {height} feet, Student: {is_student}")
```

**Expected Output:**
```
Rio
14
5.7
True
Name: Rio, Age: 14
Height: 5.7 feet, Student: True
```

**What You Learned:**
- Variables store data
- f-strings format output nicely
- Different data types: str, int, float, bool

---

### Exercise 1.2: User Input

**Objective:** Get input from user and use it in program

**Task:**
```python
# Get user input
username = input("Enter your username: ")
password = input("Enter your password: ")
target_ip = input("Enter target IP address: ")

# Use the input
print(f"Username: {username}")
print(f"Target: {target_ip}")

# Type conversion
port = int(input("Enter port number: "))
print(f"Checking port: {port}")
print(f"Port type is: {type(port)}")  # Should be <class 'int'>
```

**Expected Interaction:**
```
Enter your username: admin
Enter your password: secret123
Enter target IP address: 192.168.1.1
Username: admin
Target: 192.168.1.1
Enter port number: 22
Checking port: 22
Port type is: <class 'int'>
```

**What You Learned:**
- `input()` gets user data
- Data from input() is string by default
- `int()` converts string to integer
- `type()` shows variable type

---

### Exercise 1.3: String Operations

**Objective:** Manipulate strings (useful for parsing attacker output)

**Task:**
```python
# String methods
command_output = "SSH-2.0-OpenSSH_7.4"
log_line = "  192.168.1.1  authentication  failed  "

# String methods
print(command_output.lower())  # Lowercase
print(command_output.upper())  # Uppercase
print(log_line.strip())        # Remove whitespace
print(log_line.split())        # Split into words

# String slicing
print(command_output[0:3])     # First 3 characters: "SSH"
print(command_output[-3:])     # Last 3 characters: "7.4"

# String replacement
nmap_output = "80/tcp open http"
port = nmap_output.replace("/tcp open http", "")
print(f"Port found: {port}")

# Finding substrings
if "OpenSSH" in command_output:
    print("[+] OpenSSH detected")
```

**Expected Output:**
```
ssh-2.0-openssh_7.4
SSH-2.0-OPENSSH_7.4
192.168.1.1 authentication failed
['192.168.1.1', 'authentication', 'failed']
SSH
7.4
Port found: 80
[+] OpenSSH detected
```

**What You Learned:**
- `.lower()`, `.upper()` change case
- `.strip()` removes whitespace
- `.split()` breaks string into list
- String slicing: `string[start:end]`
- `.replace()` changes text
- `in` checks if substring exists

---

### Exercise 1.4: List Operations (String Collections)

**Objective:** Work with lists of strings (ports, IPs, credentials)

**Task:**
```python
# Create lists
target_ips = ["192.168.1.1", "192.168.1.2", "192.168.1.3"]
ports = [22, 80, 443, 3306]
usernames = ["admin", "root", "user"]

# Access list items
print(target_ips[0])    # First IP
print(ports[-1])        # Last port (443)

# List length
print(f"Targets: {len(target_ips)}")
print(f"Ports: {len(ports)}")

# Add to list
target_ips.append("192.168.1.4")
print(target_ips)

# Check if item in list
if 22 in ports:
    print("[+] SSH port found")
```

**Expected Output:**
```
192.168.1.1
3306
Targets: 3
Ports: 4
['192.168.1.1', '192.168.1.2', '192.168.1.3', '192.168.1.4']
[+] SSH port found
```

**What You Learned:**
- Lists store multiple values
- Access with `[index]` (0-based)
- `.append()` adds items
- `in` checks if item exists
- `len()` counts items

---

## Part 2: Conditional Logic (If/Else/Elif)

### Exercise 2.1: Basic If/Else

**Objective:** Make decisions based on conditions

**Task:**
```python
# Simple if/else
port = 22

if port == 22:
    print("[+] SSH port detected")
else:
    print("[-] Not SSH port")

# Compare ports
port_status = "open"

if port_status == "open":
    print("[+] Port is accessible")
else:
    print("[-] Port is closed")

# Numeric comparison
response_time = 2.5

if response_time < 1:
    print("[+] Server is fast")
else:
    print("[-] Server might be slow")
```

**Expected Output:**
```
[+] SSH port detected
[+] Port is accessible
[-] Server might be slow
```

**What You Learned:**
- `if condition:` executes if True
- `else:` executes if False
- Comparison operators: `==`, `!=`, `<`, `>`, `<=`, `>=`

---

### Exercise 2.2: If/Elif/Else (Multiple Conditions)

**Objective:** Handle multiple decision paths

**Task:**
```python
# Port identification
port = int(input("Enter port number: "))

if port == 22:
    print("[+] SSH detected")
elif port == 80:
    print("[+] HTTP detected")
elif port == 443:
    print("[+] HTTPS detected")
elif port == 3306:
    print("[+] MySQL detected")
else:
    print("[-] Unknown service")

# Service status assessment
cpu_usage = 85

if cpu_usage > 90:
    print("[!] CRITICAL - CPU overloaded")
elif cpu_usage > 75:
    print("[!] WARNING - CPU high")
elif cpu_usage > 50:
    print("[*] NOTICE - CPU moderate")
else:
    print("[+] CPU normal")
```

**Expected Interaction:**
```
Enter port number: 443
[+] HTTPS detected

# Then run again with:
Enter port number: 8080
[-] Unknown service
```

**What You Learned:**
- `elif` allows multiple conditions
- Conditions are checked in order
- First True condition executes
- `else` catches all remaining cases

---

### Exercise 2.3: Logical Operators (And/Or/Not)

**Objective:** Combine multiple conditions

**Task:**
```python
# AND operator - both must be true
port = 22
service = "SSH"

if port == 22 and service == "SSH":
    print("[+] Confirmed SSH on port 22")

# OR operator - at least one must be true
port = 80
if port == 80 or port == 443:
    print("[+] Web server detected")

# NOT operator - opposite
is_patched = False
if not is_patched:
    print("[!] System is vulnerable")

# Complex condition
cpu = 85
memory = 60
if (cpu > 80 or memory > 80) and (cpu > 50 and memory > 50):
    print("[!] System under stress")
```

**Expected Output:**
```
[+] Confirmed SSH on port 22
[+] Web server detected
[!] System is vulnerable
[!] System under stress
```

**What You Learned:**
- `and` - both conditions must be True
- `or` - at least one condition must be True
- `not` - reverses True/False

---

### Exercise 2.4: Nested Conditionals (Red Team Decision Tree)

**Objective:** Build complex decision logic

**Task:**
```python
# Reconnaissance decision tree
target_ip = "192.168.1.5"
port = 22
service = "OpenSSH_7.4"
response = "connection successful"

if response == "connection successful":
    print(f"[+] {target_ip}:{port} is reachable")
    
    if port == 22:
        print("[+] SSH service detected")
        
        if "OpenSSH_7.4" in service:
            print("[!] OpenSSH 7.4 found - possibly vulnerable")
            print("[+] Add to exploitation targets")
        else:
            print("[*] SSH version unknown")
    elif port == 80 or port == 443:
        print("[+] Web service detected")
    else:
        print("[*] Unknown service")
else:
    print(f"[-] {target_ip}:{port} is unreachable")
```

**Expected Output:**
```
[+] 192.168.1.5:22 is reachable
[+] SSH service detected
[!] OpenSSH 7.4 found - possibly vulnerable
[+] Add to exploitation targets
```

**What You Learned:**
- Nested `if` creates complex decision paths
- Useful for reconnaissance workflows
- Each level filters possibilities

---

## Part 3: Loops (For/While)

### Exercise 3.1: For Loop with Range

**Objective:** Repeat code a fixed number of times

**Task:**
```python
# Simple loop - count to 5
for i in range(5):
    print(f"Iteration {i}")

# Loop with start and end
print("\nPort scanning simulation:")
for port in range(20, 26):
    print(f"Scanning port {port}...")

# Loop backwards
print("\nReverse countdown:")
for i in range(5, 0, -1):
    print(i)
print("Blast off!")
```

**Expected Output:**
```
Iteration 0
Iteration 1
Iteration 2
Iteration 3
Iteration 4

Port scanning simulation:
Scanning port 20...
Scanning port 21...
Scanning port 22...
Scanning port 23...
Scanning port 24...
Scanning port 25...

Reverse countdown:
5
4
3
2
1
Blast off!
```

**What You Learned:**
- `for i in range(n):` loops n times (0 to n-1)
- `range(start, end)` loops from start to end-1
- `range(start, end, step)` changes increment
- Loop variable `i` can be used inside loop

---

### Exercise 3.2: For Loop with Lists

**Objective:** Loop through collections (ports, IPs, credentials)

**Task:**
```python
# Loop through list
target_ips = ["192.168.1.1", "192.168.1.2", "192.168.1.3"]

for ip in target_ips:
    print(f"Targeting: {ip}")

# Port enumeration
ports = [22, 80, 443, 3306, 5432]
open_ports = []

for port in ports:
    # Simulate port check
    if port in [22, 80, 443]:  # Assume these are open
        print(f"[+] Port {port} OPEN")
        open_ports.append(port)
    else:
        print(f"[-] Port {port} closed")

print(f"\nOpen ports found: {open_ports}")

# Credentials testing (simulated)
usernames = ["admin", "root", "user"]
password = "password123"

for username in usernames:
    print(f"Trying: {username}:{password}")
```

**Expected Output:**
```
Targeting: 192.168.1.1
Targeting: 192.168.1.2
Targeting: 192.168.1.3
[+] Port 22 OPEN
[+] Port 80 OPEN
[+] Port 443 OPEN
[-] Port 3306 closed
[-] Port 5432 closed

Open ports found: [22, 80, 443]
Trying: admin:password123
Trying: root:password123
Trying: user:password123
```

**What You Learned:**
- Loop through each item in list
- Use `append()` to collect results
- Lists let you automate repetitive tasks

---

### Exercise 3.3: While Loop

**Objective:** Repeat code while condition is true

**Task:**
```python
# Simple while loop
count = 0
while count < 5:
    print(f"Count: {count}")
    count = count + 1  # Must increment or infinite loop!

# Simulated brute force attempt
attempt = 1
max_attempts = 5
password = "secret123"

while attempt <= max_attempts:
    guess = input(f"Attempt {attempt}/{max_attempts} - Enter password: ")
    
    if guess == password:
        print("[+] Password correct!")
        break  # Exit loop
    else:
        print("[-] Wrong password")
        attempt = attempt + 1

if attempt > max_attempts:
    print("[!] Max attempts exceeded. Account locked.")
```

**Expected Interaction:**
```
Count: 0
Count: 1
Count: 2
Count: 3
Count: 4
Attempt 1/5 - Enter password: wrong
[-] Wrong password
Attempt 2/5 - Enter password: alsowrong
[-] Wrong password
Attempt 3/5 - Enter password: secret123
[+] Password correct!
```

**What You Learned:**
- `while condition:` repeats while True
- Must modify condition or infinite loop
- `break` exits loop early
- Useful for: login attempts, retries, scanning

---

### Exercise 3.4: Break and Continue

**Objective:** Control loop flow

**Task:**
```python
# Break - exit loop immediately
print("Searching for port 22:")
ports = [20, 21, 22, 23, 24]
for port in ports:
    if port == 22:
        print(f"[+] Found SSH on port {port}")
        break  # Stop loop
    else:
        print(f"[-] Port {port} not SSH")

# Continue - skip to next iteration
print("\nScanning only even ports:")
for port in range(20, 30):
    if port % 2 != 0:  # If odd
        continue  # Skip to next
    print(f"[+] Scanning even port: {port}")
```

**Expected Output:**
```
Searching for port 22:
[-] Port 20 not SSH
[-] Port 21 not SSH
[+] Found SSH on port 22

Scanning only even ports:
[+] Scanning even port: 20
[+] Scanning even port: 22
[+] Scanning even port: 24
[+] Scanning even port: 26
[+] Scanning even port: 28
```

**What You Learned:**
- `break` exits loop immediately
- `continue` skips to next iteration
- Useful for: filtering results, stopping early

---

### Exercise 3.5: Nested Loops (Scanning All Ports on All Targets)

**Objective:** Combine loops for automated reconnaissance

**Task:**
```python
# Scan multiple targets and ports
targets = ["192.168.1.1", "192.168.1.2"]
ports = [22, 80, 443]

print("Starting network scan...")
for target in targets:
    print(f"\n[*] Scanning {target}...")
    for port in ports:
        # Simulate port check
        if target == "192.168.1.1" and port in [22, 80]:
            print(f"    [+] Port {port} OPEN")
        elif target == "192.168.1.2" and port == 443:
            print(f"    [+] Port {port} OPEN")
        else:
            print(f"    [-] Port {port} closed")

print("\n[*] Scan complete")
```

**Expected Output:**
```
Starting network scan...

[*] Scanning 192.168.1.1...
    [+] Port 22 OPEN
    [+] Port 80 OPEN
    [-] Port 443 closed

[*] Scanning 192.168.1.2...
    [-] Port 22 closed
    [-] Port 80 closed
    [+] Port 443 OPEN

[*] Scan complete
```

**What You Learned:**
- Nested loops create 2D scanning (all targets × all ports)
- Outer loop: iterate through targets
- Inner loop: iterate through ports for each target
- This is how real port scanners work

---

## Challenge Exercise: Combine Everything

**Build a Simple Credential Checker**

```python
# Week 2 Challenge: Credential Validation

targets = ["192.168.1.1", "192.168.1.2"]
usernames = ["admin", "root"]
password = "password123"

print("=" * 50)
print("CREDENTIAL CHECK - WEEK 2 CHALLENGE")
print("=" * 50)

successful_logins = []

for target in targets:
    print(f"\n[*] Testing {target}...")
    
    for username in usernames:
        print(f"  Trying {username}@{target}...", end="")
        
        # Simulate credential validation
        if (target == "192.168.1.1" and username == "admin") or \
           (target == "192.168.1.2" and username == "root"):
            print(" [+] SUCCESS")
            successful_logins.append(f"{username}@{target}")
        else:
            print(" [-] FAILED")

print(f"\n[*] Successful logins found:")
for login in successful_logins:
    print(f"    [+] {login}")
```

**Expected Output:**
```
==================================================
CREDENTIAL CHECK - WEEK 2 CHALLENGE
==================================================

[*] Testing 192.168.1.1...
  Trying admin@192.168.1.1... [+] SUCCESS
  Trying root@192.168.1.1... [-] FAILED

[*] Testing 192.168.1.2...
  Trying admin@192.168.1.2... [-] FAILED
  Trying root@192.168.1.2... [+] SUCCESS

[*] Successful logins found:
    [+] admin@192.168.1.1
    [+] root@192.168.1.2
```

---

## Your Assignment: Write These 5 Programs

**Due by end of Week 2:**

1. **variables-and-input.py** - Variables, print, input from Exercise 1.1-1.2
2. **string-operations.py** - String parsing from Exercise 1.3-1.4
3. **conditionals.py** - If/else/elif decision tree from Exercise 2.1-2.4
4. **loops.py** - For and while loops from Exercise 3.1-3.4
5. **challenge.py** - Credential checker combining all concepts

---

**Status:** Lab Guide Complete | Ready for Week 2 Python Practice
