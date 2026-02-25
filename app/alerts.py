import requests
from app.config import settings
from app.models import Opportunity

def maybe_alert_discord(opp: Opportunity) -> bool:
    """
    Returns True if alert was sent, else False.
    """
    if not settings.DISCORD_WEBHOOK_URL:
        return False
    if opp.score < settings.ALERT_SCORE_MIN:
        return False

    payload = {
        "content": (
            f"🟣 s_hunter HIGH SCORE: **{opp.score:.0f}**\n"
            f"**{opp.title}**\n"
            f"{opp.url}"
        )
    }
    try:
        r = requests.post(settings.DISCORD_WEBHOOK_URL, json=payload, timeout=10)
        return 200 <= r.status_code < 300
    except Exception:
        return False