import json
from datetime import tzinfo
from typing import Dict, Callable

from singleton_decorator import singleton
from pytz import timezone

CustomConverters = Dict[str, Callable]


@singleton
class Options:
    options_filename: str
    last_regret_allowed_interval: int
    funnify_text_replacement_file: str
    funnify_word_replace_chance: float
    watch_json_data_files: bool
    timezone: tzinfo
    custom_converters: CustomConverters

    def __init__(self, options_filename: str):
        self.options_filename = options_filename

        with open(options_filename, encoding='utf-8') as f:
            _options = json.load(f)

        # Custom converters are used if the type defined in annotations can't
        # properly convert the option value
        # Currently used to convert a timezone string
        # to a datetime.tzinfo using pytz.timezone
        self.custom_converters = {
            'timezone': timezone
        }

        # print(self.__annotations__)
        # print(self.custom_converters)

        # Convert options json data to defined types
        for option, value in _options.items():
            if option in self.custom_converters:
                # Convert the value with a custom converter function
                setattr(self, option, self.custom_converters[option](value))
                continue

            if option in self.__annotations__:
                # Convert the value to the predefined type
                setattr(self, option, self.__annotations__[option](value))
                continue

            # default - just use the string value directly
            setattr(self, option, value)

        print(f"Options loaded")
        # print(self)

    def __repr__(self) -> str:
        return_string = ""
        for key, value in self.__dict__.items():
            return_string = f"{return_string}{key} ({type(key).__name__}): {value} ({type(value).__name__})\n"
        return_string = return_string[:-1]
        return return_string
