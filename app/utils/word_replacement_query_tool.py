""" This tool can be used to fetch daily texts, ask word replacements and save them to json """
from datetime import datetime, timedelta
import json
import os
import sys
import re
import asyncio

sys.path.insert(0, os.getcwd())  # Can't import from app without this

from app.services.daily_text import daily_text


def _save_json(replacements, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(replacements, f, sort_keys=True, indent=4, ensure_ascii=False)
    print('JSON saved')


async def main():
    if not os.path.isfile('main.py'):
        print(f"Run this script from the project top folder")
        sys.exit(1)

    day = datetime.now()
    replacements_json_filename = 'app/json_data/string_replacements.json'
    with open(replacements_json_filename, 'r', encoding='utf-8') as f:
        replacements = json.load(f)
    print(f"loaded {len(replacements)} word replacements")

    running = True

    while running:
        dtext = await daily_text(day)
        words = re.split(r"\W+", dtext)
        for word_number, word in enumerate(words):
            if not word or not word.isalpha():
                continue
            print("------------------------------------------------")
            print(f'"{word.lower()}" ({word_number + 1} / {len(words)})')

            try:
                print(replacements[word.lower()])
                word_exists = True
            except KeyError:
                print([])
                word_exists = False

            print("ENTER to skip - comma-separated list of words to add those words - q to quit")
            print("n - next day, p - previous day")
            user_input = input().strip()

            if user_input == '':
                continue

            if user_input == 'n':
                day = day + timedelta(days=1)
                print(day)
                break

            if user_input == 'p':
                day = day - timedelta(days=1)
                print(day)
                break

            if user_input == 'q':
                running = False
                break

            user_words = user_input.split(',')

            if word_exists:
                replacements[word.lower()].extend(user_words)
            else:
                replacements[word.lower()] = user_words

            print(replacements[word.lower()])
            _save_json(replacements=replacements, filename=replacements_json_filename)

        day = day + timedelta(days=1)

    print(f"Saving JSON...")
    _save_json(replacements=replacements, filename=replacements_json_filename)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

