from deep_translator import GoogleTranslator

def translate(text: str, source: str = "en", target: str = "pt") -> str:
    """
    Translate text using GoogleTranslator.
    Defaults: English -> Portuguese.
    Returns translated text, or original text if translation fails.
    """
    try:
        if not text.strip():
            return text
        return GoogleTranslator(source=source, target=target).translate(text)
    except Exception as e:
        print(f"Translation error: {e}")
        return text
