"""Database persistence for cluster memberships and top attractions."""

from __future__ import annotations

from typing import Dict, List

import numpy as np

from config import CLUSTER_TOP_ATTRACTIONS_TABLE, USER_CLUSTER_MEMBERSHIPS_TABLE
from db import execute, fetch_all, connection_cursor


def ensure_tables() -> None:
    execute(
        f"""
        CREATE TABLE IF NOT EXISTS {USER_CLUSTER_MEMBERSHIPS_TABLE} (
            user_id BIGINT NOT NULL,
            cluster_id INT NOT NULL,
            membership_score DECIMAL(10,8) NOT NULL,
            is_hard_assignment TINYINT(1) NOT NULL,
            PRIMARY KEY (user_id),
            KEY idx_user_cluster_memberships_cluster (cluster_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """
    )
    execute(
        f"""
        CREATE TABLE IF NOT EXISTS {CLUSTER_TOP_ATTRACTIONS_TABLE} (
            cluster_id INT NOT NULL,
            attraction_id BIGINT NOT NULL,
            rank_no INT NOT NULL,
            popularity_score DECIMAL(18,8) NOT NULL,
            PRIMARY KEY (cluster_id, rank_no),
            KEY idx_cluster_top_attr_cluster (cluster_id),
            KEY idx_cluster_top_attr_attraction (attraction_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """
    )


def save_user_cluster_memberships(user_ids: List[int], membership: np.ndarray, hard_labels: np.ndarray) -> None:
    ensure_tables()
    rows = []
    for pos, user_id in enumerate(user_ids):
        cluster_id = int(np.argmax(membership[:, pos]))
        rows.append((int(user_id), cluster_id, float(np.max(membership[:, pos])), 1))
    with connection_cursor(dictionary=False) as (_, cur):
        cur.execute(f"DELETE FROM {USER_CLUSTER_MEMBERSHIPS_TABLE}")
        cur.executemany(
            f"INSERT INTO {USER_CLUSTER_MEMBERSHIPS_TABLE} (user_id, cluster_id, membership_score, is_hard_assignment) VALUES (%s, %s, %s, %s)",
            rows,
        )


def save_cluster_top_attractions(cluster_top: Dict[int, List[dict]]) -> None:
    ensure_tables()
    rows = []
    for cluster_id, items in cluster_top.items():
        for item in items:
            rows.append((int(cluster_id), int(item["attraction_id"]), int(item["rank"]), float(item["popularity_score"])))
    with connection_cursor(dictionary=False) as (_, cur):
        cur.execute(f"DELETE FROM {CLUSTER_TOP_ATTRACTIONS_TABLE}")
        if rows:
            cur.executemany(
                f"INSERT INTO {CLUSTER_TOP_ATTRACTIONS_TABLE} (cluster_id, attraction_id, rank_no, popularity_score) VALUES (%s, %s, %s, %s)",
                rows,
            )
