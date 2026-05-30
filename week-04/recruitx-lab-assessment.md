# RecruitX Web Application Assessment
## Lab-Based Vulnerability Report from Guided Pentest: Web (TryHackMe)

**Assessment Date:** May 2026  
**Scope:** Guided Pentest: Web Room (https://tryhackme.com/room/guidedpentestweb)  
**Platform:** TryHackMe Lab Environment  

---

This report demonstrates end-to-end vulnerability assessment methodology on a deliberately vulnerable web application. Findings and remediation recommendations reflect real-world security practices applied to a controlled lab environment.

---

EXECUTIVE VULNERABILITY ASSESSMENT & ENTERPRISE RISK REPORT

RecruitX Web Application | May 2026

Prepared For: Chief Risk Officer, Board of Directors, CISO

---

EXECUTIVE SUMMARY (1-Minute Read)

A critical attack chain affecting RecruitX can lead to unauthorized administrative access and large-scale data exposure. The vulnerability sequence has high likelihood of exploitation and significant potential impact to regulatory compliance, customer relationships, and operational continuity. Immediate executive action is required within 24-48 hours to contain risk and enable decision-making on remediation investment.

---

SITUATION AT A GLANCE

What We Found:
Four connected vulnerabilities permit unauthenticated external access to administrative accounts and sensitive data (2.3M candidate profiles, 450 client workforce strategies).

Attack Timeline:
From initial access to full system compromise: 2-3 hours.

Current Risk Status:
Critical. Vulnerability chain is technically feasible and likely unknown to the organization's current monitoring systems.

What This Means for the Business:
- Data exposure affecting 2.3M candidates and 450 enterprise clients
- Operational disruption risk (48-72 hour recovery window)
- Regulatory exposure under PDPA and employment law frameworks
- Estimated financial impact: USD 500M-$1B+ across breach, operational, regulatory, and reputational scenarios

Required Decision:
Allocate emergency budget (USD 50K-$150K) and assign executive ownership within 24 hours to activate containment measures.

---

SECTION 1: VULNERABILITY OVERVIEW

1.1 What Was Assessed

RecruitX Platform:
- 450+ enterprise clients
- 2.3M candidate profiles
- USD 8.5B annual transaction volume
- Real-time integration with enterprise HR systems
- Contains proprietary client workforce strategies and candidate PII

Assessment Scope:
Web application infrastructure (10.49.179.76) for unauthenticated entry points and privilege escalation pathways.

1.2 The Attack Chain: Four Connected Vulnerabilities

Vulnerability 1: Insecure Direct Object Reference (IDOR)

What It Is:
API endpoints at /api/user?id=[ID] lack authorization validation. Any unauthenticated person can modify the ID parameter and extract user data.

What Happens:
Attacker systematically retrieves administrator credentials (s.mitchell@recruitx.thm) without authentication.

Why It Matters:
Creates direct pathway to privileged account access and enables all downstream attacks.

---

Vulnerability 2: Password Reset Token Exposure

What It Is:
Password recovery mechanism displays reset tokens in plaintext HTTP response instead of secure email delivery.

What Happens:
Attacker uses stolen admin credentials to trigger password reset. Application displays active 6-digit token on screen. Attacker immediately resets password and hijacks admin account.

Why It Matters:
Converts credential leak into account takeover within minutes.

---

Vulnerability 3: Arbitrary File Upload via Extension Bypass

What It Is:
File upload validation uses blocklist (denies .php) but permits .phtml, .php5, .php7. Files stored in web-accessible directory.

What Happens:
Attacker uploads malicious .phtml file containing code execution payload. File becomes directly executable via HTTP request.

Why It Matters:
Provides mechanism to achieve arbitrary code execution on production server.

---

Vulnerability 4: Remote Code Execution (RCE)

What It Is:
Compromised web shell permits interactive command-line access to production server.

What Happens:
Attacker establishes reverse shell connection and gains full system privileges.

Why It Matters:
Grants complete access to databases, file systems, and internal infrastructure.

---

End-to-End Attack Sequence:

T+0:00 - IDOR exploitation extracts admin credentials
T+1:00 - Password reset hijacks admin account
T+1:30 - Malicious file uploaded to web server
T+2:00 - Code execution achieves system access
T+2:30 - Attacker begins data extraction and reconnaissance

Total time from initial access to complete system compromise: 2-3 hours.

---

SECTION 2: BUSINESS IMPACT ANALYSIS

2.1 Three Core Impact Scenarios

The vulnerability chain creates exposure across three primary impact categories. Financial ranges below represent conservative to high-impact scenarios based on industry breach data and RecruitX-specific factors (candidate volume, client contract values, regulatory exposure).

---

SCENARIO 1: Data Breach & Competitive Intelligence Loss

What Happens:
Attacker gains access to database containing 2.3M candidate profiles and 450 clients' workforce strategies.

Financial Impact (Conservative):
- Candidate data exposure: 2.3M records × USD 50 (dark web pricing) = USD 115M direct asset loss
- Client intellectual property theft: 5-10 high-value clients × USD 25M strategic value = USD 125M-$250M
- Total direct loss: USD 240M-$365M

Financial Impact (High):
- Complete database exfiltration becomes competitive advantage for attacker
- Estimated total impact: USD 300M-$500M

Likelihood:
High (90%+). Threat actor motivation for financial gain or competitive disruption is clear.

Regulatory Exposure:
PDPA violation for inadequate data protection. Estimated fine: USD 5M-$15M.

Timeline to Impact:
4-8 weeks. Typical dwell time for detection; longer delay increases likelihood of data monetization.

---

SCENARIO 2: Operational Disruption via Ransomware

What Happens:
Attacker deploys ransomware or deletes critical systems, forcing extended service outage.

Operational Impact:
- RecruitX generates USD 23.3M daily revenue (based on USD 8.5B annual)
- Estimated recovery time: 48-72 hours
- Revenue loss during downtime: USD 46.6M-$69.9M

Customer Impact:
- 450 corporate clients unable to access hiring platform
- 40-50% contract churn expected during and after incident: USD 100M-$150M lost annual revenue
- 2.3M candidates migrate to competitor platforms: USD 75M-$100M lost future value

Ransom & Recovery:
- Ransom demand: USD 2M-$10M
- Forensics and incident response: USD 1M-$3M
- System rebuilding: USD 5M-$10M

Total Operational Impact:
USD 228M-$342M

Likelihood:
Medium-High (70%). Depends on attacker motivation and detection timing.

Timeline to Impact:
Immediate upon exploit. Recovery window is 48-72 hours.

---

SCENARIO 3: Regulatory & Legal Liability

What Happens:
Breach triggers regulatory investigation and customer lawsuits.

Regulatory Exposure:
- PDPA fine for inadequate access controls: USD 5M-$15M
- Employment law violations (salary/contract exposure): USD 2M-$5M
- Operating license suspension risk: Potential

Legal Liability:
- Candidate class action (2.3M × USD 1,000 average settlement): USD 2.3B exposure
- Corporate client litigation (450 × USD 500K average): USD 225M exposure
- Defense costs: USD 50M-$100M

Total Regulatory & Legal:
USD 7M-$20M immediate fines + USD 2.5B-$2.7B litigation exposure

Likelihood:
High (80%+) for regulatory action. Medium (60%) for material customer litigation.

---

Impact Summary Table:

Scenario | Conservative | High-Impact | Probability | Timeline
--- | --- | --- | --- | ---
Data Breach | USD 240M | USD 500M | 90% | 4-8 weeks
Operational Disruption | USD 230M | USD 340M | 70% | 48-72 hours
Regulatory/Legal | USD 7M immediate + USD 2.5B litigation | USD 20M + USD 2.7B | 80% regulatory, 60% litigation | Months-years

**Total Potential Exposure: USD 500M-$1.3B across scenarios**

2.2 Scenario Probability & Timeline Impact

Detection speed directly affects financial damage:

Detection Timing | Attacker Capability | Expected Loss
--- | --- | ---
< 4 hours | Initial reconnaissance | USD 0-$50M
4-24 hours | Credential theft, database mapping | USD 50M-$200M
24-72 hours | Data exfiltration begins, ransomware deployment possible | USD 200M-$500M
72+ hours | Complete database download, persistence mechanisms, market intelligence sale | USD 500M-$1.3B+

Key Insight: Every 24 hours of undetected compromise increases financial exposure by approximately USD 100M-$200M.

2.3 Basis for Financial Estimates

These impact ranges are derived from:

Data Points:
- USD 8.5B RecruitX annual transaction volume (basis for daily revenue calculation)
- 450 enterprise clients at USD 150K-$500K average annual contract value
- 2.3M candidate profiles at USD 50 dark web pricing standard
- Industry breach settlement averages (Ponemon Institute, SANS, Verizon DBIR)
- PDPA statutory penalty ranges

Conservative Scenario:
Assumes limited data monetization, lower customer churn rate (40%), 4-week detection window.

High-Impact Scenario:
Assumes extensive data harvesting, maximum customer migration (50%), extended 8-week dwell time, organized threat actor involvement.

Confidence Level:
These are risk estimates, not guarantees. Actual impact depends on attacker sophistication, detection timing, and crisis response effectiveness. Ranges provided to enable decision-making under uncertainty.

---

SECTION 3: IMMEDIATE CONTAINMENT (24-48 Hours)

Three actions required within 24-48 hours to transition from uncontrolled to managed risk status.

Action 1: Emergency Network Restriction

What to Do:
- Restrict /admin and /api/admin/* endpoints to internal IP ranges only
- Deploy WAF rules to block external access to vulnerable endpoints
- Disable file upload functionality at web server level

Timeline:
2-4 hours

Owner:
Infrastructure/Network team with CISO approval

Business Impact:
Minimal. Internal staff retain full access; external attack surface eliminated.

Success Metric:
External network probes to admin endpoints receive 403 Forbidden.

---

Action 2: Disable Vulnerable Token Exposure

What to Do:
- Remove password reset token from HTTP response
- Implement manual admin password reset requiring CISO approval
- Disable file upload module until allowlist validation deployed

Timeline:
1-2 hours

Owner:
Engineering team with on-call support

Business Impact:
Manual password resets add 15-30 min per request; temporary friction acceptable.

Success Metric:
Password reset endpoint returns "Token will be sent via email" without displaying actual token.

---

Action 3: Forensic Investigation & Breach Detection

What to Do:
- Scan web server logs for suspicious API access patterns (/api/user?id=1,2,3...)
- Check for unauthorized password reset activity
- Search filesystem for unauthorized .phtml/.php5 files in /uploads/
- Review database audit logs for large data extraction queries
- Check system logs for reverse shell activity (netcat connections)

Timeline:
Initial scan: 2-4 hours
Comprehensive forensics: 24-48 hours

Owner:
CISO with external forensics firm if needed

Success Metric:
Determine breach status. If compromised, trigger incident response protocol (customer notification, regulatory disclosure).

Cost:
USD 50K-$150K if outsourced to external forensics firm

---

SECTION 4: SHORT-TERM REMEDIATION (1-4 Weeks)

Four structural fixes required to eliminate vulnerability chain.

Fix 1: Implement Server-Side Authorization

Technical Change:
API endpoints must validate that requesting user owns the requested resource or possesses admin role.

Implementation:
- Every API call requires valid authentication token + user verification
- Authorization check: "Does current_user match requested_resource_owner OR is current_user admin?"
- Deny-by-default for any unvalidated request
- Rate limiting: Max 10 requests per IP per minute

Timeline:
2 weeks

Owner:
Engineering lead

Success Metric:
- Penetration test confirms unauthenticated /api/user?id=X requests return 403 Forbidden
- All 50+ API endpoints validated for authorization checks

Cost:
USD 50K-$100K (engineering time + security review)

---

Fix 2: Redesign Password Reset Flow

Current State:
6-digit token, plaintext display, 15-minute window.

Redesigned State:
- Token: 32-character cryptographically secure string (2^190 entropy)
- Delivery: Encrypted email only; never displayed in UI
- Expiration: 10 minutes, single-use only
- Verification: Max 5 failed attempts before lockout
- For admin accounts: Optional SMS/authenticator OTP required

Timeline:
2 weeks

Owner:
Engineering lead

Success Metric:
- Penetration test cannot reuse tokens or guess token values
- Email delivery confirmed working
- Token entropy validated at >128 bits

Cost:
USD 30K-$50K

---

Fix 3: File Upload Security - Allowlist Validation

Current State:
Extension blocklist (blocks .php but allows .phtml, .php5, .php7).

New State:
- Only allow: .pdf, .docx, .xlsx, .jpeg, .jpg, .png, .gif
- Validate MIME type (don't trust client-supplied Content-Type)
- Scan files for malware using antivirus engine (ClamAV)
- Store in non-web-accessible location: /var/data/uploads/ (not /var/www/html/uploads/)
- Serve via authenticated download endpoint, not direct HTTP access

Timeline:
3 weeks (includes storage migration)

Owner:
Infrastructure + Engineering team

Success Metric:
- Upload of .phtml file is rejected
- Previously uploaded malicious files are isolated/removed
- All downloads require authentication + permission validation

Cost:
USD 80K-$150K (storage infrastructure, migration, testing)

---

Fix 4: Deploy Web Application Firewall (WAF)

Technical Change:
Runtime detection and blocking of common attack patterns.

Implementation:
- ModSecurity or Cloudflare WAF with OWASP Core Rule Set
- Block: SQL injection, directory traversal, file upload abuse, RCE patterns
- Configure in blocking mode (not just logging)
- Weekly tuning to reduce false positives

Timeline:
1 week

Owner:
Infrastructure team

Success Metric:
WAF blocks attack attempts; legitimate traffic passes through.

Cost:
USD 20K-$50K (annual service fee)

---

SECTION 5: LONG-TERM CONTROL UPLIFT (4-12 Weeks)

Three structural improvements to prevent recurrence and meet regulatory expectations.

Improvement 1: Security Development Lifecycle (SDLC) Integration

What It Does:
Embeds security checks into code deployment process to prevent future vulnerabilities.

Implementation:
- Mandatory security code review for authentication/authorization changes
- Automated vulnerability scanning (SAST) in CI/CD pipeline; fail builds on critical findings
- Weekly penetration testing against staging environment
- Threat modeling for all high-risk features before development

Timeline:
3 weeks setup; ongoing

Owner:
CISO + Engineering lead

Cost:
USD 50K-$100K (annual tooling + training)

---

Improvement 2: 24/7 Security Monitoring (SOC)

What It Does:
Real-time detection of exploit attempts and unauthorized access.

Implementation:
- Log aggregation from web server, database, firewall, system logs
- Automated alerts for: IDOR patterns, auth bypass attempts, RCE indicators, file upload abuse
- 24/7 security team on-call with 5-minute response time for critical alerts
- Incident response procedures documented and tested quarterly

Timeline:
6 weeks setup; ongoing

Owner:
CISO + Security operations team

Cost:
USD 100K-$200K initial setup + USD 400K-$600K annually (team + tooling)

---

Improvement 3: Quarterly Red Team Exercises

What It Does:
Validates security posture against real-world attack scenarios.

Implementation:
- Internal red team exercise quarterly (simulates attack chain)
- External penetration testing annually (third-party firm)
- Post-exercise reporting to Board with remediation tracking
- Use findings to prioritize future security investments

Timeline:
Ongoing quarterly cadence

Owner:
CISO + Red Team

Cost:
USD 50K-$100K annual (external pentest) + internal resource allocation

---

SECTION 6: REMEDIATION ROADMAP & INVESTMENT

Phase | Duration | Key Action | Owner | Budget
--- | --- | --- | --- | ---
Emergency Containment | 24-48 hours | Network ACLs, token disable, forensic scan | CISO/Infra | USD 50K-$150K
Code Remediation | 1-4 weeks | Authorization controls, password reset fix, upload validation | CTO/Engineering | USD 200K-$300K
WAF & Detection | 1-2 weeks | WAF deployment, initial monitoring | Infra/CISO | USD 40K-$70K
SDLC Integration | 3-4 weeks | Tooling, training, process updates | CISO/Engineering | USD 50K-$100K
SOC Standup | 6 weeks | Staffing, tooling, runbooks | CISO/Ops | USD 100K-$200K
Third-Party Validation | 4 weeks | External penetration test | CISO (outsourced) | USD 50K-$100K
--- | --- | --- | --- | ---
**Total One-Time Cost** | **4-12 weeks** | | | **USD 590K-$920K**
**Annual Ongoing Cost** | **Ongoing** | SOC team, tooling, training, pentesting | CISO | **USD 450K-$800K**

Financial Note: One-time cost of USD 590K-$920K prevents USD 500M-$1.3B exposure. Ongoing annual cost of USD 450K-$800K represents 0.05-0.09% of annual revenue.

---

SECTION 7: EXECUTIVE DECISION POINTS

Three specific questions requiring executive approval:

Decision 1: Activate Emergency Containment? (24-hour decision)

Question:
Approve emergency budget (USD 50K-$150K) and assign CISO as executive owner for 24-48 hour containment measures?

Outcome if Yes:
- External attack surface eliminated within 2-4 hours
- Forensic investigation determines breach status
- Decision to proceed with full remediation informed by forensics

Outcome if No:
- Vulnerability remains exploitable indefinitely
- Risk exposure: USD 500M-$1.3B financial loss, USD 5M-$20M regulatory penalties
- Estimated incident probability within 6 months: 70-80%

Recommendation:
Approve immediately. Risk of inaction significantly exceeds cost of containment.

---

Decision 2: Fund Short-Term Remediation? (1-week decision)

Question:
Allocate budget (USD 200K-$300K) and assign engineering resources for 1-4 week code remediation?

Outcome if Yes:
- Vulnerabilities eliminated by end of Week 4
- Third-party validation via penetration testing confirms remediation
- Platform returned to acceptable risk posture

Outcome if No:
- Vulnerabilities persist for 4-12 weeks (extended timeline for alternatives)
- Forensic investigation may reveal ongoing compromise during delay
- Each week of delay increases likelihood of exploitation by ~10-15%

Recommendation:
Approve. Short-term cost (USD 200K-$300K) prevents potential USD 500M+ loss from extended vulnerability window.

---

Decision 3: Invest in Long-Term Control Uplift? (2-week decision)

Question:
Fund 12-week program (USD 400K-$600K initial + USD 450K-$800K annually) to implement SOC, SDLC integration, and continuous testing?

Outcome if Yes:
- Industry-standard security operations established
- Regulatory expectations met (PDPA, ISO 27001 alignment)
- Recurrence of similar vulnerability chains prevented through continuous testing
- Board governance requirements satisfied

Outcome if No:
- Operational risk remains elevated post-remediation
- Regulatory compliance gaps persist
- Vulnerability likelihood increases over time as codebase evolves

Recommendation:
Approve. Annual cost (USD 450K-$800K) is 0.05-0.09% of revenue; ROI unlimited given risk prevention benefit.

---

SECTION 8: COMPLIANCE & GOVERNANCE ALIGNMENT

This vulnerability assessment maps to regulatory requirements:

Regulatory Framework | Requirement | Remediation Impact
--- | --- | ---
PDPA (Data Protection Act) | Implement technical controls for personal data | Authorization controls + WAF satisfy requirement
ISO 27001 (A.13, A.14) | Access controls, change management | SDLC integration + SOC monitoring required
NIST Cybersecurity Framework | Detect/Respond functions | 24/7 SOC directly addresses NIST Detect layer
Employment Law | Protect confidential employee/candidate data | All four short-term fixes required for compliance

Board Governance:
- Failure to remediate represents governance risk in cybersecurity oversight
- Board fiduciary duty requires documented cybersecurity risk management
- Remediation plan demonstrates proactive risk management to regulators and auditors

---

SECTION 9: CONCLUSION

Finding:
A material attack chain exposes RecruitX to significant operational, regulatory, and financial risk. Exploitation is technically feasible and likely to occur within 6-12 months without remediation.

Impact Magnitude:
Conservative estimate: USD 500M-$1B+ across multiple scenarios.

Recommended Action:
- Immediate (24-48 hours): Activate emergency containment
- Short-term (1-4 weeks): Implement code remediation
- Medium-term (4-12 weeks): Establish 24/7 SOC and SDLC controls
- Long-term (ongoing): Quarterly testing and continuous monitoring

Investment Required:
- One-time: USD 590K-$920K
- Annual: USD 450K-$800K

ROI:
Prevents USD 500M-$1.3B potential loss. Payback period: < 1 year.

---

APPENDIX A: TECHNICAL REFERENCES

Attack Timeline:
T+0:00 - IDOR: /api/user?id=1 returns admin credentials
T+1:00 - Password reset: 6-digit token displayed in response
T+1:30 - File upload: shell.phtml uploaded to /uploads/
T+2:00 - RCE: GET /uploads/shell.phtml?cmd=whoami returns www-data
T+2:30 - Reverse shell: Interactive command-line access established

Forensic IOCs (Indicators of Compromise):
- API logs: Sequential /api/user?id=[1-100] requests from external IP
- Upload directory: .phtml, .php5, .php7 files with recent timestamps
- Database logs: UNION-based query attempts or large SELECT statements
- System logs: netcat connection attempts, shell_exec() execution
- Process logs: Unauthorized command execution under www-data context

---

APPENDIX B: RISK DECISION MATRIX

Risk Element | Severity | Likelihood | Remediation Impact | Priority
--- | --- | --- | --- | ---
IDOR Exploitation | Critical | 95% | Eliminates with authorization controls | Immediate
Password Reset Bypass | Critical | 95% | Eliminates with token redesign | Immediate
File Upload RCE | Critical | 90% | Eliminates with allowlist + isolated storage | Immediate
Data Exfiltration | Critical | 85% | Reduced to low with early detection | High
Ransomware Deployment | High | 70% | Reduced to low with monitoring | High
Regulatory Fines | High | 80% | Compliance achieved with SDLC | Medium
Customer Churn | High | 70% | Risk acceptance with rapid response plan | Medium

---

**Report Classification: CONFIDENTIAL**
**Authorized Recipients: CRO, Board, CISO Only**

**Prepared by: Offensive Security Assessment Unit**
**Date: May 2026**

---

END OF REPORT
