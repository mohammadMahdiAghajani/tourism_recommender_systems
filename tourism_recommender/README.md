# Tourism Recommender

A modular Python project that:

- extracts user features from `user_profiles` and `interactions`
- builds a fuzzy c-means recommender pipeline
- searches `c` from 4 to 10 using FPC, Xie-Beni, and cluster balance
- stores hard and soft user cluster assignments
- stores the top 200 attractions per cluster

## Files

- `config.py`: database and feature configuration
- `db.py`: mysql-connector-python helpers
- `extract_features.py`: user feature pipeline
- `clustering_engine.py`: FCM implementation and model selection
- `recommender.py`: cluster attraction ranking
- `storage.py`: table creation and persistence
- `main.py`: pipeline entry point

## Run

Set the database credentials in `config.py`, then run:

```bash
python main.py
```

The pipeline writes a `run_summary.json` file in the project directory and persists results to:

- `user_cluster_memberships`
- `cluster_top_attractions`

## Notes

- The column name `cltural_experience` is preserved exactly.
- A small self-contained FCM fallback is included, so the project still runs if `scikit-fuzzy` is not installed.
- The project uses ASCII-only source files.
