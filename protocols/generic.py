import asyncio
from typing import Optional
from storage.models import BannerResult

async def generic_banner(ip: str, port: int, timeout: float = 3.0) -> Optional[BannerResult]:
    try:
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(ip, port),
            timeout=timeout
        )
        
        # Depending on port, we might need to send a payload first (e.g., HTTP)
        # For a truly generic banner grabber, we can wait a moment to see if the server sends anything first.
        # If it doesn't, we can send a generic probe.
        
        # Wait a bit for welcome banner (SSH, FTP, SMTP)
        try:
            data = await asyncio.wait_for(reader.read(1024), timeout=1.0)
        except asyncio.TimeoutError:
            data = b""

        if not data:
            # Send generic probe
            writer.write(b"HEAD / HTTP/1.0\r\n\r\n")
            await writer.drain()
            try:
                data = await asyncio.wait_for(reader.read(1024), timeout=timeout)
            except asyncio.TimeoutError:
                data = b""
                
        writer.close()
        await writer.wait_closed()
        
        if data:
            banner_text = data.decode("utf-8", errors="ignore").strip()
            return BannerResult(banner=banner_text, protocol="tcp")
            
    except Exception:
        pass
        
    return None