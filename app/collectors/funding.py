import re
from app.collectors.rss import fetch_rss

FUNDING_KEYWORDS = [
    "raises", "raised", "funding", "seed", "series", "round",
    "invest", "investment", "backed", "led by", "valuation",
    "strategic", "financing"
]

# Heuristic: extrage "Project" din titluri de tipul:
# "Project raises $X..." / "Project secures funding..." / "Project closes Series A..."
PROJECT_PATTERNS = [
    re.compile(r"^([A-Z][A-Za-z0-9\-\._ ]{1,40})\s+(raises|raised|secures|lands|closes|announces)\b", re.I),
    re.compile(r"^([A-Z][A-Za-z0-9\-\._ ]{1,40})\s+(seed|series)\b", re.I),
]

def looks_like_funding(title: str) -> bool:
    t = (title or "").lower()
    return any(k in t for k in FUNDING_KEYWORDS)

def extract_project_name(title: str) -> str | None:
    if not title:
        return None
    for pat in PROJECT_PATTERNS:
        m = pat.search(title.strip())
        if m:
            name = m.group(1).strip()
            # curățare ușoară
            name = re.sub(r"\s{2,}", " ", name)
            # evităm titluri gen "Crypto VC..." ca nume
            if len(name) >= 2:
                return name
    return None

def fetch_funding_from_rss(feed_url: str):
    items = fetch_rss(feed_url)
    out = []
    for it in items:
        title = it.get("title", "")
        if not looks_like_funding(title):
            continue
        project = extract_project_name(title)
        it["type"] = "funding"
        it["meta"] = {**it.get("meta", {}), "project": project}
        out.append(it)
    return out