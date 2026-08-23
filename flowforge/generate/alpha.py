"""Alpha signal generation.

Implements "bootstrap alphas" as used by Kolm & Westray: the signal for
period t is a rho-mixture of the *realized* return of period t and
independent noise,

    alpha_i = rho * r_i + sqrt(1 - rho**2) * z_i,      z_i ~ N(0, sigma_i**2)

so that the information coefficient IC = corr(alpha_i, r_i) is approximately
``rho`` by construction, and the cross-sectional structure of the signal
(volatilities, correlations) is inherited from the return panel rather than
modeled separately.  Setting ``rho = 0`` yields pure-noise (uninformed)
signals -- the one-parameter switch between "observational" informed flow
and "interventional" randomized flow used in the causal A/B-testing
companion paper (Kolm & Westray, SSRN 4160945).

An optional AR(1) smoothing with a given half-life makes the signal
persistent, which produces the gradual position adjustment (and hence
autocorrelated order signs) characteristic of real institutional flow.
"""

from __future__ import annotations

import numpy as np


class BootstrapAlpha:
    """Generate bootstrap alpha signals with tunable IC and persistence.

    Parameters
    ----------
    rho : float
        Target information coefficient in [0, 1).  ``rho = 0`` gives
        uninformed (pure noise) signals.
    vols : np.ndarray
        Per-asset return volatilities (per period), shape (n_assets,).
        Used to scale the noise leg so that alpha has the same
        cross-sectional dispersion as returns.
    half_life : float or None
        If given, the raw bootstrap signal is smoothed through an AR(1)
        filter with this half-life (in periods), adding persistence while
        approximately preserving the unconditional IC.
    rng : np.random.Generator or None
        Source of randomness.
    """

    def __init__(
        self,
        rho: float,
        vols: np.ndarray,
        half_life: float | None = None,
        rng: np.random.Generator | None = None,
    ) -> None:
        if not 0.0 <= rho < 1.0:
            raise ValueError("rho must be in [0, 1)")
        self.rho = float(rho)
        self.vols = np.asarray(vols, dtype=float)
        self.rng = rng if rng is not None else np.random.default_rng()
        if half_life is not None and half_life > 0:
            self.phi = float(0.5 ** (1.0 / half_life))
        else:
            self.phi = 0.0
        self._state: np.ndarray | None = None

    @property
    def informed(self) -> bool:
        return self.rho > 0.0

    def sample(self, realized_returns: np.ndarray) -> np.ndarray:
        """Draw the alpha vector for one period.

        Parameters
        ----------
        realized_returns : np.ndarray
            The realized returns of the period the signal is meant to
            predict, shape (n_assets,).

        Returns
        -------
        np.ndarray of shape (n_assets,)
        """
        r = np.asarray(realized_returns, dtype=float)
        z = self.rng.normal(0.0, self.vols)
        raw = self.rho * r + np.sqrt(1.0 - self.rho**2) * z
        if self.phi == 0.0:
            return raw
        if self._state is None:
            self._state = raw.copy()
        else:
            # AR(1) smoothing; innovation scaled to keep variance constant.
            self._state = self.phi * self._state + np.sqrt(1.0 - self.phi**2) * raw
        return self._state.copy()

    def reset(self) -> None:
        """Clear the AR(1) state (e.g. between independent simulations)."""
        self._state = None
