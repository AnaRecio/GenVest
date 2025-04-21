from flask import Blueprint, request, jsonify
from app.services.openai_client import generate_investment_recommendation

# Define a Flask Blueprint for the recommendation endpoint
recommendation_bp = Blueprint("recommendation", __name__)

@recommendation_bp.route('/api/recommendation', methods=['POST'])
def get_recommendation():
    try:
        # Extract required inputs from the request payload
        forecast = request.json.get("forecast")          # List of predicted price points
        news_summary = request.json.get("news")          # Summary of recent news for the company
        company_name = request.json.get("company")       # Optional company name
        api_key = request.json.get("openai_key")         # OpenAI API key provided by the client

        # Validate required fields are present
        if not forecast or not news_summary or not api_key:
            return jsonify({"error": "Missing forecast, news, or OpenAI key"}), 400

        # Generate a recommendation using the OpenAI service
        result = generate_investment_recommendation(forecast, news_summary, company_name, api_key)

        # Return the recommendation as a JSON response
        return jsonify(result)

    except Exception as e:
        # Handle unexpected server-side errors
        return jsonify({"error": str(e)}), 500
