from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class HTTPResult:
    url: str
    status: int
    title: str
    server: str
    headers: dict

@dataclass
class BannerResult:
    banner: str
    protocol: str

@dataclass
class FingerprintResult:
    name: str
    confidence: int
    severity: str

@dataclass
class ScanResult:
    ip: str
    port: int
    service: str = ""
    version: str = ""
    banner: Optional[BannerResult] = None
    http: Optional[HTTPResult] = None
    fingerprints: List[FingerprintResult] = field(default_factory=list)

    def to_dict(self):
        return {
            "ip": self.ip,
            "port": self.port,
            "service": self.service,
            "version": self.version,
            "banner": self.banner.banner if self.banner else None,
            "http_title": self.http.title if self.http else None,
            "http_server": self.http.server if self.http else None,
            "fingerprints": [{"name": fp.name, "severity": fp.severity, "confidence": fp.confidence} for fp in self.fingerprints]
        }
