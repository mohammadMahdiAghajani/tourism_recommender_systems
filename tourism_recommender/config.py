"""Project configuration and schema metadata."""

from __future__ import annotations

DB_CONFIG = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "",
    "database": "test",
    "charset": "utf8mb4",
}

PROFILE_CATEGORICALS = {
    "nationality": ["iranian", "turkish", "azerbaijani", "kurdish", "arab", "afghan", "pakistani", "other"],
    "language": ["fa", "en", "tr", "ar", "az", "ku", "other"],
    "age_band": ["under_18", "18_24", "25_34", "35_44", "45_54", "55_plus"],
    "budget_band": ["low", "medium", "high", "luxury"],
    "travel_style": ["budget", "balanced", "luxury", "backpacker", "family", "romantic", "adventure", "religious", "cultural"],
    "travel_party_type": ["solo", "couple", "family", "friends", "group"],
    "activity_level": ["low", "moderate", "high"],
    "mobility_level": ["no_limit", "minor_limit", "limited", "wheelchair_needed"],
    "season_preference": ["spring", "summer", "autumn", "winter", "all_year"],
    "religious_travel_preference": ["none", "halal_friendly", "prayer_space_needed", "modest_environment_preferred", "gender_sensitive"],
    "ethnic_group": ["persian", "kurdish", "azerbaijani", "lor", "arab", "baluch", "other", "prefer_not_to_say"],
}

BEHAVIOR_FEATURES = ["view_count", "visit_count", "save_count", "like_count", "avg_rate_norm"]
PROFILE_WEIGHT = 0.30
BEHAVIOR_WEIGHT = 0.70
CLUSTER_RANGE = list(range(4, 11))
FCM_M = 2.0
FCM_ERROR = 1e-5
FCM_MAX_ITER = 250
RANDOM_SEED = 42
TOP_ATTRACTIONS_PER_CLUSTER = 200

ACTION_WEIGHTS = {
    "view": 1.0,
    "click": 0.8,
    "save": 3.0,
    "like": 4.0,
    "rate": 2.5,
    "visit": 5.0,
    "share": 1.5,
    "dislike": -2.5,
}

PROFILE_TABLE = "user_profiles"
INTERACTIONS_TABLE = "interactions"
ATTRACTIONS_TABLE = "attractions"
ATTRACTION_PROFILES_TABLE = "attraction_profiles"
USERS_TABLE = "users"
USER_CLUSTER_MEMBERSHIPS_TABLE = "user_cluster_memberships"
CLUSTER_TOP_ATTRACTIONS_TABLE = "cluster_top_attractions"

PROFILE_BLOCK_COLUMNS = [
    f"{column}={value}"
    for column, values in PROFILE_CATEGORICALS.items()
    for value in values
]
