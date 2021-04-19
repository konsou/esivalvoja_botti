import json
from typing import Dict, List, Optional

Trigger = List[str]
TriggersForCategory = Dict[str, Trigger]
AllTriggers = Dict[str, TriggersForCategory]


def load_triggers(triggers_filename: str) -> AllTriggers:
    with open(triggers_filename, encoding='utf-8') as f:
        trigger_words = json.load(f)
    print(f"Trigger words loaded")
    return trigger_words


def is_activated(message: str, triggers: AllTriggers) -> Optional[str]:
    """Return the name of the trigger or None if no triggers activate"""
    message = message.lower()
    for trigger_name, values in triggers.items():
        for partial_trigger in values['partial']:
            if partial_trigger in message:
                return trigger_name
    return None

