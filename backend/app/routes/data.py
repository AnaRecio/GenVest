from flask import Blueprint, request, jsonify
import yfinance as yf

# Create a Blueprint for stock data routes
data_bp = Blueprint('data', __name__)

# POST endpoint to fetch stock data for one or more tickers
@data_bp.route('/api/stock-data', methods=['POST'])
def get_stock_data():
    try:
        # Get list of ticker symbols from request body
        tickers = request.json.get("tickers", [])
        if not tickers:
            return jsonify({"error": "No tickers provided"}), 400

        results = []

        # Loop through each ticker and fetch financial data
        for symbol in tickers:
            stock = yf.Ticker(symbol)  # Create yfinance object
            info = stock.info          # Retrieve company info

            # Extract relevant data and append to results list
            results.append({
                "ticker": symbol,
                "longName": info.get("longName"),                # Full company name
                "currentPrice": info.get("currentPrice"),        # Latest market price
                "marketCap": info.get("marketCap"),              # Market capitalization
                "trailingPE": info.get("trailingPE"),            # Price-to-Earnings ratio (trailing 12 months)
                "volume": info.get("volume"),                    # Latest trading volume
                "fiftyTwoWeekHigh": info.get("fiftyTwoWeekHigh"),# 52-week high
                "fiftyTwoWeekLow": info.get("fiftyTwoWeekLow"),  # 52-week low
                "sector": info.get("sector"),                    # Business sector (e.g., Technology)
            })

        # Return the list of company data as JSON
        return jsonify(results)
    
    except Exception as e:
        # Handle and return any unexpected errors
        return jsonify({"error": str(e)}), 500

