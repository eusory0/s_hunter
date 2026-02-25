from app.config import settings
from app.scoring import score_opportunity
from app.models import Opportunity
from app.store import upsert_opportunity
from app.alerts import maybe_alert_discord
from app.collectors.rss import fetch_rss
from app.collectors.github import fetch_releases
from app.collectors.funding import fetch_funding_from_rss
from app.coingecko import coingecko_search

def run_pipeline() -> dict:
    new_count = 0
    scanned = 0

    # 1) RSS (general)
    rss_urls = [u.strip() for u in settings.RSS_URLS.split(",") if u.strip()]
    for url in rss_urls:
        for item in fetch_rss(url):
            scanned += 1
            s = score_opportunity(item["source"], item["type"], item["title"], item["url"], item["meta"])
            opp = Opportunity(**item, score=s)
            if upsert_opportunity(opp):
                new_count += 1
                maybe_alert_discord(opp)

    # 2) Funding RSS + token check
    funding_urls = [u.strip() for u in settings.FUNDING_RSS_URLS.split(",") if u.strip()]
    for furl in funding_urls:
        for item in fetch_funding_from_rss(furl):
            scanned += 1

            project = (item.get("meta") or {}).get("project")
            token_found = None
            token_best = None
            if project:
                try:
                    res = coingecko_search(project)
                    token_found = bool(res.get("found"))
                    token_best = res.get("best")
                except Exception:
                    token_found = None

            item["meta"] = {
                **(item.get("meta") or {}),
                "token_found": token_found,
                "token_best": token_best,
            }

            s = score_opportunity(item["source"], item["type"], item["title"], item["url"], item["meta"])
            opp = Opportunity(**item, score=s)
            if upsert_opportunity(opp):
                new_count += 1
                maybe_alert_discord(opp)

    # 3) GitHub releases
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
            pass

    return {"scanned": scanned, "new": new_count}