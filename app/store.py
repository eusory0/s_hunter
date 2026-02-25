import json
from app.db import connect
from app.models import Opportunity

def upsert_opportunity(opp: Opportunity) -> bool:
    """
    Returns True if inserted (new), False if already existed.
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT id FROM opportunities WHERE id = ?", (opp.id,))
    exists = cur.fetchone() is not None
    if not exists:
        cur.execute("""
            INSERT INTO opportunities (id, source, type, title, url, ts, score, meta_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (opp.id, opp.source, opp.type, opp.title, opp.url, opp.ts, opp.score, json.dumps(opp.meta)))
        conn.commit()
    conn.close()
    return not exists

def list_opportunities(limit: int = 200):
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, source, type, title, url, ts, score, meta_json
        FROM opportunities
        ORDER BY score DESC, ts DESC
        LIMIT ?
    """, (limit,))
    rows = cur.fetchall()
    conn.close()
    out = []
    for r in rows:
        out.append({
            "id": r["id"],
            "source": r["source"],
            "type": r["type"],
            "title": r["title"],
            "url": r["url"],
            "ts": r["ts"],
            "score": r["score"],
        })
    return out