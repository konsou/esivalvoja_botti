# DEPRECATED - REMOVE
import os

from dotenv import load_dotenv
import requests

load_dotenv()

API_BASE_URL = "https://uncovered-treasure-v1.p.rapidapi.com"
API_REQUEST_HEADERS = {
    "x-rapidapi-key": os.getenv('RAPIDAPI_KEY'),
    "x-rapidapi-host": "uncovered-treasure-v1.p.rapidapi.com",
}
API_ENDPOINTS = {
    'random': '/random',
    'today': '/today',
}


def _fetch_quote(quote_type: str) -> str:
    url = f"{API_BASE_URL}{API_ENDPOINTS[quote_type]}"
    response = requests.get(url, headers=API_REQUEST_HEADERS)
    result_quote = response.json()['results'][0]
    return_string = f"{result_quote['text']} ({', '.join(result_quote['scriptures'])})"
    return return_string


def random_quote() -> str:
    return _fetch_quote('random')


def daily_quote() -> str:
    return _fetch_quote('today')

