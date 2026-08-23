"""Synthetic cross-section of assets for the order flow simulator.

Provides a one-factor covariance matrix and liquidity attributes (ADV,
market cap) with the empirically observed coupling: dollar volume scales
with market cap, and volatility is mildly declining in size.  These are the
ingredients needed for the simulator to reproduce the Kolm-Westray
validation facts -- order size (as % ADV) positively related to
participation, order size negatively related to market cap, and power-law
participation rates.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np


@dataclass
class MarketModel:
    """A static cross-section of ``n_assets`` synthetic securities.

    Attributes
    ----------
    vols : per-period return volatilities, shape (n,).
    betas : loadings on a single market factor, shape (n,).
    cov : full covariance matrix ``beta beta' s_m^2 + diag(idio^2)``.
    market_caps : dollar market capitalizations, shape (n,).
    adv : average daily dollar volume, shape (n,).
    """

    n_assets: int
    seed: int | None = None
    market_vol: float = 0.01
    vols: np.ndarray = field(init=False)
    betas: np.ndarray = field(init=False)
    cov: np.ndarray = field(init=False)
    market_caps: np.ndarray = field(init=False)
    adv: np.ndarray = field(init=False)

    def __post_init__(self) -> None:
        rng = np.random.default_rng(self.seed)
        n = self.n_assets
        # Log-normal size distribution spanning a few decades.
        self.market_caps = np.exp(rng.normal(22.0, 1.2, n))
        # ADV ~ 0.5% of market cap turned over per day, with noise.
        self.adv = 0.005 * self.market_caps * np.exp(rng.normal(0.0, 0.4, n))
        # Idiosyncratic vol mildly decreasing in size.
        size_rank = np.argsort(np.argsort(self.market_caps)) / max(n - 1, 1)
        idio = (0.025 - 0.01 * size_rank) * np.exp(rng.normal(0.0, 0.15, n))
        self.betas = rng.normal(1.0, 0.25, n)
        self.cov = (
            np.outer(self.betas, self.betas) * self.market_vol**2 + np.diag(idio**2)
        )
        self.vols = np.sqrt(np.diag(self.cov))

    def sample_returns(self, n_periods: int, rng: np.random.Generator) -> np.ndarray:
        """Draw an (n_periods, n_assets) return panel from the factor model."""
        factor = rng.normal(0.0, self.market_vol, n_periods)
        idio_vol = np.sqrt(np.clip(np.diag(self.cov) - self.betas**2 * self.market_vol**2, 1e-12, None))
        idio = rng.normal(0.0, 1.0, (n_periods, self.n_assets)) * idio_vol
        return factor[:, None] * self.betas[None, :] + idio
