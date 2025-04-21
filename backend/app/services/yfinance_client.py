import yfinance as yf

def get_stock_data_from_yf(ticker):
    """
    Fetches basic market information for a given stock ticker using yfinance.

    Parameters:
        ticker (str): The stock ticker symbol (e.g., "AAPL", "TSLA").

    Returns:
        dict: A dictionary containing key market data for the specified stock.
    """
    # Create a yfinance Ticker object for the given symbol
    stock = yf.Ticker(ticker)

    # Retrieve the stock's information dictionary
    info = stock.info

    # Return selected fields in a structured dictionary
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
