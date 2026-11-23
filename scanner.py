import socket
import threading
import argparse
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Global list to store open ports
open_ports = []

def scan_port(target, port):
    try:
        # Create a socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1) # 1 second timeout
        
        # Try to connect
        result = s.connect_ex((target, port))
        
        if result == 0:
            print(f"{Fore.GREEN}[+] Port {port} is OPEN")
            open_ports.append(port)
            
            # Try to grab banner (optional)
            try:
                s.send(b"Hello\r\n")
                banner = s.recv(1024).decode().strip()
                if banner:
                    print(f"    {Fore.CYAN}[*] Banner: {banner}")
            except:
                pass
                
        s.close()
    except Exception as e:
        pass

def main():
    parser = argparse.ArgumentParser(description="LiveMedia Port Scanner")
    parser.add_argument("-t", "--target", required=True, help="Target IP address")
    parser.add_argument("-p", "--ports", default="1-1000", help="Port range (e.g., 1-1000)")
    args = parser.parse_args()

    target = args.target
    port_range = args.ports.split("-")
    start_port = int(port_range[0])
    end_port = int(port_range[1]) if len(port_range) > 1 else start_port

    print(f"{Fore.CYAN}=== LiveMedia48 Port Scanner ===")
    print(f"{Fore.YELLOW}[*] Target: {target}")
    print(f"{Fore.YELLOW}[*] Scanning ports {start_port} to {end_port}...\n")

    threads = []
    for port in range(start_port, end_port + 1):
        t = threading.Thread(target=scan_port, args=(target, port))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print(f"\n{Fore.CYAN}[*] Scan complete. Found {len(open_ports)} open ports.")

if __name__ == "__main__":
    main()
