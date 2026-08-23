"""Impact stylized-fact diagnostics.

Three tests from the metaorder literature, applied to the output of
:func:`flowforge.reconstruct.build_metaorders`:

- :func:`square_root_law` -- peak impact vs volume fraction,
  ``I(Q)/sigma_D = Y * (Q/V_D)**gamma`` with the empirical benchmarks
  ``gamma ~ 0.5`` and ``Y in [0.5, 1]``.
- :func:`execution_profile` -- average rescaled price path during
  execution vs executed-volume fraction ``phi``; the benchmark is the
  concave ``sqrt(phi)`` profile.
- :func:`impact_decay` -- average rescaled impact after execution as a
  function of ``z = 1 + elapsed/T``, comparable to the propagator fit
  ``z**(1-beta) - (z-1)**(1-beta)`` of Bucci et al.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats


def square_root_law(
    metaorders: pd.DataFrame,
    n_bins: int = 25,
    q_min: float = 1e-6,
    q_max: float = 1.0,
) -> dict:
    """Fit ``I(Q)/sigma_D = Y (Q/V_D)**gamma`` on log-spaced volume bins.

    Returns a dict with the fitted prefactor ``Y``, exponent ``gamma``,
    their standard errors, and the binned curve for plotting.
    """
    m = metaorders.dropna(subset=["impact", "sigma_d", "q_frac"]).copy()
    m = m[(m["q_frac"] >= q_min) & (m["q_frac"] <= q_max) & (m["sigma_d"] > 0)]
    if len(m) < 100:
        raise ValueError("need at least 100 metaorders for a meaningful fit")
    m["rescaled_impact"] = m["impact"] / m["sigma_d"]

    edges = np.logspace(np.log10(m["q_frac"].min()), np.log10(m["q_frac"].max()), n_bins + 1)
    bin_idx = np.clip(np.digitize(m["q_frac"], edges) - 1, 0, n_bins - 1)
    grouped = m.groupby(bin_idx).agg(
        q_frac=("q_frac", "mean"),
        impact=("rescaled_impact", "mean"),
        count=("rescaled_impact", "size"),
    )
    grouped = grouped[(grouped["count"] >= 20) & (grouped["impact"] > 0)]
    if len(grouped) < 4:
        raise ValueError("too few populated bins with positive mean impact")

    fit = stats.linregress(np.log(grouped["q_frac"]), np.log(grouped["impact"]))
    return {
        "Y": float(np.exp(fit.intercept)),
        "exponent": float(fit.slope),
        "exponent_stderr": float(fit.stderr),
        "r_value": float(fit.rvalue),
        "n_metaorders": int(len(m)),
        "curve": grouped.reset_index(drop=True),
    }


def execution_profile(children: pd.DataFrame, n_bins: int = 20) -> pd.DataFrame:
    """Average normalized impact vs executed-volume fraction ``phi``.

    Returns a frame with columns ``phi, impact, sqrt_benchmark, count``;
    ``impact`` is directly comparable to ``Y * sqrt(phi)``.
    """
    c = children.dropna(subset=["phi", "norm_child_impact"])
    if len(c) == 0:
        raise ValueError("empty children table")
    edges = np.linspace(0.0, 1.0, n_bins + 1)
    bin_idx = np.clip(np.digitize(c["phi"], edges) - 1, 0, n_bins - 1)
    grouped = c.groupby(bin_idx).agg(
        phi=("phi", "mean"),
        impact=("norm_child_impact", "mean"),
        count=("norm_child_impact", "size"),
    )
    grouped["sqrt_benchmark"] = np.sqrt(grouped["phi"])
    return grouped.reset_index(drop=True)


def impact_decay(
    metaorders: pd.DataFrame,
    trades: pd.DataFrame,
    z_grid: np.ndarray | None = None,
    session_col: str = "date",
    min_duration: float = 30.0,
) -> pd.DataFrame:
    """Average rescaled impact after execution at horizons ``z = 1 + dt/T``.

    For each metaorder of duration ``T`` the price is sampled at times
    ``t_end + (z - 1) * T`` within the same session, normalized by
    ``sigma_D * sqrt(Q/V_D)``, and averaged.  ``z = 1`` reproduces the
    peak impact; the decay toward larger ``z`` is the quantity fitted by
    propagator models.
    """
    if z_grid is None:
        z_grid = np.array([1.0, 1.25, 1.5, 2.0, 2.5, 3.0])
    m = metaorders[metaorders["duration"] >= min_duration]
    if len(m) == 0:
        raise ValueError("no metaorders above min_duration")

    results = {float(z): [] for z in z_grid}
    for session_id, session in trades.groupby(session_col, sort=True):
        s = session.sort_values("timestamp")
        ts = s["timestamp"].to_numpy()
        logp = np.log(s["price"].to_numpy(dtype=float))
        ms = m[m["session"] == session_id]
        if len(ms) == 0:
            continue
        t_end = ms["t_end"].to_numpy()
        t_dur = ms["duration"].to_numpy()
        p_start = np.log(ms["p_start"].to_numpy(dtype=float))
        sign = ms["sign"].to_numpy()
        norm = ms["sigma_d"].to_numpy() * np.sqrt(ms["q_frac"].to_numpy())
        for z in z_grid:
            target = t_end + _as_timedelta(ts, (z - 1.0) * t_dur)
            pos = np.searchsorted(ts, target, side="left")
            valid = pos < len(ts)
            if not valid.any():
                continue
            imp = sign[valid] * (logp[pos[valid]] - p_start[valid]) / norm[valid]
            results[float(z)].extend(imp.tolist())

    rows = [
        {"z": z, "impact": float(np.mean(v)), "count": len(v)}
        for z, v in results.items()
        if len(v) > 0
    ]
    return pd.DataFrame(rows).sort_values("z").reset_index(drop=True)


def _as_timedelta(ts_array: np.ndarray, seconds: np.ndarray):
    if np.issubdtype(ts_array.dtype, np.datetime64):
        return (seconds * 1e9).astype("timedelta64[ns]")
    return seconds
