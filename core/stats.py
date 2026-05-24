import time

class ScanStats:
    def __init__(self):
        self.start_time = time.time()
        self.total_ips = 0
        self.scanned_ips = 0
        self.open_ports = 0
        self.fingerprints_found = 0
        self.http_services = 0

    def get_duration(self) -> float:
        return time.time() - self.start_time

    def format_stats(self) -> str:
        duration = self.get_duration()
        return (f"Scanned IPs: {self.scanned_ips} | "
                f"Open Ports: {self.open_ports} | "
                f"HTTP Services: {self.http_services} | "
                f"Fingerprints: {self.fingerprints_found} | "
                f"Time: {duration:.2f}s")
