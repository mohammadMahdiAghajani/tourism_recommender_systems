"""Cluster-to-attraction ranking utilities."""

from __future__ import annotations

from typing import Dict, List, Tuple

import numpy as np

from config import ACTION_WEIGHTS, ATTRACTIONS_TABLE, ATTRACTION_PROFILES_TABLE, INTERACTIONS_TABLE, TOP_ATTRACTIONS_PER_CLUSTER
from db import fetch_all


def _interaction_weight(action_type: str, score) -> float:
    base = ACTION_WEIGHTS.get(action_type, 0.0)
    if action_type == "rate":
        try:
            normalized = (float(score) - 1.0) / 4.0
        except (TypeError, ValueError):
            normalized = 0.0
        return base * max(0.0, min(1.0, normalized))
    return base


def build_cluster_top_attractions(user_ids: List[int], membership: np.ndarray, hard_labels: np.ndarray, c: int, limit: int = TOP_ATTRACTIONS_PER_CLUSTER) -> Dict[int, List[dict]]:
    user_pos = {int(uid): idx for idx, uid in enumerate(user_ids)}
    interactions = fetch_all(
        f"""
        SELECT user_id, attraction_id, action_type, score
        FROM {INTERACTIONS_TABLE}
        """
    )
    attraction_names = {
        int(row["id"]): row["name"]
        for row in fetch_all(f"SELECT id, name FROM {ATTRACTIONS_TABLE}")
    }
    attraction_clusters: Dict[int, Dict[int, float]] = {cluster_id: {} for cluster_id in range(c)}

    for row in interactions:
        uid = int(row["user_id"])
        aid = int(row["attraction_id"])
        pos = user_pos.get(uid)
        if pos is None:
            continue
        w = _interaction_weight(str(row["action_type"]), row.get("score"))
        if w == 0:
            continue
        for cluster_id in range(c):
            score = float(membership[cluster_id, pos]) * w
            attraction_clusters[cluster_id][aid] = attraction_clusters[cluster_id].get(aid, 0.0) + score

    # Light popularity backoff from attraction profiles when interaction data is sparse.
    profile_rows = fetch_all(f"SELECT attraction_id, popularity_level FROM {ATTRACTION_PROFILES_TABLE}")
    popularity_boost = {
        "جاذبه کمتر شناخته‌شده": 0.25,
        "جاذبه منطقه‌ای": 0.5,
        "جاذبه ملی": 0.75,
        "جاذبه بین‌المللی": 1.0,
    }
    for row in profile_rows:
        aid = int(row["attraction_id"])
        boost = popularity_boost.get(row.get("popularity_level"), 0.0)
        if boost <= 0:
            continue
        for cluster_id in range(c):
            attraction_clusters[cluster_id][aid] = attraction_clusters[cluster_id].get(aid, 0.0) + 0.05 * boost

    ranked: Dict[int, List[dict]] = {}
    for cluster_id in range(c):
        items = sorted(attraction_clusters[cluster_id].items(), key=lambda kv: (-kv[1], kv[0]))[:limit]
        ranked[cluster_id] = [
            {
                "cluster_id": cluster_id,
                "attraction_id": int(aid),
                "attraction_name": attraction_names.get(int(aid)),
                "popularity_score": float(score),
                "rank": rank + 1,
            }
            for rank, (aid, score) in enumerate(items)
        ]
    return ranked
