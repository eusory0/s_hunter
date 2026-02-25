from app.config import settings
from app.scoring import score_opportunity
from app.models import Opportunity
from app.store import upsert_opportunity, mark_alerted
from app.alerts import maybe_alert_discord
from app.collectors.rss import fetch_rss
from app.collectors.github import fetch_releases
from app.collectors.testnet import fetch_testnet_from_rss
from app.coingecko import coingecko_search

def _handle_item(item: dict) -> bool:
    s = score_opportunity(item["source"], item["type"], item["title"], item["url"], item.get("meta") or {})
    opp = Opportunity(**item, score=s)

    inserted = upsert_opportunity(opp)
    if inserted:
        sent = maybe_alert_discord(opp)
        if sent:
            mark_alerted(opp.id)
    return inserted

def run_pipeline() -> dict:
    new_count = 0
    scanned = 0

    # RSS
    rss_urls = [u.strip() for u in settings.RSS_URLS.split(",") if u.strip()]
    for url in rss_urls:
        for item in fetch_rss(url):
            scanned += 1
            if _handle_item(item):
                new_count += 1

# Testnet Hunter
for url in rss_urls:
    for item in fetch_testnet_from_rss(url):
        scanned += 1

        project = (item.get("meta") or {}).get("project")
        token_found = None

        if project:
            try:
                res = coingecko_search(project)
                token_found = bool(res.get("found"))
            except Exception:
                token_found = None

        item["meta"] = {
            **(item.get("meta") or {}),
            "token_found": token_found
        }

        if _handle_item(item):
            new_count += 1

    # GitHub
    repos = [r.strip() for r in settings.GITHUB_REPOS.split(",") if r.strip()]
    for repo in repos:
        try:
            for item in fetch_releases(repo):
                scanned += 1
                if _handle_item(item):
                    new_count += 1
        except Exception:
            pass

    return {"scanned": scanned, "new": new_count}