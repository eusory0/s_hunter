from app.config import settings
from app.scoring import score_opportunity
from app.models import Opportunity
from app.store import upsert_opportunity
from app.alerts import maybe_alert_discord
from app.collectors.rss import fetch_rss
from app.collectors.github import fetch_releases

def run_pipeline() -> dict:
    new_count = 0
    scanned = 0

    # RSS
    rss_urls = [u.strip() for u in settings.RSS_URLS.split(",") if u.strip()]
    for url in rss_urls:
        for item in fetch_rss(url):
            scanned += 1
            s = score_opportunity(item["source"], item["type"], item["title"], item["url"], item["meta"])
            opp = Opportunity(**item, score=s)
            if upsert_opportunity(opp):
                new_count += 1
                maybe_alert_discord(opp)

    # GitHub
    repos = [r.strip() for r in settings.GITHUB_REPOS.split(",") if r.strip()]
    for repo in repos:
        try:
            for item in fetch_releases(repo):
                scanned += 1
                s = score_opportunity(item["source"], item["type"], item["title"], item["url"], item["meta"])
                opp = Opportunity(**item, score=s)
                if upsert_opportunity(opp):
                    new_count += 1
                    maybe_alert_discord(opp)
        except Exception:
            # ignore repo failures for MVP
            pass

    return {"scanned": scanned, "new": new_count}