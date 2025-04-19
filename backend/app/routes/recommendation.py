from flask import Blueprint, request, jsonify
from app.services.openai_client import generate_investment_recommendation

recommendation_bp = Blueprint("recommendation", __name__)

@recommendation_bp.route('/api/recommendation', methods=['POST'])
def get_recommendation():
    try:
        forecast = request.json.get("forecast")       # List of future prices
        news_summary = request.json.get("news")       # Summary from GPT
        company_name = request.json.get("company")    # Optional
        api_key = request.json.get("openai_key")

        if not forecast or not news_summary or not api_key:
            return jsonify({"error": "Missing forecast, news, or OpenAI key"}), 400

        result = generate_investment_recommendation(forecast, news_summary, company_name, api_key)
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
