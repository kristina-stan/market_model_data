import aiohttp
import ssl

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

async def fetch_content(url: str, ssl_ctx=ssl_context) -> bytes:
    """Fetch content from URL with SSL disabled (if needed)."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url, ssl=ssl_ctx) as resp:
            if resp.status == 200:
                return await resp.read()
            else:
                raise Exception(f"Failed to fetch {url} (status: {resp.status})")
