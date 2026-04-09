from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from scraper import fetch_headlines
from analyzer import analyze_articles
import uvicorn

app = FastAPI(title="Indian News Sentiment Analyzer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Indian News Sentiment Analyzer — API is running"}

@app.get("/api/analyze")
def get_analysis(topic: str = "India politics", limit: int = 10):
    """
    Fetch news headlines for a topic and return LLM-based sentiment analysis.
    """
    try:
        articles = fetch_headlines(topic=topic, limit=limit)
        if not articles:
            raise HTTPException(status_code=404, detail="No articles found for this topic.")
        results = analyze_articles(articles)
        return {"topic": topic, "count": len(results), "articles": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/topics")
def get_topics():
    """Returns preset political topics for quick search."""
    return {
        "topics": [
            "India elections",
            "BJP Congress",
            "Lok Sabha",
            "India economy policy",
            "India state government",
            "India parliament",
        ]
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
