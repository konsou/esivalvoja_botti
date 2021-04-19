import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://wol.jw.org/fi/wol/h/r16/lp-fi/'


def daily_text() -> str:
    # TODO: CACHE THIS! TAKES FOREVER!
    r = requests.get(BASE_URL)
    soup = BeautifulSoup(r.text, "html.parser")
    theme_scripture = soup.find_all('p', {'class': 'themeScrp'})[1].get_text().strip()
    body_text = soup.find_all('div', {'class': 'bodyTxt'})[1].get_text().strip()
    return f"{theme_scripture}\n{body_text}"


if __name__ == '__main__':
    print(daily_text())
