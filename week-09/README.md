# Week 8: Cross-Site Scripting (XSS) & Access Control Bypass

> **From Reflected Alerts to Real-World CVEs — Blacklist Filters Are Not Security**

---

## Topics Covered This Week

### Room: XSS (In-Depth)
Explore in-depth the different types of XSS and their root causes.

**URL:** https://tryhackme.com/room/axss

**Tasks:**
1. Introduction
2. Terminology and Types
3. Causes and Implications
4. Reflected XSS
5. Vulnerable Web Application 1 (real CVE: copyparty)
6. Stored XSS
7. Vulnerable Web Application 2 (real CVE: Hospital Management System)
8. DOM-Based XSS
9. Context and Evasion
10. Conclusion

### DVWA Practice: Manual XSS Exploitation
Reflected and Stored XSS across all three difficulty levels (Low/Medium/High), demonstrating progressive filter bypass techniques.

### Theory: DOM-Based XSS + BeEF Hook Concept
Conceptual understanding of client-side-only XSS execution and how XSS serves as the delivery mechanism for browser exploitation frameworks.

### Practice: IDOR (Insecure Direct Object Reference)
User ID manipulation in URL parameters to access unauthorized account data.

---

## Learning Objectives

**By end of Week 8, you will:**
- ✅ Distinguish Reflected, Stored, and DOM-Based XSS by data flow and persistence
- ✅ Bypass blacklist-based filters using tag fragmentation and event handlers
- ✅ Understand why blacklisting specific strings (like "script") never fully solves XSS
- ✅ Exploit two real, CVE-documented XSS vulnerabilities in production-grade open source software
- ✅ Understand the conceptual link between XSS and browser exploitation frameworks (BeEF)
- ✅ Identify and exploit IDOR to access another user's data via direct parameter manipulation
- ✅ Apply context-aware evasion techniques against character-based filters

---

## Attack Chain This Week

```
[Filter Bypass Progression - DVWA]
Low:    <script>alert(document.cookie)</script>
                    ↓ (str_replace('<script>','') added)
Medium: <scr<script>ipt>alert(document.cookie)</script>
                    ↓ (preg_replace blocks "script" pattern entirely)
High:   <img src=x onerror=alert(document.cookie)>
                    ↓
[Lesson: Blacklisting keywords ≠ security. Output encoding is the only real fix.]

[Real-World Validation]
DVWA teaches the pattern → Real CVEs prove the pattern matters:
  CVE-2023-38501 (copyparty)              → Reflected XSS, unsanitized URL param
  CVE-2021-38757 (Hospital Mgmt System)    → Stored XSS, targets admin on login

[Escalation Path]
XSS confirmed → BeEF hook.js delivery (theory) → Browser control (conceptual)
                                              ↓
IDOR discovered → Direct account data access (no XSS needed, separate flaw)
```

---

## Key Learnings This Week

- **Blacklist filtering is fundamentally broken as a defense.** Every DVWA "fix" attempt (str_replace, preg_replace) was bypassed by either fragmenting the blocked keyword or avoiding it entirely with `onerror`. The only pattern that cannot be bypassed this way is output encoding — escaping `<`, `>`, `"`, `'` at render time.
- **The same bypass logic scales from a training lab to production software.** The exact "avoid the word `script`, use `onerror` instead" technique practiced on DVWA is the same root cause behind CVE-2023-38501 (copyparty) and CVE-2021-38757 (Hospital Management System) — this is not a toy problem, it is the real-world pattern.
- **Stored XSS is more dangerous than Reflected XSS because of who views it.** CVE-2021-38757 specifically targets the page an admin/receptionist views — this converts a "self-XSS" annoyance into a privileged-account compromise vector, which is why Stored XSS consistently scores higher in real assessments.
- **Client-side maxlength attributes are not security controls.** Bypassing `maxlength="10"` via browser DevTools to fit a full payload confirmed that HTML attributes only affect the UI, never the server — the server-side filter is the only thing that matters.
- **XSS and IDOR are separate bug classes with separate root causes — and separate fixes.** IDOR requires no script execution at all — it is purely a missing authorization check — while XSS requires no ID manipulation. Practicing them independently this week made it clear why a single fix (like "sanitize all input") does not address both; in real engagements the two classes can also chain together, which is exactly why conflating their fixes is a reporting mistake to avoid.
- **BeEF reframes XSS from "an alert box" to "full browser control."** Understanding that `<script src="...hook.js">` is just another XSS payload changed how I read every "harmless" alert() payload going forward — the same injection point that pops an alert can deliver a hook.

---

## Files This Week

```
week-08/
├── README.md                          (this file)
├── write-up.md                        (6-part framework)
├── dvwa-xss-exploitation-report.md    (all 6 DVWA payloads: Reflected + Stored, L/M/H)
├── real-world-cve-case-studies.md     (copyparty + Hospital Mgmt System CVEs)
├── business-impact-analysis.md        (sourced financial/regulatory impact per vulnerability type)
├── xss-advanced-concepts.md           (DOM-based theory, BeEF concept, IDOR, evasion)
├── lab-guide.md                       (TryHackMe + DVWA exercises)
└── resources.md                       (references)
```

---

**Status:** Week 8 | XSS Deep Dive + Real CVE Case Studies + IDOR | Complete
