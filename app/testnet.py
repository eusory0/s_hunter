import re
from app.collectors.rss import fetch_rss

TESTNET_KEYWORDS = [
    "testnet",
    "devnet",
    "alpha",
    "beta",
    "points program",
    "faucet",
    "incentivized",
    "incentivised"
]

NOISE_KEYWORDS = [
    "etf",
    "sec approval",
    "round-the-clock trading",
    "regulation",
    "tokenized mmes"
]

def looks_like_testnet(title: str) -> bool:
    t = (title or "").lower()
    if any(n in t for n in NOISE_KEYWORDS):
        return False
    return any(k in t for k in TESTNET_KEYWORDS)

def extract_project_from_title(title: str) -> str | None:
    # heuristic simplu: primul cuvânt capitalizat înainte de "launches" etc.
    match = re.match(r"^([A-Z][A-Za-z0-9\-\._ ]{2,40})\s+(launches|announces|introduces)", title)
    if match:
        return match.group(1).strip()
    return None

def fetch_testnet_from_rss(feed_url: str):
    items = fetch_rss(feed_url)
    out = []
    for it in items:
        title = it.get("title", "")
        if not looks_like_testnet(title):
            continue

        project = extract_project_from_title(title)

        it["type"] = "testnet"
        it["meta"] = {
            **(it.get("meta") or {}),
            "project": project,
            "testnet_detected": True
        }
        out.append(it)

    return out