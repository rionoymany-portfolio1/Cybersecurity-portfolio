# Resources: Reference Index and Source Status Check

> **Purpose:** The sources that support the claims in this repository, with official URLs and the result of a status check
> **Status checks:** Original review on 18 October 2026; selected RFC and source-status entries rechecked on 23 October 2026
> **Abbreviations:** NIST = National Institute of Standards and Technology; CSF = Cybersecurity Framework; ISO = International Organization for Standardization; IEC = International Electrotechnical Commission; IETF = Internet Engineering Task Force; RFC = Request for Comments; BCP = Best Current Practice; STD = Internet Standard; OWASP = Open Worldwide Application Security Project; HTTP = Hypertext Transfer Protocol; TLS = Transport Layer Security; HTTPS = HTTP over TLS
> **Companion files:** [README.md](README.md) -- [WRITE-UP.md](WRITE-UP.md) -- [BUSINESS-IMPACT.md](BUSINESS-IMPACT.md)

---

## Bottom Line Up Front

| Item | Result |
|---|---|
| **Sources listed** | 10 foundational (used to support claims) and 5 supplementary (recommended for further reading) |
| **Currency finding 1** | RFC 8446 is **obsolete**. RFC 9846 is the current TLS 1.3 specification and also obsoletes RFC 5246, the previous TLS 1.2 specification; it also updates requirements for TLS 1.2 implementations. RFC obsolescence should not, by itself, be treated as protocol-version deprecation. |
| **Currency finding 2** | As of 23 October 2026, RFC 6265 remains the published cookie specification. Its revision, draft-ietf-httpbis-rfc6265bis-22, remains an Internet-Draft in the RFC Editor queue with final approval pending; no published replacement was found. |
| **Currency finding 3** | The current OWASP Top 10 edition is **2025**. |
| **Limitation** | The ISO/IEC 27001:2022 text is a paid standard and is not reproduced here; only its catalogue page status was checked. |

---

## Foundational Sources

| # | Resource | Publisher or author | Identifier and date | Official URL | Concepts supported | Status check (date stated in entry) |
|---|---|---|---|---|---|---|
| 1 | The NIST Cybersecurity Framework (CSF) 2.0 | NIST | CSWP 29, February 2024 | https://csrc.nist.gov/pubs/cswp/29/the-nist-cybersecurity-framework-csf-20/final | Six Functions; Govern Categories; Core structure | Final, published 26 February 2024; no later revision shown on the page (page opened) |
| 2 | NIST Cybersecurity Framework (landing page) | NIST | Web resource | https://www.nist.gov/cyberframework | Entry point to CSF 2.0 resources | Active; presents CSF 2.0 (page opened) |
| 3 | NIST CSF Frequently Asked Questions | NIST | Web resource | https://www.nist.gov/cyberframework/faqs | NIST position that it does not offer CSF-related certifications and has no plans for a conformity assessment program | Active; page opened and relevant FAQ checked directly on 23 Oct 2026 |
| 4 | NIST CSF 2.0 Informative References | NIST | Web resource | https://www.nist.gov/cyberframework/informative-references | Community-submitted ISO/IEC 27001:2022 mapping; NIST states that it does not conduct correctness testing on non-NIST-submitted mappings and that listing does not imply endorsement | Active; page opened and relevant statement checked directly on 23 Oct 2026 |
| 5 | ISO/IEC 27001:2022, Information security management systems -- Requirements | ISO and IEC | Third edition, 2022 | https://www.iso.org/standard/27001 | ISMS requirements; Annex A structure | Published; Amendment 1 (2024) is listed on the catalogue page (page opened). Standard text is paid and was not reproduced. |
| 6 | RFC 9110: HTTP Semantics | IETF (R. Fielding, M. Nottingham, J. Reschke, eds.) | STD 97, June 2022 | https://www.rfc-editor.org/rfc/rfc9110.html | Methods; safe and idempotent semantics; status codes 401, 403, 404, 422; the https scheme | Internet Standard; no "Obsoleted by" entry found (datatracker excerpt) |
| 7 | RFC 9112: HTTP/1.1 | IETF (R. Fielding, M. Nottingham, J. Reschke, eds.) | STD 99, June 2022 | https://www.rfc-editor.org/rfc/rfc9112.html | HTTP/1.1 message format; request-response model | Internet Standard; RFC Editor identifies [RFC 9931](https://www.rfc-editor.org/info/rfc9931/) as an update. RFC 9931 adds requirements concerning security of optimistic protocol transitions; it does not replace RFC 9112. Both RFC Editor pages checked on 23 Oct 2026. |
| 8 | RFC 9846: The Transport Layer Security (TLS) Protocol Version 1.3 | IETF (E. Rescorla) | Proposed Standard, July 2026 | https://www.rfc-editor.org/info/rfc9846 | TLS 1.3 handshake; server authentication; version comparison | Current TLS 1.3 specification; published July 2026; obsoletes RFC 8446 and RFC 5246 and specifies updated requirements for TLS 1.2 implementations. Official RFC Editor search result checked on 23 Oct 2026; a direct page open was rate-limited. Obsoleting RFC 5246 does not by itself establish that TLS 1.2 is formally deprecated. |
| 9 | RFC 8996: Deprecating TLS 1.0 and TLS 1.1 | IETF (K. Moriarty, S. Farrell) | BCP 195, March 2021 | https://www.rfc-editor.org/info/rfc8996/ | TLS 1.0 and 1.1 are formally deprecated | Current; confirmed by search-result excerpt and by RFC 9846's reference to it |
| 10 | RFC 6265: HTTP State Management Mechanism | IETF (A. Barth) | Proposed Standard, April 2011 | https://www.rfc-editor.org/rfc/rfc6265.html | Cookie purpose; Secure, HttpOnly, Domain, Path, Expires, Max-Age; cookie security considerations | Still the published RFC as of 23 Oct 2026; RFC Editor page checked directly. SameSite is not defined in RFC 6265 and is addressed in the pending revision draft (S4). |

---

## Supplementary Sources for Further Reading

| # | Resource | Publisher or author | Identifier and date | Official URL | Concepts supported | Status check (date stated in entry) |
|---|---|---|---|---|---|---|
| S1 | OWASP Top 10:2025 | OWASP Foundation | 2025 edition | https://owasp.org/Top10/2025/ | Examples of application-layer weaknesses that remain possible over HTTPS, such as A01:2025 Broken Access Control and A05:2025 Injection | Current edition; supersedes the 2021 edition (search-result excerpt) |
| S2 | Session Management Cheat Sheet | OWASP Cheat Sheet Series | Living document | https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html | Cookie attributes; session identifier renewal; session lifetime | Active (search-result excerpt) |
| S3 | Transport Layer Security Cheat Sheet | OWASP Cheat Sheet Series | Living document | https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Security_Cheat_Sheet.html | TLS protects data between its endpoints; forward secrecy considerations | Active (search-result excerpt) |
| S4 | Cookies: HTTP State Management Mechanism (draft-ietf-httpbis-rfc6265bis) | IETF HTTP Working Group | Internet-Draft | https://datatracker.ietf.org/doc/draft-ietf-httpbis-rfc6265bis/ | SameSite attribute and updated cookie requirements | As of 23 Oct 2026, draft-ietf-httpbis-rfc6265bis-22 remains an Internet-Draft, not a published RFC. IETF Datatracker lists it in the RFC Editor queue with status “blocked: Final Approval Pending”; page checked directly. |
| S5 | Recommendations for Secure Use of TLS and DTLS (RFC 9325) | IETF | BCP 195 | https://www.rfc-editor.org/info/bcp195/ | Further reading on TLS configuration recommendations | Listed on the BCP 195 page as the current recommendations document (search-result excerpt) |

---

## Superseded or Pending Items

| Item | Status found | Handling in this repository |
|---|---|---|
| **RFC 8446** (TLS 1.3, 2018) | Obsolete; obsoleted by RFC 9846 | Not cited as current; RFC 9846 is cited instead |
| **RFC 5246** (TLS 1.2) | Obsoleted by RFC 9846, which also specifies updated requirements for TLS 1.2 implementations | Mentioned only for version comparison; this document status alone does not mean TLS 1.2 is formally deprecated |
| **RFC 6265** (cookies) | Still published; revision pending (S4) | Cited for the currently published behavior; SameSite is attributed to the draft |
| **OWASP Top 10:2021** | Superseded by the 2025 edition | The 2025 edition is cited |
| **RFC 2818** (HTTP Over TLS) | Obsoleted by RFC 9110 | Not cited; RFC 9110 is used for the https scheme |

---

## Source Map

| Topic | Primary source | Used in |
|---|---|---|
| Six Functions; Govern Categories | NIST CSWP 29 (1) | WRITE-UP, Monday and Wednesday |
| CSF and ISO/IEC 27001:2022 relationship | NIST FAQs (3); NIST Informative References (4); ISO page (5) | WRITE-UP, section 1.3 |
| HTTP methods and status codes | RFC 9110 (6) | WRITE-UP, sections 3.2 and 3.3 |
| HTTP/1.1 model | RFC 9112 (7) | WRITE-UP, section 3.1 |
| TLS handshake and version context | RFC 9846 (8); RFC 8996 (9) | WRITE-UP, section 3.5 |
| Session cookies | RFC 6265 (10); OWASP cheat sheet (S2); revision draft (S4) | WRITE-UP, section 3.6 |
| Weaknesses that remain over HTTPS | OWASP Top 10:2025 (S1); OWASP TLS cheat sheet (S3) | WRITE-UP, section 3.4 |

---

## Notes on Use and Verification

- **Reading claim.** Listing a source means it supports the concepts in this repository. It is **not** a claim that every page or standard was read in full.
- **How status was checked.** Entries explicitly marked as checked on 23 October 2026 were opened or reviewed directly during this revision. Entries without that date retain the status notes from the original 18 October 2026 review. Earlier entries marked as search-result excerpts remain excerpt-based and should be opened directly before being relied on for a new status claim.
- **No quotations.** Source content is paraphrased. No quotations, page numbers, or publication details are included beyond what was checked.
- **Standards text.** Source documents are summarized and linked rather than copied.

---

*Return to: [README.md](README.md)*
