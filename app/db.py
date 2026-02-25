from app.config import settings
import psycopg

def connect():
    if not settings.DATABASE_URL:
        raise RuntimeError("DATABASE_URL is not set")
    return psycopg.connect(settings.DATABASE_URL)

def _ensure_column(cur, table: str, col: str, coltype: str):
    # Safe idempotent migration
    cur.execute(
        """
        SELECT 1
        FROM information_schema.columns
        WHERE table_name = %s AND column_name = %s
        """,
        (table, col),
    )
    exists = cur.fetchone() is not None
    if not exists:
        cur.execute(f'ALTER TABLE "{table}" ADD COLUMN "{col}" {coltype}')

def init_db():
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""
            CREATE TABLE IF NOT EXISTS opportunities (
                id TEXT PRIMARY KEY,
                source TEXT NOT NULL,
                type TEXT NOT NULL,
                title TEXT NOT NULL,
                url TEXT NOT NULL,
                ts TIMESTAMPTZ NOT NULL,
                score DOUBLE PRECISION NOT NULL,
                meta_json TEXT
            )
            """)
            # Migrations for v1 automation
            _ensure_column(cur, "opportunities", "first_seen_at", "TIMESTAMPTZ")
            _ensure_column(cur, "opportunities", "last_seen_at", "TIMESTAMPTZ")
            _ensure_column(cur, "opportunities", "alerted_at", "TIMESTAMPTZ")

        conn.commit()