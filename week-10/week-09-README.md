# Week 9: File Upload Vulnerabilities — From Basic Bypass to Race Conditions

> **Five Techniques, One Root Cause: The Server Trusts What It Shouldn't**

---

## Topics Covered This Week

### PortSwigger Web Security Academy: File Upload Vulnerabilities

Four labs, increasing in difficulty from Apprentice to Expert, all built around the same vulnerable image-upload application with progressively stronger (but still bypassable) defenses.

| Lab | Difficulty | Technique |
|-----|-----------|-----------|
| [Remote code execution via web shell upload](https://portswigger.net/web-security/file-upload/lab-file-upload-remote-code-execution-via-web-shell-upload) | Apprentice | No validation at all |
| [Web shell upload via Content-Type restriction bypass](https://portswigger.net/web-security/file-upload/lab-file-upload-web-shell-upload-via-content-type-restriction-bypass) | Apprentice | HTTP header spoofing |
| [Web shell upload via path traversal](https://portswigger.net/web-security/file-upload/lab-file-upload-web-shell-upload-via-path-traversal) | Practitioner | Directory traversal to escape a non-executable folder |
| [Web shell upload via race condition](https://portswigger.net/web-security/file-upload/lab-file-upload-web-shell-upload-via-race-condition) | Expert | TOCTOU race condition + persistent dropper |

### Theory: Advanced Evasion Techniques

Double extension (`shell.php.jpg`) and null byte injection (`shell.php%00.jpg`) — legacy techniques still worth understanding even though null byte injection is largely patched in modern PHP.

**No TryHackMe room this week** — not on this week's schedule.

---

## Learning Objectives

**By end of Week 9, you will:**
- ✅ Understand why unrestricted file upload (CWE-434) is one of the most severe web vulnerability classes — it grants code execution, not just data access
- ✅ Bypass four progressively stronger upload filters, each defeated by a different flawed assumption
- ✅ Understand Time-of-Check to Time-of-Use (TOCTOU) race conditions and how modern HTTP/2 tooling makes them dramatically more reliable
- ✅ Build a persistent "dropper" payload to survive a narrow exploitation window
- ✅ Connect four of the five techniques to a real, CVE-documented breach in production software — and understand why the fifth (race conditions) is genuinely harder to trace to a single named incident
- ✅ Explain the business consequence of each bypass technique with cited, verifiable sources

---

## Key Learnings This Week

- **File upload RCE is one of the most direct pipelines to full system takeover.** SQL injection can also reach OS command execution (via `xp_cmdshell` on MSSQL, or `INTO OUTFILE` to write a webshell on MySQL), and XSS can pivot to file upload by hijacking a privileged user's session — but both typically require an escalation step. An unrestricted file upload skips that step entirely: the very first successful request grants a webshell with the web server's own privileges. Every technique this week ends at the same destination — arbitrary, persistent code execution — with fewer steps in between than most other vulnerability classes.
- **Every defense this week failed for the same underlying reason: trusting something the client controls.** Content-Type header, filename, and even the momentary existence of a file on disk are all attacker-influenced. Content inspection (magic bytes) is a real improvement over trusting a header, but it is not airtight either — a polyglot file (e.g., a PHP payload embedded inside a valid image's EXIF data or appended after a legitimate GIF89a header) can pass a magic-byte check while still containing executable code. The strongest pattern combines active image re-processing (re-rendering through a graphics library, which strips anything that isn't actual image data) with decoupling uploads from the web server entirely — storing them in isolated, script-incapable storage rather than the application's own filesystem.
- **Modern tooling turns a "theoretical" race condition into a reliable one.** A TOCTOU race condition sounds like a coin-flip exploit. Burp's single-packet attack technique (bundling requests into one TCP packet to eliminate network jitter) is specifically why this is no longer theoretical — PortSwigger's own research demonstrated this technique against real production targets, not just lab environments.
- **A "dropper" payload beats a "direct" payload for reliability.** Racing to read a secret file in the same instant the upload exists is fragile — you need to win the race twice (upload timing and read timing) in the same narrow window. Writing a small dropper that persists a second, permanent shell removes that second race entirely: win the window once, and the second shell is there indefinitely.
- **Null byte injection is a lesson in how a fix actually closes a class of bug.** PHP patched this specific technique in version 5.3.4 by changing how the underlying string-handling functions treat embedded nulls — a real example of a language-level fix eliminating an entire technique platform-wide, rather than each application having to defend against it individually.
- **Four of the five techniques this week have a real, named CVE in production software** — this isn't academic. The same bypass logic that solved a PortSwigger lab is the same logic behind a CVSS 9.8–10.0 flaw (NVD and the vendor scored it differently — see `real-world-cve-case-studies.md`) in enterprise SAP software actively exploited in 2025. The race condition technique is the exception, and the reason is worth stating precisely: automated DAST scanners are structurally poor at catching a millisecond-scale timing window, so this bug class is systematically underrepresented in CVE databases relative to how often it likely exists. That gap is exactly why it's a high-value area for manual Red Team testing and advanced bug bounty hunting rather than a lower-priority curiosity — PortSwigger's own research demonstrated it against live production targets using precision HTTP/2 tooling, not luck.

---

## Attack Chain This Week

```
[Defense Layer 1: No validation at all]
Upload shell.php directly → executes immediately
         ↓ (defense added: block by Content-Type)
[Defense Layer 2: Content-Type header check]
Spoof Content-Type: image/jpeg, keep .php body → bypassed
         ↓ (defense added: block execution in upload folder)
[Defense Layer 3: Non-executable upload directory]
Path-traverse the filename (..%2f) to escape into an executable folder → bypassed
         ↓ (defense added: validate file content before allowing it to persist)
[Defense Layer 4: Post-upload validation + deletion of invalid files]
Exploit the TOCTOU race window between write and delete,
using a dropper payload for persistence → bypassed
         ↓
[Every layer defeated → arbitrary code execution achieved]
```

---

## Files This Week

```
week-09/
├── README.md                                  (this file)
├── write-up.md                                (6-part framework — race condition RCE)
├── file-upload-exploitation-report.md         (all 4 PortSwigger labs, step by step)
├── file-upload-bypass-techniques-reference.md (all 5 techniques, theory + payloads)
├── real-world-cve-case-studies.md             (SAP, WordPress, Struts, Drupal CVEs)
├── business-impact-analysis.md                (sourced impact per technique)
├── lab-guide.md                               (hands-on PortSwigger exercises)
└── resources.md                               (references)
```

---

**Status:** Week 9 | File Upload Vulnerabilities: Basic Bypass to Race Conditions | Complete
