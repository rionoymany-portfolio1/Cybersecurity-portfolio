# Technical Write-Up: NIST CSF 2.0, the Govern Function, and HTTP/TLS Fundamentals

> **Context:** Written for entry-level Governance, Risk, and Compliance (GRC) and cybersecurity consulting readers
> **Scope:** Monday (National Institute of Standards and Technology (NIST) Cybersecurity Framework (CSF) 2.0 overview, a comparison with ISO/IEC 27001:2022 from the International Organization for Standardization (ISO) and the International Electrotechnical Commission (IEC), and scenario practice), Wednesday (the Govern Function), Friday (Hypertext Transfer Protocol (HTTP), Transport Layer Security (TLS), HTTP over TLS (HTTPS), and session cookies)
> **Method:** Conceptual study and written summaries, using referenced sources to support key explanations and connecting each concept to a governance question
> **Scenario:** OrbitDesk, a fictional Software as a Service (SaaS) startup -- assumptions are listed in [BUSINESS-IMPACT.md](03-business-impact.md)
> **Companion files:** [README.md](01-README.md) -- [BUSINESS-IMPACT.md](03-business-impact.md) -- [RESOURCES.md](04-resource.md)

---

## Bottom Line Up Front

| Day | Key learning outcome | Why it matters for GRC |
|---|---|---|
| **Monday** | The six CSF 2.0 Functions describe one risk management picture, with **Govern** informing the other five. CSF 2.0 and ISO/IEC 27001:2022 are related but **not interchangeable**. | Gives a shared vocabulary for describing gaps, ownership, and next steps |
| **Wednesday** | Govern's six Categories (**GV.OC, GV.RM, GV.RR, GV.PO, GV.OV, GV.SC**) set direction, accountability, policy, oversight, and supplier expectations. | Without them, technical controls lack an owner and a standard to be measured against |
| **Friday** | HTTP and TLS basics explain what a web connection does and does **not** protect. Status codes and cookies are observable signals a reviewer can ask about. | Turns a policy statement into a specific, evidence-backed review question |

## What This Write-Up Is and Is Not

| Activity | Status |
|---|---|
| Studied CSF 2.0 Functions and Govern Categories | Conceptual study |
| Practiced describing gaps, impacts, and actions for a fictional startup | Written exercise |
| Reviewed HTTP, TLS, and cookie concepts against primary sources | Reading and summarizing |
| Configured a server, built an application, ran a penetration test, or deployed a control | **Not done** |
| Performed a formal assessment of the Govern Categories or of any real system | **Not done** |

---

## Monday: NIST CSF 2.0 Overview and Scenario Practice

### 1.1 The Six Core Functions

| Function | Purpose (paraphrased from NIST) | Example Categories | Plain-language question |
|---|---|---|---|
| **Govern (GV)** | Establish, communicate, and monitor the organization's cybersecurity risk management strategy, expectations, and policy | GV.OC, GV.RM, GV.RR, GV.PO, GV.OV, GV.SC (see Wednesday) | Who decides, on what basis, and who is accountable? |
| **Identify (ID)** | Understand the organization's current cybersecurity risks | ID.AM Asset Management; ID.RA Risk Assessment; ID.IM Improvement | What do we have, what could go wrong, and what matters most? |
| **Protect (PR)** | Use safeguards to manage those risks | PR.AA Identity Management, Authentication, and Access Control; PR.AT Awareness and Training; PR.DS Data Security; PR.PS Platform Security; PR.IR Technology Infrastructure Resilience | Which safeguards reduce the chance or the effect of a problem? |
| **Detect (DE)** | Find and analyze possible attacks and compromises | DE.CM Continuous Monitoring; DE.AE Adverse Event Analysis | How would we notice something is wrong? |
| **Respond (RS)** | Take action once a cybersecurity incident is detected | RS.MA Incident Management; RS.AN Incident Analysis; RS.CO Incident Response Reporting and Communication | What do we do, who does it, and who is told? |
| **Recover (RC)** | Restore assets and operations affected by an incident | RC.RP Incident Recovery Plan Execution; RC.CO Incident Recovery Communication | How do we return to normal operation? |

*Category lists are examples, not the full Core. The Core contains 22 Categories and 106 Subcategories (NIST CSWP 29). CSF Tiers, Profiles, and Subcategory-level detail were outside this week's study.*

### 1.2 How the Functions Fit Together

NIST presents the Functions as connected outcomes rather than steps completed once in a fixed order. Govern provides direction across all six Functions. Identify, Protect, and Detect include ongoing activities. Organizations also need continuing preparation for Respond and Recover; incident-response and recovery activities are carried out as needed, and lessons learned can inform improvements across the Functions.

```
GOVERN: direction, policy, roles, oversight, suppliers
  (provides direction across all six Functions)

IDENTIFY / PROTECT / DETECT: include ongoing activities
RESPOND / RECOVER: require ongoing preparation; actions occur as needed

All six Functions are connected; lessons learned can inform improvement.
```

**How the six Functions contribute to cybersecurity risk management:**

- **Preparing and reducing risk:** Govern, Identify, and Protect set priorities, build understanding, and apply safeguards before anything goes wrong.
- **Discovering and handling incidents:** Govern, Detect, Respond, and Recover cover noticing a problem, acting on it, and returning to normal operation.
- **Govern appears in both groups** because it supplies the strategy and accountability that the other Functions depend on.

### 1.3 CSF 2.0 and ISO/IEC 27001:2022: Conceptual Comparison

| Dimension | NIST CSF 2.0 | ISO/IEC 27001:2022 |
|---|---|---|
| **Publisher** | NIST (United States) | International Organization for Standardization (ISO) and International Electrotechnical Commission (IEC) |
| **Nature** | Voluntary framework describing cybersecurity **outcomes** | International standard specifying **requirements** for an information security management system (ISMS) |
| **Primary purpose** | Help organizations of any size understand, communicate, and prioritize cybersecurity risk management | Provide a repeatable management system for information security that an organization can be assessed against |
| **Structure** | Six Functions, 22 Categories, 106 Subcategories | Management-system clauses 4 to 10, plus Annex A (93 controls in four themes) |
| **Conformity assessment** | NIST states it has no plans for a conformity assessment program for the CSF | An ISMS can be independently assessed by an accredited body, which may issue a certificate; this is optional |
| **Typical use** | A common language for describing current gaps and priorities, including to executives and suppliers | Building a management system with documented scope, risk assessment, risk treatment, internal audit, and management review |

**Reading the relationship:**

- **Overlap, not equivalence.** A CSF outcome and an ISO/IEC 27001 control can address related concerns without being interchangeable in scope, wording, or evidence expectations.
- **Mappings need caution.** NIST's Informative References page lists a community-submitted ISO/IEC 27001:2022-to-CSF 2.0 mapping. NIST states that it does not test the correctness of non-NIST mappings and that listing one is not an endorsement.
- **Complementary use is possible.** This is a study conclusion, not a claim about any real organization: the CSF can help frame priorities, while ISO/IEC 27001 provides a structure for running and evidencing a management system.

### 1.4 Fictional Scenario and Initial Analysis Exercise

OrbitDesk is a fictional 12-person business-to-business (B2B) help-desk SaaS startup. It exists only to practice describing gaps and decisions. Its assumptions (A1 to A8) and eight illustrative gaps (R1 to R8) are in [BUSINESS-IMPACT.md](03-business-impact.md).

> **Label:** The scenario was written for this record. It is **not** a transcript of the original Monday exercise and does not describe any real organization.

**Approach used for the exercise:**

1. State the context: team, assets, data, and suppliers.
2. Describe a gap and map it to the Function it most relates to.
3. Separate technical impact from business impact.
4. Note possible regulatory or contractual consequences as conditional and requiring verification.
5. Identify who would be accountable, then propose an initial action and the evidence to request.

**Coverage of the illustrative gaps:**

| Function | Gaps analyzed | IDs |
|---|---|---|
| Govern | 2 | R1, R2 |
| Identify | 1 | R3 |
| Protect | 2 | R4, R5 |
| Detect | 1 | R6 |
| Respond | 1 | R7 |
| Recover | 1 | R8 |
| **Total** | **8** | |

Every Function has at least one gap, which keeps the exercise from collapsing into a purely technical checklist.

---

## Wednesday: NIST CSF 2.0 Govern (GV)

### 2.1 The Six Govern Categories

| Category | Name | Purpose (paraphrased) | What it gives the other Functions |
|---|---|---|---|
| **GV.OC** | Organizational Context | Understand the mission, stakeholder expectations, dependencies, and legal, regulatory, and contractual requirements that surround cybersecurity decisions | The "why" and "what matters" behind risk decisions |
| **GV.RM** | Risk Management Strategy | Establish priorities, constraints, risk tolerance and appetite, and assumptions, and use them to support risk decisions | A basis for ranking what Identify finds and what Protect addresses |
| **GV.RR** | Roles, Responsibilities, and Authorities | Define and communicate who is accountable for cybersecurity, with the authority and resources to act | Named owners for every other Function |
| **GV.PO** | Policy | Establish, communicate, and enforce cybersecurity policy | The requirements that safeguards are measured against |
| **GV.OV** | Oversight | Use the results of risk management activity and performance to review and adjust the strategy | A feedback loop across all Functions |
| **GV.SC** | Cybersecurity Supply Chain Risk Management | Establish and run processes for managing risk from suppliers and other third parties | Supplier expectations used by Identify, Protect, and Respond |

### 2.2 How Govern Guides the Other Five Functions

| Function | How Govern influences it | Conceptual example |
|---|---|---|
| **Identify** | GV.OC and GV.RM define which dependencies and risks matter and the risk appetite used to rank findings | A startup that holds customer data for many tenants ranks tenant isolation above a low-impact internal tool |
| **Protect** | GV.PO sets the requirements; GV.RR assigns owners | A policy sentence on encrypted transport is only actionable once someone owns certificate renewal |
| **Detect** | GV.RM sets what is worth monitoring; GV.RR assigns who reviews alerts | Monitoring effort is directed to authentication and access events because the risk strategy says they matter |
| **Respond** | GV.RR defines who may declare an incident and communicate; GV.SC sets supplier expectations during incidents | An incident involving a hosting provider needs a known contact path and a decision-maker |
| **Recover** | GV.RM sets recovery priorities; GV.OV reviews recovery performance | Restoring the customer-facing service before internal tooling follows a documented priority |

**Limitations of this section:** the Categories were studied at a high level. No Subcategory-level evaluation or assessment of a real organization was performed, and the examples above are conceptual illustrations.

---

## Friday: HTTP and TLS Handshake Fundamentals

### 3.1 The HTTP Request-Response Model

- A client (for example, a browser) sends a **request**: a method, a target, header fields, and optionally a body.
- The server returns a **response**: a status code, header fields, and optionally a body.
- HTTP is **stateless**: each request is processed on its own, so applications add state, such as a login session, through mechanisms like cookies.
- HTTP/1.1 messages are text-based, as specified in Request for Comments (RFC) 9112. The newer major versions keep the same request-response semantics defined in RFC 9110.

An illustrative exchange (host name and values are invented):

```
Request (client -> server)
GET /tickets/1042 HTTP/1.1
Host: app.orbitdesk.example
Cookie: session=<opaque-session-id>
Accept: application/json

Response (server -> client)
HTTP/1.1 200 OK
Content-Type: application/json

{"id": 1042, "status": "open"}
```

### 3.2 Common HTTP Methods

**Safe** means the request is not intended to change server state. **Idempotent** means repeating the same request has the same intended effect as sending it once. These are defined semantics, and an application can still depart from them, which is itself a review point.

| Method | Core semantics (RFC 9110, paraphrased) | Safe | Idempotent | Review note |
|---|---|---|---|---|
| **GET** | Request a current representation of the target resource | Yes | Yes | Reading and changing data should be kept separate; state changes behind GET are a design concern |
| **HEAD** | Like GET, but the response carries headers only, with no content | Yes | Yes | Support varies by server and framework; observe actual behavior |
| **POST** | Ask the target resource to process the request content according to its own semantics | No | No | Often used for logins and form submissions; apply authentication and authorization as appropriate to the endpoint, and validate input before processing it |
| **PUT** | Create or replace the target resource's state with the request content | No | Yes | Object-level authorization matters: who may replace which record? |
| **DELETE** | Request that the target resource be removed | No | Yes | High impact; benefits from authorization checks and audit logging |
| **OPTIONS** | Ask which communication options (for example, supported methods) exist for a resource | Yes | Yes | Responses depend on configuration; not an access control mechanism |

**HEAD and OPTIONS in practice:** both have specific defined semantics, but how a given application handles them depends on routing, framework defaults, and configuration. A reviewer should observe actual behavior rather than assume two systems respond identically.

### 3.3 Status Codes: 401, 403, 404, and 422

Two terms underpin the first two codes:

- **Authentication:** establishing who the requester is.
- **Authorization:** deciding what that requester is allowed to do.

| Code and RFC 9110 name | Standardized meaning (paraphrased) | Failure type | What it may signal in a review | Caution |
|---|---|---|---|---|
| **401 Unauthorized** | The request lacks valid authentication credentials for the target resource; the server includes a challenge telling the client how to authenticate | **Authentication** failure: missing, invalid, or expired credentials | Bursts may point to login problems or credential attacks | The name is historical; the meaning concerns authentication, not authorization |
| **403 Forbidden** | The server understood the request but refuses to fulfill it, including when valid credentials lack permission | **Authorization** failure: identity may be known, access is not allowed | Repeated 403s may indicate probing or misconfigured roles | A server may use 404 instead to avoid confirming a resource exists |
| **404 Not Found** | No current representation was found for the target resource, **or the server is not willing to disclose that one exists** | Resource not found, or deliberately not disclosed | Inconsistent use of 403 and 404 for the same kind of resource can reveal whether a record exists | The code does not say whether the condition is temporary or permanent |
| **422 Unprocessable Content** | The server understands the content type and the syntax is correct, but it could not process the instructions contained in the request | **Semantic or validation** failure; a syntax problem would be 400 | Patterns show how input validation behaves; error text should not expose internals | Originally "Unprocessable Entity" (WebDAV, RFC 4918); renamed in RFC 9110 |

**Review note:** a status code describes what a server reported for **one request**. It is a diagnostic or review signal, and a single code is not conclusive evidence of a vulnerability.

### 3.4 Plaintext Transmission and HTTPS

**Risks of sending HTTP without transport encryption:**

| Risk | What it means | Example |
|---|---|---|
| **Eavesdropping** | Anyone on the network path can read the traffic | Credentials or session cookies read on shared Wi-Fi |
| **Tampering** | Content can be altered in transit without the recipient noticing | A response modified before reaching the browser |
| **Impersonation** | The client cannot verify it is talking to the intended server | Traffic redirected to a look-alike host |

**HTTPS** is HTTP carried over TLS. RFC 9110 defines the HTTPS scheme, and TLS 1.3 is specified in RFC 9846.

| Security property | What it provides | What it does **not** mean |
|---|---|---|
| **Confidentiality** | Data is visible only to the two TLS endpoints | Does not hide all metadata, such as destination address or message size |
| **Integrity** | Modification in transit is detected | Does not validate that the data is correct or authorized |
| **Server authentication** | Certificate-based authentication helps the client verify the intended hostname when the certificate and proof of possession of the corresponding private key are validated | A valid certificate alone does not show that the site or its application is trustworthy or secure |

**What HTTPS does not do:**

- **It does not make application logic safe.** Weaknesses such as Broken Access Control (A01:2025) and Injection (A05:2025) in the Open Worldwide Application Security Project (OWASP) Top 10 remain possible over a valid TLS connection.
- **It protects the path between the two TLS endpoints only.** If TLS ends at a load balancer or proxy, traffic beyond that point depends on separate protections.
- **It does not protect a compromised client or server.** Malware on a device or a vulnerable server sits outside what TLS covers.

### 3.5 TLS Handshake: Conceptual Walk-Through

In a standard full TLS 1.3 handshake, the client and server negotiate parameters, authenticate the server, and establish shared keying material before protected application data is sent. The diagram below shows a **simplified certificate-based full handshake**, not every possible TLS 1.3 connection mode.

```
Client                                                  Server
  |  ClientHello (versions, cipher suites, key share)     |
  |------------------------------------------------------>|
  |        ServerHello (chosen parameters, key share)     |
  |<------------------------------------------------------|
  |  (encrypted from here) server certificate, proof of   |
  |  private-key possession, Finished                     |
  |<------------------------------------------------------|
  |  Finished                                             |
  |------------------------------------------------------>|
  |        HTTP requests and responses, encrypted         |
  |<----------------------------------------------------->|
```

| Phase | What happens | Purpose |
|---|---|---|
| **Negotiate** | The client offers supported versions, cipher suites, and key-exchange material; the server picks parameters | Agree on how the connection will be protected |
| **Establish keys** | Both sides combine key-exchange material to derive shared keying material | Provide the keys used to encrypt the rest of the handshake and later traffic |
| **Authenticate the server** | In certificate-based authentication, the server sends its certificate chain and a CertificateVerify signature demonstrating possession of the corresponding private key; the client validates the chain, trust, validity, and intended hostname | Establish who the client is talking to |
| **Confirm and begin** | Both sides confirm the handshake was not altered and switch to protected application traffic | Start the encrypted HTTP exchange |

**Version context.** The handshake is not identical across TLS versions:

| Aspect | TLS 1.3 | TLS 1.2 |
|---|---|---|
| **Specification** | RFC 9846, which obsoletes RFC 8446 | RFC 5246 (obsoleted by RFC 9846, which also specifies updated requirements for TLS 1.2 implementations) |
| **Full-handshake round trips** | One | Two |
| **Server certificate** | Sent after the ServerHello, so protected by encryption | Sent in clear text |
| **Key exchange** | Static RSA and static Diffie-Hellman suites removed; all public-key-based exchanges provide forward secrecy | Depends on the negotiated cipher suite; some suites lack forward secrecy |
| **Older versions** | TLS 1.0 and 1.1 are formally deprecated (RFC 8996) | |

**Notes:**

- RFC 9846 obsoletes the earlier TLS 1.2 specification RFC 5246 and specifies updated requirements for TLS 1.2 implementations. The status of an RFC document should not, by itself, be treated as proof that a protocol version has been formally deprecated.
- TLS 1.3 supports 0-RTT early data in certain session-resumption scenarios. Because early data can be replayed, applications must account for that risk before allowing such data. The mechanics and risks of 0-RTT, other session-resumption details, client certificates, and cipher-suite details were outside this week's study.
- A minimum-TLS-version statement (for example, "TLS 1.2 or later") is an **organizational policy decision**. This write-up does not claim that any external requirement mandates a particular version.

### 3.6 Session Cookies (Introductory)

HTTP is stateless, so after a user logs in, a web application commonly issues a **session identifier** in a cookie and uses it to recognize later requests. In this write-up, "session cookie" means a cookie that carries a session identifier; whether it persists after the browser closes depends on its lifetime attributes.

| Element | Purpose | Review note |
|---|---|---|
| **Session identifier** | Opaque value the server maps to a login session | Should be unpredictable and not placed in URLs (OWASP) |
| **Secure** | Cookie is sent only over HTTPS connections | Protects confidentiality in transit; RFC 6265 notes it does not by itself protect integrity against an active network attacker |
| **HttpOnly** | Keeps the cookie out of reach of client-side scripts | Reduces session theft through script injection such as cross-site scripting (XSS) |
| **SameSite** | Limits whether the browser sends the cookie on cross-site requests | Reduces exposure to cross-site request forgery (CSRF); defined in the revised cookie specification draft rather than RFC 6265; OWASP recommends setting it explicitly (Strict preferred, or Lax) |
| **Expires / Max-Age** | Sets the cookie's lifetime | OWASP recommends non-persistent cookies for session identifiers |
| **Domain / Path** | Limits which hosts and paths receive the cookie | Narrow scope reduces unintended exposure |

**Session lifecycle points from OWASP guidance:**

- Renew the session identifier after login or any privilege change (limits session fixation).
- End sessions on logout and after inactivity or a maximum lifetime.
- Transmit session cookies only over TLS.

**Scope:** cookies were reviewed at an introductory level. No cookie behavior was tested in a browser or an application.

### 3.7 Connecting Web Security Fundamentals to GRC

- **Policy becomes reviewable.** A statement such as "customer-facing traffic uses encrypted transport" can be tested once a reviewer can ask for a hostname list and TLS scan output.
- **Ownership must be named.** Certificate renewal, session settings, and error handling need accountable owners (GV.RR).
- **Signals are not verdicts.** Status codes, response headers, and logs give evidence to ask about; interpreting them needs context, and any vulnerability claim needs appropriate technical testing beyond this study.

The detailed Concept-to-GRC mapping is in [BUSINESS-IMPACT.md](03-business-impact.md).

---

## References

Sources, official URLs, and status checks are listed in [RESOURCES.md](04-resource.md).

---

*Return to: [README.md](01-README.md)*
