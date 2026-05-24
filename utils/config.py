import os
import yaml
import json

CONFIG_DIR = "config"
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.yaml")
IP_RANGES_FILE = os.path.join(CONFIG_DIR, "ip_ranges.txt")
PORTS_FILE = os.path.join(CONFIG_DIR, "ports.txt")
FINGERPRINTS_FILE = os.path.join(CONFIG_DIR, "fingerprints.json")
FILTER_FILE = os.path.join(CONFIG_DIR, "filter.txt")

DEFAULT_CONFIG = {
    "scanner": {
        "concurrency": 1000,
        "timeout": 5.0,
        "max_retries": 1
    },
    "http": {
        "enabled": True,
        "follow_redirects": True,
        "user_agent": "SPECTRE Scanner/3.0"
    },
    "reporting": {
        "txt": True,
        "json": True,
        "csv": True,
        "sqlite": True,
        "output_dir": "reports"
    }
}

DEFAULT_PORTS = "80,443,21,22,25,8080,8443,3306,6379"
DEFAULT_IPS = "127.0.0.1\n192.168.1.0/24"
DEFAULT_FILTER = "Apache\nOpenSSH\nRouter"
DEFAULT_FINGERPRINTS = [
    {
        "name": "OpenSSH",
        "regex": r"SSH-2\\.0-OpenSSH[\\s_]([\\d\\.]+)",
        "protocol": "tcp",
        "severity": "info",
        "weight": 100
    },
    {
        "name": "Apache Web Server",
        "regex": r"(?i)Server:\\s*Apache/([\\d\\.]+)",
        "protocol": "http",
        "severity": "info",
        "weight": 100
    }
]

def init_config():
    os.makedirs(CONFIG_DIR, exist_ok=True)
    os.makedirs("reports", exist_ok=True)
    
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w") as f:
            yaml.dump(DEFAULT_CONFIG, f, default_flow_style=False)
            
    if not os.path.exists(IP_RANGES_FILE):
        with open(IP_RANGES_FILE, "w") as f:
            f.write(DEFAULT_IPS)
            
    if not os.path.exists(PORTS_FILE):
        with open(PORTS_FILE, "w") as f:
            f.write(DEFAULT_PORTS)

    if not os.path.exists(FILTER_FILE):
        with open(FILTER_FILE, "w") as f:
            f.write(DEFAULT_FILTER)
            
    if not os.path.exists(FINGERPRINTS_FILE):
        with open(FINGERPRINTS_FILE, "w") as f:
            json.dump(DEFAULT_FINGERPRINTS, f, indent=4)

def load_config():
    init_config()
    with open(CONFIG_FILE, "r") as f:
        return yaml.safe_load(f)

def load_ports():
    with open(PORTS_FILE, "r") as f:
        content = f.read()
    
    ports = []
    for part in content.replace("\n", ",").split(","):
        part = part.strip()
        if not part: continue
        if "-" in part:
            start, end = part.split("-")
            ports.extend(range(int(start), int(end) + 1))
        else:
            ports.append(int(part))
    return list(set(ports))
