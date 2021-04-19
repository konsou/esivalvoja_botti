import time
import asyncio
from typing import Optional, NamedTuple
from dataclasses import dataclass

import requests
import aiohttp
from bs4 import BeautifulSoup


@dataclass
class CachedResult:
    result: Optional[str]
    last_request_timestamp: float


_cached_result = CachedResult(result=None, last_request_timestamp=0)

BASE_URL = 'https://wol.jw.org/fi/wol/h/r16/lp-fi/'
CACHE_INVALIDATION_TIME = 3600  # seconds


def result_is_cached() -> bool:
    return _cached_result.result is not None and \
           time.time() - _cached_result.last_request_timestamp < CACHE_INVALIDATION_TIME


async def daily_text() -> Optional[str]:
    if result_is_cached():
        print(f"cached request was fetched {time.time() - _cached_result.last_request_timestamp} s ago")
        print(f"using cached result")
        return _cached_result.result

    print(f"No valid cache, re-fetching daily text...")

    # SHARED SESSION FOR APP BETTER?
    async with aiohttp.ClientSession() as session:
        async with session.get(BASE_URL) as resp:
            print(resp.status)
            html = await resp.text()
            soup = BeautifulSoup(html, "html.parser")
            theme_scripture = soup.find_all('p', {'class': 'themeScrp'})[1].get_text().strip()
            body_text = soup.find_all('div', {'class': 'bodyTxt'})[1].get_text().strip()
            return_string = f"**{theme_scripture}**\n\n{body_text}"
            _cached_result.result = return_string
            _cached_result.last_request_timestamp = time.time()
            return return_string


if __name__ == '__main__':
    async def test_main():
        print(await daily_text())
        await asyncio.sleep(5)
        print(await daily_text())
        await asyncio.sleep(5)
        print(await daily_text())


    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_main())

