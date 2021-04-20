import json
from singleton_decorator import singleton


@singleton
class Options:
    def __init__(self, options_filename: str):
        with open(options_filename, encoding='utf-8') as f:
            _options = json.load(f)

        print(f"Options loaded")

        self.last_regret_allowed_interval = int(_options["last_regret_allowed_interval"])
        self.funnify_word_replace_chance = float(_options["funnify_word_replace_chance"])
