"""The randomized trader-mapping function (Algorithm 2 of the paper).

The mapping assigns a synthetic trader ID to every public trade of a
session while preserving the true chronological order of trades.  It has
exactly two degrees of freedom, as in Maitrier, Loeper & Bouchaud (2025):
the number of traders ``n_traders`` and the distribution ``F`` of their
trading frequencies (homogeneous, or power-law ``P(f) ~ f^{-exponent}`` --
the empirically realistic choice, where a few traders account for most of
the volume).  Each trade is then drawn to a trader with probability
proportional to that trader's frequency.  Because every real trade is
assigned to exactly one synthetic trader, the mapping is a sampling
*without replacement* of the tape -- the feature the authors flag as
essential for recovering the Square Root Law.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class MappingConfig:
    """Degrees of freedom of the mapping function."""

    n_traders: int = 20
    freq_dist: str = "homogeneous"  # "homogeneous" or "powerlaw"
    exponent: float = 2.0           # power-law exponent (freq_dist="powerlaw")
    f_min: float = 1.0              # lower cutoff of the power law


def sample_trader_frequencies(
    config: MappingConfig, rng: np.random.Generator
) -> np.ndarray:
    """Draw f_i ~ F for each synthetic trader and normalize to probabilities."""
    if config.n_traders < 2:
        raise ValueError("n_traders must be >= 2")
    if config.freq_dist == "homogeneous":
        f = np.ones(config.n_traders)
    elif config.freq_dist == "powerlaw":
        if config.exponent <= 1.0:
            raise ValueError("power-law exponent must be > 1")
        # Inverse-CDF sampling of a Pareto with the given tail exponent.
        u = rng.uniform(size=config.n_traders)
        f = config.f_min * (1.0 - u) ** (-1.0 / (config.exponent - 1.0))
    else:
        raise ValueError(f"unknown freq_dist: {config.freq_dist!r}")
    return f / f.sum()


def assign_traders(
    n_trades: int, probabilities: np.ndarray, rng: np.random.Generator
) -> np.ndarray:
    """Assign each of ``n_trades`` chronologically ordered trades a trader ID.

    Vectorized version of the paper's loop: draw U ~ Uniform(0,1) per trade
    and locate it in the cumulative frequency table.
    """
    cumulative = np.cumsum(probabilities)
    cumulative[-1] = 1.0  # guard against floating-point undershoot
    u = rng.uniform(size=n_trades)
    return np.searchsorted(cumulative, u, side="right")
