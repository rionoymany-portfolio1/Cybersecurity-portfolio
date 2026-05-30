# Week 4: Web App Pentesting and Passive Reconnaissance

> **Real Attack Chains + Intelligence Gathering**

---

##  Topics Covered This Week

### Room 1: Guided Pentest: Web
Learn web application pentesting by chaining vulnerabilities from recon to full server compromise.

**Tasks:**
1. Introduction
2. Reconnaissance and Enumeration
3. IDOR (Insecure Direct Object Reference)
4. Weak Password Reset
5. Admin Panel Access
6. Remote Code Execution (RCE)
7. The Attack Chain
8. Conclusion

### Room 2: Passive Reconnaissance
Learn about essential tools for passive reconnaissance without active probing.

**Tasks:**
1. Introduction
2. Passive Versus Active Recon
3. Whois - Domain ownership & registration data
4. nslookup and dig - DNS enumeration
5. DNSDumpster - Passive DNS reconnaissance
6. Shodan.io - Internet-wide device search
7. Summary

---

##  Learning Objectives

**By end of Week 4, you will:**
-  Understand complete web app attack chain (recon → exploitation → compromise)
-  Master IDOR vulnerability exploitation
-  Identify and exploit weak password reset mechanisms
-  Gain unauthorized admin access through discovered vulnerabilities
-  Achieve remote code execution on web servers
-  Use passive reconnaissance tools (whois, DNS, Shodan, DNSDumpster)
-  Know difference between passive and active reconnaissance
-  Gather intelligence without triggering security alerts

---

##  Why This Matters for Red Team

**Room 1: Guided Pentest - Attack Chain Thinking**

Real attacks don't exploit single vulnerabilities in isolation. They chain them:

```
Recon  
  ↓
Find target weakness (IDOR, password reset)
  ↓
Exploit weakness → Gain access
  ↓
Escalate privileges (admin panel)
  ↓
Remote code execution → Full compromise
```

**Room 2: Passive Recon - Intelligence Without Detection**

Professional attackers spend 70% of time on reconnaissance:
- Whois: Find company info, registrant, location
- DNS: Enumerate subdomains, mail servers
- Shodan: Discover exposed services, devices, metadata
- DNSDumpster: Map entire domain infrastructure

---

##  TryHackMe Rooms

### Room 1: Guided Pentest: Web
**URL:** https://tryhackme.com/room/guidedpentestweb
**Time:** 1 hours
**Difficulty:** Beginner to Intermediate
**Prerequisites:** Basic Linux, web familiarity

**What you'll do:**
- Enumerate a vulnerable web application
- Identify IDOR vulnerability
- Exploit weak password reset
- Access admin panel
- Execute code on server

### Room 2: Passive Reconnaissance
**URL:** https://tryhackme.com/room/passiverecon
**Time:** 1 hours
**Difficulty:** Beginner
**Prerequisites:** Basic networking (Week 3)

**What you'll learn:**
- Whois command and data interpretation
- DNS enumeration (nslookup, dig)
- DNSDumpster for passive mapping
- Shodan for device discovery

---

##  Connection to Previous Weeks

**Week 1-3 Foundation:**
- Linux (Week 1) → Use command line tools (whois, dig, nslookup)
- Python (Week 2-3) → Parse reconnaissance output into lists/dicts
- Data Structures (Week 3) → Store findings in organized format

**Week 4 Application:**
- Apply all previous skills to **real attack scenarios**
- Use Python to **automate reconnaissance** (later)
- Understand **why** each vulnerability matters

---

##  Next Steps

1. **Complete both TryHackMe rooms**
2. **Take detailed notes** on each vulnerability
3. **Document the attack chain** - how everything connects
4. **Study business impact** - why each vulnerability costs money
5. **Write the 6-part framework** - apply Week 2-3 structure

---

**Status:** Week 4 | Web Pentesting + Passive Recon | In Progress
