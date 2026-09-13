"""Feature extraction from user_profiles and interactions."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Tuple
import numpy as np
from config import (
    BEHAVIOR_FEATURES,
    BEHAVIOR_WEIGHT,
    INTERACTIONS_TABLE,
    PROFILE_BLOCK_COLUMNS,
    PROFILE_CATEGORICALS,
    PROFILE_TABLE,
    PROFILE_WEIGHT,
)
from db import fetch_all

"""
این ماژول وظیفه دارد اطلاعات پروفایل و سوابق رفتاری کاربران را از پایگاه داده دریافت کرده و به یک ماتریس 
عددی مناسب برای الگوریتم خوشه‌بندی تبدیل کند. ابتدا تابع `_build_user_index` شناسهٔ تمام کاربرانی را که 
حداقل در جدول پروفایل یا تعاملات حضور دارند استخراج می‌کند؛ بنابراین کاربران فاقد پروفایل یا فاقد سابقهٔ 
تعامل نیز از فرایند تحلیل حذف نمی‌شوند. سپس `_load_profiles` ویژگی‌های فردی و ترجیحات سفر را از جدول 
پروفایل می‌خواند و `_load_behavior_stats` تعداد بازدیدها، حضور در جاذبه، ذخیره‌کردن و پسندیدن را برای 
هر کاربر محاسبه می‌کند. میانگین امتیازهای ثبت‌شده نیز از بازهٔ ۱ تا ۵ به بازهٔ صفر تا یک تبدیل می‌شود. ویژگی‌های 
دسته‌ای پروفایل، مانند بودجه، سبک سفر یا نوع همراهان، براساس مقادیر تعریف‌شده در 
`PROFILE_CATEGORICALS` با روش One-Hot Encoding به ستون‌های عددی تبدیل می‌شوند؛ به این ترتیب 
هر سطر نمایندهٔ یک کاربر و هر ستون نشان‌دهندهٔ یک ویژگی مشخص است. تابع `_safe_float` نیز مقادیر تهی یا 
نامعتبر را با مقدار پیش‌فرض صفر جایگزین می‌کند تا ساخت ماتریس با خطا مواجه نشود.
تابع اصلی `extract_user_features` دو بخش مستقل شامل ویژگی‌های پروفایل و ویژگی‌های رفتاری می‌سازد و 
برای جلوگیری از تأثیر نامتوازن مقیاس داده‌ها، آن‌ها را نرمال‌سازی می‌کند. بردار پروفایل هر کاربر بر مبنای نرم 
اقلیدسی سطری نرمال می‌شود؛ ویژگی‌های رفتاری نیز ابتدا به‌صورت ستونی و با روش Min-Max به بازهٔ صفر تا یک 
انتقال می‌یابند و سپس بردار رفتاری هر کاربر نرمال می‌شود. در ادامه، اهمیت نسبی هر بخش با ضرایب 
`PROFILE_WEIGHT` و `BEHAVIOR_WEIGHT` اعمال شده و دو ماتریس به‌صورت افقی به یکدیگر متصل 
می‌شوند تا ماتریس نهایی `X` تشکیل شود. خروجی تابع علاوه بر این ماتریس، شامل ترتیب شناسهٔ کاربران، نام 
ستون‌های ویژگی، پارامترهای مقیاس‌بندی برای استفاده یا بازتولید پردازش، و تعداد ویژگی‌های مربوط به هر یک از 
دو بخش پروفایل و رفتار است؛ این خروجی مستقیماً می‌تواند به الگوریتم خوشه‌بندی کاربران تحویل داده شود.
"""

@dataclass
class FeatureData:
    X: np.ndarray
    user_ids: List[int]
    feature_names: List[str]
    scaling_params: Dict[str, object]
    n_profile_features: int
    n_behavior_features: int


def _safe_float(value, default=0.0) -> float:
    if value is None:
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _build_user_index() -> List[int]:
    rows = fetch_all(
        f"""
        SELECT DISTINCT user_id
        FROM (
            SELECT user_id FROM {PROFILE_TABLE}
            UNION
            SELECT user_id FROM {INTERACTIONS_TABLE}
        ) x
        ORDER BY user_id
        """
    )
    return [int(row["user_id"]) for row in rows]


def _load_profiles() -> Dict[int, dict]:
    rows = fetch_all(f"SELECT * FROM {PROFILE_TABLE}")
    return {int(row["user_id"]): row for row in rows}


def _load_behavior_stats() -> Dict[int, dict]:
    rows = fetch_all(
        f"""
        SELECT
            user_id,
            SUM(CASE WHEN action_type = 'view' THEN 1 ELSE 0 END) AS view_count,
            SUM(CASE WHEN action_type = 'visit' THEN 1 ELSE 0 END) AS visit_count,
            SUM(CASE WHEN action_type = 'save' THEN 1 ELSE 0 END) AS save_count,
            SUM(CASE WHEN action_type = 'like' THEN 1 ELSE 0 END) AS like_count,
            AVG(CASE WHEN action_type = 'rate' THEN (COALESCE(score, 0) - 1.0) / 4.0 ELSE NULL END) AS avg_rate_norm
        FROM {INTERACTIONS_TABLE}
        GROUP BY user_id
        """
    )
    return {int(row["user_id"]): row for row in rows}


def _profile_feature_names() -> List[str]:
    names: List[str] = []
    for column, values in PROFILE_CATEGORICALS.items():
        names.extend([f"profile:{column}={value}" for value in values])
    return names


def extract_user_features() -> Tuple[np.ndarray, List[int], List[str], Dict[str, object], int, int]:
    user_ids = _build_user_index()
    profiles = _load_profiles()
    behavior = _load_behavior_stats()

    profile_names = _profile_feature_names()
    feature_names = profile_names + [f"behavior:{name}" for name in BEHAVIOR_FEATURES]

    profile_matrix = np.zeros((len(user_ids), len(profile_names)), dtype=float)
    behavior_matrix = np.zeros((len(user_ids), len(BEHAVIOR_FEATURES)), dtype=float)

    profile_offsets = {}
    offset = 0
    for column, values in PROFILE_CATEGORICALS.items():
        profile_offsets[column] = {value: offset + idx for idx, value in enumerate(values)}
        offset += len(values)

    for i, user_id in enumerate(user_ids):
        row = profiles.get(user_id, {})
        for column, values in PROFILE_CATEGORICALS.items():
            value = row.get(column)
            if value in profile_offsets[column]:
                profile_matrix[i, profile_offsets[column][value]] = 1.0

        b = behavior.get(user_id, {})
        behavior_matrix[i, 0] = _safe_float(b.get("view_count"), 0.0)
        behavior_matrix[i, 1] = _safe_float(b.get("visit_count"), 0.0)
        behavior_matrix[i, 2] = _safe_float(b.get("save_count"), 0.0)
        behavior_matrix[i, 3] = _safe_float(b.get("like_count"), 0.0)
        behavior_matrix[i, 4] = _safe_float(b.get("avg_rate_norm"), 0.0)

    profile_row_norm = np.linalg.norm(profile_matrix, axis=1, keepdims=True)
    profile_row_norm[profile_row_norm == 0] = 1.0
    profile_scaled = profile_matrix / profile_row_norm

    behavior_min = behavior_matrix.min(axis=0)
    behavior_max = behavior_matrix.max(axis=0)
    behavior_range = behavior_max - behavior_min
    behavior_range[behavior_range == 0] = 1.0
    behavior_scaled = (behavior_matrix - behavior_min) / behavior_range
    behavior_row_norm = np.linalg.norm(behavior_scaled, axis=1, keepdims=True)
    behavior_row_norm[behavior_row_norm == 0] = 1.0
    behavior_scaled = behavior_scaled / behavior_row_norm

    X = np.hstack([
        PROFILE_WEIGHT * profile_scaled,
        BEHAVIOR_WEIGHT * behavior_scaled,
    ])

    scaling_params = {
        "profile_weight": PROFILE_WEIGHT,
        "behavior_weight": BEHAVIOR_WEIGHT,
        "behavior_min": behavior_min.tolist(),
        "behavior_max": behavior_max.tolist(),
    }
    return X, user_ids, feature_names, scaling_params, profile_matrix.shape[1], behavior_matrix.shape[1]
