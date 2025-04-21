from flask import Blueprint, request, jsonify
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create a Blueprint for search-related routes
search_bp = Blueprint("search", __name__)

# Retrieve Finnhub API key from environment
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")

# In-memory cache for storing stock symbols
all_stocks = []

def load_symbols():
    """
    Load and cache a list of US common stock symbols from Finnhub API.
    This function runs once at startup.
    """
    global all_stocks
    print("Loading symbols list from Finnhub...")

    url = f"https://finnhub.io/api/v1/stock/symbol?exchange=US&token={FINNHUB_API_KEY}"
    res = requests.get(url)
    res.raise_for_status()
    data = res.json()

    all_stocks = [
        {
            "symbol": item["symbol"],
            "name": item.get("description", "") or item.get("displaySymbol", ""),
        }
        for item in data if item["type"] == "Common Stock"
    ]

    print(f"Loaded {len(all_stocks)} tickers from Finnhub")

# Initial symbol loading at application startup
load_symbols()

@search_bp.route("/api/search", methods=["GET"])
def search_tickers():
    """
    Perform a fuzzy search on cached stock symbols and return the top matches.
    Accepts query parameter "q" representing the user's search input.
    """
    query = request.args.get("q", "").strip().lower()
    if not query:
        return jsonify([])

    results = []

    for stock in all_stocks:
        symbol = stock["symbol"].lower()
        name = stock["name"].lower()

        score = 0
        if query == symbol or query == name:
            score = 100
        elif symbol.startswith(query) or name.startswith(query):
            score = 90
        elif query in symbol or query in name:
            score = 80

        if score > 0:
            results.append({**stock, "score": score})

    # Sort matches by score (descending), then by symbol (alphabetical)
    results = sorted(results, key=lambda x: (-x["score"], x["symbol"]))

    # Return top 10 matches with only relevant fields
    final = [{"symbol": r["symbol"], "name": r["name"]} for r in results[:10]]
    return jsonify(final)