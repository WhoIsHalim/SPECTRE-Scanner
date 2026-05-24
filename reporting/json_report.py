import json
from dataclasses import asdict


def save_json(results, path="results.json"):
    data = [asdict(r) for r in results]

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)