import ipaddress
from pathlib import Path


def stream_targets(path: str):
    seen = set()

    for line in Path(path).read_text().splitlines():
        line = line.strip()

        if not line or line.startswith("#"):
            continue

        try:
            network = ipaddress.ip_network(line, strict=False)

            for host in network.hosts():
                ip = str(host)

                if ip not in seen:
                    seen.add(ip)
                    yield ip

        except ValueError:
            if line not in seen:
                seen.add(line)
                yield line