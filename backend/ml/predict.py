import pandas as pd
import joblib
from datetime import timedelta
from ml.utils import fetch_stock_history, build_features
import os

# In-memory cache: ticker -> (forecast_df, history_df)
_prediction_cache = {}

def forecast_prices(ticker: str, forecast_days: int = 30):
    if ticker in _prediction_cache:
        print(f"✅ Cache hit for {ticker}")
        return _prediction_cache[ticker]

    print(f"🚀 Generating forecast for {ticker}")
    df = fetch_stock_history(ticker)
    df = build_features(df)

    model_path = f"ml/models/{ticker}.pkl"
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model not found for ticker: {ticker}. Please train it first.")

    model = joblib.load(model_path)

    # Recursive Forecast
    last_known = df.iloc[-1:].copy()
    forecasts = []
    last_date = df.index[-1]

    for i in range(forecast_days):
        features = last_known.drop(columns=['price'])
        pred = model.predict(features)[0]
        forecasts.append({
            "date": last_date + timedelta(days=i + 1),
            "predicted_price": float(pred)
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

    # Cache it
    _prediction_cache[ticker] = (forecast_df, df[["price"]])
    return forecast_df, df[["price"]]
