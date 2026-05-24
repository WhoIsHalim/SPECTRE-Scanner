import ipaddress
import os
from typing import Iterator

def stream_targets(filepath: str) -> Iterator[str]:
    if not os.path.exists(filepath):
        return
        
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
                
            try:
                # Handle CIDR or single IP
                net = ipaddress.ip_network(line, strict=False)
                for ip in net.hosts():
                    yield str(ip)
                # If it's a /32 or single IP without network prefix, hosts() might be empty, so handle it:
                if net.prefixlen == 32:
                    yield str(net.network_address)
            except ValueError:
                pass
