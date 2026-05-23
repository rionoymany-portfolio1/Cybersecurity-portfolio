# Week 2: Python Fundamentals - Core Language Features

> **Python Basics + Control Flow + Loops in One Week**

---

##  Topics Covered This Week

### Part 1: Variables, Print, Input, String Operations
- Variable declaration and data types
- Print statements and output formatting
- User input handling
- String manipulation and methods
- Type casting and conversion

### Part 2: Conditional Logic (If/Else/Elif)
- Boolean expressions
- Comparison operators
- Logical operators (and, or, not)
- If/else/elif decision trees
- Nested conditionals

### Part 3: Loops (For/While)
- For loops with ranges and iterables
- While loops and loop control
- Break and continue statements
- Nested loops
- Loop patterns (accumulation, filtering, searching)

---

##  Learning Objectives

**By end of Week 2, you will:**
-  Write Python programs with variables and user input
-  Build conditional logic for decision-making
-  Implement loops for automation and iteration
-  Understand how these are used in Red Team reconnaissance scripts
-  Complete working code examples for each concept

---

##  Why This Matters for Red Team

**Real Red Team Use Cases for Week 2 Skills:**

| Concept | Red Team Application |
|---------|---------------------|
| **Variables + Input** | Store credentials, target lists, configuration parameters |
| **String Operations** | Parse command output, extract data from logs, format payloads |
| **If/Else Logic** | Conditional reconnaissance (check if port open → continue scanning) |
| **Loops** | Automate repetitive tasks (scan 10K IP addresses, try multiple exploits) |

**Example:** A simple port scanner using week 2 concepts
```python
target = input("Enter target IP: ")
ports = [22, 80, 443, 3306, 5432]

for port in ports:
    result = check_port(target, port)  # simplified
    if result == "open":
        print(f"[+] Port {port} OPEN on {target}")
    else:
        print(f"[-] Port {port} closed")
```

---

## 📋 Weekly Schedule

| Day | Focus | Deliverable |
|-----|-------|-------------|
| **Mon** | Variables, Print, Input, String | 5 working programs |
| **Tue** | If/Else/Elif logic | 5 conditional programs |
| **Wed** | For/While loops | 5 loop programs |
| **Thu** | Write 6-part write-up | Complete analysis |
| **Fri** | Business impact analysis | Executive brief |
| **Sat** | Polish + review | Final code |
| **Sun** | Commit to GitHub | week-02 folder live |

---

##  What's Included in week-02/

```
week-02/
├── README.md (this file)
├── write-up.md (6-part framework)
├── business-impact-analysis.md
├── lab-guide.md
├── resources.md
└── code-examples/
    ├── 01-variables-print-input.py
    ├── 02-string-operations.py
    ├── 03-if-else-elif.py
    ├── 04-for-loops.py
    ├── 05-while-loops.py
    └── 06-combined-program.py
```

---

##  Next Steps

1. Start with **lab-guide.md** for step-by-step exercises
2. Write code in **code-examples/** folder
3. Read **write-up.md** to understand how these connect to Red Team work
4. Study **business-impact-analysis.md** to see why Python matters

---

**Status:** Week 2 | Python Fundamentals | Complete
