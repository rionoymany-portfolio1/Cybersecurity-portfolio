import socket
import sys
from datetime import datetime
import threading
from queue import Queue

# Define target host and well-known port range to scan
target_host = "10.48.134.77"
port_range = [21, 22, 53, 80, 139, 443, 445, 3389, 8080]

# Record scan start time and display header
print("-" * 50)
print(f"Scanning Target: {target_host}")
print(f"Time Started: {str(datetime.now())}")
print("-" * 50)
print("[*] Initializing Multi-threading Scan...")
print("-" * 50)
print(f"{'PORT':<10}{'STATE':<10}{'SERVICE':<15}")
print(f"{'----':<10}{'-----':<10}{'-------':<15}")


def scan_port(port):
    try:
        # Configure socket and set timeout to prevent hanging
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.5)

        # Attempt to create full TCP three-way handshake (TCP Connect)
        result = s.connect_ex((target_host, port))

        if result == 0:
            # Specific exception handling: catch OSError when service name not found in database
            try:
                service = socket.getservbyport(port, 'tcp')
            except OSError:
                service = "unknown"

            # Display results in professional table format
            print(f"{f'{port}/tcp':<10}{'open':<10}{service:<15}")

        s.close()

    except socket.gaierror:
        print("\n [!] Hostname Could Not Be Resolved.")
        sys.exit()
    except socket.error:
        print("\n [!] Could Not Connect To Server (Network Down).")
        sys.exit()


# Thread worker logic for concurrent port scanning
def thread_worker(queue):
    while not queue.empty():
        # Prevent race condition when scanning the last ports in queue
        try:
            port = queue.get_nowait()
        except Exception:
            break

        scan_port(port)
        queue.task_done()


def main():
    # Populate port queue
    port_queue = Queue()
    for port in port_range:
        port_queue.put(port)

    # Start 4 threads for concurrent scanning
    threads = []
    for _ in range(4):
        t = threading.Thread(target=thread_worker, args=(port_queue,))
        # Set as daemon so threads terminate when main program exits
        t.daemon = True
        t.start()
        threads.append(t)

    try:
        # Wait for all threads to complete
        for t in threads:
            t.join()

        print("-" * 50)
        print("[*] Scan Mission Accomplished Successfully.")

    except KeyboardInterrupt:
        # Handle Ctrl+C signal for graceful exit
        print("\n[!] Scan interrupted by user. Exiting gracefully...")
        sys.exit(0)


if __name__ == "__main__":
    main()
