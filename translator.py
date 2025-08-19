import re
from deep_translator import GoogleTranslator

def clean_text(text: str) -> str:
    """Remove HTML tags and trim excessive whitespace before translation."""
    text = re.sub(r"<.*?>", "", text)
    text = " ".join(text.split())
    return text

def translate(text: str, source: str = "en", target: str = "pt") -> str:
    """
    Translate text from source language to target language using GoogleTranslator.
    Returns the translated text, or the original if translation fails.
    """
    try:
        if not text.strip():
            return text
        safe_text = clean_text(text)
        return GoogleTranslator(source=source, target=target).translate(safe_text)
    except Exception as e:
        print(f"Translation error: {e}")
        return text
