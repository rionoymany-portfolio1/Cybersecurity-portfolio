# Network Fundamentals for GRC Analysts

> **Purpose:** Not "how to configure a network" but "how to audit one"
> The OSI model is a diagnostic framework for identifying where a security control operates — and therefore what it can and cannot protect.

---

## Why Networking Knowledge Is Non-Negotiable for GRC

ISO 27001:2022 Annex A.8.20 (Network Security) requires:
> "Networks and network devices should be secured, managed and controlled to protect information in systems and applications."

(Note: Annex A controls use "should" — they describe implementation guidance. The binding obligation comes from the main body clauses which use "shall." An organization must *apply* A.8.20 if selected in the Statement of Applicability, but the control text itself uses "should" to describe how.)

Auditing whether that control is implemented requires knowing what "managed and controlled" looks like technically. A GRC analyst who cannot read a firewall rule list, interpret a network topology diagram, or distinguish between a VLAN tag and a routing decision cannot assess whether A.8.20 is actually met — only whether a policy document claiming to meet it exists.

**The audit questions that require network knowledge:**
- Is the DMZ genuinely isolated from the internal network, or is the firewall ACL permitting unexpected traffic?
- Does the guest Wi-Fi VLAN have any path to internal systems?
- Is SNMP (unencrypted management protocol) exposed to external networks?
- Was the FTP server flagged in the risk register, and has it actually been replaced with SFTP?

---

## The OSI Model — 7 Layers, Audit Lens

```
┌─────────────────────────────────────────────────────────┐
│  Layer 7 — Application    HTTP, HTTPS, DNS, FTP, SMTP  │  ← WAF, content filtering, DLP
│  Layer 6 — Presentation   TLS/SSL, encoding, JPEG      │  ← Encryption (A.8.24)
│  Layer 5 — Session        Session establishment, auth  │  ← Session management controls
│  Layer 4 — Transport      TCP, UDP, port numbers       │  ← Firewall port-level rules
│  Layer 3 — Network        IP addresses, routing, ICMP  │  ← Firewall IP-level rules, routing ACLs
│  Layer 2 — Data Link      MAC addresses, VLAN tags     │  ← VLAN segmentation, 802.1X
│  Layer 1 — Physical       Cables, switches, wireless   │  ← Physical access controls, CCTV
└─────────────────────────────────────────────────────────┘
```

### Layer-by-Layer Audit Relevance

**Layer 1 — Physical**

What it does: The actual transmission medium — cables, fiber, wireless radio frequencies, network interface hardware.

Audit relevance:
- Physical access controls (server room locks, CCTV) protect Layer 1 assets
- Unauthorized physical access to a switch allows Layer 2 attacks (MAC flooding, unauthorized VLAN trunk)
- Related control: A.7.1 (Physical security perimeters), A.7.2 (Physical entry)
- **Key GRC principle:** A CCTV camera is a physical/Layer 1 control. It does not mitigate a Layer 7 application vulnerability (SQL injection) or a Layer 3 routing misuse. Proposing physical access controls as the mitigation for a database intrusion finding reflects a misunderstanding of where the vulnerability operates.

---

**Layer 2 — Data Link**

What it does: Frames data for transmission on the local network segment. Operates on MAC addresses. The layer where VLANs are defined.

Audit relevance:
- VLAN segmentation operates at Layer 2 — it defines which devices can communicate at the switch level
- A guest VLAN and a corporate VLAN can share the same physical switch while being logically isolated (if properly configured)
- MAC address spoofing attacks target this layer
- 802.1X port authentication (requiring a certificate or credential before a device gets Layer 2 access) is a common enterprise control

**Audit finding example — inadequate VLAN separation:**
```
Network topology shows Guest VLAN (10.0.2.0/24) and Internal VLAN (10.0.1.0/24)
on the same switch. Firewall ACL review shows:
  PERMIT ip 10.0.2.0/24 10.0.1.0/24 (unexpected — should be DENY)
  
Finding: Guest network has unrestricted IP-level access to internal network segment.
Layer 2 VLAN tag does not enforce isolation when Layer 3 routing rules permit traffic.
The control appears in the network diagram but is not enforced in the actual config.

ISO 27001 Control: A.8.20 (Network Security)
Severity: HIGH
```

---

**Layer 3 — Network**

What it does: Routes packets between networks using IP addresses. The layer where routers and Layer 3 firewalls operate.

Audit relevance:
- Firewall ACLs at Layer 3 filter traffic by source IP, destination IP, and protocol
- Network segmentation between DMZ, internal zone, and external is enforced here
- ICMP (ping) operates at Layer 3 — blocking unnecessary ICMP reduces reconnaissance surface

**Critical distinction for audit:** A firewall that shows VLAN separation in a diagram but has a permissive "permit any any" rule in its ACL is a paper control, not a functioning one. The audit must review the actual running config, not the diagram.

---

**Layer 4 — Transport**

What it does: Establishes end-to-end connections. TCP (connection-oriented, reliable) and UDP (connectionless, fast). Defined by port numbers.

Audit relevance:
- Port numbers determine which service is being accessed (HTTP = 80, HTTPS = 443, SSH/SFTP = 22, FTP = 21, SNMP = 161)
- Firewall rules at Layer 4 restrict which ports are accessible from which networks
- "Least privilege" in network controls means: only the ports required for a specific business function are permitted

**Key port-to-protocol mappings for GRC:**

| Port | Protocol | Status | Control Implication |
|------|----------|--------|---------------------|
| 20/21 | FTP | ❌ Non-compliant | Plaintext file transfer — violates A.8.24; replace with SFTP (22) or FTPS (port 990 implicit / port 21 explicit with AUTH TLS) |
| 22 | SSH / SFTP | ✅ Compliant | Encrypted remote access and file transfer |
| 23 | Telnet | ❌ Non-compliant | Plaintext remote admin — violates A.8.24; replace with SSH (22) |
| 80 | HTTP | ⚠️ Context-dependent | Plaintext web traffic — non-compliant for authentication pages (violates A.8.24) |
| 161/162 | SNMP v1/v2 | ❌ Non-compliant | Network management protocol with known weaknesses; use SNMPv3 |
| 443 | HTTPS (TLS) | ✅ Compliant | Encrypted web traffic — enforce TLS 1.2 minimum |
| 3389 | RDP | ⚠️ High-risk | Remote desktop — should never be exposed to external networks; requires MFA |

---

**Layer 5 — Session**

What it does: Manages the opening, maintenance, and closure of communication sessions.

Audit relevance:
- Session management vulnerabilities (session fixation, insufficient expiry) operate here
- Relevant to application security audit, less commonly a primary GRC audit focus at Layer 5 specifically

---

**Layer 6 — Presentation**

What it does: Data formatting, encoding, and encryption/decryption at the application interface level (TLS operates between Layers 5-7 in practice).

Audit relevance:
- TLS certificate validation and cipher suite configuration are Layer 6 concerns
- Weak cipher suites (RC4, DES, 3DES) represent a cryptographic control failure
- Related control: A.8.24 (Use of Cryptography) — includes requirements for key management and approved algorithms

---

**Layer 7 — Application**

What it does: The network services applications directly use. HTTP, DNS, SMTP, LDAP, APIs.

Audit relevance:
- Most web application vulnerabilities operate here (SQL injection, XSS, IDOR, file upload)
- WAF (Web Application Firewall) operates at Layer 7
- DNS poisoning, LDAP injection, API security all at this layer
- Related controls: A.8.20, A.5.15, A.8.24

---

## TCP/IP Model — Mapping to OSI

The TCP/IP model is the practical implementation model used in real networks. Understanding both is useful because vendors and engineers use TCP/IP language, while many security standards use OSI language.

```
TCP/IP Model           OSI Equivalent            Examples
─────────────────────────────────────────────────────────────
Application Layer   → Layers 5, 6, 7          HTTP, DNS, SMTP, TLS
Transport Layer     → Layer 4                 TCP, UDP
Internet Layer      → Layer 3                 IP, ICMP, routing
Network Access      → Layers 1, 2             Ethernet, Wi-Fi, MAC
```

**Practical implication for GRC:**
When a vendor provides a security assessment referring to "Application Layer controls," they mean ISO's Layers 5–7 (Session + Presentation + Application). A WAF is an Application Layer (TCP/IP) control. When a penetration test report refers to "Network Layer exposure," they mean IP-level (Layer 3 in OSI, Internet Layer in TCP/IP). These are not interchangeable in audit findings — misattributing a Layer 3 routing issue to "application security" leads to the wrong remediation owner.

---

## OSI Layer Diagnostic Framework for Audit Findings

When writing an audit finding, identifying the layer at which the vulnerability operates determines:
1. **Which technical control addresses it** (WAF at L7 ≠ firewall ACL at L3)
2. **Who owns the remediation** (Network team for L1–L3; application team for L4–L7)
3. **Which Annex A control applies**

**Quick diagnostic table:**

| Vulnerability | Layer | Annex A Control | Remediation Owner |
|--------------|-------|-----------------|-------------------|
| Unsegmented guest Wi-Fi reaches internal servers | L2-L3 | A.8.20 | Network team |
| FTP used for file transfer | L4 | A.8.24 | Network/IT team |
| Password transmitted over HTTP | L4-L7 | A.8.24 | Application team |
| SQL injection in web application | L7 | A.8.29 (Secure coding) | Development team |
| Physical server room unlocked | L1 | A.7.2 | Facilities/Security team |
| SNMP v2 enabled on edge router | L4 | A.8.20 | Network team |

---

## Common GRC Audit Misattributions to Avoid

**Misattribution 1: "We have CCTV on the server room — database is protected"**
- CCTV = physical/Layer 1 control
- Database breach = Layer 7 (application) threat
- A Layer 1 control does not mitigate a Layer 7 vulnerability
- Correct: Layer 7 controls (WAF, parameterized queries, NIDS) are required

**Misattribution 2: "We have a firewall, so our web app is secure"**
- Perimeter firewall = Layer 3–4 control (IP and port filtering)
- SQL injection = Layer 7 vulnerability
- A firewall that allows TCP/443 (HTTPS) will not inspect the SQL payload inside the HTTPS request
- Correct: A WAF is required for Layer 7 application-layer control

**Misattribution 3: "Our VLAN segmentation means guest devices can't reach internal systems"**
- VLAN tag = Layer 2 configuration
- Routing between VLANs = Layer 3 decision (firewall/router ACL)
- VLAN separation without a firewall ACL enforcement is ineffective — traffic can still be routed between VLANs
- Correct: Layer 2 VLAN + Layer 3 ACL deny rule together form the control

---

## Key Takeaway: Controls Must Match the Layer

A security control only mitigates threats that operate at the same layer (or can intercept traffic at that layer). A GRC analyst who can articulate which layer a finding operates at — and therefore which control is actually responsive — is the one who writes audit reports that result in the right fix, not just any fix.

---

## References

- Cisco: OSI Reference Model explanation — https://www.cisco.com/c/en/us/about/press/internet-protocol-journal/back-issues/table-contents-3/21-osi.html
- IANA Port Number Registry: https://www.iana.org/assignments/service-names-port-numbers/
- ISO/IEC 27001:2022 Annex A.8.20 (Network Security), A.8.24 (Use of Cryptography)
- OWASP Network Security Testing Guide: https://owasp.org/www-project-web-security-testing-guide/
