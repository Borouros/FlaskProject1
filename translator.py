from deep_translator import GoogleTranslator


translator = GoogleTranslator(source="en", target="pt")

def translate(text: str) -> str:
    """
    Translate English text into Portuguese using GoogleTranslator.
    Returns the translated text, or the original text if translation fails.
    """
    try:
        if not text.strip():
            return text
        return translator.translate(text)
    except Exception as e:
        print(f"Translation error: {e}")
        return text
