import os
import requests
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
NEWS_API_URL = "https://newsapi.org/v2/everything"

def fetch_headlines(topic: str = "India politics", limit: int = 10) -> list[dict]:
    """
    Fetches recent news headlines for a given topic using NewsAPI.
    Returns a list of article dicts with title, description, url, source.
    """
    if not NEWS_API_KEY:
        raise ValueError("NEWS_API_KEY not set in environment variables.")

    params = {
        "q": topic,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": limit,
        "apiKey": NEWS_API_KEY,
    }

    response = requests.get(NEWS_API_URL, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    articles = []
    for item in data.get("articles", []):
        articles.append({
            "title": item.get("title", ""),
            "description": item.get("description", ""),
            "url": item.get("url", ""),
            "source": item.get("source", {}).get("name", "Unknown"),
            "published_at": item.get("publishedAt", ""),
        })

    return articles
