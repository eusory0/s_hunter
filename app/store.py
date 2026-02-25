import json
from app.db import connect
from app.models import Opportunity

def upsert_opportunity(opp: Opportunity) -> bool:
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM opportunities WHERE id = %s", (opp.id,))
            exists = cur.fetchone() is not None
            if not exists:
                cur.execute("""
                    INSERT INTO opportunities (id, source, type, title, url, ts, score, meta_json)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    opp.id,
                    opp.source,
                    opp.type,
                    opp.title,
                    opp.url,
                    opp.ts,
                    opp.score,
                    json.dumps(opp.meta),
                ))
                conn.commit()
            return not exists

def list_opportunities(limit: int = 200):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, source, type, title, url, ts, score
                FROM opportunities
                ORDER BY score DESC, ts DESC
                LIMIT %s
            """, (limit,))
            rows = cur.fetchall()

    out = []
    for (id_, source, type_, title, url, ts, score) in rows:
        out.append({
            "id": id_,
            "source": source,
            "type": type_,
            "title": title,
            "url": url,
            "ts": ts.isoformat() if hasattr(ts, "isoformat") else str(ts),
            "score": float(score),
        })
    return out