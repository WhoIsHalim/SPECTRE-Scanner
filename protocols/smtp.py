import asyncio

async def smtp_banner(ip: str, port=25, timeout=5):
    try:
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(ip, port),
            timeout=timeout
        )

        data = await asyncio.wait_for(reader.read(1024), timeout=timeout)

        writer.close()
        await writer.wait_closed()

        return data.decode(errors="ignore").strip()

    except Exception:
        return ""