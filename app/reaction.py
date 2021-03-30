import json
from time import time
from random import choice, randint

with open('json_data/options.json', encoding='utf-8') as f:
    LAST_REGRET_ALLOWED_INTERVAL = int(json.load(f)["last_regret_allowed_interval"])
    print(f"Options loaded - LAST_REGRET_ALLOWED_INTERVAL: {LAST_REGRET_ALLOWED_INTERVAL}")

with open('json_data/responses.json', encoding='utf-8') as f:
    responses = json.load(f)

    TOO_SOON_REACTIONS = responses['too_soon']
    NEGATIVE_REACTIONS = responses['negative']
    POSITIVE_REACTIONS = responses['positive']
    print(f"Responses loaded")


def get_reaction(user_name: str, last_regret_timestamp: float) -> str:
    # print(f"In get_reaction - user_name: {user_name}, last_regret_timestamp: {last_regret_timestamp}")
    if (time() - last_regret_timestamp) < LAST_REGRET_ALLOWED_INTERVAL:
        reply_table = TOO_SOON_REACTIONS
    elif randint(0, 1) == 0:
        reply_table = NEGATIVE_REACTIONS
    else:
        reply_table = POSITIVE_REACTIONS

    reply = choice(reply_table)
    reply.replace('%name%', user_name)
    return f"{reply}"
