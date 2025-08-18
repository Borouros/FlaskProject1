import requests

def translate(text, source='en', target='pt'):
    url = "https://libretranslate.com/translate"

    payload = {
        'q': text,
        'source': source,
        'target': target,
        'format': 'text'
    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)

        print("→ Requested URL:", response.request.url)
        print("→ Request headers:", response.request.headers)
        print("→ Request body:", response.request.body)
        print("← Status code:", response.status_code)
        print("← Response headers:", response.headers)
        print("← First 200 chars of body:", response.text[:200])
        print("Redirect history:", response.history)

        response.raise_for_status()
        json_data = response.json()
        return json_data.get('translatedText', 'Translation error: No translatedText found')

    except requests.RequestException as e:
        return f"Network error: {e}"
    except ValueError as e:
        return f"JSON decode error: {e}"
    except Exception as e:
        return f"Unexpected error: {e}"
