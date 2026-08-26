"""Pipeline entry point."""

from __future__ import annotations

import json
from pathlib import Path

from clustering_engine import fit_best_fcm
from extract_features import extract_user_features
from recommender import build_cluster_top_attractions
from storage import ensure_tables, save_cluster_top_attractions, save_user_cluster_memberships


def main() -> None:
    ensure_tables()
    X, user_ids, feature_names, scaling_params, n_profile_features, n_behavior_features = extract_user_features()
    if len(user_ids) == 0:
        print("No users found in user_profiles or interactions.")
        return

    clustering_result, candidates = fit_best_fcm(X)
    cluster_top = build_cluster_top_attractions(user_ids, clustering_result.membership, clustering_result.hard_labels, clustering_result.c)
    save_user_cluster_memberships(user_ids, clustering_result.membership, clustering_result.hard_labels)
    save_cluster_top_attractions(cluster_top)

    summary = {
        "users": len(user_ids),
        "features": len(feature_names),
        "n_profile_features": n_profile_features,
        "n_behavior_features": n_behavior_features,
        "selected_c": clustering_result.c,
        "fpc": clustering_result.fpc,
        "xie_beni": clustering_result.xie_beni,
        "balance": clustering_result.balance,
        "score": clustering_result.score,
        "cluster_sizes": clustering_result.counts.astype(int).tolist(),
        "candidates": [
            {
                "c": item["c"],
                "fpc": item["fpc"],
                "xie_beni": item["xie_beni"],
                "balance": item["balance"],
                "score": item["score"],
                "cluster_sizes": item["counts"].astype(int).tolist(),
            }
            for item in candidates
        ],
    }
    out = Path("run_summary.json")
    out.write_text(json.dumps(summary, ensure_ascii=True, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()
