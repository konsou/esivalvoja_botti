import json

from singleton_decorator import singleton
from pytz import timezone


@singleton
class Options:
    last_regret_allowed_interval: int
    funnify_text_replacement_file: str
    funnify_word_replace_chance: float
    watch_json_data_files: bool
    timezone: timezone

    def __init__(self, options_filename: str):
        with open(options_filename, encoding='utf-8') as f:
            _options = json.load(f)

        print(self.__annotations__)

        # Convert to defined types
        for option, value in _options.items():
            if option in self.__annotations__:
                # Convert the value to the predefined type
                setattr(self, option, self.__annotations__[option](value))
            else:
                setattr(self, option, value)

        print(f"Options loaded")
        # print(self)

    def __repr__(self) -> str:
        return_string = ""
        for key, value in self.__dict__.items():
            return_string = f"{return_string}{key} ({type(key).__name__}): {value} ({type(value).__name__})\n"
        return_string = return_string[:-1]
        return return_string
