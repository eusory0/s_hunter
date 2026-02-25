import requests
from hashlib import sha1
from dateutil import parser as dtparser

def fetch_releases(repo: str):
    # repo like "owner/name"
    url = f"https://api.github.com/repos/{repo}/releases"
    r = requests.get(url, timeout=15, headers={"Accept": "application/vnd.github+json"})
    r.raise_for_status()
    releases = r.json()[:10]

    items = []
    for rel in releases:
        title = rel.get("name") or rel.get("tag_name") or f"Release {repo}"
        link = rel.get("html_url") or ""
        published = rel.get("published_at") or rel.get("created_at") or ""
        try:
            ts = dtparser.parse(published).isoformat()
        except Exception:
            ts = "1970-01-01T00:00:00"

        oid = sha1(f"github|{repo}|{link}|{title}".encode("utf-8")).hexdigest()
        items.append({
            "id": oid,
            "source": "github",
            "type": "release",
            "title": f"{repo}: {title}",
            "url": link,
            "ts": ts,
            "meta": {"repo": repo}
        })
    return items