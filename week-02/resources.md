# Resources: Week 2 - Python Fundamentals

---

## Official Documentation

### Python Basics
- **Python Official Docs:** https://docs.python.org/3/
- **Python Tutorial:** https://docs.python.org/3/tutorial/
- **Built-in Functions:** https://docs.python.org/3/library/functions.html

### Quick References
- **String Methods:** https://docs.python.org/3/library/stdtypes.html#string-methods
- **List Operations:** https://docs.python.org/3/tutorial/datastructures.html
- **Control Flow:** https://docs.python.org/3/tutorial/controlflow.html

---

## Learning Platforms

### Free Resources
- **W3Schools Python:** https://www.w3schools.com/python/
  - Beginner-friendly, interactive exercises
  - Covers all Week 2 topics
  
- **Real Python:** https://realpython.com/
  - In-depth tutorials
  - Articles on Python best practices
  
- **DataCamp Python Basics:** https://www.datacamp.com/courses/intro-to-python-for-data-science
  - Hands-on coding
  - Covers variables, strings, loops, conditionals

### Interactive Coding
- **Codecademy Python Course:** https://www.codecademy.com/learn/learn-python
  - Browser-based Python practice
  - Immediate feedback
  
- **LeetCode Easy Problems:** https://leetcode.com/
  - Practice loops and conditionals
  - Some problems free, some paid

---

## Red Team Specific Resources

### Security-Focused Python
- **OWASP Secure Coding Practices:** https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/
- **CWE/SANS Top 25 Software Errors:** https://cwe.mitre.org/top25/
  - Understand what you're trying to exploit

### Python for Security
- **Black Hat Python:** https://www.blackhatpython.com/
  - Python for penetration testing
  - Advanced techniques (not Week 2, but preview)
  
- **Violent Python:** https://syngress.com/violent-python/
  - Network analysis with Python
  - Malware analysis basics

---

## Tools & Environment

### Python Installation
- **Windows:** Download from https://www.python.org/downloads/
  - **Important:** Check "Add Python to PATH" during installation
  
- **macOS:** `brew install python3`
  
- **Linux:** Already installed, or `apt install python3`

### Code Editors
- **VS Code (Free):** https://code.visualstudio.com/
  - Install Python extension
  - Recommended for Week 2
  
- **PyCharm Community (Free):** https://www.jetbrains.com/pycharm/download/
  - Full Python IDE
  - Great for larger projects
  
- **Jupyter Notebook:** https://jupyter.org/
  - Browser-based Python
  - Good for learning/experimentation

### Virtual Environments (Setup for Week 3)
```bash
# Create virtual environment
python3 -m venv week02_env

# Activate (on Linux/macOS)
source week02_env/bin/activate

# Activate (on Windows)
week02_env\Scripts\activate

# Install libraries
pip install requests paramiko nmap
```

---

## Week 2 Specific Topics

### Variables & Data Types
- **Type Conversions:** `int()`, `str()`, `float()`, `bool()`
- **String Formatting:** f-strings (preferred), `.format()`, `%` operator
- **Common Methods:** `.upper()`, `.lower()`, `.split()`, `.strip()`, `.replace()`

### Control Flow
- **Comparison Operators:** `==`, `!=`, `<`, `>`, `<=`, `>=`
- **Logical Operators:** `and`, `or`, `not`
- **Truthiness:** Empty strings/lists are False, non-empty are True

### Loops
- **For Loop:** Fixed number of iterations or iterate through collection
- **While Loop:** Unknown number of iterations, condition-based
- **Loop Control:** `break` (exit), `continue` (skip to next), `else` (if no break)

---

## Cheat Sheets

### Python Variables & Strings
```python
# Variables
name = "Rio"
age = 14
height = 5.7

# Print
print(name, age)  # Comma-separated
print(f"{name} is {age}")  # f-string (Python 3.6+)

# String methods
text = "  Hello World  "
print(text.strip())        # "Hello World"
print(text.lower())        # "  hello world  "
print(text.split())        # ["Hello", "World"]
print("World" in text)     # True

# Input
username = input("Enter name: ")
age = int(input("Enter age: "))
```

### Conditionals
```python
# If/else
if age >= 18:
    print("Adult")
else:
    print("Minor")

# If/elif/else
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
else:
    grade = "F"

# Logical operators
if age >= 18 and has_license:
    print("Can drive")

if port == 22 or port == 23:
    print("SSH/Telnet")

if not is_admin:
    print("Not an admin")
```

### Loops
```python
# For loop with range
for i in range(5):
    print(i)  # 0, 1, 2, 3, 4

# For loop with list
fruits = ["apple", "banana", "orange"]
for fruit in fruits:
    print(fruit)

# For loop with enumerate (get index)
for index, fruit in enumerate(fruits):
    print(f"{index}: {fruit}")

# While loop
count = 0
while count < 5:
    print(count)
    count += 1

# Break and continue
for i in range(10):
    if i == 5:
        break  # Exit loop
    if i == 2:
        continue  # Skip this iteration
    print(i)

# Loop with else
for i in range(5):
    if i == 10:
        break
else:
    print("Loop completed normally")
```

---

## Common Mistakes (Learn From These!)

### Mistake 1: Forgetting to Convert Input
```python
 WRONG:
age = input("Enter age: ")
if age >= 18:  # Error! String can't compare to int
    print("Adult")

 CORRECT:
age = int(input("Enter age: "))
if age >= 18:
    print("Adult")
```

### Mistake 2: Infinite Loops
```python
 WRONG:
while True:
    print("This never stops")
    # No way to exit!

 CORRECT:
count = 0
while count < 5:
    print(count)
    count += 1  # Must update condition
```

### Mistake 3: Indentation Errors (Python is sensitive!)
```python
 WRONG:
if x > 5:
print("Greater")  # Indentation missing!

 CORRECT:
if x > 5:
    print("Greater")  # 4 spaces or 1 tab
```

### Mistake 4: Modifying List While Looping
```python
 PROBLEMATIC:
items = [1, 2, 3, 4, 5]
for item in items:
    if item == 3:
        items.remove(item)  # Skips elements!

 BETTER:
items = [1, 2, 3, 4, 5]
items = [item for item in items if item != 3]  # List comprehension
```

---

## Week 2 to Week 3 Bridge

### What's Coming Next Week (Week 3 - Your Planned Topic)

Once you confirm Week 3 topic, resources will include:
- Topic-specific documentation
- Lab guide for your Week 3 focus
- Business impact analysis for Week 3
- Integration with Week 2 Python concepts

**For now, Python fundamentals in Week 2 set foundation for:**
- Week 3+: Using Python to automate security testing
- Network scanning with Python
- Web exploitation with Python
- Data analysis and reconnaissance with Python

---

## Practice Challenges

### Beginner Level (Do These This Week)
1. **Temperature Converter:** Input Celsius, output Fahrenheit using variables and print
2. **Name Reversal:** Input name, reverse it using string slicing, print
3. **Multiplication Table:** Use for loop to print 5×5 multiplication table
4. **Password Validator:** Check if password meets requirements (if/else/length check)
5. **Countdown:** Use while loop to countdown from 10 to 0

### Intermediate Level (Do These After Week 2)
1. **Port Scanner Simulator:** Loop through ports [20-25], check if "open" (nested loops)
2. **Credential Tester:** Loop through usernames/passwords, log successes
3. **Log Parser:** Read output, find errors using string methods and loops
4. **Grade Calculator:** Input scores, use if/elif to assign grades, collect in list

---

## Study Schedule

### Monday
- Read this resource guide
- Install Python + code editor
- Work through Exercise 1.1-1.4 (Variables, Input, Strings)

### Tuesday
- Work through Exercise 2.1-2.4 (Conditionals)
- Write small programs for each concept
- Test your understanding

### Wednesday
- Work through Exercise 3.1-3.5 (Loops)
- Combine concepts from Mon-Tue
- Practice nested loops

### Thursday
- Write the Challenge Program (credential checker)
- Test edge cases
- Document your code with comments

### Friday-Saturday
- Polish all programs
- Add comments explaining code
- Test for errors (edge cases, invalid input)

### Sunday
- Commit to GitHub (week-02 folder)
- Reflect on what you learned
- Plan for Week 3

---

## Tips for Success

### 1. **Type Along, Don't Copy-Paste**
- Manually type examples
- Your fingers learn the syntax
- You'll catch mistakes faster

### 2. **Test Everything**
- Try your code with different inputs
- What happens if someone enters wrong data?
- Break it intentionally to understand

### 3. **Comment Your Code**
```python
# Good comment - explains WHY
count = 0  # Initialize counter before loop

# Bad comment - explains WHAT (code already shows this)
count = 0  # Set count to zero
```

### 4. **Use Meaningful Variable Names**
```python
 x = input("Enter IP: ")  # What is x?
 target_ip = input("Enter IP: ")  # Clear!

 p = [22, 80, 443]
 common_ports = [22, 80, 443]
```

### 5. **Test Error Cases**
```python
# What if user enters negative number?
# What if user enters text instead of number?
# What if list is empty?
# Test these!
```

---

## Final Reminders

 **Do:**
- Practice typing code yourself
- Test with different inputs
- Ask questions if confused
- Save all your programs

 **Don't:**
- Just watch tutorials without coding
- Copy-paste without understanding
- Skip the practice exercises
- Ignore error messages (they're helpful!)

---

**Next Step:** Start with Exercise 1.1 from lab-guide.md

**Week 2 Goal:** Comfortable writing Python programs with variables, conditionals, and loops

**Red Team Connection:** These are the FOUNDATIONS. Every network scanner, exploit script, and automation tool you'll build in Year 2-4 uses these concepts.

---

**Resources Updated:** Week 2 | Python Fundamentals  
**Next Review:** After Week 2 completion
