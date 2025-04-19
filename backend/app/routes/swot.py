from flask import Blueprint, request, jsonify
from app.services.openai_client import generate_swot_analysis

# Create a Blueprint for SWOT and summaries
swot_bp = Blueprint('swot', __name__)

# POST endpoint to generate SWOT + investment summary
@swot_bp.route('/api/swot', methods=['POST'])
def get_swot_and_summary():
    try:
        company_name = request.json.get("company")
        api_key = request.json.get("openai_key")

        if not company_name or not api_key:
            return jsonify({"error": "Missing company name or OpenAI key"}), 400

        result = generate_swot_analysis(company_name, api_key)
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
