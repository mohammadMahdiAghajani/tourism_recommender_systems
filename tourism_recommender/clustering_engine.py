"""FCM clustering and cluster selection."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

import numpy as np

from config import CLUSTER_RANGE, FCM_ERROR, FCM_M, FCM_MAX_ITER, RANDOM_SEED

try:
    import skfuzzy as fuzz  # type: ignore
    SKFUZZY_AVAILABLE = True
except Exception:
    fuzz = None
    SKFUZZY_AVAILABLE = False


@dataclass
class ClusteringResult:
    c: int
    centers: np.ndarray
    membership: np.ndarray
    hard_labels: np.ndarray
    fpc: float
    xie_beni: float
    balance: float
    score: float
    counts: np.ndarray


def _normalize_columns(X: np.ndarray) -> np.ndarray:
    min_vals = X.min(axis=0)
    max_vals = X.max(axis=0)
    scale = max_vals - min_vals
    scale[scale == 0] = 1.0
    return (X - min_vals) / scale


def _init_membership(n_samples: int, c: int, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    u = rng.random((c, n_samples))
    u /= u.sum(axis=0, keepdims=True)
    return u


def _update_centers(X: np.ndarray, U: np.ndarray, m: float) -> np.ndarray:
    um = U ** m
    denom = um.sum(axis=1, keepdims=True)
    denom[denom == 0] = 1.0
    return (um @ X) / denom


def _update_membership(X: np.ndarray, centers: np.ndarray, m: float) -> np.ndarray:
    dist = np.linalg.norm(X[None, :, :] - centers[:, None, :], axis=2)
    dist = np.maximum(dist, 1e-12)
    power = 2.0 / (m - 1.0)
    inv = dist[:, None, :] / dist[None, :, :]
    inv = np.maximum(inv, 1e-12) ** power
    U = 1.0 / inv.sum(axis=1)
    return U


def _fcm_fallback(X: np.ndarray, c: int, m: float, error: float, max_iter: int, seed: int):
    Xn = _normalize_columns(X)
    U = _init_membership(Xn.shape[0], c, seed)
    centers = None
    for _ in range(max_iter):
        centers_new = _update_centers(Xn, U, m)
        dist = np.linalg.norm(Xn[None, :, :] - centers_new[:, None, :], axis=2)
        dist = np.maximum(dist, 1e-12)
        power = 2.0 / (m - 1.0)
        ratio = (dist[:, None, :] / dist[None, :, :]) ** power
        U_new = 1.0 / ratio.sum(axis=1)
        if centers is not None:
            delta = np.max(np.abs(centers_new - centers))
            if delta < error:
                centers = centers_new
                U = U_new
                break
        centers = centers_new
        U = U_new
    return centers, U


def _fcm_skfuzzy(X: np.ndarray, c: int, m: float, error: float, max_iter: int, seed: int):
    data = X.T.astype(float)
    cntr, u, _, _, _, _, _ = fuzz.cluster.cmeans(
        data,
        c,
        m,
        error=error,
        maxiter=max_iter,
        init=None,
        seed=seed,
    )
    return cntr, u


def _compute_fpc(U: np.ndarray) -> float:
    n = U.shape[1]
    return float(np.sum(U ** 2) / max(n, 1))


def _compute_xie_beni(X: np.ndarray, centers: np.ndarray, U: np.ndarray, m: float) -> float:
    Xn = _normalize_columns(X)
    dist2 = np.square(np.linalg.norm(Xn[None, :, :] - centers[:, None, :], axis=2))
    numerator = np.sum((U ** m) * dist2)
    center_dists = np.square(np.linalg.norm(centers[:, None, :] - centers[None, :, :], axis=2))
    np.fill_diagonal(center_dists, np.inf)
    denominator = X.shape[0] * np.min(center_dists)
    if not np.isfinite(denominator) or denominator <= 0:
        denominator = 1e-12
    return float(numerator / denominator)


def _cluster_balance(labels: np.ndarray, c: int) -> tuple[float, np.ndarray]:
    counts = np.bincount(labels, minlength=c).astype(float)
    mean = counts.mean() if counts.size else 0.0
    std = counts.std() if counts.size else 0.0
    cv = std / mean if mean > 0 else 1.0
    balance = 1.0 / (1.0 + cv)
    return float(balance), counts


def _score_candidates(results: List[dict]) -> None:
    fpcs = np.array([r["fpc"] for r in results], dtype=float)
    xbs = np.array([r["xie_beni"] for r in results], dtype=float)
    balances = np.array([r["balance"] for r in results], dtype=float)

    def norm(arr):
        if np.allclose(arr.max(), arr.min()):
            return np.ones_like(arr)
        return (arr - arr.min()) / (arr.max() - arr.min())

    fpc_n = norm(fpcs)
    xb_n = norm(xbs)
    bal_n = norm(balances)
    scores = 0.45 * fpc_n + 0.35 * (1.0 - xb_n) + 0.20 * bal_n
    for r, s in zip(results, scores):
        r["score"] = float(s)


def fit_best_fcm(X: np.ndarray, c_range: List[int] = CLUSTER_RANGE, m: float = FCM_M, error: float = FCM_ERROR, max_iter: int = FCM_MAX_ITER, seed: int = RANDOM_SEED) -> tuple[ClusteringResult, List[dict]]:
    candidates: List[dict] = []
    for c in c_range:
        if SKFUZZY_AVAILABLE:
            centers, U = _fcm_skfuzzy(X, c, m, error, max_iter, seed)
        else:
            centers, U = _fcm_fallback(X, c, m, error, max_iter, seed)
        labels = np.argmax(U, axis=0)
        fpc = _compute_fpc(U)
        xb = _compute_xie_beni(X, centers, U, m)
        balance, counts = _cluster_balance(labels, c)
        candidates.append({
            "c": c,
            "centers": centers,
            "membership": U,
            "hard_labels": labels,
            "fpc": fpc,
            "xie_beni": xb,
            "balance": balance,
            "counts": counts,
        })

    _score_candidates(candidates)
    best = max(candidates, key=lambda r: r["score"])
    result = ClusteringResult(
        c=int(best["c"]),
        centers=np.asarray(best["centers"]),
        membership=np.asarray(best["membership"]),
        hard_labels=np.asarray(best["hard_labels"]),
        fpc=float(best["fpc"]),
        xie_beni=float(best["xie_beni"]),
        balance=float(best["balance"]),
        score=float(best["score"]),
        counts=np.asarray(best["counts"]),
    )
    return result, candidates
