import json
from time import time
from random import choice, randint
from typing import Dict


def load_responses(response_filename: str) -> Dict[str, str]:
    with open(response_filename, encoding='utf-8') as f:
        responses = json.load(f)

    print(f"Responses loaded")
    return responses


def get_response(user_name: str, last_regret_timestamp: float,
                 options, responses: dict) -> str:
    # print(f"In get_response - user_name: {user_name}, last_regret_timestamp: {last_regret_timestamp}")
    # print(f"options: {options}, responses: {responses}")
    if (time() - last_regret_timestamp) < options.last_regret_allowed_interval:
        reply_table = responses['too_soon']
    elif randint(0, 1) == 0:
        reply_table = responses['negative']
    else:
        reply_table = responses['positive']

    # print(f"reply_table: {reply_table}")

    reply = choice(reply_table)
    reply = reply.replace('%name%', user_name)
    return f"{reply}"
