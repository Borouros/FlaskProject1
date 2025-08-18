from transformers import pipeline

translator_hf = pipeline("translation_en_to_pt")

def translate(text: str) -> str:
    """
    Translate English to Portuguese using an offline HF pipeline.
    Falls back to returning the original text on any error.
    """
    try:
        result = translator_hf(text)
        return result[0].get("translation_text", text)
    except Exception as e:
        print("Translation error:", e)
        return text
