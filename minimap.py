import socket
import threading
import queue
import argparse
import time

HEADER = 1024                                           # No. of bytes of data to receive from Target
num_threads = 150                                       # Maximum number of active threads

port_queue = queue.Queue()
print_lock = threading.Lock()                           # For thread safe printing

# Port Scanner
def scan(host):
    while True:
        try:
            port = port_queue.get(timeout=1)            # Gets ports from the Queue
        except queue.Empty:
            break

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # Creates a socket object
        s.settimeout(2)                                         # Sets the Socket to timeout after 5 seconds
        try:
            result = s.connect_ex((host, port))                 # Returns 0 if connection is successful
            if result == 0:
                banner_grab(s, port)                            # Calls Banner function if connection is Successful
        except socket.timeout:
            with print_lock:
                print(f"Socket: Port {port} timed out")
        except socket.error:
            with print_lock:
                print("Socket: Connection error")
        except Exception as e:
            with print_lock:
                print(f"Error: {e}")
        finally:
            s.close()                                           # Closes the socket
            port_queue.task_done()                              # Tells the Queue that Task was completed



# Banner Grabber
def banner_grab(s, port):

    msg = None

    # Send a specific protocol request based on common services running on specified port
    if port == 21: msg = b"HELP\r\n"; service = "FTP"
    elif port == 22: service = "SSH"
    elif port == 23: msg = b"\r\n"; service = "TELNET"
    elif port == 25: msg = b"HELO example.com\r\n"; service = "SMTP"
    elif port == 80 or port == 8080: msg = b"HEAD / HTTP/1.0\r\n\r\n"; service = "HTTP"
    elif port == 110: msg = b"USER test\r\n"; service = "POP3"
    elif port == 143: msg = b"a1 CAPABILITY\r\n"; service = "IMAP"
    elif port == 443: service = "HTTPS"
    elif port == 3306: service = "MySQL"
    else: service = "Unknown Service"

    # Banner Grabbing Logic
    try:
        if msg:
            s.sendall(msg)                                          # Sends protocol request
        banner = s.recv(HEADER).decode().strip()                    # Receives 1024 bytes from the Target after connecting

        lines = banner.splitlines()                                 # Splits the banner into lines
        if len(lines)<3:                                            # If the number of lines in banner is less than 3
            with print_lock:                                        # then prints the first line
                print(f"\nPort {port} is open")
                print(f"Service: [{service}]  \nBanner:\n{lines[0]}")
        else:                                                       # Otherwise prints first three lines
            with print_lock:
                print(f"\nPort {port} is open")
                print(f"Service: [{service}]  \nBanner:\n{lines[0]}\n{lines[1]}\n{lines[2]}")
    except socket.timeout:
        with print_lock:
            print(f"\nPort {port} is open")
            print(f"    Service: {service}  Banner: Banner Grabbing failed")
    except socket.error as e:
        with print_lock:
            print(f"\nPort {port} is open")
            print(f"    Service: {service}  Banner: Banner not found on port {port}: {e}")
    except ValueError:
        with print_lock:
            print("\nPort {port} is open")
            print("Unable to retrieve banner; Please try again.")
    except Exception as e:
        with print_lock:
            print(f"Error: {e}")



# Main Function
def main():

    # Argument Parser
    parser = argparse.ArgumentParser(description="Port Scanner")

    # Flag for Host
    parser.add_argument("-H", "--host", dest="host", help="IP address or domain to scan", required=True)

    # Flag for Ports
    parser.add_argument("-P", "--ports", dest="ports", help="Port or range of ports to scan (e.g. 22 or 20-80)", default='1-1024')

    args = parser.parse_args()
    host = args.host
    port_range = args.ports

    # Divides the input range into two parts( lower limit and upper limit of ports to scan)
    if '-' in port_range:
        lower, upper = port_range.split("-")
        lower = int(lower)
        upper = int(upper)
    else:
        lower = upper = int(port_range)

    # Checks if the port range is valid
    if not (1 <= lower <= 65535) or not (1 <= upper <= 65535) or lower > upper:
        print("Invalid range")
        exit(1)

    # test: scanme.nmap.org
    try:
        host = socket.gethostbyname(host)
    except socket.gaierror:
        print("Hostname could not be resolved")
        exit(1)

    # Puts ports into the queue
    print("\nMinimap started...")
    print(f"Scanning {host}")
    for port in range(lower, upper + 1):
        port_queue.put(port)

    # Creates Threads
    threads = []

    for _ in range(num_threads):
        thread = threading.Thread(target = scan, args  = (host,))
        thread.daemon = True
        thread.start()
        threads.append(thread)



# Calls the main function
# Detects for keyboard interrupts to stop the scan
if __name__ == "__main__":
    start = time.time()
    main()
    try:
        while True:
            if not port_queue.empty():
                time.sleep(1)
            else:
                break
    except KeyboardInterrupt:
        print("Scan Stopped by User")
        exit(1)
    port_queue.join()
    duration = time.time() - start
    print(f"\nScan Completed in {duration:.2f} seconds\n")