import aiohttp
import asyncio
from bs4 import BeautifulSoup
from typing import Optional
from storage.models import HTTPResult

async def probe_http(session: aiohttp.ClientSession, ip: str, port: int, timeout: float = 5.0) -> Optional[HTTPResult]:
    scheme = "https" if port in [443, 8443] else "http"
    url = f"{scheme}://{ip}:{port}/"
    
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=timeout), ssl=False, allow_redirects=True) as response:
            text = await response.text(errors='ignore')
            
            # Extract title
            title = ""
            if text:
                soup = BeautifulSoup(text, "html.parser")
                if soup.title and soup.title.string:
                    title = soup.title.string.strip()
                    
            server = response.headers.get("Server", "")
            
            return HTTPResult(
                url=str(response.url),
                status=response.status,
                title=title,
                server=server,
                headers=dict(response.headers)
            )
            
    except Exception:
        return None