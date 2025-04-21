from flask import Blueprint, request, jsonify
from ml.predict import forecast_prices
from ml.train import train_and_save
from app.utils.charts import plot_predictions
import os

# Define a Flask Blueprint for prediction-related routes
prediction_bp = Blueprint("prediction", __name__)

@prediction_bp.route('/api/predict', methods=['POST'])
def predict_stock_prices():
    try:
        # Extract ticker symbol from incoming JSON request
        ticker = request.json.get("ticker")
        if not ticker:
            return jsonify({"error": "Ticker is required"}), 400

        try:
            # Attempt to generate forecast using existing model
            forecast_df, history_df, mae = forecast_prices(ticker)
        except FileNotFoundError:
            # If model doesn't exist, train it and retry forecasting
            print(f"Model missing for {ticker}, training now...")
            train_and_save(ticker)
            forecast_df, history_df, mae = forecast_prices(ticker)

        # Generate chart from historical and predicted data
        chart_base64 = plot_predictions(history_df, forecast_df)

        # Return the forecast, chart, and MAE metric as JSON response
        return jsonify({
            "ticker": ticker,
            "predictions": forecast_df.to_dict(orient="records"),
            "chart": chart_base64,
            "mae": round(mae, 4)
        })

    except Exception as e:
        # Catch-all error handler for unexpected issues
        return jsonify({"error": str(e)}), 500
