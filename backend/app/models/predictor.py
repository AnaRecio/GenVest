import yfinance as yf
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from datetime import timedelta

def fetch_stock_history(ticker, days=90):
    """
    Fetches the last `days` of historical daily price data for a given stock.
    """
    stock = yf.Ticker(ticker)
    df = stock.history(period=f"{days}d")
    return df[['Close']].rename(columns={"Close": "price"})

def predict_future_prices(ticker, forecast_days=14):
    """
    Uses a Random Forest Regressor to predict the next `forecast_days` prices.
    Returns a DataFrame with both historical and predicted values.
    """
    df = fetch_stock_history(ticker)

    # Feature engineering: lagged price values
    df['lag_1'] = df['price'].shift(1)
    df['lag_2'] = df['price'].shift(2)
    df = df.dropna()

    # Prepare train data
    X = df[['lag_1', 'lag_2']]
    y = df['price']

    # Train model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)

    # Start prediction from the last known values
    last_values = df.iloc[-1][['price', 'lag_1']].values.tolist()
    predictions = []
    dates = []

    last_date = df.index[-1]

    for i in range(forecast_days):
        next_input = [last_values[-1], last_values[-2]]  # lag_1, lag_2
        pred = model.predict([next_input])[0]
        predictions.append(pred)

        # Update lag values for next step
        last_values = [pred] + last_values[:-1]

        next_date = last_date + timedelta(days=i + 1)
        dates.append(next_date)

    forecast_df = pd.DataFrame({
        "date": dates,
        "predicted_price": predictions
    })

    return forecast_df, df  # Return both prediction and history for chart
