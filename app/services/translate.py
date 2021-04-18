from google.cloud import translate_v2 as translate
from dotenv import load_dotenv

load_dotenv()


def translate_text(text: str) -> str:
    """Translates text into the target language.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """
    translate_client = translate.Client()

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(text,
                                        target_language='fi',
                                        source_language='en-US')

    print(f"Text: {text}")
    print(f"Translation: {result['translatedText']}")
    print(f"Detected source language: {result['detectedSourceLanguage']}")
    return result['translatedText']


if __name__ == '__main__':
    test_text = "God's people speaking clearly by the Spirit what is revealed in the Word build up (mature) " \
                "the body of Christ. (1 Corinthians 14:1 - 20, 26, 39)"
    print(translate_text(test_text))
