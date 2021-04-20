# DEPRECATED - REMOVE
import os

import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://translation.googleapis.com/language/translate/v2"


def translate_text(text: str,
                   source_language: str = 'en',
                   target_language: str = 'fi') -> str:
    """Translates text into the target language.

    Target and source must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """

    query_params = {
        "q": text,
        "source": source_language,
        "target": target_language,
        "format": "text",
        "key": os.getenv('GOOGLE_TRANSLATE_API_KEY'),
    }

    response = requests.post(API_URL,
                             params=query_params)

    response_json = response.json()

    return response_json['data']['translations'][0]['translatedText']

