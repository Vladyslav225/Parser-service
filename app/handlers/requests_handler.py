import ssl
from aiohttp import ClientSession, ClientError, ClientTimeout, TCPConnector
from fastapi import HTTPException
from app.project_configs.headers import HEADERS

import asyncio
import certifi


class RequestsHandler:
    @staticmethod
    async def fetch_data(url: str, timeout_limit: int = None):
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        connector = TCPConnector(ssl=ssl_context)
        timeout = ClientTimeout(total=timeout_limit) if timeout_limit else None

        async with ClientSession(connector=connector, timeout=timeout) as session:
            try:
                async with session.get(url, headers=HEADERS) as response:
                    response.raise_for_status()
                    
                    if response.status != 200:
                        raise HTTPException(status_code=response.status, detail=f"Failed to fetch data from {url}")
                    
                    return await response.text()
            except ClientError:
                raise HTTPException(status_code=429, detail=f"ClientError: Failed to fetch data from {url}")
                
            except asyncio.TimeoutError:
                raise HTTPException(status_code=408, detail=f"TimeoutError: Request to {url} timed out")
            
            
    @staticmethod
    async def fetch_redirect_url(url: str):
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        connector = TCPConnector(ssl=ssl_context)

        retries = 3
        async with ClientSession(connector=connector) as session:
            for attempt in range(retries):
                try:
                    async with session.get(
                        url,
                        allow_redirects=True,
                        headers={"User-Agent": "Mozilla/5.0"}
                    ) as response:
                        response.raise_for_status()
                        return str(response.url)
                except ClientError:
                    if attempt < retries - 1:
                        await asyncio.sleep(2 * (attempt + 1))
                        continue
                    return None
                except asyncio.TimeoutError:
                    return None
        return None