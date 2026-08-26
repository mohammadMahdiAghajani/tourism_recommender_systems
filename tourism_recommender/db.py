"""Database helpers for MariaDB/MySQL access."""

from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator

import mysql.connector
from mysql.connector import Error

from config import DB_CONFIG


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


@contextmanager
def connection_cursor(dictionary: bool = True) -> Iterator[tuple]:
    conn = get_connection()
    cursor = conn.cursor(dictionary=dictionary)
    try:
        yield conn, cursor
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()


def fetch_all(query: str, params: tuple | None = None):
    with connection_cursor(dictionary=True) as (_, cur):
        cur.execute(query, params or ())
        return cur.fetchall()


def fetch_one(query: str, params: tuple | None = None):
    with connection_cursor(dictionary=True) as (_, cur):
        cur.execute(query, params or ())
        return cur.fetchone()


def execute(query: str, params: tuple | None = None) -> int:
    with connection_cursor(dictionary=False) as (_, cur):
        cur.execute(query, params or ())
        return cur.rowcount
