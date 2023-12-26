import json

import requests


def translate_word(word, source_lang="en", target_lang="it"):
    url = f"http://translator:3000/translate/{word}/{source_lang}/{target_lang}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        translation = response.json().get("translation")
        return translation
    except requests.exceptions.RequestException as e:
        raise e
        return None


# Example usage
if __name__ == "__main__":
    word_to_translate = "exam"
    source_language = "en"
    target_language = "it"

    translation_result = translate_word(
        word_to_translate, source_language, target_language
    )
    print(json.dumps(translation_result, indent=2))
