# Indian News Sentiment Analyzer

An LLM-powered web application that fetches real-time Indian political news and performs sentiment analysis, topic classification, and entity extraction using Large Language Models (LangChain + OpenAI).

![Python](https://img.shields.io/badge/Python-3.10+-blue) ![FastAPI](https://img.shields.io/badge/FastAPI-0.110-green) ![LangChain](https://img.shields.io/badge/LangChain-0.1-orange) ![React](https://img.shields.io/badge/Frontend-HTML%2FJS-yellow)

## Features

- Real-time news fetching via NewsAPI for any political topic
- LLM-based sentiment scoring (positive / negative / neutral) with a confidence score
- Political topic classification (Elections, Economy, Parliament, Governance, etc.)
- Key entity extraction — identifies parties, politicians, and organizations
- One-line AI summary per article
- Clean dashboard UI with stats breakdown and sentiment score bars
- RESTful FastAPI backend with CORS support

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, FastAPI, Uvicorn |
| LLM Integration | LangChain, OpenAI GPT-3.5-turbo |
| News Data | NewsAPI |
| Frontend | HTML, CSS, Vanilla JavaScript |
| Environment | python-dotenv |

## Project Structure

```
indian-news-sentiment-analyzer/
├── backend/
│   ├── main.py          # FastAPI app and routes
│   ├── analyzer.py      # LangChain + LLM analysis logic
│   ├── scraper.py       # NewsAPI integration
│   └── requirements.txt
├── frontend/
│   ├── index.html       # Dashboard UI
│   ├── app.js           # Fetch + render logic
│   └── style.css        # Styles
├── .env.example
└── README.md
```

## Setup & Run

### 1. Clone the repository
```bash
git clone https://github.com/dishankj100/indian-news-sentiment-analyzer.git
cd indian-news-sentiment-analyzer
```

### 2. Set up environment variables
```bash
cp .env.example .env
# Edit .env and add your API keys
```

You need two free API keys:
- **NewsAPI**: Get a free key at [newsapi.org](https://newsapi.org)
- **OpenAI**: Get a key at [platform.openai.com](https://platform.openai.com)

### 3. Install Python dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 4. Run the backend
```bash
python main.py
# API runs at http://localhost:8000
```

### 5. Open the frontend
Open `frontend/index.html` in your browser. No build step needed.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| GET | `/api/analyze?topic=India+elections&limit=10` | Fetch + analyze articles |
| GET | `/api/topics` | Get preset topic suggestions |

### Sample Response
```json
{
  "topic": "India elections",
  "count": 10,
  "articles": [
    {
      "title": "BJP announces campaign strategy for upcoming state polls",
      "sentiment": "positive",
      "sentiment_score": 0.62,
      "political_topic": "Elections",
      "key_entities": ["BJP", "Amit Shah", "state polls"],
      "one_line_summary": "BJP outlines a multi-phase campaign targeting key constituencies ahead of state elections.",
      "source": "The Hindu",
      "url": "https://..."
    }
  ]
}
```

## How It Works

1. User enters a topic (e.g., "Lok Sabha") in the frontend
2. Frontend calls `/api/analyze` on the FastAPI backend
3. Backend fetches 10 latest articles from NewsAPI
4. Each article is passed to LangChain with a structured prompt
5. GPT-3.5-turbo returns JSON with sentiment, topic, entities, and summary
6. Results are returned to frontend and rendered as cards with score bars

## Future Improvements

- Add a historical sentiment trend chart (track topic sentiment over days)
- Support Hindi news sources via translation pipeline
- Add a comparison mode — compare sentiment across two topics side by side
- Integrate Redis caching to reduce API calls

## Author

Dishank Jain — [github.com/dishankj100](https://github.com/dishankj100) | [linkedin.com/in/dishankjain01](https://linkedin.com/in/dishankjain01)
