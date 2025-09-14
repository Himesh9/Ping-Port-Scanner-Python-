import subprocess
import socket
import platform

# Function to check if host is live or not live
def ping_host(ip):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    result = subprocess.run(['ping', param, '1', ip], stdout=subprocess.PIPE)
    if result.returncode == 0:
        return f"{ip} is live"
    else:
        return f"{ip} is not live"

# Function to scan ports on a given IP and check if they are open or closed
def scan_ports(ip, port_range):
    open_ports = []
    for port in port_range:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)  # Set timeout to 2 seconds for connection attempts
            result = sock.connect_ex((ip, port))
            if result == 0:
                open_ports.append(port)
            sock.close()
        except socket.error as e:
            print(f"Error scanning port {port}: {e}")
    return open_ports

# Taking user input for IP address
ip_address = input("Enter the IP address to ping and scan: ")

# Ping the host and display the result
ping_result = ping_host(ip_address)
print(ping_result)

# Only proceed to port scanning if the host is live
if "live" in ping_result:
    # Get the port range from the user
    start_port = int(input("Enter the starting port: "))
    end_port = int(input("Enter the ending port: "))

    # Scan ports in the given range
    ports = range(start_port, end_port + 1)
    open_ports = scan_ports(ip_address, ports)

    # Display open ports
    if open_ports:
        print(f"Open ports on {ip_address}: {open_ports}")
    else:
        print(f"No open ports found on {ip_address} in the range {start_port}-{end_port}")
else:
    print(f"Skipping port scanning as {ip_address} is not live.")
