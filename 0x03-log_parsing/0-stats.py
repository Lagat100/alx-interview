import sys
import signal
from collections import defaultdict

# Initialize variables
total_file_size = 0
status_code_counts = defaultdict(int)
valid_status_codes = {200, 301, 400, 401, 403, 404, 405, 500}
line_count = 0

def print_statistics():
    print(f"File size: {total_file_size}")
    for code in sorted(valid_status_codes):
        if status_code_counts[code] > 0:
            print(f"{code}: {status_code_counts[code]}")

def process_line(line):
    global total_file_size, line_count

    parts = line.split()
    if len(parts) < 7:
        return

    ip, dash, date, method, path, protocol, status_code, file_size 
    = parts[0], parts[1], parts[2], parts[3], parts[4], parts[5], parts[6], parts[7]

    if not (path == 'GET' and protocol == 'HTTP/1.1'):
        return

    try:
        status_code = int(status_code)
        file_size = int(file_size)
    except ValueError:
        return

    if status_code in valid_status_codes:
        status_code_counts[status_code] += 1
    total_file_size += file_size
    line_count += 1

    if line_count == 10:
        print_statistics()
        line_count = 0

def signal_handler(sig, frame):
    print_statistics()
    sys.exit(0)

# Register the signal handler
signal.signal(signal.SIGINT, signal_handler)

# Read lines from stdin
for line in sys.stdin:
    process_line(line.strip())

