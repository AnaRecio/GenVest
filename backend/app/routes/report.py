from flask import Blueprint, request, jsonify, send_file
from app.routes.data import get_stock_data
from app.services.serper_client import fetch_news
from app.services.openai_client import (
    summarize_articles,
    generate_swot_analysis,
    generate_investment_recommendation
)
from app.models.predictor import predict_future_prices
from app.utils.charts import plot_predictions
from app.services.yfinance_client import get_stock_data_from_yf
from app.utils.pdf import generate_pdf_report

import tempfile
import io

report_bp = Blueprint("report", __name__, url_prefix="/api")

# === Primary Report Generator Endpoint ===
@report_bp.route("/report", methods=["POST"])
def generate_full_report():
    try:
        print("📥 POST /api/report hit")

        # 🔑 Input
        data = request.get_json()
        ticker = data.get("ticker")
        openai_key = data.get("openai_key")
        serper_key = data.get("serper_key")

        print(f"➡️ Ticker: {ticker}, OpenAI Key received: {bool(openai_key)}, Serper Key received: {bool(serper_key)}")

        if not ticker or not openai_key or not serper_key:
            return jsonify({"error": "Missing ticker, OpenAI key, or Serper key"}), 400

        # Step 1: Financial Data
        stock_data = get_stock_data_from_yf(ticker)
        print("📊 Stock data fetched")

        company_name = stock_data.get("longName", ticker)

        # Step 2: News + Summary
        articles = fetch_news(company_name, serper_key)
        print(f"📰 {len(articles)} articles fetched")
        news_summary = summarize_articles(articles, openai_key)
        print("📝 News summarized")

        # Step 3: SWOT
        swot_markdown = generate_swot_analysis(company_name, openai_key).get("markdown", "")
        print("✅ SWOT generated")

        # Step 4: Price Forecast
        forecast_df, history_df = predict_future_prices(ticker)
        forecast_list = forecast_df.to_dict(orient="records")
        chart_base64 = plot_predictions(history_df, forecast_df)
        print("📈 Price forecast complete")

        # Step 5: Recommendation
        recommendation_data = generate_investment_recommendation(
            forecast_list, news_summary, company_name, openai_key
        )
        recommendation = recommendation_data.get("recommendation", "No recommendation.")
        print("💡 Recommendation generated")

        # Final Report
        report = {
            "ticker": ticker,
            "company": company_name,
            "marketData": stock_data,
            "news": {
                "summary": news_summary,
                "articles": articles
            },
            "swot": swot_markdown,
            "forecast": forecast_list,
            "priceChart": chart_base64,
            "recommendation": recommendation
        }

        print("✅ Report assembled")
        return jsonify(report)

    except Exception as e:
        print("❌ Error generating report:", str(e))
        return jsonify({"error": str(e)}), 500

# === PDF Download Endpoint ===
@report_bp.route("/report/download", methods=["POST"])
def download_pdf_report():
    try:
        report_data = request.get_json().get("report")
        if not report_data:
            return jsonify({"error": "No report data provided"}), 400

        pdf_bytes = generate_pdf_report(report_data)

        return send_file(
            io.BytesIO(pdf_bytes),
            mimetype="application/pdf",
            as_attachment=True,
            download_name="genvest_report.pdf"
        )

    except Exception as e:
        print("❌ PDF download failed:", str(e))
        return jsonify({"error": str(e)}), 500
