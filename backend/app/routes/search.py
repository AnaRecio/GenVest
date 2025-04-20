from flask import Blueprint, request, jsonify
import requests
import os
from dotenv import load_dotenv
load_dotenv()

search_bp = Blueprint("search", __name__)
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")

# Cache all stocks
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

# Load once
load_symbols()

@search_bp.route("/api/search", methods=["GET"])
def search_tickers():
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

    # Sort highest score first, then alphabetically
    results = sorted(results, key=lambda x: (-x["score"], x["symbol"]))

    final = [{"symbol": r["symbol"], "name": r["name"]} for r in results[:10]]
    return jsonify(final)
