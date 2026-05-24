import json
import re
import os
from typing import List, Dict, Any
from utils.config import FINGERPRINTS_FILE
from storage.models import FingerprintResult

class SignatureEngine:
    def __init__(self):
        self.signatures = []
        self._load_signatures()

    def _load_signatures(self):
        if not os.path.exists(FINGERPRINTS_FILE):
            return
            
        try:
            with open(FINGERPRINTS_FILE, "r") as f:
                data = json.load(f)
            
            for sig in data:
                try:
                    compiled_regex = re.compile(sig["regex"], re.IGNORECASE)
                    self.signatures.append({
                        "name": sig["name"],
                        "regex": compiled_regex,
                        "protocol": sig.get("protocol", "all").lower(),
                        "severity": sig.get("severity", "info"),
                        "weight": sig.get("weight", 100)
                    })
                except re.error as e:
                    print(f"Failed to compile regex for {sig['name']}: {e}")
        except Exception as e:
            print(f"Error loading fingerprints: {e}")

    def match(self, protocol: str, data: str) -> List[FingerprintResult]:
        results = []
        if not data:
            return results

        for sig in self.signatures:
            if sig["protocol"] != "all" and sig["protocol"] != protocol.lower():
                continue
                
            if sig["regex"].search(data):
                # Calculate confidence or just use weight if it's a direct match
                results.append(FingerprintResult(
                    name=sig["name"],
                    confidence=sig["weight"],
                    severity=sig["severity"]
                ))
                
        return results

# Singleton instance
engine = SignatureEngine()
