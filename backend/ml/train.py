import os
import joblib
from xgboost import XGBRegressor
from ml.utils import fetch_stock_history, build_features
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_absolute_error

def train_model(X, y):
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
    df = fetch_stock_history(ticker)
    df = build_features(df)

    X = df.drop(columns=["price"])
    y = df["price"]

    tscv = TimeSeriesSplit(n_splits=5)
    val_scores = []

    for train_idx, val_idx in tscv.split(X):
        if len(val_idx) == 0:
            continue  # ✅ Skip if validation set is empty

        X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
        y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]

        model = train_model(X_train, y_train)
        preds = model.predict(X_val)

        if len(y_val) > 0:
            mae = mean_absolute_error(y_val, preds)
            val_scores.append(mae)

    avg_mae = sum(val_scores) / len(val_scores) if val_scores else 0.0  # ✅ Prevent division by zero

    # Final model trained on all available data
    final_model = train_model(X, y)
    model_path = os.path.join("ml", "models", f"{ticker}.pkl")
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(final_model, model_path)

    return avg_mae

if __name__ == "__main__":
    ticker = "AAPL"
    mae = train_and_save(ticker)
    print(f"✅ Model trained and saved for {ticker} — Validation MAE: {mae:.2f}")
