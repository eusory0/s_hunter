import requests
from app.config import settings
from app.models import Opportunity

def maybe_alert_discord(opp: Opportunity):
    if not settings.DISCORD_WEBHOOK_URL:
        return
    if opp.score < settings.ALERT_SCORE_MIN:
        return

    payload = {
        "content": f"🟣 s_hunter HIGH SCORE: **{opp.score:.0f}**\n**{opp.title}**\n{opp.url}"
    }
    try:
        requests.post(settings.DISCORD_WEBHOOK_URL, json=payload, timeout=10)
    except Exception:
        pass