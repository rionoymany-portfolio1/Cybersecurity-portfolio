# Network Security Audit Write-Up: 15-Scenario Simulation

> **Format:** Simulated audit scenarios combining log analysis, network topology review, and firewall ACL assessment
> **ISO 27001 Controls in Focus:** A.8.20 (Network Security), A.8.24 (Use of Cryptography), A.5.15 (Access Control)

---

## Scenario 1: Geo-Velocity Anomaly in Authentication Logs

**Setting:** SOC analyst reviews authentication logs during morning triage. Finds the following entries for a single user account:

```
2025-07-14 22:47:33 UTC   LOGIN SUCCESS   user: finance.manager@retailco.th   IP: 203.150.x.x [TH, Bangkok]
2025-07-15 03:12:18 UTC   LOGIN SUCCESS   user: finance.manager@retailco.th   IP: 91.108.x.x  [RU, Moscow]
```

**Analysis:**
- Time gap: approximately 4 hours 25 minutes
- Distance: Bangkok → Moscow ≈ 7,400 km
- Physical travel time required: ~10 hours minimum (direct flight)
- Conclusion: Both logins cannot represent the same physical person — one is anomalous

**GRC Audit Finding:**

- **Finding:** Geo-Velocity Anomaly — Probable Credential Compromise
- **Observation:** Authentication log shows successful login from Bangkok at 22:47 UTC and a second successful login from Moscow at 03:12 UTC (4h 25m later), using the same account. Travel time between these locations exceeds the time gap by a factor of 2+. This is a strong indicator of credential compromise.
- **Severity:** CRITICAL
- **Business Impact:** A compromised finance manager account grants unauthorized access to financial records and ERP systems, creating direct exposure to fraudulent transactions and data theft. If personal financial data of employees or customers was accessed, this constitutes a PDPA Section 37 violation — exposing the organization to regulatory investigation and penalties. An undetected breach of this nature, if later disclosed by a third party, would severely damage client trust and may trigger ISO 27001 nonconformity findings related to A.5.15 and A.8.16.
- **Root Cause:** No automated geo-velocity detection rule in SIEM. No step-up authentication triggered for geographically anomalous login.
- **Recommendation:**
  1. Immediately suspend the finance.manager account pending investigation
  2. Review all actions taken under this account in the 4h 25m window
  3. Implement SIEM rule for geo-velocity anomaly detection (configurable threshold)
  4. Implement Conditional Access / MFA step-up for logins from new geographies

  *Timeline:* Immediate (account suspension); 30 days (SIEM rule implementation) | *Owner:* SOC / IT Security Manager

---

## Scenario 2: Time-of-Day Anomaly — 3AM Access to Financial System

**Setting:** Internal audit reviewing ERP access logs flags unusual access pattern.

```
Date        Time (Local)   User              Action                   System
2025-07-20  03:14:07       erp.batch.user    SELECT * FROM invoices   ERP Database
2025-07-20  03:14:09       erp.batch.user    EXPORT TO CSV            ERP Database
2025-07-20  03:14:11       erp.batch.user    FILE TRANSFER 47MB       FTP Port 21
```

**Analysis:**
- Batch account accessing financial records at 3:14 AM is within normal pattern if scheduled jobs run overnight — this requires context
- However: data exported via FTP (port 21) — plaintext protocol — is the immediate finding
- 47MB CSV export = substantial data volume; could represent entire invoice database

**GRC Audit Finding — Finding 1:**

- **Finding:** Unencrypted Data Transfer via FTP
- **Observation:** ERP batch process exports financial data (47MB) via FTP (Port 21). FTP transmits data in plaintext — interceptable on any network segment between the ERP server and the FTP destination.
- **Severity:** HIGH
- **Business Impact:** A 47MB financial dataset transmitted in plaintext represents a critical data-in-transit exposure — any attacker with access to the same network segment can capture the entire invoice database with standard packet-capture tools. This directly violates ISO 27001 A.8.24 (Use of Cryptography) and may constitute a breach of PDPA Section 37(1) if the exported data contains supplier or employee personal information. Financial and reputational consequences include potential breach notification obligations, loss of client confidence, and certification body findings if discovered during a surveillance audit.
- **Root Cause:** No encryption policy enforced for scheduled data transfer jobs; FTP was configured at system setup and never reviewed against current security requirements.
- **Recommendation:** Replace FTP with SFTP (Port 22) or encrypt data before transfer. FTP listener on the destination server must be disabled after migration.

  *Timeline:* 14 days

**GRC Audit Finding — Finding 2:**

- **Finding:** Batch Account with Excessive Database Privileges
- **Observation:** erp.batch.user executes SELECT * against the invoices table. Principle of least privilege (A.5.15) requires batch accounts to have access only to the specific data required for their function. Full-table read on financial data requires justification.
- **Severity:** MEDIUM
- **Business Impact:** An over-privileged batch account increases the blast radius of any credential compromise — an attacker who gains control of this service account can exfiltrate the entire invoice dataset rather than a limited subset. This represents a failure of access control governance that would be flagged as a nonconformity against A.5.15 in any ISO 27001 audit, and may undermine the organization's ability to demonstrate the principle of least privilege to certification bodies or enterprise clients.
- **Root Cause:** No periodic review process for service account permissions; original permissions granted at project inception were never scoped down.
- **Recommendation:** Review batch account permissions; restrict to minimum required dataset; implement query-level access control.

  *Timeline:* 30 days

---

## Scenario 3: Firewall ACL Review — DMZ to Internal Zone

**Setting:** Network security audit reviews firewall configuration between the DMZ (web servers) and the Internal Zone (ERP, file servers).

**ACL reviewed:**

```
# Firewall: fw-main-01
# Rule set: DMZ → Internal

Rule 1:  PERMIT TCP 10.10.1.0/24 → 10.0.1.50 PORT 443   [Web to ERP API — justified]
Rule 2:  PERMIT TCP 10.10.1.0/24 → 10.0.1.0/24 PORT 22  [SSH — potentially over-broad]
Rule 3:  PERMIT IP  10.10.1.0/24 → 10.0.1.0/24 ANY      [ALL traffic DMZ to Internal — critical gap]
Rule 4:  DENY   IP  ANY → ANY                             [Implicit deny at bottom]
```

**Analysis:**
- Rule 1: Justified — web server calls ERP API
- Rule 2: SSH from entire DMZ subnet to entire internal subnet is over-broad. SSH should be restricted to specific jump-box IP, not the entire DMZ range
- Rule 3: **CRITICAL** — "PERMIT IP ANY ANY" from DMZ to Internal means any compromised DMZ server can reach any internal resource on any port. Rule 4's implicit deny is never reached for DMZ traffic

**GRC Audit Finding:**

- **Finding:** DMZ to Internal — Unrestricted Traffic Permitted (Rule 3)
- **Observation:** Firewall rule 3 permits ALL IP traffic from the DMZ subnet (10.10.1.0/24) to the internal network (10.0.1.0/24) on ANY port. This effectively eliminates DMZ isolation — a compromised web server can reach internal ERP systems, file servers, or any other internal asset without restriction. This negates the security value of the DMZ architecture entirely.
- **Severity:** CRITICAL
- **Business Impact:** A single compromised internet-facing web server becomes a direct pivot point into the organization's core internal systems, including ERP and file servers containing sensitive financial and personal data. This scenario represents the highest-tier breach risk — an attacker who exploits a web vulnerability can move laterally to the entire internal network without any additional barrier, potentially leading to ransomware deployment, full data exfiltration, and prolonged undetected presence. The financial exposure includes breach remediation costs, PDPA notification obligations, and the very real risk of losing ISO 27001 certification if discovered during an audit, directly impacting the organization's B2B client relationships that depend on that certification.
- **Root Cause:** Rule 3 appears to be a temporary troubleshooting rule ("permit any to fix connectivity") that was never removed.
- **Recommendation:**
  1. IMMEDIATELY remove or disable Rule 3 (or restrict to DENY)
  2. Replace with specific permit rules for documented, justified traffic flows
  3. Review all current firewall rules quarterly (configuration management)
  4. Implement a firewall rule change review process requiring security sign-off

  *Timeline:* Immediate (Rule 3 removal); 7 days (replacement rules); 30 days (process) | *Owner:* Network Security Engineer / CISO

---

## Scenario 4: SNMP v2 Enabled on Edge Routers

**Network scan output:**
```
Nmap scan: edge-router-01 (203.150.x.x)
PORT    STATE SERVICE VERSION
161/udp open  snmp    SNMPv2c public (community string: "public")
```

**Analysis:**
- SNMPv2c community string "public" = default, publicly known
- SNMPv2 transmits community strings in plaintext (no encryption)
- SNMP read access can expose full router configuration, routing tables, interface statistics
- SNMP write access (if configured) can modify routing — high-severity escalation path

**GRC Audit Finding:**

- **Finding:** SNMPv2 with Default Community String on Internet-Facing Router
- **Observation:** Edge router exposes SNMPv2 service on UDP/161 to the internet, using the default community string "public." SNMPv2c provides no encryption or authentication beyond the community string, which is transmitted in plaintext and trivially brute-forced. This provides any external attacker with read access to router configuration and potentially write access depending on community string configuration.
- **Severity:** CRITICAL
- **Business Impact:** Read access to the edge router's configuration exposes the organization's full internal network topology, IP addressing scheme, and routing paths — intelligence that dramatically reduces the effort required for a targeted attack. If write access is also available, an attacker can reroute network traffic, create persistent backdoors, or cause a total network outage, directly disrupting business operations and customer-facing services. This finding represents a violation of both A.8.20 (Network Security) and A.8.24 (Use of Cryptography), and would be classified as a critical nonconformity in an ISO 27001 audit, potentially placing the organization's certification at risk.
- **Root Cause:** SNMP was enabled at device deployment with factory default settings and no security hardening was applied before connecting to the internet-facing interface.
- **Recommendation:**
  1. Disable SNMP on the external interface immediately; restrict to management VLAN interface only
  2. Migrate to SNMPv3 with authentication (AuthNoPriv or AuthPriv mode)
  3. Change all SNMP community strings from defaults

  *Timeline:* Immediate | *Owner:* Network team

---

## Scenario 5: Guest Wi-Fi VLAN — Path to Internal Systems

**Topology:** Single physical switch hosts both Guest VLAN (VLAN 10, 10.0.2.0/24) and Corporate VLAN (VLAN 20, 10.0.1.0/24). Firewall sits between VLANs.

**Test result (Nmap from guest device):**
```
nmap -sn 10.0.1.0/24 (run from guest VLAN 10.0.2.50)

Host: 10.0.1.1    Up    (ERP server)
Host: 10.0.1.50   Up    (File server)
Host: 10.0.1.100  Up    (Domain controller)
```

**Firewall ACL finding:**
```
PERMIT icmp 10.0.2.0/24 10.0.1.0/24  [should be DENY]
PERMIT tcp  10.0.2.0/24 10.0.1.0/24 PORT 80,443 [unnecessary — guest should have internet only]
```

**GRC Audit Finding:**

- **Finding:** Inadequate Guest Wi-Fi Isolation — Internal Hosts Reachable
- **Observation:** A test device connected to the Guest Wi-Fi VLAN (10.0.2.0/24) successfully enumerated internal hosts including the ERP server, file server, and domain controller via Nmap scan. Firewall ACL analysis confirms ICMP and HTTP/HTTPS traffic is permitted from the guest VLAN to the internal VLAN. Guest network users (visitors, contractors, unmanaged devices) should have internet access only — no path to internal resources should exist.
- **Severity:** HIGH
- **Business Impact:** Any visitor, delivery person, or contractor who connects to the guest Wi-Fi can conduct reconnaissance of the internal network using freely available tools, with no authentication required beyond a Wi-Fi password. A successful follow-on attack from the guest network against internal hosts — particularly the domain controller — could result in full Active Directory compromise, affecting every user account and system in the organization. This also represents a third-party risk exposure that violates the network segmentation expectations of ISO 27001 A.8.20 and would be flagged immediately in any penetration test or certification audit.
- **Root Cause:** Firewall ACL between Guest and Corporate VLANs was not configured to deny all inter-VLAN traffic; ICMP and web traffic were permitted without documented justification.
- **Recommendation:**
  1. Update firewall ACL — explicit DENY ALL between Guest VLAN and Internal VLAN
  2. Permit only DNS (UDP/53) and DHCP (UDP/67-68) from guest VLAN to infrastructure
  3. Verify fix with post-remediation Nmap test from guest network

  *Timeline:* 7 days | *Owner:* Network Security Engineer

---

## Scenario 6: Telnet Enabled on Internal Switch

**Evidence:**
```
Port 23/tcp open on switch-floor-02.internal
```

- **Finding:** Telnet (Plaintext Remote Management) Active on Internal Network Switch
- **Observation:** Telnet service is enabled and accessible on an internal floor switch, allowing network device management credentials and session content to be transmitted in plaintext across the network.
- **Severity:** HIGH
- **Business Impact:** Any attacker with access to the same network segment — including a compromised endpoint or a guest-VLAN pivot — can capture Telnet credentials using passive packet capture, gaining administrative control over network infrastructure. Loss of switch administrative access enables an attacker to reconfigure VLANs, disable security controls, or create persistent access paths, representing a critical infrastructure integrity risk. This is a clear violation of A.8.24 (Use of Cryptography) and would constitute an audit finding against the organization's network device hardening standards.
- **Root Cause:** Legacy configuration applied at device deployment; no network device hardening standard in place or not enforced.
- **Recommendation:** Disable Telnet service on all network devices; enable SSH (Port 22) exclusively. Create and enforce a network device hardening configuration standard.

  *Control:* A.8.24 (Cryptography)

---

## Scenario 7: RDP Exposed to Internet

**Evidence:**
```
Nmap from internet: 203.150.x.x PORT 3389/tcp OPEN (RDP)
```

- **Finding:** Remote Desktop Protocol (RDP) Exposed Directly to the Internet Without MFA
- **Observation:** Port 3389/tcp (RDP) is accessible from the internet on a public IP address with no multi-factor authentication requirement, exposing remote desktop access to brute-force and credential-stuffing attacks.
- **Severity:** HIGH
- **Business Impact:** Internet-exposed RDP without MFA is one of the most commonly exploited initial access vectors in ransomware attacks — it is explicitly referenced in incident reports from organizations suffering ransomware deployment via this exact configuration. A successful brute-force or credential-stuffing attack results in authenticated remote access to an internal Windows host, from which lateral movement, data exfiltration, and ransomware deployment are all viable. The financial cost of a ransomware incident (recovery, downtime, potential ransom, PDPA notification) typically dwarfs the cost of implementing a VPN, and this finding would be considered a major nonconformity in any ISO 27001 audit.
- **Root Cause:** RDP opened directly to the internet for remote access convenience without implementing a VPN or MFA as a compensating control.
- **Recommendation:** Immediately restrict RDP to internal/VPN access only; remove from public exposure. Implement MFA for all remote access. Restrict RDP to known IP ranges if VPN is not immediately available.

  *Control:* A.8.20 (Network Security), A.5.15 (Access Control)

---

## Scenario 8: Weak TLS on Customer-Facing API

**Evidence:**
```
SSL Labs scan: retailco-api.com — Grade C
TLS 1.0 and 1.1 enabled; RC4 cipher suite permitted
```

- **Finding:** Deprecated TLS Versions and Weak Cipher Suites on Customer-Facing API
- **Observation:** The customer-facing API endpoint accepts connections using TLS 1.0 and TLS 1.1 (both deprecated since 2020 per RFC 8996) and permits the RC4 cipher suite, which has known cryptographic weaknesses and is prohibited under PCI DSS.
- **Severity:** HIGH
- **Business Impact:** Customers connecting to the API over TLS 1.0/1.1 or RC4 are exposed to BEAST, POODLE, and RC4-specific attacks that can decrypt session traffic, potentially exposing authentication tokens and personal data in transit. For an e-commerce platform, this creates direct PDPA Section 37(1) liability — the organization is required to implement "appropriate security measures" for personal data, and using cryptographically broken protocols does not meet that standard. This finding would also prevent compliance with PCI DSS requirements if cardholder data interfaces with this endpoint, and would result in a failed A.8.24 assessment during any ISO 27001 audit.
- **Root Cause:** TLS configuration was not reviewed or updated following deprecation announcements; no automated TLS posture monitoring in place.
- **Recommendation:** Disable TLS 1.0 and TLS 1.1; enforce TLS 1.2 minimum (TLS 1.3 preferred); remove RC4 from permitted cipher suites. Retest with SSL Labs post-remediation to confirm Grade A.

  *Control:* A.8.24 (Use of Cryptography — approved algorithms)

---

## Scenario 9: Version Disclosure on DMZ Web Server

**Evidence:**
```
Nmap -sV: Apache httpd 2.4.41 on dmz-web-01
```

- **Finding:** Web Server Version Banner Disclosed on Internet-Facing Host
- **Observation:** The internet-facing web server returns a full version banner (Apache httpd 2.4.41) in HTTP response headers, enabling targeted enumeration of version-specific CVEs without any active exploitation attempt required.
- **Severity:** MEDIUM
- **Business Impact:** While version disclosure is not directly exploitable, it dramatically lowers the cost of a targeted attack — an attacker queries the banner, identifies applicable CVEs from NVD, and proceeds directly to exploitation without a reconnaissance phase. Apache 2.4.41 is a 2019 release with multiple known vulnerabilities; combining version disclosure with an unpatched server creates a high-confidence exploitation path. From a GRC perspective, version disclosure reflects a failure of patch management governance (A.8.8) and increases the organization's attack surface in a way that would be noted in a penetration test report delivered to clients or certification auditors.
- **Root Cause:** Default Apache installation returns the Server header with version information; server hardening configuration was not applied; no patch management cycle enforced to keep the server on a current release.
- **Recommendation:** Suppress the Server version banner in Apache configuration (`ServerTokens Prod`); implement a patch management cycle with defined SLAs for critical and high CVEs; update Apache to the current stable release.

  *Control:* A.8.20 (Network Security), A.8.8 (Management of technical vulnerabilities)

---

## Scenario 10: No Active Network Monitoring

**Evidence:**
```
Question to IT team: "Where are your network flow logs and SIEM alerts?"
Response: "We have a firewall but don't review logs actively."
```

- **Finding:** Absence of Active Network Monitoring and Security Event Detection
- **Observation:** The organization has a perimeter firewall but does not actively review logs or operate any SIEM or alert-based monitoring capability. Security events — including intrusions, data exfiltration, and anomalous behavior — may go entirely undetected.
- **Severity:** HIGH
- **Business Impact:** Without active monitoring, the organization's mean time to detect (MTTD) a breach is effectively infinite — incidents are only discovered when the attacker chooses to make themselves visible (e.g., ransomware deployment) or when a third party reports the compromise. IBM's Cost of a Data Breach Report 2023 identifies detection and containment speed as the single greatest determinant of breach cost; organizations that identify breaches within 200 days spend on average $1.02M less than those that take longer. The absence of monitoring is a direct nonconformity against ISO 27001 A.8.16 (Monitoring activities), which requires that networks be monitored for anomalous behavior, and would be classified as a major finding in any certification audit.
- **Root Cause:** No security monitoring strategy or tooling investment; security operations treated as reactive rather than continuous.
- **Recommendation:** Implement SIEM with network flow analysis and defined use cases; establish alert thresholds and response procedures; assign responsibility for daily alert review to a named individual or team.

  *Control:* A.8.16 (Monitoring activities)

---

## Scenario 11: MAC Address Spoofing Bypassing 802.1X

**Evidence:**
```
802.1X port authentication configured on corporate switches.
Finding during test: Attacker device copies MAC of an authorized laptop.
Result: Switch grants access before certificate authentication completes.
```

- **Finding:** 802.1X Network Access Control Bypassable via MAC Spoofing
- **Observation:** The 802.1X implementation relies on MAC Authentication Bypass (MAB) as a fallback, allowing an attacker who copies the MAC address of a known-good device to gain network access before EAP-TLS certificate validation completes.
- **Severity:** HIGH
- **Business Impact:** An attacker who gains physical access to a network port — or who can observe a legitimate device's MAC address — can join the corporate network as an authenticated device, bypassing the organization's primary network access control mechanism. This undermines the entire 802.1X investment and places all internal systems within reach of an unauthenticated attacker. From a compliance perspective, this represents a gap in physical and logical access control (A.5.15, A.8.20) that would be exposed in any physical penetration test, and the finding would require documented compensating controls to maintain ISO 27001 certification.
- **Root Cause:** 802.1X configured with MAB fallback enabled; EAP-TLS certificate-based validation not enforced as the sole authentication path.
- **Recommendation:** Disable MAB fallback or reduce its window to zero; enforce certificate-based EAP-TLS as the sole 802.1X authentication method. Implement dynamic VLAN assignment to restrict access even for authenticated devices.

  *Control:* A.5.15 (Access Control), A.8.20 (Network Security)

---

## Scenario 12: Unrestricted Outbound DNS — Tunneling Risk

**Evidence:**
```
DNS queries leaving the network on UDP/53 are not logged.
```

- **Finding:** Outbound DNS Traffic Unmonitored — DNS Tunneling Exfiltration Undetectable
- **Observation:** DNS queries on UDP/53 leave the network without logging or restriction to designated resolvers. DNS tunneling — encoding data within DNS queries to exfiltrate information to an attacker-controlled domain — would be completely undetected under the current configuration.
- **Severity:** MEDIUM
- **Business Impact:** DNS tunneling is a well-documented data exfiltration technique used by both opportunistic attackers and advanced persistent threats precisely because DNS traffic is almost universally permitted through firewalls and rarely monitored. Sensitive data, including customer personal information subject to PDPA, could be exfiltrated over an extended period without triggering any alert. The absence of DNS monitoring also undermines the organization's ability to detect command-and-control communications from malware that uses DNS as a covert channel, representing a gap against A.8.16 and A.8.20.
- **Root Cause:** No DNS security policy; outbound DNS not restricted to controlled resolvers; no logging infrastructure for DNS traffic.
- **Recommendation:** Restrict outbound DNS to designated internal resolvers only; implement DNS logging and anomaly detection (high query volume to new domains, long subdomain strings); consider DNS filtering solutions for threat intelligence-based blocking.

  *Control:* A.8.20 (Network Security), A.8.16 (Monitoring activities)

---

## Scenario 13: Unencrypted Backup Transfer with SMBv1

**Evidence:**
```
Weekly backup job transfers 80GB from ERP server to NAS via SMB over the network.
No encryption in transit. SMB v1 in use (EternalBlue-vulnerable).
```

- **Finding:** Unencrypted Backup Transfer Using EternalBlue-Vulnerable SMBv1
- **Observation:** A weekly backup job transfers 80GB of ERP data to a NAS device using SMBv1 with no encryption. SMBv1 is the protocol exploited by EternalBlue (MS17-010), used in the WannaCry and NotPetya ransomware campaigns. The backup data is also transmitted in plaintext on the internal network.
- **Severity:** HIGH
- **Business Impact:** The dual exposure here is severe: the plaintext backup transfer allows any attacker with internal network access to capture an 80GB copy of ERP data passively (no exploitation required), while SMBv1 on any network-accessible system creates a remote code execution vector that has been weaponized in two of the most financially damaging ransomware attacks in history (WannaCry estimated $4–8 billion in global damages; NotPetya estimated $10 billion). The combination of unencrypted personal data in transit and a known critical vulnerability on a backup system creates simultaneous exposure under ISO 27001 A.8.24, A.8.8, and PDPA Section 37.
- **Root Cause:** Backup configuration not reviewed since initial setup; SMBv1 not disabled as part of system hardening; no encryption-in-transit requirement enforced for backup jobs.
- **Recommendation:** Upgrade to SMB v3 (which supports encryption); alternatively migrate backup transfer to SCP or SFTP. Disable SMBv1 organization-wide immediately via Group Policy. Encrypt backup data at rest and in transit.

  *Control:* A.8.24 (Use of Cryptography), A.8.8 (Technical vulnerability management)

---

## Scenario 14: OT/IT Flat Network — Legacy Manufacturing Segment

**Evidence:**
```
Legacy manufacturing floor segment connected to corporate network.
Firewall rule: PERMIT IP ANY ANY (because legacy PLCs require broad connectivity)
```

- **Finding:** Flat OT/IT Network — No Segmentation Between Manufacturing PLCs and Corporate Systems
- **Observation:** The legacy manufacturing floor segment (containing Programmable Logic Controllers) is connected to the corporate network with a firewall rule permitting all IP traffic in both directions. A compromise of any corporate device creates a direct path to manufacturing control systems, and vice versa.
- **Severity:** CRITICAL
- **Business Impact:** A ransomware infection or targeted attack originating from the corporate IT network can propagate directly to manufacturing PLCs, causing production line stoppages that, in manufacturing environments, can cost $500K–$1M+ per hour of downtime (per industry estimates). Conversely, a legacy, unpatched PLC compromised from the internet creates an attacker foothold directly inside the corporate network with no network-level barrier. OT/IT convergence attacks of this type have caused documented real-world manufacturing shutdowns; the absence of segmentation also represents a critical gap against ISO 27001 A.8.20 and would require compensating controls to be documented in the Statement of Applicability.
- **Root Cause:** Legacy OT systems require connectivity that cannot be easily scoped; segmentation was deferred indefinitely and no compensating controls were documented.
- **Recommendation:** Implement OT/IT network segmentation with a dedicated security appliance or unidirectional gateway (data diode) at the boundary. Where full isolation is not immediately feasible, document compensating controls in the risk register and Statement of Applicability. Engage an OT security specialist for a dedicated assessment.

  *Control:* A.8.20 (Network Security)

---

## Scenario 15: Log Retention Below Regulatory Requirement

**Evidence:**
```
System logs retained for 30 days.
PDPA investigation obligations and ISO 27001 A.8.15 require retention
sufficient to support incident investigation — typically 90 days minimum.
```

- **Finding:** System Log Retention Period Insufficient for Regulatory and Audit Requirements
- **Observation:** System and security logs are retained for only 30 days. This is insufficient to support incident investigation (most intrusions are detected weeks after initial compromise), PDPA compliance obligations, and ISO 27001 A.8.15 requirements for logging and log protection.
- **Severity:** MEDIUM
- **Business Impact:** If a security incident is detected after 30 days — which is common given that IBM's 2023 breach report shows a global average detection time of 204 days — there will be no logs available to reconstruct the attacker's actions, determine the scope of data access, or fulfill PDPA obligations to investigate and report data breaches. The inability to produce logs during a PDPA regulatory investigation or an ISO 27001 certification audit is itself a compliance failure, separate from the underlying incident. This gap also undermines the organization's ability to demonstrate due diligence in incident response, which directly affects both regulatory outcomes and civil liability.
- **Root Cause:** No documented log retention policy; default retention period applied without regulatory or security review.
- **Recommendation:** Extend log retention to 90 days minimum (1 year preferred for security-relevant logs); archive to immutable storage to prevent tampering; document the retention policy with legal review for PDPA obligations; review annually.

  *Control:* A.8.15 (Logging), A.5.33 (Protection of records)

---

## Summary: Audit Findings by Control

| Scenario | Severity | Primary Control | Category |
|----------|---------|-----------------|----------|
| 1 — Geo-velocity anomaly | Critical | A.8.16 + A.5.15 | Log analysis |
| 2 — 3AM FTP export | High | A.8.24 + A.5.15 | Log + config analysis |
| 3 — DMZ permit any any | Critical | A.8.20 | ACL review |
| 4 — SNMPv2 public | Critical | A.8.20 + A.8.24 | Config review |
| 5 — Guest VLAN reachable internal | High | A.8.20 | Topology + ACL |
| 6 — Telnet on switch | High | A.8.24 | Config review |
| 7 — RDP internet-exposed | High | A.8.20 + A.5.15 | Port scan |
| 8 — Weak TLS | High | A.8.24 | SSL scan |
| 9 — Version disclosure | Medium | A.8.8 | Config review |
| 10 — No monitoring | High | A.8.16 | Process gap |
| 11 — 802.1X bypass | High | A.5.15 + A.8.20 | Technical test |
| 12 — Unrestricted DNS | Medium | A.8.20 + A.8.16 | Config review |
| 13 — Unencrypted backup + SMBv1 | High | A.8.24 + A.8.8 | Config review |
| 14 — OT/IT flat network | Critical | A.8.20 | Architecture review |
| 15 — Short log retention | Medium | A.8.15 | Policy review |

---

## References

- ISO/IEC 27001:2022 Annex A controls cited throughout
- PDPA Thailand: https://www.pdpc.or.th/
- OWASP Top 10: https://owasp.org/Top10/
- NIST SP 800-41 (Firewall guidelines): https://csrc.nist.gov/publications/detail/sp/800-41/rev-1/final
- IBM Cost of a Data Breach Report 2023: https://www.ibm.com/reports/data-breach
