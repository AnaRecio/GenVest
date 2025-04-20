import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_absolute_error
from datetime import timedelta


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


def train_model(X, y):
    model = GradientBoostingRegressor(n_estimators=300, learning_rate=0.05, random_state=42)
    model.fit(X, y)
    return model


def predict_future_prices(ticker, forecast_days=30):
    df = fetch_stock_history(ticker)
    df = build_features(df)

    X = df.drop(columns=['price'])
    y = df['price']

    model = train_model(X, y)

    # Recursive Forecast
    last_known = df.iloc[-1:].copy()
    forecasts = []
    last_date = df.index[-1]

    for i in range(forecast_days):
        features = last_known.drop(columns=['price'])
        pred = model.predict(features)[0]
        forecasts.append({
            "date": last_date + timedelta(days=i + 1),
            "predicted_price": pred
        })

        new_row = last_known.copy()
        new_row['price'] = pred

        # Shift lag features
        for lag in range(10, 1, -1):
            new_row[f"lag_{lag}"] = new_row[f"lag_{lag-1}"]
        new_row["lag_1"] = pred
        new_row["rolling_mean_3"] = new_row[[f"lag_{i}" for i in range(1, 4)]].mean(axis=1)
        new_row["rolling_std_5"] = new_row[[f"lag_{i}" for i in range(1, 6)]].std(axis=1)

        last_known = new_row

    forecast_df = pd.DataFrame(forecasts)
    return forecast_df, df[["price"]]  # Return predictions and history
