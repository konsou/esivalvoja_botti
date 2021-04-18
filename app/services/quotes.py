import os

from dotenv import load_dotenv
import requests

load_dotenv()

API_ENDPOINT = "https://uncovered-treasure-v1.p.rapidapi.com"


def get_random_quote() -> str:
    url = f"{API_ENDPOINT}/random"
    response = requests.get(url,
                            headers={
                                "x-rapidapi-key": os.getenv('RAPIDAPI_KEY'),
                                "x-rapidapi-host": "uncovered-treasure-v1.p.rapidapi.com",
                            })
    result_quote = response.json()['results'][0]
    return_string = f"{result_quote['text']} ({', '.join(result_quote['scriptures'])})"
    return return_string


if __name__ == "__main__":
    print(get_random_quote())
