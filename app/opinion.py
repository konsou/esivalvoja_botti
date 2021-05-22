import json
from typing import Dict, Optional

Opinions = Dict[str, str]


def load_opinions(opinion_filename: str) -> Opinions:
    with open(opinion_filename, encoding='utf-8') as f:
        opinions = json.load(f)

    print(f"Opinions loaded")
    return opinions


def check_user_mentioned(message: str, opinions: Opinions) -> Optional[str]:
    message = message.lower()
    for user in opinions.keys():
        if user in message:
            return user
    return None


def get_opinion(user_name: Optional[str],
                opinions: Opinions) -> str:
    if user_name in opinions:
        return opinions[user_name]
    else:
        return opinions['no_opinion']
