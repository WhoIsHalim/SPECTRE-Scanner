import asyncio

async def ssh_banner(ip: str, port=22, timeout=3):
    try:
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(ip, port),
            timeout=timeout
        )

        data = await asyncio.wait_for(reader.readline(), timeout=timeout)

        writer.close()
        await writer.wait_closed()

        return data.decode(errors="ignore").strip()

    except Exception:
        return ""