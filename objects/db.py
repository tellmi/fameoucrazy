# objects/db.py
# -*- coding: utf-8 -*-

import aiomysql
import logging


POOL_SIZE = 5

DB_CONFIG = {
    "user": "Betreuung",
    "password": "@cAring2025=",
    "host": "192.168.178.78",
    "port": 3306,
    "db": "Betreuung",
    "charset": "utf8mb4",
    "autocommit": True,
}

pool: aiomysql.Pool | None = None


# -------------------------------------------------------
#   DB CONNECTION POOL INITIALISIERUNG
# -------------------------------------------------------
async def init_pool():
    """Erstellt den globalen Connection-Pool."""
    global pool

    if pool is not None:
        return

    logging.info("[DB] Erstelle Async-Connection-Pool...")


    try:
        pool = await aiomysql.create_pool(
            **DB_CONFIG,
            minsize=1,
            maxsize=POOL_SIZE,
            pool_recycle=60,       # alte Verbindungen nach 60s erneuern
            connect_timeout=5,     # schnellerer Fehlerfall
        )
        logging.info("[DB] Async-Pool bereit.")
    except Exception as e:
        logging.warning("[DB] Fehler beim Erstellen des Pools:", e)
        raise


# -------------------------------------------------------
#   HELPERS
# -------------------------------------------------------
async def _ensure_connection(conn):
    """
    MySQL trennt Verbindungen nach einer gewissen Idle-Zeit.
    Dieser Ping stellt sicher, dass sie noch gültig ist.
    """
    try:
        await conn.ping(reconnect=True)
    except Exception as e:
        print(f"[DB] Ping fehlgeschlagen: {e}")
        logging.warning("[DB] Ping fehlgeschlagen:", e)
        raise


# -------------------------------------------------------
#   QUERY
# -------------------------------------------------------
async def query(sql, params=None):
    """
    Führt eine SELECT-Query aus.
    Gibt eine Liste von Tupeln zurück.
    """
    if pool is None:
        raise RuntimeError("DB-Pool nicht initialisiert")

    async with pool.acquire() as conn:
        await _ensure_connection(conn)

        async with conn.cursor() as cur:
            try:
                await cur.execute(sql, params or ())
                rows = await cur.fetchall()
                return rows
            except Exception as e:
                logging.warning(
                    "[DB] QUERY FEHLER: %s | params=%s | error=%s",
                    sql,
                    params,
                    e
                )

                raise


# -------------------------------------------------------
#   EXECUTE (INSERT / UPDATE / DELETE)
# -------------------------------------------------------
async def execute(sql, params=None):
    """
    Führt Insert/Update/Delete aus.
    Gibt die Anzahl der betroffen Zeilen zurück.
    """
    if pool is None:
        raise RuntimeError("DB-Pool nicht initialisiert")

    async with pool.acquire() as conn:
        await _ensure_connection(conn)

        async with conn.cursor() as cur:
            try:
                await cur.execute(sql, params or ())
                await conn.commit()
                return cur.rowcount
            except Exception as e:
                logging.warning(
                    "[DB] EXECUTE FEHLER: %s | params=%s | error=%s",
                    sql,
                    params,
                    e
                )
                raise


# -------------------------------------------------------
#   POOL SCHLIESSEN
# -------------------------------------------------------
async def close_pool():
    """Schließt den Pool beim App-Beenden."""
    global pool
    if pool is not None:
        pool.close()
        await pool.wait_closed()
        pool = None
        logging.info("[DB] Pool geschlossen.")
