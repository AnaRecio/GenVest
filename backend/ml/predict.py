import pandas as pd
import joblib
from datetime import timedelta
from ml.utils import fetch_stock_history, build_features
import os

# In-memory cache for storing previously computed forecasts
# Structure: { ticker: (forecast_df, historical_df) }
_prediction_cache = {}

def forecast_prices(ticker: str, forecast_days: int = 30):
    """
    Generates a forecast of future stock prices using a pre-trained model.
    Uses a recursive approach to predict prices day by day.

    Parameters:
        ticker (str): The stock ticker symbol.
        forecast_days (int): Number of days into the future to predict.

    Returns:
        Tuple[pd.DataFrame, pd.DataFrame]:
            - forecast_df: DataFrame of future dates and predicted prices
            - historical_df: DataFrame of historical prices used for context
    """
    # Return cached result if available
    if ticker in _prediction_cache:
        print(f"✅ Cache hit for {ticker}")
        return _prediction_cache[ticker]

    print(f"🚀 Generating forecast for {ticker}")

    # Fetch and prepare historical data
    df = fetch_stock_history(ticker)
    df = build_features(df)

    # Load pre-trained model
    model_path = f"ml/models/{ticker}.pkl"
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model not found for ticker: {ticker}. Please train it first.")
    
    model = joblib.load(model_path)

    # Initialize forecast with last known data point
    last_known = df.iloc[-1:].copy()
    forecasts = []
    last_date = df.index[-1]

    # Predict recursively one day at a time
    for i in range(forecast_days):
        features = last_known.drop(columns=['price'])
        pred = model.predict(features)[0]

        forecasts.append({
            "date": last_date + timedelta(days=i + 1),
            "predicted_price": float(pred)
        })

        # Create new row using prediction and updated lag/rolling features
        new_row = last_known.copy()
        new_row['price'] = pred

        # Update lag features
        for lag in range(10, 1, -1):
            new_row[f"lag_{lag}"] = new_row[f"lag_{lag-1}"]
        new_row["lag_1"] = pred

        # Recalculate rolling statistics
        new_row["rolling_mean_3"] = new_row[[f"lag_{i}" for i in range(1, 4)]].mean(axis=1)
        new_row["rolling_std_5"] = new_row[[f"lag_{i}" for i in range(1, 6)]].std(axis=1)

        last_known = new_row

    # Format forecast output
    forecast_df = pd.DataFrame(forecasts)

    # Cache the forecast and historical data
    _prediction_cache[ticker] = (forecast_df, df[["price"]])
    
    return forecast_df, df[["price"]]
