from flask import Blueprint, request, jsonify, send_file
from app.routes.data import get_stock_data
from app.services.serper_client import fetch_news
from app.services.openai_client import (
    summarize_articles,
    generate_swot_analysis,
    generate_investment_recommendation
)
from ml.predict import forecast_prices
from ml.train import train_and_save
from app.utils.charts import plot_predictions
from app.services.yfinance_client import get_stock_data_from_yf
from app.utils.pdf import generate_pdf_report
import io

# Define a Flask Blueprint for report generation endpoints
report_bp = Blueprint("report", __name__, url_prefix="/api")

@report_bp.route("/report", methods=["POST", "OPTIONS"])
def generate_full_report():
    # Handle preflight CORS requests
    if request.method == "OPTIONS":
        return '', 204

    try:
        # Parse input data from request payload
        data = request.get_json()
        ticker = data.get("ticker")
        openai_key = data.get("openai_key")
        serper_key = data.get("serper_key")

        # Validate required fields
        if not ticker or not openai_key or not serper_key:
            return jsonify({"error": "Missing ticker, OpenAI key, or Serper key"}), 400

        # Retrieve core financial data for the specified ticker
        stock_data = get_stock_data_from_yf(ticker)
        company_name = stock_data.get("longName", ticker)

        # Retrieve and summarize news articles for the company
        articles = fetch_news(company_name, serper_key)
        news_summary = summarize_articles(articles, openai_key)

        # Generate SWOT analysis using OpenAI
        swot_markdown = generate_swot_analysis(company_name, openai_key).get("markdown", "")

        # Attempt to forecast future stock prices
        try:
            forecast_df, history_df = forecast_prices(ticker)
            mae = None
        except FileNotFoundError:
            # If model not found, train a new one and forecast again
            mae = train_and_save(ticker)
            forecast_df, history_df = forecast_prices(ticker)

        # Prepare data for frontend rendering
        forecast_list = forecast_df.to_dict(orient="records")
        chart_base64 = plot_predictions(history_df, forecast_df)

        # Generate investment recommendation based on forecast and news
        recommendation_data = generate_investment_recommendation(
            forecast_list, news_summary, company_name, openai_key
        )
        recommendation = recommendation_data.get("recommendation", "No recommendation.")

        # Assemble full report response
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
            "mae": round(mae, 2) if mae is not None else None,
            "priceChart": chart_base64,
            "recommendation": recommendation
        }

        return jsonify(report)

    except Exception as e:
        # Handle unexpected application errors
        return jsonify({"error": str(e)}), 500

@report_bp.route("/download", methods=["POST"])
def download_pdf_report():
    try:
        # Parse report content from the request
        report_data = request.get_json().get("report")
        if not report_data:
            return jsonify({"error": "No report data provided"}), 400

        # Generate PDF file bytes from report content
        pdf_bytes = generate_pdf_report(report_data)

        # Return PDF as downloadable file
        return send_file(
            io.BytesIO(pdf_bytes),
            mimetype="application/pdf",
            as_attachment=True,
            download_name="genvest_report.pdf"
        )

    except Exception as e:
        # Handle PDF generation or transmission errors
        return jsonify({"error": str(e)}), 500