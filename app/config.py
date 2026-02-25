import os
from pydantic import BaseModel

class Settings(BaseModel):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")

    RSS_URLS: str = os.getenv("RSS_URLS", "https://blog.arbitrum.io/rss/")
    GITHUB_REPOS: str = os.getenv("GITHUB_REPOS", "ethereum/consensus-specs,solana-labs/solana")

    DISCORD_WEBHOOK_URL: str | None = os.getenv("DISCORD_WEBHOOK_URL")
    ALERT_SCORE_MIN: float = float(os.getenv("ALERT_SCORE_MIN", "80"))

settings = Settings()