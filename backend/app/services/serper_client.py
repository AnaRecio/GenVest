import requests

def fetch_news(query, api_key):
    """
    Fetches the latest news articles related to a given query using the Serper API.

    Parameters:
        query (str): The search term (e.g., company name or stock symbol).
        api_key (str): The Serper API key for authorization.

    Returns:
        list: A list of news article dictionaries returned by the API.
    """
    # Set request headers including API key and content type
    headers = {
        "X-API-KEY": api_key,
        "Content-Type": "application/json"
    }

    # Define request payload with search parameters
    payload = {
        "q": query,        # Search query
        "gl": "us",        # Geographic location (United States)
        "hl": "en",        # Language (English)
        "num": 5           # Number of results to return
    }

    # Make POST request to Serper's news search endpoint
    response = requests.post(
        "https://google.serper.dev/news",
        headers=headers,
        json=payload
    )
    
    # Raise an exception for any non-successful response
    response.raise_for_status()

    # Return the list of news items (empty list if not found)
    return response.json().get("news", [])
