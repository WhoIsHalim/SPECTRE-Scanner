import asyncio
import aiohttp
from typing import List
from core.stats import ScanStats
from core.generator import stream_targets
from utils.config import load_ports, IP_RANGES_FILE, FILTER_FILE
from utils.logger import log
from scanner.discovery import tcp_connect
from scanner.http import probe_http
from protocols.generic import generic_banner
from signatures.engine import engine as sig_engine
from reporting.manager import ReportManager
from storage.models import ScanResult

class ScannerEngine:
    def __init__(self, config: dict, custom_filter_enabled: bool = False):
        self.config = config
        self.custom_filter_enabled = custom_filter_enabled
        self.filter_terms = []
        self.stats = ScanStats()
        self.report_manager = ReportManager()
        self.ports = load_ports()
        
        scanner_conf = self.config.get("scanner", {})
        concurrency = scanner_conf.get("concurrency", 1000)
        self.timeout = scanner_conf.get("timeout", 5.0)
        
        self.semaphore = asyncio.Semaphore(concurrency)
        self.shutdown_event = asyncio.Event()

    async def init(self):
        await self.report_manager.init_db()
        if self.custom_filter_enabled:
            try:
                import os
                if os.path.exists(FILTER_FILE):
                    with open(FILTER_FILE, 'r') as f:
                        self.filter_terms = [line.strip().lower() for line in f if line.strip() and not line.startswith('#')]
                log.ui(f"[*] Custom filter enabled with {len(self.filter_terms)} terms.")
            except Exception as e:
                log.ui(f"[!] Failed to load filter file: {e}")

    async def worker(self, ip: str, port: int, session: aiohttp.ClientSession):
        if self.shutdown_event.is_set():
            return
            
        async with self.semaphore:
            is_open = await tcp_connect(ip, port, timeout=self.timeout)
            
            if not is_open:
                return

            self.stats.open_ports += 1
            result = ScanResult(ip=ip, port=port)
            
            # Banner Grabbing
            banner = await generic_banner(ip, port, timeout=self.timeout)
            if banner:
                result.banner = banner
                result.service = banner.banner[:40]
                result.version = banner.banner[:100]

            # HTTP Probing
            http = None
            if self.config.get("http", {}).get("enabled", True):
                http = await probe_http(session, ip, port, timeout=self.timeout)
                if http:
                    result.http = http
                    self.stats.http_services += 1

            # Fingerprinting
            fp_text = " ".join(filter(None, [
                banner.banner if banner else "",
                http.title if http else "",
                http.server if http else ""
            ]))
            
            fingerprints = sig_engine.match("all", fp_text) # Simple matching
            if fingerprints:
                result.fingerprints = fingerprints
                self.stats.fingerprints_found += len(fingerprints)

            if self.custom_filter_enabled and self.filter_terms:
                matched = False
                check_text = fp_text.lower()
                for term in self.filter_terms:
                    if term in check_text:
                        matched = True
                        break
                    # Check fingerprint names as well
                    for fp in result.fingerprints:
                        if term in fp.name.lower():
                            matched = True
                            break
                    if matched: break
                
                if not matched:
                    return

            await self.report_manager.save_result(result)

    async def run(self):
        log.ui(f"\n[*] Starting scan with {self.semaphore._value} concurrency limit...")
        
        timeout = aiohttp.ClientTimeout(total=self.timeout)
        connector = aiohttp.TCPConnector(limit=0, ssl=False) # We use our own semaphore
        
        tasks = []
        
        try:
            async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
                for ip in stream_targets(IP_RANGES_FILE):
                    if self.shutdown_event.is_set():
                        break
                        
                    for port in self.ports:
                        if self.shutdown_event.is_set():
                            break
                        
                        task = asyncio.create_task(self.worker(ip, port, session))
                        tasks.append(task)
                        
                    self.stats.scanned_ips += 1
                    
                    if len(tasks) >= 10000:
                        # Periodically wait for tasks to avoid memory buildup with huge ranges
                        done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
                        tasks = list(pending)
                        log.ui(f"\r[*] Progress: {self.stats.format_stats()}", end="")

                if tasks:
                    await asyncio.gather(*tasks)
                    
        except asyncio.CancelledError:
            log.ui("\n[!] Scan cancelled by user. Saving progress...")
            self.shutdown_event.set()
        finally:
            log.ui(f"\n[*] Final Stats: {self.stats.format_stats()}")
            await self.report_manager.close()

    def stop(self):
        self.shutdown_event.set()
