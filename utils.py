import requests
import json

base_url = "http://localhost:1234"


def get_response(messages, model, base_url, response_format=None):
    url = base_url + "/v1/chat/completions"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": -1,
        "stream": False,
        **({"response_format": response_format} if response_format else {})
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()

def get_models(base_url):
    url = base_url + "/v1/models"
    response = requests.get(url)
    return response.json()

def parse_response_text(response):
    return response["choices"][0]["message"]["content"]
