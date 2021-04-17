import json
import re
from typing import Dict, List

Trigger = List[str]
TriggersForCategory = Dict[str, Trigger]
AllTriggers = Dict[str, TriggersForCategory]


def load_triggers(triggers_filename: str) -> AllTriggers:
    with open(triggers_filename, encoding='utf-8') as f:
        trigger_words = json.load(f)
    print(f"Trigger words loaded")
    return trigger_words


def is_activated(message: str, triggers: AllTriggers) -> bool:
    message = message.lower()
    # message = re.sub(r'[\W_]+', '', message)  # strip non-alphanumeric characters
    # print(f"in is_activated")
    # print(f"message: {message}")
    # print(f"triggers:\n{triggers}")
    return any((trigger_word in message for trigger_word in triggers['regret']['partial']))
