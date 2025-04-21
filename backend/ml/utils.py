import yfinance as yf
import pandas as pd

def fetch_stock_history(ticker, days=180):
    """
    Fetches recent historical closing prices for a given stock ticker.

    Parameters:
        ticker (str): Stock ticker symbol (e.g., "AAPL").
        days (int): Number of past days of data to retrieve.

    Returns:
        pd.DataFrame: DataFrame containing a 'price' column with datetime index.
    """
    # Download historical stock data from Yahoo Finance
    stock = yf.Ticker(ticker)
    df = stock.history(period=f"{days}d")

    # Extract and rename the closing price
    df = df[['Close']].rename(columns={"Close": "price"})

    # Ensure index is datetime for proper time series operations
    df.index = pd.to_datetime(df.index)

    return df

def build_features(df, lags=10):
    """
    Constructs lag features and rolling statistics for time series forecasting.

    Parameters:
        df (pd.DataFrame): DataFrame containing a 'price' column.
        lags (int): Number of lag features to generate.

    Returns:
        pd.DataFrame: Feature-enhanced DataFrame with lag and rolling features.
    """
    # Generate lag features: previous price values up to `lags` days back
    for i in range(1, lags + 1):
        df[f"lag_{i}"] = df['price'].shift(i)

    # Add short-term rolling statistics as additional features
    df['rolling_mean_3'] = df['price'].rolling(3).mean()
    df['rolling_std_5'] = df['price'].rolling(5).std()

    # Remove rows with NaNs caused by shifting and rolling operations
    df = df.dropna()

    return df
