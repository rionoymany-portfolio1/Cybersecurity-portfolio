# Resources: ISO/IEC 27001 Annex A.7 Physical Controls and AWS Cloud Security

> **Scope:** Reference materials, whitepapers, and frameworks used to build the Annex A.7 Physical Controls simulation and the FinTrust Startup AWS Cloud Security assessment
> **Companion Files:** [Technical Write-Up](02-write-up-a7-and-aws-cloud-security.md) -- [Business Impact and Risk Analysis](03-business-impact-a7-and-aws-cloud-security.md) -- [Evidence Matrix](04-evidence-matrix-a7-and-aws-cloud-security.md)

---

## ISO/IEC 27001:2022 Standard and Supporting Documents

| Resource | Detail |
|---|---|
| ISO/IEC 27001:2022 (official) | Third edition -- main body Clauses 1-10 plus Annex A, Theme 7 (Physical Controls, 14 controls) |
| ISO/IEC 27002:2022 | Implementation guidance for Annex A controls, including detailed guidance text for each of the 14 A.7 controls |
| ISO/IEC 27000:2018 | ISMS vocabulary and definitions |

**Key A.7 structural facts (verified):**
- 14 controls total, numbered A.7.1 through A.7.14
- A.7.4 (Physical security monitoring) is a new control introduced in the 2022 revision, with no direct equivalent in the 2013 edition
- The 2013 edition spread physical and environmental security across the separate A.11 domain; the 2022 revision consolidated this into the single Annex A.7 Physical Controls theme

---

## Data Protection and Privacy Regulation

| Resource | Relevance |
|---|---|
| Regulation (EU) 2016/679 (GDPR), Article 5(1)(c) -- Data Minimization | Basis for the visitor logbook National ID number finding -- personal data must be adequate, relevant, and limited to what is necessary |
| Regulation (EU) 2016/679 (GDPR), Article 5(1)(e) -- Storage Limitation | Basis for the visitor logbook retention finding -- personal data must be kept no longer than necessary, with a defined retention period |
| Regulation (EU) 2016/679 (GDPR), Article 5(1)(f) -- Confidentiality (Integrity and Confidentiality principle) | Basis for the shared visitor logbook exposure finding -- personal data must be processed with appropriate security against unauthorized disclosure |

---

## AWS Cloud Security and Shared Responsibility Model

| Resource | Relevance |
|---|---|
| AWS Shared Responsibility Model (official AWS documentation) | Primary source for the Security OF the Cloud vs. Security IN the Cloud distinction applied throughout Project 2 |
| AWS Documentation -- IAM Database Authentication for MariaDB, MySQL, and PostgreSQL | Primary source for the RDS IAM Database Authentication remediation direction proposed for the Master Credential Sharing finding |
| AWS Documentation -- S3 Block Public Access | Reference for the account-level default-deny control proposed for the KYC document exposure finding |
| AWS Secrets Manager (official AWS documentation) | Reference for the centralized credential-management remediation direction proposed as a complement to IAM Database Authentication |
| AWS WorkSpaces (official AWS documentation) | Reference for Desktop-as-a-Service classification and MFA enforcement configuration for the developer remote access component of the FinTrust architecture |

---

## Cloud Service Models (IaaS / PaaS / SaaS)

| Resource | Relevance |
|---|---|
| NIST SP 800-145 -- The NIST Definition of Cloud Computing | Foundational reference for the IaaS/PaaS/SaaS service model classifications applied to the FinTrust architecture |

---

## GRC Frameworks Referenced

| Resource | Relevance |
|---|---|
| ISO 31000:2018 -- Risk Management | Risk classification and severity terminology applied throughout the Business Impact and Risk Analysis |

---

## Related Portfolio Entries

| Entry | Connection |
|---|---|
| Week 13 -- ISO/IEC 27001 Annex A.5 Deep-Dive and IPv4 Subnetting | A.7.2's physical access lifecycle parallels the Joiner-Mover-Leaver access governance model documented for A.5.15 in the prior week's entry |

---

## References

- ISO/IEC 27001:2022 (Third Edition), Annex A, Theme 7 -- Physical Controls
- ISO/IEC 27002:2022 -- Implementation guidance for Annex A controls
- Regulation (EU) 2016/679 (GDPR)
- AWS Shared Responsibility Model
- NIST SP 800-145 -- The NIST Definition of Cloud Computing

---

*Return to: [Week 14 README](week14-readme.md)*
