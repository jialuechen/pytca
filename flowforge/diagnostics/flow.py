"""Order flow stylized-fact diagnostics for the generation engine.

Validation facts from Kolm & Westray: simulated buy-side flow should show
positively autocorrelated order signs (order splitting / persistence),
participation positively related to order size (as %ADV), and order size
negatively related to market cap.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def sign_autocorrelation(
    orders: pd.DataFrame, max_lag: int = 20, min_orders: int = 10
) -> pd.DataFrame:
    """Per-lag autocorrelation of order signs, averaged across assets.

    Expects the long-format order table of
    :class:`flowforge.generate.OrderFlowSimulator` (columns ``asset``,
    ``period``, ``sign``).  Returns columns ``lag, autocorr, n_assets``.
    """
    acfs: dict[int, list[float]] = {lag: [] for lag in range(1, max_lag + 1)}
    for _, g in orders.sort_values("period").groupby("asset"):
        s = g["sign"].to_numpy(dtype=float)
        if len(s) < min_orders:
            continue
        s = s - s.mean()
        denom = float(np.dot(s, s))
        if denom <= 0:
            continue
        for lag in range(1, min(max_lag, len(s) - 1) + 1):
            acfs[lag].append(float(np.dot(s[:-lag], s[lag:]) / denom))
    rows = [
        {"lag": lag, "autocorr": float(np.mean(v)), "n_assets": len(v)}
        for lag, v in acfs.items()
        if v
    ]
    return pd.DataFrame(rows)


def participation_stats(orders: pd.DataFrame) -> dict:
    """Cross-sectional relations used to validate simulated flow realism.

    Returns Spearman correlations of order notional (%ADV) with
    participation and with market cap, plus a tail-exponent estimate of the
    participation distribution (Hill estimator on the top decile).
    """
    o = orders.dropna(subset=["participation", "notional", "adv", "market_cap"])
    if len(o) < 100:
        raise ValueError("need at least 100 orders")
    size_pct_adv = o["notional"] / o["adv"]

    def _spearman(a: pd.Series, b: pd.Series) -> float:
        return float(a.rank().corr(b.rank()))

    part = o["participation"].to_numpy(dtype=float)
    tail = np.sort(part[part > 0])
    k = max(len(tail) // 10, 10)
    top = tail[-k:]
    if len(top) > 1 and top[0] > 0:
        denom = float(np.mean(np.log(top / top[0])))
        hill = 1.0 / denom if denom > 0 else np.nan
    else:
        hill = np.nan

    return {
        "corr_size_participation": _spearman(size_pct_adv, o["participation"]),
        "corr_size_marketcap": _spearman(size_pct_adv, o["market_cap"]),
        "participation_tail_exponent": float(hill),
        "mean_participation": float(part.mean()),
        "n_orders": int(len(o)),
    }
