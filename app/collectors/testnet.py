import re
from hashlib import sha1
from app.collectors.rss import fetch_rss

TESTNET_KEYWORDS = [
    "testnet", "devnet", "alpha", "beta",
    "points program", "points", "faucet",
    "incentivized", "incentivised"
]

NOISE_KEYWORDS = [
    "etf", "sec approval", "round-the-clock trading",
    "regulation", "tokenized", "wall street", "wisdomtree"
]

def looks_like_testnet(title: str) -> bool:
    t = (title or "").lower()
    if any(n in t for n in NOISE_KEYWORDS):
        return False
    return any(k in t for k in TESTNET_KEYWORDS)

def extract_project_from_title(title: str) -> str | None:
    m = re.match(r"^([A-Z][A-Za-z0-9\-\._ ]{2,40})\s+(launches|announces|introduces)", title or "")
    if m:
        return m.group(1).strip()
    return None

def fetch_testnet_from_rss(feed_url: str):
    items = fetch_rss(feed_url)
    out = []
    for it in items:
        title = it.get("title", "")
        url = it.get("url", "")
        if not looks_like_testnet(title):
            continue

        project = extract_project_from_title(title)

        oid = sha1(f"testnet|{feed_url}|{url}|{title}".encode("utf-8")).hexdigest()

        out.append({
            "id": oid,
            "source": "rss",
            "type": "testnet",
            "title": title,
            "url": url,
            "ts": it.get("ts", "1970-01-01T00:00:00"),
            "meta": {
                "feed": feed_url,
                "project": project,
                "testnet_detected": True,
            }
        })
    return out