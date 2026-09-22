from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from .config import settings
from .database import Base, engine, get_db
from .services.aggregator import Aggregator

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Dev Dashboard", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
async def health():
    return {"status": "ok", "token_configured": bool(settings.github_token)}


@app.get("/api/dashboard")
async def dashboard(username: str | None = None, db: Session = Depends(get_db)):
    target = username or settings.github_username
    try:
        return await Aggregator(db).get_dashboard(target)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"GitHub API error: {e}") from e


# --- раздача фронтенда ---
frontend_dir = Path(__file__).resolve().parent.parent.parent / "frontend"
if frontend_dir.exists():
    app.mount("/", StaticFiles(directory=str(frontend_dir), html=True), name="frontend")