import requests

def translate(text, source='en', target='pt'):
    url = "https://libretranslate.de/translate"
    payload = {
        'q': text,
        'source': source,
        'target': target,
        'format': 'text'
    }
    response = requests.post(url, data=payload)
    return response.json()['translatedText']

print(translate("Hello world", source='en', target='pt'))
