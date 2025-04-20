import yfinance as yf

def get_stock_data_from_yf(ticker):
    """
    Returns a single stock’s core market data as a dict.
    """
    stock = yf.Ticker(ticker)
    info = stock.info
    return {
        "ticker": ticker,
        "longName": info.get("longName"),
        "currentPrice": info.get("currentPrice"),
        "marketCap": info.get("marketCap"),
        "trailingPE": info.get("trailingPE"),
        "volume": info.get("volume"),
        "fiftyTwoWeekHigh": info.get("fiftyTwoWeekHigh"),
        "fiftyTwoWeekLow": info.get("fiftyTwoWeekLow"),
        "sector": info.get("sector"),
        "exchange": info.get("exchange"), 
    }
