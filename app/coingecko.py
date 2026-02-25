import requests
from app.config import settings

def coingecko_search(query: str) -> dict:
    if not query:
        return {"found": False, "best": None}

    url = f"{settings.COINGECKO_BASE_URL}/search"
    r = requests.get(url, params={"query": query}, timeout=15)
    r.raise_for_status()
    data = r.json()

    coins = data.get("coins", []) or []
    if not coins:
        return {"found": False, "best": None}

    best = coins[0]
    return {"found": True, "best": {"id": best.get("id"), "name": best.get("name"), "symbol": best.get("symbol")}}