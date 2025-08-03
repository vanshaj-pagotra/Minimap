# **Python Port Scanner**

### This is a multithreaded port scanner written in Python. 
### It scans specified ports on a target host, reports open ports, and attempts banner grabbing to identify running services.


## Features
- Scan single ports or port ranges.

- Multithreaded scanning for improved speed.

- Banner grabbing for service identification.

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
python port_scanner.py -H scanme.nmap.org
```

### Scan a specific range:

- Use `-P` flag
- Put `-` between the lower and upper limit of the range
```cmd
python port_scanner.py -H 192.168.1.1 -P 20-100
```

### Scan a single port:
- Use `-P` flag
- Only give one value
```cmd
python port_scanner.py -H example.com -P 443
```

## How It Works
- Ports to scan are added to a queue.

- Worker threads pull ports from the queue and attempt to connect.

- Successful connections are checked for banner information.

- Results are printed to the console.

## Requirements

- Python 3.x

No external dependencies are required.

## Notes
- The scanner uses 100 threads by default for faster scanning.

- Only include scanning targets or ports you have permission to test.
