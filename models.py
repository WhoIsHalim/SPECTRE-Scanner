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