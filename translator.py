from transformers import pipeline

translator_hf = pipeline("translation_en_to_pt")

def translate(text: str) -> str:
    try:
        result = translator_hf(text)
        return result[0].get("translation_text", text)
    except Exception as e:
        print("Translation error:", e)
        return text