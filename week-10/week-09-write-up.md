# Write-Up: TOCTOU Race Condition in File Upload Leading to Persistent RCE

---

## 1. VULNERABILITY: Time-of-Check to Time-of-Use (TOCTOU) in Upload Validation

### Root Cause

The application's upload handler performs validation in the wrong order relative to where the file is written:

```php
$target_file = "avatars/" . $_FILES["avatar"]["name"];

// Step 1: File is written to the PUBLIC, web-accessible directory FIRST
move_uploaded_file($_FILES["avatar"]["tmp_name"], $target_file);

// Step 2: Validation happens AFTER the file already exists on disk
if (checkViruses($target_file) && checkFileType($target_file)) {
    echo "The file has been uploaded.";
} else {
    // Step 3: Only NOW is the invalid file removed
    unlink($target_file);
    http_response_code(403);
}
```

Between Step 1 and Step 3, the uploaded file — even a raw `.php` file — physically exists inside the web root and is servable by the web server. This gap is the "Time of Check to Time of Use" window: the file's legitimacy is *checked* at one moment, but the file has already been in a *usable* state since an earlier moment. Any request that reaches the file during that window executes it before the server ever gets the chance to delete it.

### Vulnerability Classification

| Property | Value |
|----------|-------|
| **Type** | Race Condition (TOCTOU) leading to Remote Code Execution |
| **CWE** | CWE-367: Time-of-check Time-of-use (TOCTOU) Race Condition |
| **Secondary CWE** | CWE-434: Unrestricted Upload of File with Dangerous Type |
| **OWASP** | A04:2021 — Insecure Design |
| **Architectural Flaw** | Validation performed after the file is already in a publicly-servable, executable location |

---

## 2. EXPLOITATION: Winning the Race with a Persistent Dropper

### Why a Direct Payload Isn't Reliable Enough

The naive approach — upload a webshell and immediately request it, hoping to land inside the validation window — requires winning the race **and** correctly timing the follow-up read **in the same narrow window**, every single time you want to use the shell again. A far more reliable approach is to make the *first* successful race permanent.

### The Dropper Strategy

**Payload uploaded (`payload.php`):**
```php
<?php file_put_contents('shell.php', '<?php echo file_get_contents("/home/carlos/secret"); ?>'); ?>
```

This payload does almost nothing when it runs — it simply writes a **second** file, `shell.php`, containing the actual data-exfiltration logic. The critical property: nothing in the application ever calls `unlink()` on `shell.php`. Only `payload.php` (the original upload) gets deleted once validation fails. If `payload.php` executes even once during the race window, `shell.php` persists on disk permanently.

**Scope note:** this lab's `shell.php` is deliberately narrow — it reads one file, because that is the lab's defined objective. In a real engagement, the same persistent-dropper technique is the entry point, not the endpoint: once arbitrary code execution survives past the race window, the natural next steps are dumping environment variables (frequently containing cloud provider credentials), enumerating the internal network from the compromised host, or replacing the dropper with a full command-execution shell for sustained access. The lab's single-file read demonstrates the mechanism; a real assessment would document the full reachable blast radius from that same foothold.

```
Timeline:

T+0ms   move_uploaded_file() writes payload.php to /avatars/
        │
        ├── RACE WINDOW OPEN ──────────────────┐
        │                                       │
T+Xms   Attacker's GET request to payload.php   │
        arrives inside the window, executes it  │
        → shell.php is written to disk          │
        │                                       │
        └── RACE WINDOW CLOSES ─────────────────┘
        │
T+Yms   Validation fails, unlink(payload.php) removes the dropper
        (shell.php is untouched — it was never the file being validated)
        │
T+later Attacker requests shell.php at leisure — no race required,
        it has existed as a normal file ever since T+Xms
```

### Making the Race Reliable: Burp Suite's Single-Packet Attack

A standard race attempt sent as two separate HTTP requests over a normal connection is subject to network jitter — the two requests may arrive milliseconds apart due to ordinary network variance, which is often wider than the actual TOCTOU window. Burp Suite Repeater's **"Send group in parallel" (single-packet attack)** feature solves this using an HTTP/2-specific technique: multiple complete HTTP requests are packed into a single TCP packet, so the server's network stack processes all of them at effectively the same instant, eliminating the jitter that would otherwise cause a race attempt to miss the window.

**Execution:**
```
1. Upload payload.php (containing the dropper) via the avatar upload form
2. Send the upload (POST) request AND a GET request for payload.php
   as a "Send group in parallel" batch in Burp Repeater
3. Because both requests hit the server in the same TCP packet,
   the GET has a dramatically higher chance of landing inside
   the TOCTOU window than it would over two separate connections
4. Once shell.php exists, request it directly — no further racing needed
5. Retrieve the secret: browse to /files/avatars/shell.php
```

### CVSS Assessment: Why Tooling Changes the Effective Severity

**Traditional classification (race conditions generally require conditions outside the attacker's full control):**
```
CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H = 8.5 (High)
```

**With single-packet-attack tooling (jitter eliminated, race reliability dramatically increased):**
```
CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H = 9.9 (Critical)
```

**Which applies?** CVSS's Attack Complexity metric asks whether success requires "conditions beyond the attacker's control." A traditional two-request race genuinely does — network timing isn't something an attacker controls precisely. But the single-packet attack technique specifically removes that dependency by collapsing both requests into one packet. A report should note both figures: 8.5 reflects the vulnerability class in the abstract, but 9.9 reflects the *actual, present-day exploitability* once this publicly documented tooling is available to any attacker — which it is, built into a widely used, free tool.

---

## 3. BUSINESS IMPACT: Full Server Compromise, Not Just Data Exposure

### Why File Upload RCE Outranks Injection and XSS in Severity

SQL injection typically grants data access. XSS typically grants a victim's browser session. A file upload vulnerability that leads to webshell execution grants the attacker **the server's own operating-system-level privileges** — the ability to read any file the web server process can read, write any file it can write, spawn other processes, pivot to internal network segments, and establish long-term persistence.

### Real-World Validation

**Accuracy note:** the CVE cited below shares this lab's ultimate consequence (webshell RCE via file upload) but not its specific mechanism — CVE-2025-31324 is a *missing-validation* case (matching this week's Apprentice lab), not a race condition. It is cited here because no single named CVE for the TOCTOU race condition technique specifically exists in public reporting (see `real-world-cve-case-studies.md` for why), so it serves to establish that the *destination* this technique reaches — full webshell-based RCE — is unambiguously real and catastrophic in production software, even though the *path* there differs from this lab's TOCTOU mechanism. The race condition mechanism's own real-world validity rests on a different kind of evidence: PortSwigger's own research team has publicly demonstrated the exact single-packet-attack technique used in this lab against real production targets during authorized research.

This exact consequence pattern — unrestricted or insufficiently-validated file upload leading to webshell-based RCE — is the root cause of **CVE-2025-31324**, a critical vulnerability in SAP NetWeaver Visual Composer's Metadata Uploader component scored 9.8 by NVD and 10.0 by SAP's own CNA assessment (the two differ only on CVSS Scope; both land in the maximum-severity band), actively exploited in the wild throughout 2025. Attackers uploaded JSP webshells (observed names include `helper.jsp`, `cache.jsp`, and randomly-named 8-character files) via an unauthenticated endpoint, achieving code execution with the SAP application's own operating-system privileges — predominantly targeting manufacturing-sector organizations. Some observed intrusions proceeded to deploy the Brute Ratel command-and-control framework for follow-on access. Full technical details and sourcing are in `real-world-cve-case-studies.md`.

### Financial Exposure

A detailed, source-cited breakdown of financial and regulatory consequences for every technique demonstrated this week (not just the race condition) is in `business-impact-analysis.md`. Summary for this specific technique:

| Consequence | Basis |
|-------------|-------|
| Full server compromise (OS-level code execution) | Direct technical consequence, confirmed via lab exploitation |
| Business process manipulation (finance, HR, production systems) | Documented consequence of CVE-2025-31324 exploitation |
| Regulatory exposure (SOX, GDPR) if compromised system touches financial/personal data | Documented in CVE-2025-31324 analysis |

---

## 4. TECHNICAL FIX: Validate Before the File Is Servable, Not After

### The Fix: Reorder Validation to Happen Before Public Placement

```php
// SECURE: Validate in an isolated location BEFORE moving to the public directory
$tmp_path = $_FILES["avatar"]["tmp_name"];  // Already in a non-web-accessible temp location

if (checkFileType($tmp_path) && checkViruses($tmp_path)) {
    // Only move to the public, web-servable directory AFTER validation passes
    $safe_filename = bin2hex(random_bytes(16)) . '.jpg';  // Random name, forced extension
    move_uploaded_file($tmp_path, "avatars/" . $safe_filename);
    echo "The file has been uploaded.";
} else {
    http_response_code(403);
    // Nothing to unlink — the file never left the isolated temp location
}
```

**Why this eliminates the race entirely:** there is no window where an unvalidated file exists in a location the web server will execute. The file only ever reaches the public directory once every check has already passed — there is nothing left to "race."

### Defense-in-Depth: Disable Execution in Upload Directories

```apache
# Apache: prevent PHP execution regardless of extension games
<Directory "/var/www/html/avatars">
    php_flag engine off
    RemoveHandler .php .php3 .php4 .php5 .phtml
</Directory>
```

```nginx
# Nginx: never pass requests in the upload directory to the PHP handler
location /avatars/ {
    location ~ \.php$ {
        deny all;
    }
}
```

Even if a race condition or filter bypass slips a `.php` file into the upload directory, the web server itself refuses to execute it — a second, independent layer that doesn't depend on the upload validation logic being correct.

### The Stronger Pattern: Remove the Race Entirely by Removing the Server From the Loop

The fixes above eliminate this specific race condition on an application that still stores uploads on its own web server — a legitimate, immediately-applicable fix for an existing codebase. The architecturally stronger pattern, used by most modern cloud-native applications, goes further: uploads are streamed directly to decoupled, script-incapable object storage (e.g., an S3 bucket or Blob container with no execution capability at all) rather than the application server's own filesystem, and served to users through a separate, isolated domain. When the storage tier is structurally incapable of executing anything, there is no TOCTOU window to race in the first place — not because the timing was closed, but because the entire class of "a file briefly exists somewhere executable" no longer applies. The code-level fix above remains the right answer for validating on the application server itself when a full architecture migration isn't the immediate option; both approaches converge on the same principle of never letting an unvalidated (or execution-capable) file sit in a servable location.

---

## 5. POLICY FIX: Architectural Standards for Upload Handling

### Policy 1: Validate-Before-Move Is Mandatory

```
Standard: File content validation (type checking, malware scanning) must
complete in an isolated, non-web-accessible location before any file is
moved into a directory the web server can serve. Validating a file already
in a public directory is not an approved pattern, regardless of how fast
the deletion-on-failure logic runs.
```

### Policy 2: Uploaded Files Are Never Directly Executable

```
Standard: Directories containing user-uploaded content must have script
execution disabled at the web server configuration level (not just
relying on extension filtering). This is enforced independently of
whatever application-level validation exists.
```

### Policy 3: System-Generated Filenames Only

```
Standard: User-supplied filenames are never used to construct the final
storage path. All stored filenames are server-generated (UUID or
equivalent), eliminating path traversal and double-extension tricks as
a category, not just the specific patterns currently on a blocklist.
```

### Policy 4: Race-Condition Review for Any Multi-Step File Operation

```
Standard: Any code path involving upload → validate → accept-or-reject
must be reviewed for TOCTOU exposure specifically, as a named item in
security code review checklists — not folded generically into "input
validation review."
```

---

## 6. DETECTION RULE: Identifying Upload-Based Attack Attempts

### Sigma Rule: Rapid Duplicate Requests to a Recently Uploaded File

```yaml
title: Potential Race Condition Exploitation - Rapid Access to Newly Uploaded File
description: >
  Detects a GET request to a recently uploaded file arriving within
  milliseconds of the upload POST request — characteristic of a
  TOCTOU race condition exploitation attempt
logsource:
  category: webserver
  product: any
detection:
  selection_upload:
    http_method: "POST"
    url_path|contains: "/avatars/"
  selection_immediate_get:
    http_method: "GET"
    url_path|endswith:
      - ".php"
      - ".phtml"
    timeframe: 200ms
  condition: selection_upload followed by selection_immediate_get
falsepositives:
  - Legitimate immediate preview/thumbnail generation requests
level: high
tags:
  - attack.execution
  - attack.t1190
  - cwe.367
  - cwe.434
```

### WAF / Server Rule: Executable Extensions in Upload Directories

```
Block or alert on any HTTP request where:
  - URL path matches an upload/avatar directory pattern
  - Requested filename ends in an executable extension
    (.php, .phtml, .php3-.php7, .jsp, .asp, .aspx)

This catches successful uploads regardless of which bypass technique
got the file there in the first place — detection at the "attempt to
execute" stage is more resilient than trying to detect every possible
upload-time bypass individually.
```

### Log Correlation for Post-Incident Detection

```
For any confirmed or suspected upload-based compromise:
  1. Search web server access logs for POST requests to upload endpoints
     immediately followed (within ~1 second) by GET requests to the
     same or a very similarly-named file
  2. Check file system timestamps in upload directories for files with
     executable extensions that don't match expected content types
  3. Cross-reference with CVE-2025-31324-style known webshell filenames
     (helper.jsp, cache.jsp, or suspicious randomly-named files) as a
     starting hunting pattern
```

---

## Summary

| Skill | Evidence |
|-------|---------|
| Race condition theory | Diagnosed the exact TOCTOU window between move_uploaded_file() and unlink() |
| Modern exploitation tooling | Applied Burp's single-packet attack to make an unreliable race dramatically more reliable |
| Payload engineering | Designed a two-stage dropper for persistence rather than relying on a single-shot direct payload |
| CVSS reasoning | Calculated and justified both the traditional (8.5) and tooling-adjusted (9.9) severity readings |
| Real-world grounding | Connected the lab's consequence class (webshell RCE via upload) to CVE-2025-31324, an actively exploited CVSS 10.0 flaw — while being explicit that the specific TOCTOU mechanism itself is separately validated via PortSwigger's own production-targeted research, not this CVE |
| Layered remediation | Validate-before-move (primary) + execution-disabled directories (defense-in-depth) + system-generated filenames |

---

**Status:** Week 9 Complete | TOCTOU Race Condition File Upload RCE Mastered | 6-Part Framework Applied

**References:**
- CWE-367: https://cwe.mitre.org/data/definitions/367.html
- CWE-434: https://cwe.mitre.org/data/definitions/434.html
- PortSwigger Race Conditions: https://portswigger.net/web-security/race-conditions
- CVE-2025-31324: https://nvd.nist.gov/vuln/detail/CVE-2025-31324
