import re
import json
import random


def funnify_text(text: str,
                 text_replacements: dict,
                 options) -> str:

    def test_match(match) -> str:
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
                        test_match,
                        text,
                        flags=re.IGNORECASE)
    return funny_text


if __name__ == '__main__':
    with open('json_data/string_replacements.json', encoding='utf8') as f:
        text_replacements = json.load(f)

    options = {
        "funnify_word_replace_chance": 1
    }

    funnify_text("Suuri Babylon, väärän uskonnon maailmanmahti, on aiheuttanut paljon häpeää Jumalan nimelle.",
                 text_replacements,
                 options)

