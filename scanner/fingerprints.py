import json
import re
from pathlib import Path
from models import FingerprintResult

SIGNATURES = json.loads(
    Path("signatures/fingerprints.json").read_text(encoding="utf-8")
)


def fingerprint(text: str):
    text = text.lower()

    matches = []

    for sig in SIGNATURES:
        score = 0

        for pattern in sig["patterns"]:
            if re.search(pattern, text):
                score += sig.get("weight", 50)

        if score:
            matches.append(
                FingerprintResult(
                    name=sig["name"],
                    confidence=min(score, 100),
                    severity=sig.get("severity", "info")
                )
            )

    return matches