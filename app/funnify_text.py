from __future__ import annotations
import re
import random
import hashlib
import json
from typing import Dict, List, TYPE_CHECKING


if TYPE_CHECKING:
    from app.options import Options

TextReplacements = Dict[str, List[str]]


def load_text_replacements(filename: str,
                           options: Options) -> TextReplacements:
    with open(filename, encoding='utf8') as f:
        string_contents = f.read()
        text_replacements = json.loads(string_contents)
        if options.watch_json_data_files:
            _hash = hashlib.sha256(bytes(string_contents, encoding='utf-8')).hexdigest()
            print(f"Hash: {_hash}")
            text_replacements['__hash__'] = [_hash]

    print(f"Text replacements loaded")
    return text_replacements


def funnify_text(text: str,
                 text_replacements: dict,
                 options: Options) -> str:

    def replace_match(match: re.Match) -> str:
        match_string = match.group(0)
        match_lower = match_string.lower()
        starts_with_uppercase = match_string[0].isupper()

        if random.random() <= options.funnify_word_replace_chance:
            return_string = random.choice(text_replacements[match_lower])
        else:
            return_string = match_string

        if starts_with_uppercase:
            return_string = return_string[0].upper() + return_string[1:]

        return return_string

    words_to_replace = text_replacements.keys()
    words_with_pipes = "|".join(words_to_replace)
    expression = f'\\b({words_with_pipes})\\b'
    funny_text = re.sub(expression,
                        replace_match,
                        text,
                        flags=re.IGNORECASE)
    return funny_text

