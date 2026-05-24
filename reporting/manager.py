import os
import json
import csv
import aiosqlite
from storage.models import ScanResult
from utils.config import load_config
from utils.logger import log

class ReportManager:
    def __init__(self):
        self.config = load_config().get("reporting", {})
        self.output_dir = self.config.get("output_dir", "reports")
        os.makedirs(self.output_dir, exist_ok=True)
        
        self.txt_path = os.path.join(self.output_dir, "report.txt")
        self.csv_path = os.path.join(self.output_dir, "report.csv")
        self.json_path = os.path.join(self.output_dir, "report.json")
        self.db_path = os.path.join(self.output_dir, "report.db")

        self.db = None
        self._init_csv()
        
    async def init_db(self):
        if self.config.get("sqlite"):
            self.db = await aiosqlite.connect(self.db_path)
            await self.db.execute('''
                CREATE TABLE IF NOT EXISTS results (
                    ip TEXT,
                    port INTEGER,
                    service TEXT,
                    version TEXT,
                    banner TEXT,
                    http_title TEXT,
                    http_server TEXT,
                    fingerprints TEXT,
                    UNIQUE(ip, port)
                )
            ''')
            await self.db.commit()

    async def close(self):
        if self.db:
            await self.db.close()

    def _init_csv(self):
        if self.config.get("csv"):
            with open(self.csv_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["IP", "Port", "Service", "Version", "Banner", "HTTP Title", "HTTP Server", "Fingerprints"])

    async def save_result(self, result: ScanResult):
        if self.config.get("txt"):
            with open(self.txt_path, "a", encoding='utf-8') as f:
                f.write(f"[{result.ip}:{result.port}] {result.service} {result.version}\n")
                if result.http:
                    f.write(f"  --> HTTP Title: {result.http.title}\n")
                for fp in result.fingerprints:
                    f.write(f"  --> FP: {fp.name} (Conf: {fp.confidence}, Sev: {fp.severity})\n")

        if self.config.get("json"):
            with open(self.json_path, "a", encoding='utf-8') as f:
                f.write(json.dumps(result.to_dict()) + "\n")

        if self.config.get("csv"):
            with open(self.csv_path, "a", newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                fps = ", ".join([fp.name for fp in result.fingerprints])
                writer.writerow([
                    result.ip,
                    result.port,
                    result.service,
                    result.version,
                    result.banner.banner if result.banner else "",
                    result.http.title if result.http else "",
                    result.http.server if result.http else "",
                    fps
                ])

        if self.db and self.config.get("sqlite"):
            fps_json = json.dumps([{"name": fp.name, "severity": fp.severity} for fp in result.fingerprints])
            await self.db.execute('''
                INSERT OR REPLACE INTO results 
                (ip, port, service, version, banner, http_title, http_server, fingerprints)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                result.ip, 
                result.port, 
                result.service, 
                result.version,
                result.banner.banner if result.banner else "",
                result.http.title if result.http else "",
                result.http.server if result.http else "",
                fps_json
            ))
            await self.db.commit()
