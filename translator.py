import requests

def translate(text, source='en', target='pt'):
    url = "https://libretranslate.de/translate"
    payload = {
        'q': text,
        'source': source,
        'target': target,
        'format': 'text'
    }
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status() 
        
        if response.headers.get('content-type', '').startswith('application/json'):
            json_data = response.json()
            if 'translatedText' in json_data:
                return json_data['translatedText']
            else:
                return f"Translation error: {json_data.get('error', 'Unknown error')}"
        else:
            return f"API returned non-JSON response: {response.text[:100]}"
            
    except requests.RequestException as e:
        return f"Network error: {str(e)}"
    except ValueError as e:
        return f"JSON decode error: {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"