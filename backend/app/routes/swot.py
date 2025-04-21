from flask import Blueprint, request, jsonify
from app.services.openai_client import generate_swot_analysis

# Define a Flask Blueprint for the SWOT analysis endpoint
swot_bp = Blueprint('swot', __name__)

# POST endpoint to generate a SWOT analysis and investment summary using OpenAI
@swot_bp.route('/api/swot', methods=['POST'])
def get_swot_and_summary():
    try:
        # Extract input values from the request payload
        company_name = request.json.get("company")
        api_key = request.json.get("openai_key")

        # Validate required inputs
        if not company_name or not api_key:
            return jsonify({"error": "Missing company name or OpenAI key"}), 400

        # Generate SWOT analysis using the OpenAI API
        result = generate_swot_analysis(company_name, api_key)

        # Return the result as a JSON response
        return jsonify(result)

    except Exception as e:
        # Return a JSON-formatted error message if something goes wrong
        return jsonify({"error": str(e)}), 500
