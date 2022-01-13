import psycopg2
from psycopg2.extras import DictCursor
import os

DB_URL = os.environ.get("DATABASE_URL", "dbname=project-2-cryptrack")


def sql_select(query, params):
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor(cursor_factory=DictCursor)
    cur.execute(query, params)
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results
