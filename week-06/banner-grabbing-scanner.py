import socket
import threading
import sys

# Thread lock to prevent output collision when multiple threads print simultaneously
print_lock = threading.Lock()


def grab_banner(s, port, target_host):
    """
    Attempt to retrieve the service banner from an open port.
    Banner reveals software name and version for CVE vulnerability matching.
    """
    try:
        # HTTP and HTTP-alt ports do not auto-broadcast a banner on connect.
        # Must send a HEAD request to prompt the server to respond with headers.
        if port in (80, 8080):
            request = f"HEAD / HTTP/1.1\r\nHost: {target_host}\r\n\r\n".encode()
            s.sendall(request)

        # Receive up to 1024 bytes and decode to readable string
        banner = s.recv(1024).decode("utf-8", errors="ignore").strip()

        # For HTTP responses, extract only the Server header line
        if "HTTP/" in banner:
            for line in banner.split("\n"):
                if "Server:" in line:
                    return line.strip()

        return banner if banner else "Open (No banner response)"

    except socket.timeout:
        return "Open (Banner grab timed out)"
    except Exception as e:
        return f"Open (Error: {type(e).__name__})"


def scan_port(target_host, port):
    """
    Scan a single TCP port and attempt banner grabbing if open.
    Runs in its own thread for concurrent execution.
    """
    s = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.5)

        # connect_ex() returns 0 on success, errno on failure (does not raise)
        result = s.connect_ex((target_host, port))

        if result == 0:
            banner = grab_banner(s, port, target_host)
            with print_lock:
                print(f"[+] Port {port:<5}/tcp OPEN   | [BANNER: {banner}]")

    except Exception:
        pass
    finally:
        # Guarantee socket is always closed, even if an exception occurs mid-scan
        if s:
            s.close()


def main():
    # Accept target IP as optional command-line argument
    # Usage: python3 banner-grabbing-scanner.py 10.48.134.77
    if len(sys.argv) == 2:
        target_host = sys.argv[1]
    else:
        target_host = "x.x.x.x"

    # Well-known ports covering common Red Team attack surface
    # FTP, SSH, Telnet, SMTP, HTTP, POP3, NetBIOS, HTTPS, SMB, HTTP-Alt
    target_ports = [21, 22, 23, 25, 80, 110, 139, 443, 445, 8080]

    print("-" * 65)
    print(f"[*] Target Locked: {target_host}")
    print("[*] Starting Multi-Threaded Banner Grabbing Scanner...")
    print("-" * 65)

    # One thread per port - acceptable for small fixed port lists (<=20 ports)
    # For large port ranges, use a Queue-based thread pool (see simple-port-scanner.py)
    threads = []
    for port in target_ports:
        t = threading.Thread(target=scan_port, args=(target_host, port))
        t.daemon = True  # Threads terminate automatically when main program exits
        threads.append(t)
        t.start()

    # Wait for all threads to finish before printing summary
    for t in threads:
        t.join()

    print("-" * 65)
    print("[*] Scan Completed!")


if __name__ == "__main__":
    main()
