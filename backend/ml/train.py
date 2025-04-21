import os
import joblib
from xgboost import XGBRegressor
from ml.utils import fetch_stock_history, build_features
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_absolute_error

def train_model(X, y):
    """
    Trains an XGBoost regression model on the provided dataset.

    Parameters:
        X (pd.DataFrame): Feature matrix
        y (pd.Series): Target variable (price)

    Returns:
        XGBRegressor: Trained model instance
    """
    model = XGBRegressor(
        n_estimators=300,
        learning_rate=0.05,
        objective="reg:squarederror",
        random_state=42,
        verbosity=0
    )
    model.fit(X, y)
    return model

def train_and_save(ticker):
    """
    Fetches data for a stock ticker, trains a model using cross-validation,
    saves the final model, and returns the average validation MAE.

    Parameters:
        ticker (str): Stock ticker symbol

    Returns:
        float: Average mean absolute error (MAE) across validation folds
    """
    # Fetch historical price data and generate lag-based features
    df = fetch_stock_history(ticker)
    df = build_features(df)

    X = df.drop(columns=["price"])
    y = df["price"]

    # Use time series-aware cross-validation
    tscv = TimeSeriesSplit(n_splits=5)
    val_scores = []

    for train_idx, val_idx in tscv.split(X):
        if len(val_idx) == 0:
            continue  # Skip iteration if validation set is empty

        X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
        y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]

        model = train_model(X_train, y_train)
        preds = model.predict(X_val)

        if len(y_val) > 0:
            mae = mean_absolute_error(y_val, preds)
            val_scores.append(mae)

    # Calculate average MAE or fallback to 0 if no valid folds
    avg_mae = sum(val_scores) / len(val_scores) if val_scores else 0.0

    # Train a final model on all available data
    final_model = train_model(X, y)

    # Save the model to disk
    model_path = os.path.join("ml", "models", f"{ticker}.pkl")
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(final_model, model_path)

    return avg_mae

if __name__ == "__main__":
    # Run standalone training for a specific ticker (used for manual testing/debugging)
    ticker = "AAPL"
    mae = train_and_save(ticker)
    print(f"Model trained and saved for {ticker} — Validation MAE: {mae:.2f}")
