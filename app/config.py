import os
from pydantic import BaseModel

class Settings(BaseModel):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")

    RSS_URLS: str = os.getenv("RSS_URLS", "https://blog.arbitrum.io/rss/")
    GITHUB_REPOS: str = os.getenv("GITHUB_REPOS", "ethereum/consensus-specs,solana-labs/solana")

    # NEW: funding feeds
    FUNDING_RSS_URLS: str = os.getenv("FUNDING_RSS_URLS", "https://www.coindesk.com/arc/outboundfeeds/rss/")

    # NEW: token check
    COINGECKO_BASE_URL: str = os.getenv("COINGECKO_BASE_URL", "https://api.coingecko.com/api/v3")

    DISCORD_WEBHOOK_URL: str | None = os.getenv("DISCORD_WEBHOOK_URL")
    ALERT_SCORE_MIN: float = float(os.getenv("ALERT_SCORE_MIN", "80"))

settings = Settings()