from flask import Blueprint, request, jsonify
import requests
import os
from rapidfuzz import fuzz, process

search_bp = Blueprint("search", __name__)
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")

# Cache all stocks here
all_stocks = []

def load_symbols():
    global all_stocks
    print("🔁 Loading symbols list from Finnhub...")
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
    print(f"✅ Loaded {len(all_stocks)} tickers from Finnhub")

# Load on app start
load_symbols()

@search_bp.route("/api/search", methods=["GET"])
def search_tickers():
    query = request.args.get("q", "").strip().lower()
    if not query:
        return jsonify([])

    results = []

    for stock in all_stocks:
        name = stock["name"].lower()
        symbol = stock["symbol"].lower()

        # Prioritize direct inclusion first
        if query in name or query in symbol:
            score = 100
        else:
            score = max(
                fuzz.partial_ratio(query, name),
                fuzz.partial_ratio(query, symbol),
                fuzz.token_set_ratio(query, name)
            )

        if score >= 60:
            results.append({**stock, "score": score})

    # Sort by score and alphabetically to ensure consistency
    results = sorted(results, key=lambda x: (-x["score"], x["symbol"]))

    # Return top 5 without score
    final = [{"symbol": r["symbol"], "name": r["name"]} for r in results[:5]]
    return jsonify(final)
