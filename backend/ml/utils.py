import yfinance as yf
import pandas as pd

def fetch_stock_history(ticker, days=180):
    stock = yf.Ticker(ticker)
    df = stock.history(period=f"{days}d")
    df = df[['Close']].rename(columns={"Close": "price"})
    df.index = pd.to_datetime(df.index)
    return df

def build_features(df, lags=10):
    for i in range(1, lags + 1):
        df[f"lag_{i}"] = df['price'].shift(i)
    df['rolling_mean_3'] = df['price'].rolling(3).mean()
    df['rolling_std_5'] = df['price'].rolling(5).std()
    df = df.dropna()
    return df
