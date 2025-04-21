from flask import Blueprint, request, jsonify
from app.services.serper_client import fetch_news
from app.services.openai_client import summarize_articles

# Create a Blueprint for news endpoints
news_bp = Blueprint('news', __name__)

# POST endpoint to fetch & summarize latest news for a company
@news_bp.route('/api/news', methods=['POST'])
def get_news_summary():
    try:
        query = request.json.get("query")  
        openai_key = request.json.get("openai_key")  
        serper_key = request.json.get("serper_key") 

        if not query or not openai_key or not serper_key:
            return jsonify({"error": "Missing query, OpenAI key, or Serper key"}), 400

        # Fetch news articles using Serper
        articles = fetch_news(query, serper_key)

        # Summarize articles with GPT
        summary = summarize_articles(articles, openai_key)

        return jsonify({
            "summary": summary,
            "articles": articles
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
