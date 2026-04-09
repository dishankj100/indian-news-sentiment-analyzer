const API_BASE = "http://localhost:8000";

function setTopic(topic) {
  document.getElementById("topicInput").value = topic;
  runAnalysis();
}

async function runAnalysis() {
  const topic = document.getElementById("topicInput").value.trim();
  if (!topic) return;

  const loader = document.getElementById("loader");
  const resultsGrid = document.getElementById("resultsGrid");
  const statsRow = document.getElementById("statsRow");
  const errorMsg = document.getElementById("errorMsg");

  loader.style.display = "block";
  resultsGrid.innerHTML = "";
  statsRow.style.display = "none";
  errorMsg.style.display = "none";

  try {
    const response = await fetch(`${API_BASE}/api/analyze?topic=${encodeURIComponent(topic)}&limit=10`);
    if (!response.ok) {
      const err = await response.json();
      throw new Error(err.detail || "API error");
    }
    const data = await response.json();
    renderResults(data);
  } catch (err) {
    errorMsg.textContent = `Error: ${err.message}. Make sure the backend is running at ${API_BASE}`;
    errorMsg.style.display = "block";
  } finally {
    loader.style.display = "none";
  }
}

function renderResults(data) {
  const articles = data.articles || [];
  if (!articles.length) return;

  const pos = articles.filter(a => a.sentiment === "positive").length;
  const neg = articles.filter(a => a.sentiment === "negative").length;
  const neu = articles.filter(a => a.sentiment === "neutral").length;

  document.getElementById("totalCount").textContent = articles.length;
  document.getElementById("posCount").textContent = pos;
  document.getElementById("negCount").textContent = neg;
  document.getElementById("neuCount").textContent = neu;
  document.getElementById("statsRow").style.display = "grid";

  const grid = document.getElementById("resultsGrid");
  grid.innerHTML = articles.map(article => buildCard(article)).join("");
}

function buildCard(a) {
  const sentClass = `badge-${a.sentiment || "neutral"}`;
  const entities = (a.key_entities || []).map(e => `<span class="entity-tag">${e}</span>`).join("");
  const score = a.sentiment_score ?? 0;
  const barWidth = Math.round(((score + 1) / 2) * 100);
  const barColor = score > 0.1 ? "#2e7d32" : score < -0.1 ? "#c62828" : "#888";

  return `
    <a href="${a.url}" target="_blank" rel="noopener">
      <div class="article-card">
        <div class="card-top">
          <div class="article-title">${escHtml(a.title || "")}</div>
          <span class="sentiment-badge ${sentClass}">${a.sentiment || "neutral"}</span>
        </div>
        <p class="summary">${escHtml(a.one_line_summary || a.description || "")}</p>
        <div class="card-meta">
          ${a.political_topic ? `<span class="topic-tag">${escHtml(a.political_topic)}</span>` : ""}
          ${entities}
          <span class="source">${escHtml(a.source || "")}</span>
        </div>
        <div class="score-bar">
          <div class="score-fill" style="width:${barWidth}%; background:${barColor};"></div>
        </div>
      </div>
    </a>`;
}

function escHtml(str) {
  return str.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");
}
