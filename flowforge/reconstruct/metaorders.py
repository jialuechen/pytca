"""Build synthetic metaorders from public trade data (Algorithm 1).

Input is a public tape: one row per market order with a timestamp, a price,
a size and a sign (+1 buyer-initiated / -1 seller-initiated).  Session by
session the algorithm (i) computes daily volume ``V_D`` and intraday
volatility ``sigma_D = (max p - min p) / p_open``, (ii) randomly assigns
trades to synthetic traders through the mapping function, (iii) sorts by
(trader, timestamp) and defines a metaorder as a maximal run of same-sign
trades by the same trader, and (iv) records per-metaorder features.

Price convention with trade-only data: the start price ``p_s`` is the price
of the last trade *before* the first child order (falling back to the first
child's price at the session open), and the end price ``p_e`` is the price
of the trade *immediately following* the last child order -- the trade-tape
analogue of the paper's "mid just before" convention.  The signed impact is
``sign * (log p_e - log p_s)``.

Two tables are returned: the metaorder table, and a child-order table
carrying the executed-volume fraction ``phi`` and the running impact of
each child, which feeds the concave-execution-profile diagnostic.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from flowforge.reconstruct.mapping import (
    MappingConfig,
    assign_traders,
    sample_trader_frequencies,
)

REQUIRED_COLUMNS = ("timestamp", "price", "size", "sign")


def build_metaorders(
    trades: pd.DataFrame,
    config: MappingConfig | None = None,
    min_children: int = 2,
    session_col: str | None = "date",
    seed: int | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Generate synthetic metaorders from a public trade tape.

    Parameters
    ----------
    trades : pd.DataFrame
        Public tape with columns ``timestamp, price, size, sign`` and, if
        ``session_col`` is given, a session/date column.  Rows must be in
        chronological order within each session (they are sorted anyway).
    config : MappingConfig
        Parameters of the trader-mapping function.
    min_children : int
        Keep only metaorders with at least this many child orders
        (the paper keeps > 1).
    session_col : str or None
        Column defining a trading session; ``None`` treats the whole
        frame as a single session.
    seed : int or None
        RNG seed; a fresh frequency vector is drawn per session.

    Returns
    -------
    (metaorders, children) : tuple of pd.DataFrame
        ``metaorders`` columns: session, trader, sign, volume, q_frac,
        n_children, t_start, t_end, duration, p_start, p_end, impact,
        norm_impact, sigma_d, v_d.
        ``children`` columns: meta_id, session, phi, child_impact,
        norm_child_impact.
    """
    _validate(trades)
    config = config if config is not None else MappingConfig()
    rng = np.random.default_rng(seed)

    if session_col is not None and session_col in trades.columns:
        sessions = [g for _, g in trades.groupby(session_col, sort=True)]
        session_ids = [key for key, _ in trades.groupby(session_col, sort=True)]
    else:
        sessions, session_ids = [trades], [0]

    meta_frames: list[pd.DataFrame] = []
    child_frames: list[pd.DataFrame] = []
    meta_offset = 0
    for session_id, session in zip(session_ids, sessions):
        meta, children = _process_session(session, session_id, config, rng, meta_offset)
        if len(meta):
            meta_frames.append(meta)
            child_frames.append(children)
            meta_offset += len(meta)

    if not meta_frames:
        return _empty_meta(), _empty_children()

    metaorders = pd.concat(meta_frames, ignore_index=True)
    children = pd.concat(child_frames, ignore_index=True)
    keep = metaorders["n_children"] >= min_children
    kept_ids = set(metaorders.loc[keep, "meta_id"])
    metaorders = metaorders.loc[keep].reset_index(drop=True)
    children = children[children["meta_id"].isin(kept_ids)].reset_index(drop=True)
    return metaorders, children


def _process_session(
    session: pd.DataFrame,
    session_id,
    config: MappingConfig,
    rng: np.random.Generator,
    meta_offset: int,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    s = session.sort_values("timestamp", kind="mergesort").reset_index(drop=True)
    n = len(s)
    if n < 3:
        return _empty_meta(), _empty_children()

    price = s["price"].to_numpy(dtype=float)
    size = s["size"].to_numpy(dtype=float)
    sign = s["sign"].to_numpy(dtype=int)
    ts = s["timestamp"].to_numpy()
    log_price = np.log(price)

    v_d = float(size.sum())
    sigma_d = float((price.max() - price.min()) / price[0])
    if v_d <= 0 or sigma_d <= 0:
        return _empty_meta(), _empty_children()

    probabilities = sample_trader_frequencies(config, rng)
    trader = assign_traders(n, probabilities, rng)

    # Sort by (trader, chronology); within a trader the original order of
    # trades is preserved because the sort is stable on the time index.
    order = np.lexsort((np.arange(n), trader))
    trader_sorted = trader[order]
    sign_sorted = sign[order]
    tape_idx = order  # position of each sorted row in the original tape

    # A new metaorder starts whenever the trader or the sign changes.
    new_run = np.ones(n, dtype=bool)
    new_run[1:] = (trader_sorted[1:] != trader_sorted[:-1]) | (
        sign_sorted[1:] != sign_sorted[:-1]
    )
    run_id = np.cumsum(new_run) - 1
    n_runs = run_id[-1] + 1

    meta_records = []
    child_records = []
    for r in range(n_runs):
        members = tape_idx[run_id == r]
        members.sort()  # chronological child orders on the original tape
        first, last = members[0], members[-1]
        n_children = len(members)
        q = float(size[members].sum())
        mo_sign = int(sign[first])

        p_start = price[first - 1] if first > 0 else price[first]
        if last + 1 < n:
            p_end = price[last + 1]
        else:
            p_end = price[last]
        impact = mo_sign * (np.log(p_end) - np.log(p_start))
        q_frac = q / v_d
        norm = sigma_d * np.sqrt(q_frac)

        meta_id = meta_offset + r
        meta_records.append(
            (
                meta_id, session_id, int(trader[first]), mo_sign, q, q_frac,
                n_children, ts[first], ts[last],
                _duration(ts[first], ts[last]),
                float(p_start), float(p_end), float(impact),
                float(impact / norm) if norm > 0 else np.nan,
                sigma_d, v_d,
            )
        )

        if n_children >= 2:
            phi = np.cumsum(size[members]) / q
            child_impact = mo_sign * (log_price[members] - np.log(p_start))
            norm_child = child_impact / norm if norm > 0 else np.full(n_children, np.nan)
            child_records.append(
                pd.DataFrame(
                    {
                        "meta_id": meta_id,
                        "session": session_id,
                        "phi": phi,
                        "child_impact": child_impact,
                        "norm_child_impact": norm_child,
                    }
                )
            )

    meta = pd.DataFrame(
        meta_records,
        columns=[
            "meta_id", "session", "trader", "sign", "volume", "q_frac",
            "n_children", "t_start", "t_end", "duration",
            "p_start", "p_end", "impact", "norm_impact", "sigma_d", "v_d",
        ],
    )
    children = (
        pd.concat(child_records, ignore_index=True)
        if child_records
        else _empty_children()
    )
    return meta, children


def _duration(t0, t1) -> float:
    delta = t1 - t0
    if isinstance(delta, np.timedelta64):
        return float(delta / np.timedelta64(1, "s"))
    return float(delta)


def _validate(trades: pd.DataFrame) -> None:
    missing = [c for c in REQUIRED_COLUMNS if c not in trades.columns]
    if missing:
        raise ValueError(f"trade tape is missing required columns: {missing}")
    signs = set(pd.unique(trades["sign"]))
    if not signs <= {-1, 1}:
        raise ValueError("trade signs must be +1 (buy) or -1 (sell)")


def _empty_meta() -> pd.DataFrame:
    return pd.DataFrame(
        columns=[
            "meta_id", "session", "trader", "sign", "volume", "q_frac",
            "n_children", "t_start", "t_end", "duration",
            "p_start", "p_end", "impact", "norm_impact", "sigma_d", "v_d",
        ]
    )


def _empty_children() -> pd.DataFrame:
    return pd.DataFrame(
        columns=["meta_id", "session", "phi", "child_impact", "norm_child_impact"]
    )
