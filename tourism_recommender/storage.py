"""Database persistence for cluster memberships and top attractions."""

from __future__ import annotations

from typing import Dict, List

import numpy as np

from config import CLUSTER_TOP_ATTRACTIONS_TABLE, DB_CONFIG, USER_CLUSTER_MEMBERSHIPS_TABLE
from db import execute, fetch_all, connection_cursor


def ensure_tables() -> None:
    execute(
        f"""
        CREATE TABLE IF NOT EXISTS {USER_CLUSTER_MEMBERSHIPS_TABLE} (
            user_id BIGINT NOT NULL,
            cluster_id INT NOT NULL,
            cluster_1_membership_percent DECIMAL(10,8) NULL,
            cluster_2_membership_percent DECIMAL(10,8) NULL,
            cluster_3_membership_percent DECIMAL(10,8) NULL,
            cluster_4_membership_percent DECIMAL(10,8) NULL,
            cluster_5_membership_percent DECIMAL(10,8) NULL,
            cluster_6_membership_percent DECIMAL(10,8) NULL,
            cluster_7_membership_percent DECIMAL(10,8) NULL,
            cluster_8_membership_percent DECIMAL(10,8) NULL,
            cluster_9_membership_percent DECIMAL(10,8) NULL,
            cluster_10_membership_percent DECIMAL(10,8) NULL,
            is_hard_assignment TINYINT(1) NOT NULL,
            PRIMARY KEY (user_id),
            KEY idx_user_cluster_memberships_cluster (cluster_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """
    )
    with connection_cursor(dictionary=False) as (_, cur):
        db_name = DB_CONFIG.get("database")
        cur.execute(
            "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s",
            (db_name, USER_CLUSTER_MEMBERSHIPS_TABLE),
        )
        existing_columns = {row[0] for row in cur.fetchall()}
        for i in range(1, 11):
            col_name = f"cluster_{i}_membership_percent"
            if col_name not in existing_columns:
                cur.execute(
                    f"ALTER TABLE {USER_CLUSTER_MEMBERSHIPS_TABLE} ADD COLUMN {col_name} DECIMAL(10,8) NULL"
                )
        if "membership_score" in existing_columns:
            cur.execute(
                f"ALTER TABLE {USER_CLUSTER_MEMBERSHIPS_TABLE} DROP COLUMN membership_score"
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
    c = membership.shape[0]
    rows = []
    for pos, user_id in enumerate(user_ids):
        cluster_id = int(hard_labels[pos])
        percents = [
            float(membership[idx, pos] * 100.0) if idx < min(c, 10) else None
            for idx in range(10)
        ]
        row = (int(user_id), cluster_id, *percents, 1)
        rows.append(row)

    placeholders = ", ".join(["%s"] * 13)
    cols = [
        "user_id",
        "cluster_id",
        "cluster_1_membership_percent",
        "cluster_2_membership_percent",
        "cluster_3_membership_percent",
        "cluster_4_membership_percent",
        "cluster_5_membership_percent",
        "cluster_6_membership_percent",
        "cluster_7_membership_percent",
        "cluster_8_membership_percent",
        "cluster_9_membership_percent",
        "cluster_10_membership_percent",
        "is_hard_assignment",
    ]
    cols_str = ", ".join(cols)

    with connection_cursor(dictionary=False) as (_, cur):
        cur.execute(f"DELETE FROM {USER_CLUSTER_MEMBERSHIPS_TABLE}")
        cur.executemany(
            f"INSERT INTO {USER_CLUSTER_MEMBERSHIPS_TABLE} ({cols_str}) VALUES ({placeholders})",
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
