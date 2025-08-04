# **Python Port Scanner**

### This is a multithreaded port scanner written in Python. 
### It scans specified ports on a target host, reports open ports, and attempts banner grabbing to identify running services.


## Features
- Scan any IP address for a specified port or port range.

- Multithreaded scanning for improved speed.

- Grabs service banner using specific protocol requests.

- Thread-safe console output.

## Usage
### Run the script from the command line:

```cmd
python minimap.py -H <target_host> -P <port_range>
```

-H, --host: Target IP address or domain name (required).

-P, --ports: Port or range of ports to scan (default: 1-1024). Example: 22 or 20-80.

## Example Scans

### Scan default ports(1-1024):

- Only use the `-H` flag

```cmd
python minimap.py -H example.com
```

### Scan a specific range:

- Use `-P` flag
- Put `-` between the lower and upper limit of the range
```cmd
python minimap.py -H exapmle.com -P 20-100
```

### Scan a single port:
- Use `-P` flag
- Only give one value
```cmd
python port_scanner.py -H example.com -P 443
```

## How It Works
- Ports are added to a queue.

- Threads pull ports from the queue and attempt to connect.

- Open ports are identified.

- Successful connections are checked for banner information.

- Results are displayed to the terminal.



```markdown
## Sample Output

Minimap started...
Scanning 45.33.32.156

Port 22 is open
Service: [SSH]  
Banner:
SSH-2.0-OpenSSH_6.6.1p1 Ubuntu-2ubuntu2.13

Scan Completed in 0.67 seconds
```

## Requirements

- Python 3.x

No external dependencies are required.

## Disclaimer
**Only scan targets or ports you have permission to test.**
