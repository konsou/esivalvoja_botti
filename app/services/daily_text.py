import time
import asyncio
from typing import Optional
from dataclasses import dataclass
from datetime import datetime, timedelta

import aiohttp
from bs4 import BeautifulSoup


@dataclass
class CachedResult:
    result: Optional[str]
    last_request_timestamp: float
    date: Optional[datetime]


# TODO: Make a dict that holds cached results for different dates
_cached_result = CachedResult(result=None, last_request_timestamp=0, date=None)

BASE_URL = 'https://wol.jw.org/fi/wol/h/r16/lp-fi/'
CACHE_INVALIDATION_TIME = 3600  # seconds


def result_is_cached(date: datetime = None) -> bool:
    if date is None:
        date = datetime.now()

    if _cached_result.result is None or _cached_result.date is None:
        return False

    c_date = _cached_result.date
    return (time.time() - _cached_result.last_request_timestamp < CACHE_INVALIDATION_TIME and
            (date.day == c_date.day and date.month == c_date.month and date.year == c_date.year))


async def daily_text(date: datetime = None) -> Optional[str]:
    if date is None:
        date = datetime.now()

    if result_is_cached(date=date):
        # print(f"cached request was fetched {time.time() - _cached_result.last_request_timestamp} s ago")
        # print(f"using cached result")
        return _cached_result.result

    print(f"No valid cache, fetching daily text...")

    full_url = f"{BASE_URL}{date.year}/{date.month}/{date.day}"
    print(f"full url: {full_url}")

    # SHARED SESSION FOR APP BETTER?
    async with aiohttp.ClientSession() as session:
        # Mimic a real browser for MUCH better performance
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0'}
        async with session.get(full_url, headers=headers) as resp:
            html = await resp.text()
            soup = BeautifulSoup(html, "html.parser")
            theme_scripture = soup.find_all('p', {'class': 'themeScrp'})[1].get_text().strip()
            body_text = soup.find_all('div', {'class': 'bodyTxt'})[1].get_text().strip()
            return_string = f"**{theme_scripture}**\n\n{body_text}"
            _cached_result.result = return_string
            _cached_result.last_request_timestamp = time.time()
            _cached_result.date = date
            return return_string


if __name__ == '__main__':
    async def test_main():
        today = datetime.now()
        tomorrow = today + timedelta(days=1)
        yesterday = today - timedelta(days=1)

        print(await daily_text())
        print(await daily_text(today))
        print(await daily_text(tomorrow))
        print(await daily_text(yesterday))
        print(await daily_text(yesterday))


    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_main())
