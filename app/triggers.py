import json
from typing import Dict


def load_triggers(triggers_filename: str = 'json_data/triggers.json') -> Dict[str, str]:
    with open(triggers_filename, encoding='utf-8') as f:
        trigger_words = json.load(f)['partial']
    print(f"Trigger words loaded")
    return trigger_words
