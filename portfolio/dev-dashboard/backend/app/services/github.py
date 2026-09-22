from typing import Any

import httpx


class GitHubClient:
    REST = "https://api.github.com"
    GRAPHQL = "https://api.github.com/graphql"

    def __init__(self, token: str = ""):
        self.token = token
        headers = {"Accept": "application/vnd.github+json"}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        self.headers = headers

    async def get_user(self, username: str) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get(f"{self.REST}/users/{username}", headers=self.headers)
            r.raise_for_status()
            return r.json()

    async def get_repos(self, username: str, per_page: int = 100) -> list[dict[str, Any]]:
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get(
                f"{self.REST}/users/{username}/repos",
                headers=self.headers,
                params={"per_page": per_page, "sort": "updated"},
            )
            r.raise_for_status()
            return r.json()

    async def get_contributions(self, username: str) -> dict[str, Any]:
        if not self.token:
            return {"total": 0, "days": []}

        query = """
        query($login: String!) {
          user(login: $login) {
            contributionsCollection {
              contributionCalendar {
                totalContributions
                weeks {
                  contributionDays {
                    date
                    contributionCount
                  }
                }
              }
            }
          }
        }
        """
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.post(
                self.GRAPHQL,
                headers=self.headers,
                json={"query": query, "variables": {"login": username}},
            )
            r.raise_for_status()
            payload = r.json()

        user = (payload.get("data") or {}).get("user")
        if not user:
            return {"total": 0, "days": []}

        cal = user["contributionsCollection"]["contributionCalendar"]
        days = [d for week in cal["weeks"] for d in week["contributionDays"]]
        return {"total": cal["totalContributions"], "days": days}