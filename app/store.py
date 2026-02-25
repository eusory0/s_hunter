import json
from datetime import datetime, timezone
from app.db import connect
from app.models import Opportunity

def _now():
    return datetime.now(timezone.utc)

def upsert_opportunity(opp: Opportunity) -> bool:
    """
    Returns True if inserted (new), False if already existed.
    Also updates last_seen_at for existing records.
    """
    now = _now()
    meta_json = json.dumps(opp.meta)

    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM opportunities WHERE id = %s", (opp.id,))
            exists = cur.fetchone() is not None

            if not exists:
                cur.execute("""
                    INSERT INTO opportunities
                      (id, source, type, title, url, ts, score, meta_json, first_seen_at, last_seen_at, alerted_at)
                    VALUES
                      (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NULL)
                """, (
                    opp.id,
                    opp.source,
                    opp.type,
                    opp.title,
                    opp.url,
                    opp.ts,
                    opp.score,
                    meta_json,
                    now,
                    now,
                ))
                conn.commit()
                return True

            # Existing: refresh last_seen_at; optionally refresh score/title/url/meta
            cur.execute("""
                UPDATE opportunities
                SET
                  last_seen_at = %s,
                  score = GREATEST(score, %s),
                  title = %s,
                  url = %s,
                  meta_json = %s
                WHERE id = %s
            """, (now, opp.score, opp.title, opp.url, meta_json, opp.id))
            conn.commit()
            return False

def mark_alerted(opp_id: str):
    now = _now()
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE opportunities
                SET alerted_at = %s
                WHERE id = %s AND alerted_at IS NULL
            """, (now, opp_id))
        conn.commit()

def list_opportunities(limit: int = 200, min_score: float | None = None):
    with connect() as conn:
        with conn.cursor() as cur:
            if min_score is None:
                cur.execute("""
                    SELECT id, source, type, title, url, ts, score
                    FROM opportunities
                    ORDER BY score DESC, ts DESC
                    LIMIT %s
                """, (limit,))
            else:
                cur.execute("""
                    SELECT id, source, type, title, url, ts, score
                    FROM opportunities
                    WHERE score >= %s
                    ORDER BY score DESC, ts DESC
                    LIMIT %s
                """, (min_score, limit))
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

def list_high(min_score: float = 85.0, limit: int = 200):
    return list_opportunities(limit=limit, min_score=min_score)