import os
from pydantic import BaseModel

class Settings(BaseModel):
    # DB (MVP): local sqlite file
    SQLITE_PATH: str = os.getenv("SQLITE_PATH", "shunter.sqlite")

    # Collectors
    RSS_URLS: str = os.getenv("RSS_URLS", "https://blog.arbitrum.io/rss/")
    GITHUB_REPOS: str = os.getenv("GITHUB_REPOS", "ethereum/consensus-specs,solana-labs/solana")

    # Alerts (optional)
    DISCORD_WEBHOOK_URL: str | None = os.getenv("DISCORD_WEBHOOK_URL")

    # Scoring thresholds
    ALERT_SCORE_MIN: float = float(os.getenv("ALERT_SCORE_MIN", "80"))

settings = Settings()