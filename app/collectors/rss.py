import feedparser
from dateutil import parser as dtparser
from hashlib import sha1

def fetch_rss(url: str):
    d = feedparser.parse(url)
    items = []
    for e in d.entries[:30]:
        title = getattr(e, "title", "") or ""
        link = getattr(e, "link", "") or ""
        published = getattr(e, "published", None) or getattr(e, "updated", None) or ""
        try:
            ts = dtparser.parse(published).isoformat()
        except Exception:
            ts = "1970-01-01T00:00:00"

        oid = sha1(f"rss|{url}|{link}|{title}".encode("utf-8")).hexdigest()
        items.append({
            "id": oid,
            "source": "rss",
            "type": "post",
            "title": title,
            "url": link,
            "ts": ts,
            "meta": {"feed": url}
        })
    return items