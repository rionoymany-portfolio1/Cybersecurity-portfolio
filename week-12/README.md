# Network Architecture Risk Assessment: Bridging Technical Topology with GRC Controls

> **Format:** Theoretical assessment — conceptual Packet Tracer topology reviewed through a GRC lens
> **Method:** AI-assisted simulation (Gemini) generating a realistic three-zone network scenario for GRC analysis practice
> **Approach:** Technical findings → ISO 27001 Annex A control mapping → Business impact translation

---

## Purpose of This Assessment

This exercise practices the skill most critical to a GRC analyst working alongside a technical team: taking a network diagram and producing not a list of technical misconfigurations, but a set of structured findings that connect each misconfiguration to a specific ISO 27001 control gap and a specific business consequence.

A network engineer reviewing this topology would note "PERMIT ANY ANY — that's wrong." A GRC analyst's output must say: this rule means X, it violates control Y, it creates regulatory/financial/operational exposure Z, and here is the corrective action with an owner and a deadline. That difference is the entire value of the GRC function in a technical conversation.

---

## Simulated Topology: FastBuy Three-Zone Architecture

### Zone Structure

```
INTERNET
    │
    │ (Public traffic)
    ▼
┌─────────────────────────────────────────┐
│  EDGE ROUTER                            │
│  - Gateway between internet and DMZ     │
│  - Performs basic packet routing        │
│  - No stateful inspection               │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│  STATEFUL FIREWALL (fw-main-01)         │
│  - Primary security enforcement point   │
│  - Rules define what crosses zones      │
└─────────────────────────────────────────┘
    │               │
    ▼               ▼
┌──────────┐   ┌──────────────────────────┐
│   DMZ    │   │     INTERNAL ZONE        │
│          │   │                          │
│ Web      │   │  IT Systems (ERP, file   │
│ Server   │   │  servers, endpoints)     │
│          │   │                          │
│ [!] Also │   │  Finance Department      │
│ hosts DB │   │  (separate VLAN planned  │
│          │   │  but not yet implemented)│
└──────────┘   └──────────────────────────┘
```

### Key Devices

| Device | Role | Zone |
|--------|------|------|
| Edge Router | Routing / gateway to internet | Perimeter |
| Stateful Firewall (fw-main-01) | Zone separation enforcement | Perimeter |
| Layer 2 Switch | VLAN assignment, port security | Internal |
| Web Server | Customer-facing e-commerce application | DMZ |
| Database Server | Customer PII storage | DMZ (misconfiguration) |
| Internal Workstations | Staff devices | Internal |
| Finance VLAN (planned) | Finance department isolation | Not yet implemented |

---

## Firewall Ruleset Review

**Current ruleset on fw-main-01:**

```
# Reviewed ruleset — fw-main-01
# Zones: Internet / DMZ / Internal

Rule 1:  PERMIT TCP INTERNET → DMZ PORT 80, 443     [Legitimate — web traffic]
Rule 2:  PERMIT TCP INTERNET → DMZ PORT 3389        [RDP exposed to internet — finding]
Rule 3:  PERMIT IP  DMZ → INTERNAL ANY              [ALL traffic — critical gap]
Rule 4:  PERMIT IP  INTERNAL → DMZ ANY              [Over-broad outbound]
Rule 5:  PERMIT IP  INTERNAL → INTERNET ANY         [Any outbound — no egress filtering]
[NO EXPLICIT DENY RULE AT BOTTOM]
Rule 6:  [Implicit allow on some firewall platforms  [Platform-dependent — dangerous assumption]
          if no explicit deny exists]
```

**Critical observation:** The absence of an explicit DENY-ALL rule at the bottom of the ruleset is a significant finding on any firewall platform. Most enterprise firewalls default to implicit deny at the end of a ruleset, but this behavior is platform-specific and must never be assumed. An explicit DENY-ALL must always be the final rule.

---

## Finding 1: No Implicit Deny — Firewall Relies on Assumed Default Behavior

**Observation:** The firewall ruleset does not include an explicit "DENY ALL" rule at the bottom. The current rules permit specific categories of traffic, but traffic not matched by any permit rule relies on the platform's default behavior (which varies by vendor and configuration).

**Severity:** HIGH

**Business Impact:** On firewall platforms where the default is "permit" rather than "deny" (some older or misconfigured devices), the absence of an explicit deny rule means all unmatched traffic flows freely — eliminating the security function of the firewall entirely. Even on platforms that correctly default to implicit deny (the majority of modern enterprise firewalls — Cisco ASA, Palo Alto, Fortinet), relying on assumed vendor behavior creates a hidden dependency that will fail silently if the platform changes, is replaced, or has its defaults modified by a configuration change. The principle of explicit intent in security configuration — stating what is permitted and denying everything else in writing — is a governance requirement, not merely a recommendation. A firewall ruleset that requires a reader to know the vendor's default behavior to understand its security posture is a documentation and change management risk.

**ISO 27001 Control:** A.8.21 (Security of network services)

**Root Cause:** Firewall configuration was not built from a secure baseline that mandates explicit deny-all as the final rule. No firewall change management process enforces this requirement.

**Recommendation:**
1. Add explicit DENY IP ANY ANY as the final rule on fw-main-01 immediately
2. Update firewall change management process to require explicit deny-all in all rulesets as a mandatory configuration element — any rule change submission missing this element should be rejected

*Owner:* Network Security Engineer | *Timeline:* Immediate

---

## Finding 2: Rule 3 — Unrestricted DMZ to Internal Traffic (PERMIT IP ANY ANY)

**Observation:** Firewall Rule 3 permits ALL IP traffic from the DMZ to the Internal zone on any port. This means any device in the DMZ — including the web server — can initiate connections to any device in the internal zone without restriction.

**Severity:** CRITICAL

**Business Impact:** The DMZ exists specifically to create an isolation boundary between internet-facing services and internal systems. Rule 3 eliminates that boundary entirely. A compromised web server (via any web application vulnerability) immediately becomes a foothold inside the internal network — reaching ERP systems, finance workstations, file servers, and any other internal resource without any additional barrier. The financial exposure includes a full internal network compromise propagating from a single web application vulnerability. For FastBuy's PDPA obligations, this means a web application breach could expose not just the customer database but internal HR records, internal communications, and any other data stored on internal systems.

**ISO 27001 Control:** A.8.20 (Networks security), A.8.22 (Segregation in networks)

**Root Cause:** Rule 3 was identified as a "troubleshooting rule" — a temporary permit-all added during a connectivity issue that was never removed after the issue was resolved. No change management process tracked the rule's addition or required its removal.

**Recommendation:**
1. Remove Rule 3 immediately
2. Replace with specific, justified permit rules for each documented DMZ→Internal traffic flow (e.g., web server to internal logging server on UDP/514 only)
3. Implement firewall rule review on a quarterly basis — any rule lacking a documented justification and expiry date is flagged for review

*Owner:* Network Security Engineer | *Timeline:* Immediate

---

## Finding 3: RDP (Port 3389) Exposed to Internet (Rule 2)

**Observation:** Rule 2 permits inbound TCP/3389 (Remote Desktop Protocol) from the internet to the DMZ. RDP is a remote administration protocol that should never be directly accessible from the internet without a VPN or MFA requirement.

**Severity:** HIGH

**Business Impact:** Internet-exposed RDP is one of the most commonly exploited initial access vectors in ransomware attacks. Brute-force and credential-stuffing attacks against RDP are fully automated and continuous — any internet-facing RDP endpoint will be probed within minutes of exposure. A successful authentication (through brute force or reuse of a credential from another breach) gives an attacker an authenticated remote desktop session from which lateral movement, data exfiltration, and ransomware deployment are all straightforward. For an e-commerce business handling customer PII, a ransomware event triggers mandatory PDPA breach notification even if the primary impact is business disruption rather than data theft.

**ISO 27001 Control:** A.8.20 (Networks security), A.5.15 (Access control)

**Root Cause:** RDP was opened directly to the internet for remote administration convenience, without implementing a VPN or MFA as a security prerequisite.

**Recommendation:**
1. Remove Rule 2 immediately — RDP must not be internet-accessible
2. Implement VPN for remote administration access; require all remote access to occur over VPN only
3. If RDP must be accessible, place behind MFA and restrict to a known set of administrator IP addresses as a minimum compensating control

*Owner:* Network Security Engineer / IT Manager | *Timeline:* Immediate

---

## Finding 4: No Egress Filtering — Unrestricted Internal-to-Internet (Rule 5)

**Observation:** Rule 5 permits all outbound traffic from the internal zone to the internet on any port. No egress filtering is applied.

**Severity:** MEDIUM

**Business Impact:** Without egress filtering, an attacker who has compromised an internal device can communicate with external command-and-control servers on any port, exfiltrate data without restriction, and use internal systems for external attacks. Specifically: DNS tunneling (encoding exfiltration traffic in DNS queries), HTTPS-encrypted C2 communication, and data exfiltration to cloud storage services are all undetectable and unrestricted under this ruleset. This is also a gap against A.8.16 (Monitoring activities) — meaningful monitoring requires that outbound traffic is controlled and inspected, not simply permitted without observation.

**ISO 27001 Control:** A.8.20 (Networks security), A.8.16 (Monitoring activities)

**Recommendation:**
1. Implement egress filtering — restrict outbound internet access to specific approved ports (80, 443, 53 to designated resolvers)
2. Route all HTTP/HTTPS traffic through a proxy for inspection
3. Enable DNS logging; restrict outbound DNS to corporate resolvers only

*Owner:* Network Security Engineer | *Timeline:* 30 days

---

## Finding 5: Finance VLAN Planned But Not Implemented

**Observation:** Network design documentation references a separate Finance VLAN for isolating the finance department's systems and data. This VLAN has not been implemented — finance workstations are currently on the same internal network segment as all other departments.

**Severity:** MEDIUM

**Business Impact:** Finance systems process payroll data, financial records, and bank account information. In the absence of VLAN isolation, any compromised internal workstation (in any department) can attempt lateral movement to finance systems without any additional network barrier. For a company handling this class of data, the absence of internal segmentation between departments increases the scope of any internal breach from one department to all departments simultaneously. This is a documented gap against A.8.22 (Segregation in networks) — the design intent exists but has not been operationalized.

**ISO 27001 Control:** A.8.22 (Segregation in networks)

**Root Cause:** Implementation deferred due to infrastructure project prioritization. Design approved but not executed.

**Recommendation:**
1. Prioritize Finance VLAN implementation within 60 days
2. Apply firewall ACL between Finance VLAN and General Internal — permit only specific, documented traffic flows
3. Document the current gap as a known risk in the risk register with an accepted interim risk level and target remediation date

*Owner:* Network Team | *Timeline:* 60 days

---

## Finding 6: Shadow IT — Unauthorized Connectivity Bypassing All Network Controls

**Observation:** As identified in the FastBuy risk register (Risk 002), the current network architecture has no technical enforcement preventing employees from connecting personal mobile hotspots to corporate devices. Traffic using alternate connectivity bypasses fw-main-01, all egress filtering, DLP, and proxy inspection entirely.

**Severity:** HIGH (cross-referenced with FastBuy risk register Risk 002)

**Business Impact:** From a network architecture perspective, a mobile hotspot connection creates a second network interface on the corporate device that is not visible to any corporate security control. The corporate laptop becomes a bridge between the corporate network and an uncontrolled internet connection. Any data transmitted over the hotspot interface travels without inspection. For FastBuy's customer PII, this creates an unmonitored data-in-transit path that is inconsistent with PDPA Section 37(1) security obligations.

**ISO 27001 Control:** A.8.20 (Networks security), A.8.21 (Security of network services), A.6.3 (Information security awareness)

**Recommendation:** See FastBuy Risk Register Risk 002 — 802.1X deployment, acceptable use policy update, and mandatory awareness training.

---

## GRC Analysis: Layer-to-Control Mapping

| Finding | OSI Layer | ISO 27001 Control | Business Domain |
|---------|-----------|-------------------|-----------------|
| No explicit deny rule | L3-L4 | A.8.21 | Network security governance |
| DMZ→Internal permit any | L3 | A.8.20, A.8.22 | Network architecture |
| RDP internet-exposed | L4 | A.8.20, A.5.15 | Access control |
| No egress filtering | L3-L4 | A.8.20, A.8.16 | Monitoring + egress control |
| Finance VLAN missing | L2-L3 | A.8.22 | Internal segmentation |
| Shadow IT / hotspot | L1-L2 | A.8.20, A.6.3 | Human + technical control |

---

## The GRC Analyst's Contribution in a Technical Assessment

A network engineer reviewing this topology would produce a list of misconfigurations and recommended fixes. A GRC analyst's output adds three things the technical list does not:

**1. Regulatory framing:** "PERMIT IP ANY ANY from DMZ to Internal" is a misconfiguration. Reframed: it means a web application vulnerability creates immediate PDPA breach notification exposure for 500,000 customer records. The first sentence is for the network team. The second sentence is what changes the CEO's prioritization of the fix.

**2. Control traceability:** Each finding maps to a specific ISO 27001 Annex A control. This creates an audit trail — when a certification auditor asks "how do you know your network security is adequate," the answer is not "our network team said so" but "our network architecture assessment found these gaps, mapped them to A.8.20 and A.8.22, and these corrective actions address them."

**3. Risk acceptance documentation:** Some findings will not be fixed immediately due to resource constraints (Finding 5 — Finance VLAN). The GRC analyst's role is to ensure that unaddressed findings are documented in the risk register with an explicit risk acceptance decision from an appropriate authority, a rationale, and a target remediation date — not left as implicit, undocumented gaps.

---

## References

- ISO/IEC 27001:2022 Annex A.8.20, A.8.21, A.8.22
- NIST SP 800-41 Rev 1 (Firewall guidelines): https://csrc.nist.gov/publications/detail/sp/800-41/rev-1/final
- PDPA Thailand Section 37: https://www.pdpc.or.th/

---

## Repository Structure

├── README.md                              (Index and project overview)
├── 
