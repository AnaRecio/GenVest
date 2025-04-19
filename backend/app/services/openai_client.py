from openai import OpenAI

def summarize_articles(articles, api_key):
    """
    Sends a list of articles to GPT and returns a summarized explanation.
    Each article should have 'title' and 'snippet'.
    """
    client = OpenAI(api_key=api_key)

    article_texts = [f"- {a['title']}: {a.get('snippet', '')}" for a in articles]
    prompt = (
        "Summarize the following recent news for an investor audience. "
        "Highlight sentiment, key facts, and trends:\n\n"
        + "\n".join(article_texts)
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{ "role": "user", "content": prompt }],
        temperature=0.5,
        max_tokens=300
    )

    return response.choices[0].message.content


def generate_swot_analysis(company_name, api_key):
    """
    Uses GPT to generate a company profile, SWOT analysis, and general investment outlook.
    """
    client = OpenAI(api_key=api_key)

    prompt = (
        f"Provide a professional investment summary for {company_name}. Include:\n"
        "- A short company description (1 paragraph)\n"
        "- A SWOT analysis (Strengths, Weaknesses, Opportunities, Threats)\n"
        "- Conclude with an overall outlook (bullish/bearish/neutral) with reasoning\n"
        "Respond in clear markdown format with bold headers for each section."
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{ "role": "user", "content": prompt }],
        temperature=0.5,
        max_tokens=500
    )

    return {
        "markdown": response.choices[0].message.content
    }


def generate_investment_recommendation(forecast_prices, news_summary, company_name, api_key):
    """
    Uses GPT to analyze news and price forecast to return a buy/hold/sell recommendation.
    """
    client = OpenAI(api_key=api_key)

    try:
        prices = [p["predicted_price"] for p in forecast_prices]
        trend = "rising" if prices[-1] > prices[0] else "falling"
    except:
        trend = "unknown"

    company_info = f"For {company_name}, " if company_name else ""

    prompt = (
        f"{company_info}based on the following:\n"
        f"1. News Summary: {news_summary}\n"
        f"2. Price Trend: The stock is expected to be {trend} over the next days.\n\n"
        "Please provide an investment recommendation: Buy, Hold, or Sell.\n"
        "Explain your reasoning in a short paragraph for an investor audience."
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{ "role": "user", "content": prompt }],
        temperature=0.4,
        max_tokens=300
    )

    return {
        "recommendation": response.choices[0].message.content
    }

