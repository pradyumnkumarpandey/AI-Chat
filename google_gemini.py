import requests
import json
from decouple import config
import logging
logger = logging.getLogger(__name__)
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
    logger.info(json.dumps({"status":"response from AI","status":str(response)}))
    data = response.text
    data = json.loads(data)
    logger.info({"status":"response from AI- data","data":data})
    print(type(data))
    return data['candidates'][0]['content']['parts'][0]['text']
    # print(response.text)
