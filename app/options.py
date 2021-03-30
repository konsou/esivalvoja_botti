import json
from singleton_decorator import singleton


@singleton
class Options:
    def __init__(self, options_filename: str = 'options.json'):
        with open(options_filename, encoding='utf-8') as f:
            _options = json.load(f)

        print(f"Options loaded")
        print(_options)

        self.LAST_REGRET_ALLOWED_INTERVAL = int(_options["last_regret_allowed_interval"])
