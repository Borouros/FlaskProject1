from googletrans import Translator

translator = Translator()

def translate(text, src="en", dest="pt"):
    return translator.translate(text, src=src, dest=dest).text