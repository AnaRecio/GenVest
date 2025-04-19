from flask import Blueprint, request, jsonify
from app.models.predictor import predict_future_prices
from app.utils.charts import plot_predictions

prediction_bp = Blueprint("prediction", __name__)

@prediction_bp.route('/api/predict', methods=['POST'])
def predict_stock_prices():
    try:
        ticker = request.json.get("ticker")
        if not ticker:
            return jsonify({"error": "Ticker is required"}), 400

        forecast_df, history_df = predict_future_prices(ticker)
        chart_base64 = plot_predictions(history_df, forecast_df)

        return jsonify({
            "ticker": ticker,
            "predictions": forecast_df.to_dict(orient="records"),
            "chart": chart_base64
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
