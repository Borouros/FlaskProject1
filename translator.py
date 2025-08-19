from deep_translator import GoogleTranslator

def translate(text: str, source: str = "en", target: str = "pt") -> str:
    """
    Translate text from source language to target language using GoogleTranslator.
    Returns the translated text, or the original text if translation fails.
    """
    try:
        if not text.strip():
            return text
        translator = GoogleTranslator(source=source, target=target)
        return translator.translate(text)
    except Exception as e:
        print(f"Translation error: {e}")
        return text
