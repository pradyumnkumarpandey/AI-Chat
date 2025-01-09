import requests
import json
from decouple import config
def get_gemini_reponse(message):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key={config('API_KEY')}"

    payload = json.dumps({
    "contents": [
        {
        "parts": [
            {
            "text": f"{message}"
            }
        ]
        }
    ]
    })
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    data = response.text
    data = json.loads(data)
    print(type(data))
    return data['candidates'][0]['content']['parts'][0]['text']
    # print(response.text)
