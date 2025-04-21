from openai import OpenAI

def summarize_articles(articles, api_key):
    """
    Summarizes a list of news articles using OpenAI's GPT model.
    Each article should include a 'title' and a 'snippet'.
    """
    # Initialize the OpenAI client with the user's API key
    client = OpenAI(api_key=api_key)

    # Build a structured prompt using the titles and snippets of each article
    article_texts = [f"- {a['title']}: {a.get('snippet', '')}" for a in articles]
    prompt = (
        "Summarize the following recent news for an investor audience. "
        "Highlight sentiment, key facts, and trends:\n\n"
        + "\n".join(article_texts)
    )

    # Request a summary from the OpenAI Chat Completion API
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{ "role": "user", "content": prompt }],
        temperature=0.5,
        max_tokens=300
    )

    # Return the generated summary text
    return response.choices[0].message.content


def generate_swot_analysis(company_name, api_key):
    """
    Generates a SWOT analysis and investment summary for a given company.
    The response includes a company description, SWOT details, and outlook.
    """
    # Initialize the OpenAI client with the user's API key
    client = OpenAI(api_key=api_key)

    # Prompt describing the structure and content expected in the response
    prompt = (
        f"Provide a professional investment summary for {company_name}. Include:\n"
        "- A short company description (1 paragraph)\n"
        "- A SWOT analysis (Strengths, Weaknesses, Opportunities, Threats)\n"
        "- Conclude with an overall outlook (bullish/bearish/neutral) with reasoning\n"
        "Respond in clear markdown format with bold headers for each section."
    )

    # Request the SWOT analysis from the GPT model
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{ "role": "user", "content": prompt }],
        temperature=0.5,
        max_tokens=500
    )

    # Return the formatted markdown content
    return {
        "markdown": response.choices[0].message.content
    }


def generate_investment_recommendation(forecast_prices, news_summary, company_name, api_key):
    """
    Uses OpenAI to analyze forecasted prices and news sentiment, then provides
    an investment recommendation (Buy, Hold, or Sell) with reasoning.
    """
    # Initialize the OpenAI client with the user's API key
    client = OpenAI(api_key=api_key)

    # Attempt to determine price trend direction
    try:
        prices = [p["predicted_price"] for p in forecast_prices]
        trend = "rising" if prices[-1] > prices[0] else "falling"
    except:
        trend = "unknown"

    # Include company name in prompt if available
    company_info = f"For {company_name}, " if company_name else ""

    # Prompt combines company trend and news summary for recommendation
    prompt = (
        f"{company_info}based on the following:\n"
        f"1. News Summary: {news_summary}\n"
        f"2. Price Trend: The stock is expected to be {trend} over the next days.\n\n"
        "Please provide an investment recommendation: Buy, Hold, or Sell.\n"
        "Explain your reasoning in a short paragraph for an investor audience."
    )

    # Request recommendation from the GPT model
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{ "role": "user", "content": prompt }],
        temperature=0.4,
        max_tokens=300
    )

    # Return the recommendation message
    return {
        "recommendation": response.choices[0].message.content
    }
