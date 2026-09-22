# 📊 Dev Dashboard

A personal developer statistics dashboard.

Fetches data from the GitHub API and displays it in a clean web interface: profile, language breakdown, top repositories, and a GitHub-style yearly contribution heatmap.

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=flat-square&logo=fastapi&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-F7DF1E?style=flat-square&logo=javascript&logoColor=black)
![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=flat-square&logo=sqlite&logoColor=white)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)

---

## 📸 Screenshot

> Add a screenshot here after your first run. Drag a PNG into the GitHub README editor — it will upload and insert the correct link automatically.

---

## ✨ Features

- 👤 **Profile** — avatar, name, bio, followers, public repo count
- 📈 **Key stats** — total stars, commits over the past year, language count
- 🍩 **Language chart** — doughnut chart of repository languages
- 🟩 **Contribution heatmap** — 365-day activity calendar, GitHub-style
- ⭐ **Top repositories** — top 6 repos sorted by stars, with descriptions
- ⚡ **Caching** — responses stored in SQLite with configurable TTL
- 📅 **Daily snapshots** — metrics saved for future trend charts
- 🔍 **Username search** — look up any public GitHub account

---

## 🛠 Tech Stack

**Backend**
- Python 3.11+
- FastAPI
- SQLAlchemy
- httpx
- pydantic-settings

**Frontend**
- Vanilla JavaScript (ES6+)
- Chart.js
- Plain CSS with custom properties
- Responsive layout

**Database**
- SQLite (cache + snapshots)

**APIs**
- GitHub REST API
- GitHub GraphQL API

---

## 📁 Project Structure
dev-dashboard/
├── backend/
│ ├── app/
│ │ ├── init.py
│ │ ├── config.py # settings loaded from .env
│ │ ├── database.py # SQLAlchemy setup
│ │ ├── models.py # CacheEntry, Snapshot
│ │ ├── main.py # FastAPI entry point
│ │ └── services/
│ │ ├── init.py
│ │ ├── github.py # GitHub REST + GraphQL client
│ │ └── aggregator.py # aggregation + cache logic
│ ├── requirements.txt
│ └── .env.example
├── frontend/
│ ├── index.html
│ ├── style.css
│ ├── app.js
│ └── chart.min.js
├── .gitignore
└── README.md


---

## 🚀 Getting Started

### Requirements

- Python 3.11+ — https://www.python.org/downloads/
- Git — https://git-scm.com/
- GitHub Personal Access Token — https://github.com/settings/tokens?type=beta

### 1. Clone the repository

```bash
git clone https://github.com/SouthVirginia19/dev-dashboard.git
cd dev-dashboard/backend
python -m venv .venv
```
# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1

# Windows (cmd)
.venv\Scripts\activate.bat

# Linux / macOS
source .venv/bin/activate

    ⚠️ If PowerShell blocks script execution:
    powershell

    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

    Confirm with Y. This affects only your user account.

3. Install dependencies

pip install -r requirements.txt

4. Create a GitHub token

    Open https://github.com/settings/tokens?type=beta

    Generate new token — give it any name

    Expiration: 90 days or longer

    Repository access: All repositories

    Account permissions — enable:

        Followers → Read-only

        Starring → Read-only

    Generate token, copy it immediately (shown only once)

    💡 The app runs without a token, but the contribution heatmap and yearly commit count stay empty — the GraphQL endpoint requires authentication.

5. Configure .env

Create backend/.env:
env

GITHUB_TOKEN=github_pat_your_token_here
GITHUB_USERNAME=your_github_username
DATABASE_URL=sqlite:///./dashboard.db
CACHE_TTL_MINUTES=60

No spaces, no quotes. One key per line.
6. Start the server
bash

uvicorn app.main:app --reload --port 8000

Expected output:
text

INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.

7. Open in your browser

👉 http://127.0.0.1:8000
🎮 Usage

    By default, the dashboard shows stats for the user defined in .env (GITHUB_USERNAME).

    To view another user, enter their username in the search field at the top and click Load.

    Responses are cached for 60 minutes (configurable via CACHE_TTL_MINUTES). Repeated requests are served from SQLite.

    Badge in the profile corner:

        🟢 "fresh data" — just fetched from GitHub

        🔵 "from cache" — served from the local database

Resetting the cache

To force a refresh:
bash

rm dashboard.db            # Linux / macOS
Remove-Item dashboard.db   # Windows PowerShell

The file is recreated automatically on the next request.
🔌 API Endpoints
Method	Endpoint	Params	Description
GET	/api/health	—	Server status and token presence
GET	/api/dashboard	?username= (optional)	Full user statistics
Example response from /api/dashboard
json

{
  "user": {
    "login": "SouthVirginia19",
    "name": "...",
    "avatar_url": "https://...",
    "followers": 42,
    "public_repos": 12
  },
  "stats": {
    "total_stars": 15,
    "total_commits": 68,
    "languages": { "Python": 5, "JavaScript": 4, "Rust": 2 }
  },
  "top_repos": [],
  "contributions": [],
  "cached": false,
  "fetched_at": "2026-09-22T12:34:56"
}

⚙️ Configuration

All options are set through .env:
Variable	Default	Description
GITHUB_TOKEN	""	Personal Access Token. Required for GraphQL
GITHUB_USERNAME	SouthVirginia19	Default username
DATABASE_URL	sqlite:///./dashboard.db	SQLAlchemy connection string
CACHE_TTL_MINUTES	60	Cache lifetime in minutes
🗺 Roadmap

    ☑

    MVP: profile, key stats, heatmap, top repos
    ☑

    SQLite caching
    ☑

    Daily metric snapshots
    □

    📈 Trend charts for stars / followers (/api/snapshots)
    □

    🧩 LeetCode panel (GraphQL)
    □

    🦀 Rust CLI (devdash stats <username>)
    □

    🚀 Deploy to Railway / Fly.io
    □

    🤖 GitHub Action for nightly snapshots
    □

    🌓 Dark / light theme toggle

🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you'd like to change.

    Fork the repository

    Create a branch: git checkout -b feature/amazing-feature

    Commit: git commit -m "Add amazing feature"

    Push: git push origin feature/amazing-feature

    Open a Pull Request

📄 License

Released under the MIT License. See LICENSE for details.
👤 Author

SouthVirginia19

GitHub: @SouthVirginia19

⭐ If this project was useful, consider giving it a star!
