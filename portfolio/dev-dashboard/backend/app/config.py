from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    github_token: str = ""
    github_username: str = "SouthVirginia19"
    database_url: str = "sqlite:///./dashboard.db"
    cache_ttl_minutes: int = 60


settings = Settings()