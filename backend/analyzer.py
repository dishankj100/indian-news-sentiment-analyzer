import os
import json
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0,
    openai_api_key=OPENAI_API_KEY,
)

ANALYSIS_PROMPT = PromptTemplate(
    input_variables=["title", "description"],
    template="""
You are a political news analyst specializing in Indian politics.

Analyze this news article and return ONLY a valid JSON object with these fields:
- sentiment: one of "positive", "negative", or "neutral"
- sentiment_score: float between -1.0 (most negative) and 1.0 (most positive)
- political_topic: short label e.g. "Elections", "Economy", "Parliament", "Governance", "Security"
- key_entities: list of up to 3 political entities/parties/people mentioned
- one_line_summary: one concise sentence summarizing the article

Article Title: {title}
Article Description: {description}

Return ONLY valid JSON, no explanation, no markdown.
"""
)

def analyze_single(article: dict) -> dict:
    """Runs LLM analysis on a single article and merges results."""
    prompt = ANALYSIS_PROMPT.format(
        title=article.get("title", ""),
        description=article.get("description", ""),
    )
    try:
        response = llm.invoke(prompt)
        analysis = json.loads(response.content)
    except (json.JSONDecodeError, Exception):
        analysis = {
            "sentiment": "neutral",
            "sentiment_score": 0.0,
            "political_topic": "General",
            "key_entities": [],
            "one_line_summary": article.get("title", ""),
        }

    return {**article, **analysis}

def analyze_articles(articles: list[dict]) -> list[dict]:
    """Analyzes a list of articles and returns enriched results."""
    return [analyze_single(a) for a in articles]
