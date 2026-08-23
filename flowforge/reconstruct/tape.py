"""Synthetic public trade tape.

Generates a realistic-enough tape for demos and tests when the user has no
market data at hand: order signs follow a persistent Markov chain (order
splitting), sizes are log-normal, and the log price responds to signed
volume through a slowly decaying power-law propagator kernel plus diffusive
noise -- the minimal ingredients under which the reconstruction engine can
recover square-root-like impact.  This mirrors the paper's appendix sanity
check of running the algorithm on synthetic prices.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def synthetic_tape(
    n_sessions: int = 20,
    trades_per_session: int = 2000,
    sign_persistence: float = 0.72,
    impact_coeff: float = 2e-4,
    decay_exponent: float = 0.6,
    kernel_length: int = 500,
    noise_vol: float = 1.5e-4,
    base_price: float = 100.0,
    session_seconds: float = 28800.0,
    seed: int | None = None,
) -> pd.DataFrame:
    """Simulate a public tape: columns ``date, timestamp, price, size, sign``.

    Parameters
    ----------
    sign_persistence : probability that a trade keeps the previous sign.
    impact_coeff : scale of the propagator response of log price to a
        unit signed sqrt-volume innovation.
    decay_exponent : power-law exponent ``beta`` of the kernel
        ``G(l) ~ l**-beta``.
    noise_vol : per-trade diffusive log-price noise.
    """
    rng = np.random.default_rng(seed)
    lags = np.arange(1, kernel_length + 1, dtype=float)
    kernel = lags ** (-decay_exponent)

    frames = []
    last_price = base_price
    for day in range(n_sessions):
        n = trades_per_session
        signs = _persistent_signs(n, sign_persistence, rng)
        sizes = np.exp(rng.normal(4.0, 1.0, n)).round().clip(min=1.0)
        innovation = signs * np.sqrt(sizes / np.exp(4.0))
        impact_path = impact_coeff * np.convolve(innovation, kernel)[:n]
        noise_path = np.cumsum(rng.normal(0.0, noise_vol, n))
        log_price = np.log(last_price) + impact_path + noise_path
        price = np.exp(log_price)
        last_price = float(price[-1])

        seconds = np.sort(rng.uniform(0.0, session_seconds, n))
        timestamp = (
            pd.Timestamp("2024-01-02")
            + pd.to_timedelta(day, unit="D")
            + pd.to_timedelta(seconds, unit="s")
        )
        frames.append(
            pd.DataFrame(
                {
                    "date": pd.Timestamp("2024-01-02") + pd.to_timedelta(day, unit="D"),
                    "timestamp": timestamp,
                    "price": price,
                    "size": sizes,
                    "sign": signs.astype(int),
                }
            )
        )
    return pd.concat(frames, ignore_index=True)


def _persistent_signs(n: int, persistence: float, rng: np.random.Generator) -> np.ndarray:
    signs = np.empty(n)
    signs[0] = rng.choice([-1.0, 1.0])
    stay = rng.uniform(size=n) < persistence
    for i in range(1, n):
        signs[i] = signs[i - 1] if stay[i] else -signs[i - 1]
    return signs
