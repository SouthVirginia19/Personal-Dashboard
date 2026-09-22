import json
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from ..config import settings
from ..models import CacheEntry, Snapshot
from .github import GitHubClient


class Aggregator:
    def __init__(self, db: Session):
        self.db = db
        self.gh = GitHubClient(settings.github_token)

    def _cache_get(self, key: str):
        entry = self.db.query(CacheEntry).filter_by(key=key).first()
        if entry and entry.expires_at > datetime.utcnow():
            return json.loads(entry.value)
        return None

    def _cache_set(self, key: str, value: dict):
        expires = datetime.utcnow() + timedelta(minutes=settings.cache_ttl_minutes)
        entry = self.db.query(CacheEntry).filter_by(key=key).first()
        if entry:
            entry.value = json.dumps(value)
            entry.expires_at = expires
        else:
            self.db.add(CacheEntry(key=key, value=json.dumps(value), expires_at=expires))
        self.db.commit()

    async def get_dashboard(self, username: str) -> dict:
        cache_key = f"dashboard:{username}"
        cached = self._cache_get(cache_key)
        if cached:
            cached["cached"] = True
            return cached

        user = await self.gh.get_user(username)
        repos = await self.gh.get_repos(username)
        contrib = await self.gh.get_contributions(username)

        languages: dict[str, int] = {}
        total_stars = 0
        for r in repos:
            if r.get("language"):
                languages[r["language"]] = languages.get(r["language"], 0) + 1
            total_stars += r.get("stargazers_count", 0)

        top_repos = sorted(repos, key=lambda r: r.get("stargazers_count", 0), reverse=True)[:6]

        result = {
            "user": {
                "login": user["login"],
                "name": user.get("name"),
                "avatar_url": user["avatar_url"],
                "bio": user.get("bio"),
                "followers": user["followers"],
                "following": user["following"],
                "public_repos": user["public_repos"],
                "created_at": user["created_at"],
            },
            "stats": {
                "total_stars": total_stars,
                "total_commits": contrib["total"],
                "languages": dict(sorted(languages.items(), key=lambda x: -x[1])),
            },
            "top_repos": [
                {
                    "name": r["name"],
                    "description": r.get("description"),
                    "stars": r["stargazers_count"],
                    "forks": r["forks_count"],
                    "language": r.get("language"),
                    "url": r["html_url"],
                }
                for r in top_repos
            ],
            "contributions": contrib["days"],
            "cached": False,
            "fetched_at": datetime.utcnow().isoformat(),
        }

        self._cache_set(cache_key, result)
        self._save_snapshot(result)
        return result

    def _save_snapshot(self, data: dict):
        today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        exists = self.db.query(Snapshot).filter(Snapshot.date >= today).first()
        if exists:
            return
        self.db.add(
            Snapshot(
                date=datetime.utcnow(),
                followers=data["user"]["followers"],
                public_repos=data["user"]["public_repos"],
                total_stars=data["stats"]["total_stars"],
                total_commits=data["stats"]["total_commits"],
            )
        )
        self.db.commit()