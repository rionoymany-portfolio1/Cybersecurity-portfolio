# File Upload Bypass Techniques: Reference Guide

> **Five Ways to Defeat a Filter That Trusts the Wrong Thing**

---

## Overview

Every file upload bypass technique exploits the same category of mistake: the server trusts a signal it should not — a client-supplied header, a client-supplied filename, or the assumption that a file's state at one moment still holds true a moment later. This reference covers all five techniques encountered this week.

```
File Upload Bypass Techniques
├── No Validation                    ← Trivial baseline case
├── Content-Type / MIME Spoofing     ← Trusts a client-controlled header
├── Path Traversal                   ← Trusts sanitization order
├── Race Condition (TOCTOU)          ← Trusts a moment-in-time state
└── Extension-Layer Tricks
    ├── Double Extension             ← Trusts the LAST extension only
    └── Null Byte Injection          ← Trusts high-level string handling
```

---

## Technique 1: No Validation (Baseline)

**Mechanism:** The server performs no check at all — any file, with any extension and any content, is accepted and stored in a web-servable location.

```
Payload: exploit.php containing <?php system($_GET['cmd']); ?>
Result:  Direct upload, direct execution
```

This is included as the baseline not because it's interesting, but because every other technique in this document is best understood as "what an attacker does when this trivial case has been blocked."

---

## Technique 2: Content-Type / MIME Spoofing

**Mechanism:** The server checks the `Content-Type` value in the multipart form-data request to decide whether to accept a file. This value is set by the client and is never cross-checked against the file's actual bytes.

```
Blocked:  Content-Type: application/x-php
Bypass:   Content-Type: image/jpeg  (extension and body remain .php)
```

**Why it works:** MIME type, as declared in an HTTP request, is metadata the client asserts about itself — conceptually no different from a person filling out their own name tag. Magic-byte / file-signature inspection is a real improvement, since it reads the file's actual first bytes rather than believing the label — but it is not a complete fix on its own. A polyglot file (for example, PHP code embedded inside a legitimate image's EXIF metadata, or appended after a valid GIF89a header) can present entirely correct magic bytes while still carrying executable content further into the file. The more complete remediation for image uploads specifically is active re-processing: forcing the file through a graphics library to re-render it, which discards anything that isn't genuine image data — a polyglot payload doesn't survive being decoded and re-encoded as a fresh image.

**Real-world precedent:** CVE-2021-24145 (WordPress Modern Events Calendar plugin) — full details in `real-world-cve-case-studies.md`.

---

## Technique 3: Path Traversal

**Mechanism:** A directory is correctly configured to disable script execution, but the *filename* supplied by the client is used to construct the storage path with insufficient sanitization — specifically, sanitization that runs before URL-decoding.

```
Stripped:  filename="../exploit.php"        → traversal removed, stays in avatars/
Bypass:    filename="..%2fexploit.php"      → decoded to ../ AFTER the filter runs,
                                               lands one directory above avatars/
```

**Why it works:** the filter's ordering assumption ("check for `../` in the raw input") breaks the moment the true traversal sequence only exists in encoded form until after the check has already passed. This is a general lesson about sanitization order, not specific to file uploads — the same class of bug appears anywhere decode-then-use logic is implemented as check-then-decode instead.

**Real-world precedent:** CVE-2023-50164 (Apache Struts 2) — full details in `real-world-cve-case-studies.md`.

---

## Technique 4: Race Condition (TOCTOU)

**Mechanism:** The file is written to a public, executable directory *before* content validation completes. Between the write and the (conditional) delete, a window exists where the file is servable.

```
move_uploaded_file() → [RACE WINDOW] → validate() → unlink() if invalid
```

**Why it works:** validation logic that is *correct in principle* can still be defeated if the object being validated is reachable by an attacker during the validation process itself. Modern tooling (Burp's single-packet attack, bundling requests into a single TCP packet to eliminate network jitter) makes this window reliably exploitable rather than a matter of luck.

**Full technical detail:** `write-up.md` and `file-upload-exploitation-report.md` (Lab 4).

---

## Technique 5: Extension-Layer Tricks — Double Extension & Null Byte

These two techniques both exploit a mismatch between how *different layers* of a system parse a filename — the web application, the web server, and the operating system filesystem API don't always agree on "what the extension is."

### 5a. Double Extension

```
Filename: shell.php.jpg
```

**Mechanism:** A naive filter checks only the final extension (`.jpg`) and approves the file. But some web server configurations (notably legacy Apache setups using `AddHandler` rather than `SetHandler`) will execute a file as PHP if `.php` appears *anywhere* in the filename, regardless of what comes after it — because `AddHandler` associates a handler with an extension token found anywhere in the name, not strictly the final suffix.

```
AddHandler application/x-httpd-php .php
```
combined with Apache's `mod_negotiation` (Multiviews) can cause `shell.php.jpg` to still be processed by the PHP handler, because the server's extension-matching logic doesn't require `.php` to be the absolute last token.

**Why it still matters today:** while well-configured modern servers are not vulnerable to this, the underlying misconfiguration (`AddHandler` instead of `SetHandler`) is still found in real deployments, particularly older or migrated hosting environments.

### 5b. Null Byte Injection

```
Filename: shell.php%00.jpg
```

**Mechanism:** The web application (in a high-level language like PHP) validates the filename and sees it ends in `.jpg` — passes the check. But when that filename string is passed down to lower-level, C-based filesystem APIs, the null byte (`%00`, ASCII 0) is historically interpreted as a **string terminator**. The underlying OS/filesystem call reads the string only up to the null byte, saving the file as `shell.php` — silently dropping everything after the null byte, including the `.jpg` the application thought it had enforced.

**Current status — verified:** This specific technique was patched at the language level in **PHP 5.3.4** (2010), which changed how PHP's string-handling functions treat embedded null bytes before they reach OS-level calls. On any modern, currently-supported PHP version, this exact technique no longer functions. It is documented here because (a) legacy or unpatched systems may still run affected versions, and (b) the underlying lesson — different layers of a stack parsing the same string differently — recurs constantly in other forms (see: path traversal above, which is the same category of "different layer, different interpretation" bug).

**This is not a PHP-only historical footnote.** The null byte's behavior as a string terminator is a structural property of C, not a PHP-specific quirk — PHP was simply the language whose *own standard file-handling functions* were shown to be exploitable this way, and it fixed the problem at that layer. Modern high-level languages (Python, Node.js, Go) similarly guard their own standard library file APIs against embedded null bytes by default. The risk that persists is narrower but real: any application code that bypasses those guarded standard-library entry points — by calling native C/C++ extensions directly, using a Foreign Function Interface (FFI), or shelling out to legacy OS-level command execution — can reintroduce this exact mismatch if it doesn't independently validate for embedded null bytes before that boundary. The lesson to carry forward is architectural: know where your code crosses from a memory-safe, length-prefixed string representation into a null-terminated C-style one, and validate at that boundary specifically.

**Real-world precedent:** CVE-2012-5653 (Drupal core, prior to the PHP-level fix being universally deployed) — full details in `real-world-cve-case-studies.md`.

---

## Comparison Table

| Technique | Layer Exploited | Still Effective Today? | Fix |
|-----------|-----------------|--------------------------|-----|
| No validation | Application (absent) | Yes, wherever present | Implement any validation at all |
| Content-Type spoofing | Application (trusts client header) | Yes, very common | Magic-byte / file-signature inspection |
| Path traversal | Application (sanitization order) | Yes, common | Sanitize *after* decoding; use `basename()` + `realpath()` |
| Race condition (TOCTOU) | Application (operation ordering) | Yes, especially with modern race tooling | Validate before moving to a public/executable location |
| Double extension | Web server configuration | Only on misconfigured servers | Use `SetHandler`, not `AddHandler` |
| Null byte injection | Language runtime / OS API mismatch | No — patched since PHP 5.3.4 | N/A on modern PHP; historically, strict extension whitelisting |

---

## The One Fix That Defeats All Six

Every technique above is defeated simultaneously by the same combination:

1. **Decouple storage from the application server entirely** — the strongest version of this control streams uploads directly to isolated, script-incapable storage (e.g., an S3 bucket or Blob container with no execution capability), served from a separate domain. When the storage tier cannot execute anything, path traversal, extension tricks, and race conditions all become structurally irrelevant rather than merely blocked. Where a full architecture change isn't immediately available, the equivalent on a traditional server is: validate file content in an isolated, non-web-accessible location *before* the file can be reached by any request, and disable script execution at the web server level for any directory serving user content, independent of the validation logic.
2. **Re-process file content rather than only inspecting it** — for images specifically, re-rendering the upload through a graphics library (stripping anything that isn't genuine image data) defeats polyglot files that would otherwise pass a magic-byte check while still carrying executable content.
3. **Store with a system-generated filename** (UUID) — eliminates path traversal and extension tricks as a category, since the client's filename is never used to construct a path.

No blacklist of "known bad" extensions, headers, or filename patterns is required, because none of these three controls depend on anticipating a specific attacker technique.

---

## References

- CWE-434 (Unrestricted Upload): https://cwe.mitre.org/data/definitions/434.html
- CWE-367 (TOCTOU): https://cwe.mitre.org/data/definitions/367.html
- CWE-22 (Path Traversal): https://cwe.mitre.org/data/definitions/22.html
- CWE-626 (Null Byte Interaction Error): https://cwe.mitre.org/data/definitions/626.html
- PortSwigger File Upload Vulnerabilities: https://portswigger.net/web-security/file-upload
- OWASP File Upload Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html
