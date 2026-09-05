# Evidence Matrix: ISO/IEC 27001 Annex A.7 Physical Controls and AWS Cloud Security

> **Purpose:** Control-by-control and service-by-service evidence mapping across Design, Operating, and Effectiveness evidence categories, plus Auditor Testing Approach for AWS services
> **Companion Files:** [Technical Write-Up](write-up-a7-and-aws-cloud-security.md) -- [Business Impact and Risk Analysis](business-impact-a7-and-aws-cloud-security.md) -- [Resource and Reference Library](resource-a7-and-aws-cloud-security.md)

---

## How to Read This Matrix

Three evidence categories are used consistently across every control in this matrix:

- **Design Evidence** -- Does a documented control exist on paper (policy, procedure, configuration standard)?
- **Operating Evidence** -- Is the control being followed and configured correctly in practice, right now?
- **Effectiveness Evidence** -- Does the control demonstrably achieve its intended security outcome over a review period?

Full reasoning behind this three-way distinction, and the four evidence quality attributes (Authenticity, Timeliness, Completeness, Traceability) applied to specific artifacts below, is documented in the companion [Technical Write-Up](write-up-a7-and-aws-cloud-security.md).

---

## Part 1 -- ISO/IEC 27001:2022 Annex A.7 Physical Controls: Full 14-Control Evidence Matrix

| Control | Title | Design Evidence | Operating Evidence | Effectiveness Evidence |
|---|---|---|---|---|
| A.7.1 | Physical security perimeters | Documented facility security perimeter plan defining boundaries requiring access control | Physical inspection confirming perimeter barriers (fencing, walls, controlled doors) match the documented plan | Periodic perimeter walk-through audit with no undocumented breach points identified |
| A.7.2 | Physical entry | Physical Access Control Policy defining badge issuance, visitor sign-in, and entry logging requirements | Sample of badge access logs and visitor sign-in records for a defined period, showing entries consistent with policy | Quarterly access review confirming no former employees or expired visitors retain active access credentials |
| A.7.3 | Securing offices, rooms and facilities | Documented classification of secure areas (server room, records room) with corresponding access requirements | Confirmation that classified secure areas have the specific additional controls documented (dedicated locks, restricted badge groups) | No unauthorized entry incidents recorded for classified secure areas over the review period |
| A.7.4 | Physical security monitoring | CCTV and monitoring policy defining coverage areas, retention period, and review responsibility | Confirmation that CCTV coverage matches the documented coverage plan and that the storage system's configured retention matches the documented retention period | Sample review of retained footage confirming it is retrievable, viewable, and covers the full documented retention window (this is the control where the CCTV retention gap finding was identified -- see Business Impact file) |
| A.7.5 | Protecting against physical and environmental threats | Documented environmental risk assessment covering fire, flood, and power loss for facilities holding information assets | Confirmation that proportionate protections (fire suppression, water detection, UPS) are installed matching the risk assessment | Maintenance and test logs confirming environmental protection systems are tested at defined intervals and functioning |
| A.7.6 | Working in secure areas | Documented rules for staff and visitor behavior within secure areas (no unescorted visitors, no photography) | Staff and visitor briefing records confirming rules are communicated before secure area access is granted | Observation or spot-check confirming secure area rules are followed in practice, not only communicated on entry |
| A.7.7 | Clear desk and clear screen | Clear Desk and Clear Screen policy defining requirements for unattended workspaces | Periodic clear desk walk-through spot-check results | Trend of clear desk violations over successive walk-throughs showing the control is being sustained, not only enforced once |
| A.7.8 | Equipment siting and protection | Documented equipment placement standard addressing environmental hazard avoidance and visibility from public areas | Physical confirmation that server and network equipment placement matches the documented standard | No equipment damage or tampering incidents attributable to poor siting over the review period |
| A.7.9 | Security of assets off-premises | Remote and off-premises asset handling policy (laptop encryption requirement, device handling in transit) | Sample confirmation that off-premises devices (developer laptops) have required encryption and management agent enrollment active | Device inventory reconciliation confirming no off-premises assets are unaccounted for or missing required controls |
| A.7.10 | Storage media | Storage media lifecycle policy covering acquisition, labelling, use, and secure disposal of removable media | Media inventory log showing current removable media tracked with owner and location | Disposal log confirming media reaching end-of-life were disposed of per the documented secure disposal method, with no unaccounted-for media |
| A.7.11 | Supporting utilities | Documented utility resilience requirements (power, cooling, telecommunications) for facilities housing information processing equipment | Confirmation that backup power (generator, UPS) and redundant connectivity are provisioned matching the documented requirement | Test logs from scheduled failover or load tests confirming utility redundancy functions as intended when the primary utility is interrupted |
| A.7.12 | Cabling security | Cabling security standard addressing protection from interception, interference, and physical damage | Physical inspection confirming network and power cabling routing matches the documented standard (for example, separated pathways, protective conduit) | No cabling-related security incidents (interception, accidental damage causing outage) recorded over the review period |
| A.7.13 | Equipment maintenance | Equipment maintenance schedule and standard defining maintenance intervals and authorized maintenance personnel | Maintenance logs confirming scheduled maintenance was performed within defined intervals by authorized personnel | Equipment failure rate and unscheduled maintenance incident trend, used to confirm the maintenance schedule is adequate rather than reactive |
| A.7.14 | Secure disposal or re-use of equipment | Secure disposal and equipment re-use policy defining approved wiping or destruction methods before disposal or re-use | Disposal log confirming each decommissioned asset was processed through the documented method, with certificate of destruction where applicable | Sample verification (or vendor attestation review) confirming disposed media is genuinely unrecoverable, not only that a disposal process was followed on paper |

---

## Part 2 -- AWS Cloud Security: Evidence Matrix and Auditor Testing Approach

This matrix covers all six services referenced in the FinTrust Startup architecture (EC2, VPC, S3, RDS, Lambda, WorkSpaces), with the heaviest evidence and testing detail concentrated on S3, RDS, and WorkSpaces, reflecting where the Business Impact and Risk Analysis findings are concentrated.

### 2.1 Full Six-Service Evidence Matrix

| Service | Design Evidence | Operating Evidence | Effectiveness Evidence |
|---|---|---|---|
| EC2 | Documented server hardening and patching standard for guest operating systems | Sample confirmation that a running instance's OS patch level matches the documented standard, and that security group rules match the documented network access requirement | Vulnerability scan results over successive scan cycles showing patch compliance is sustained, not only correct at one point in time |
| VPC | Documented network segmentation design (subnet layout, route tables, security group and NACL rules) | Configuration export of actual VPC route tables, security groups, and NACLs, compared against the documented design | Periodic network configuration review confirming no undocumented or unapproved rule changes have been introduced since the last review |
| S3 | Documented data classification and storage standard specifying encryption and access requirements by data sensitivity tier | Bucket policy and Access Control List configuration export for the KYC document bucket, plus confirmation of the account-level Block Public Access setting | Access log review (S3 server access logging or equivalent) confirming actual access to the KYC bucket is limited to the specific application roles documented as authorized, with no anomalous or public access events |
| RDS | Documented database access control standard specifying authentication method and prohibition on shared credential use | Configuration confirmation of the authentication method actually enabled on the instance (IAM Database Authentication status, master user usage policy) | Database connection log or CloudTrail review confirming connections are attributable to individually identifiable IAM principals, with no ongoing use of the Master User account for routine developer access |
| Lambda | Documented function permission standard requiring least-privilege execution roles scoped per function | IAM execution role policy export for each function, compared against the documented least-privilege standard | Periodic review of unused or overly broad permissions granted to execution roles, confirming permissions are pruned rather than accumulating unused grants over time |
| WorkSpaces | Documented developer remote access standard requiring MFA enforcement for all WorkSpaces sessions | Confirmation that MFA is configured as a requirement in the WorkSpaces directory or identity provider configuration | Direct observation of a live login confirming MFA is actually prompted and enforced in practice, not only configured as a requirement in policy |

### 2.2 Auditor Testing Approach by Service (Priority Focus: S3, RDS, WorkSpaces)

| Service | Interview | Document Review | Observation | Sampling |
|---|---|---|---|---|
| S3 | Ask the engineering lead to describe the process for provisioning a new bucket and who approves public-access exceptions, if any | Review the bucket policy JSON and IAM policies attached to roles with access to the KYC bucket; confirm Block Public Access is enabled at the account level | Not typically applicable at the bucket-configuration level, since bucket policy state is fully captured by Document Review | Sample a set of S3 access log entries across a defined period to confirm access patterns match documented authorized roles, with no unexpected source |
| RDS | Ask developers directly how they currently connect to the production database when troubleshooting an issue -- this is the specific interview question that surfaces shared Master User credential use in practice | Review the RDS instance's authentication configuration (IAM Database Authentication enabled/disabled) and any documented database access standard | Not typically applicable, since authentication configuration is a static setting fully captured by Document Review | Sample a set of database connection or query logs across a date range to check whether entries are attributable to individually identifiable users or concentrated under a shared Master User account |
| WorkSpaces | Ask a sample of developers to describe their login process, to check whether their description matches the documented MFA requirement | Review the WorkSpaces directory or identity provider configuration confirming MFA is set as a requirement | Directly observe a live WorkSpaces login attempt to confirm an MFA prompt genuinely appears and is enforced, not merely configured | Sample a set of login events across multiple users and sessions to confirm MFA challenge events are consistently present in the authentication log |
| EC2 | Ask the infrastructure lead to describe the patching cadence and who is responsible for triggering it | Review the patch management policy and the most recent patch compliance report | Not typically applicable at the instance-configuration level | Sample a set of running instances and compare actual installed patch levels against the documented patching standard |
| VPC | Ask the network lead to describe the change-approval process for security group or route table modifications | Review exported security group rules, NACLs, and route tables against the documented network segmentation design | Not typically applicable, since network configuration is a static state fully captured by Document Review | Sample a subset of security group rules across the environment to check for undocumented overly permissive rules (for example, unrestricted inbound access) |
| Lambda | Ask the development lead to describe how function execution role permissions are decided and reviewed | Review IAM execution role policies attached to each function against the documented least-privilege standard | Not typically applicable, since execution role permissions are a static configuration fully captured by Document Review | Sample a subset of function execution roles to check for unused or overly broad permission grants accumulated over time |

**Why Document Review dominates cloud evidence-gathering, and why Observation is reserved narrowly:** as established in the companion write-up, most cloud control states are configuration artifacts rather than directly observable physical conditions, which is why Document Review appears as the primary testing method across nearly every service above. Observation is reserved specifically for WorkSpaces MFA in this matrix because it is the one control where a static configuration export (MFA is "enabled" in a policy setting) does not fully confirm the control's actual runtime behavior (an MFA prompt genuinely appearing and being enforced during a live session) -- the gap between configured intent and live behavior is exactly what Observation is suited to close, and exactly why it is not needed for the other, purely configuration-state controls in this matrix.

---

## References

- ISO/IEC 27001:2022 (Third Edition), Annex A, Theme 7 -- Physical Controls
- AWS Shared Responsibility Model
- AWS Documentation -- IAM Database Authentication for MariaDB, MySQL, and PostgreSQL
- AWS Documentation -- S3 Block Public Access

---

*Return to: [Week 14 README](week14-readme.md)*
