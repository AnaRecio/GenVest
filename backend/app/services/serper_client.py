import requests

def fetch_news(query, api_key):
    headers = {
        "X-API-KEY": api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "q": query,
        "gl": "us",
        "hl": "en",
        "num": 5
    }

    response = requests.post(
        "https://google.serper.dev/news",
        headers=headers,
        json=payload
    )
    
    response.raise_for_status()
    return response.json().get("news", [])
