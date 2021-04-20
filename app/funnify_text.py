from __future__ import annotations
import re
import random
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.options import Options


def funnify_text(text: str,
                 text_replacements: dict,
                 options: Options) -> str:

    def replace_match(match: re.Match) -> str:
        match_string = match.group(0)
        match_lower = match_string.lower()
        starts_with_uppercase = match_string[0].isupper()

        if random.random() <= options.FUNNIFY_WORD_REPLACE_CHANCE:
            return_string = random.choice(text_replacements[match_lower])
        else:
            return_string = match_string

        if starts_with_uppercase:
            return_string = return_string.capitalize()

        return return_string

    words_to_replace = text_replacements.keys()
    words_with_pipes = "|".join(words_to_replace)
    expression = f'\\b({words_with_pipes})\\b'
    funny_text = re.sub(expression,
                        replace_match,
                        text,
                        flags=re.IGNORECASE)
    return funny_text

