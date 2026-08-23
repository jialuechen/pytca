"""Mean-variance optimization with quadratic transaction costs.

Each period the simulated trader solves

    max_x  alpha' (w + x)  -  lam * (w + x)' Sigma (w + x)  -  x' Gamma x

where ``w`` is the current portfolio, ``x`` the trade vector, ``lam`` the
risk-aversion coefficient and ``Gamma`` a positive-definite quadratic
transaction-cost matrix.  The first-order condition gives the closed form

    x* = (lam * Sigma + Gamma)^{-1} * lam * Sigma * (w_M - w),

with the Markowitz (frictionless) target ``w_M = Sigma^{-1} alpha / (2 lam)``.
This is the Garleanu-Pedersen style partial adjustment: the trader moves a
fraction of the way from the current portfolio toward the aim portfolio,
with the trading rate set by the ratio of risk aversion to trading costs.
The gradual adjustment is what endogenously produces order-splitting and
positively autocorrelated order signs in the simulated flow.

Everything is a dense linear solve, so simulating thousands of assets over
thousands of periods is cheap -- this is the computational-efficiency design
goal of the Kolm-Westray simulator.  Optional linear constraints (e.g.
sector/beta neutrality) can be imposed by projecting the trade onto the
constraint null space.
"""

from __future__ import annotations

import numpy as np
from scipy import linalg


def markowitz_target(alpha: np.ndarray, cov: np.ndarray, risk_aversion: float) -> np.ndarray:
    """Frictionless mean-variance target ``Sigma^{-1} alpha / (2 lam)``."""
    return linalg.solve(cov, alpha, assume_a="pos") / (2.0 * risk_aversion)


def partial_adjustment_trades(
    weights: np.ndarray,
    alpha: np.ndarray,
    cov: np.ndarray,
    risk_aversion: float,
    tcost: float | np.ndarray,
    neutrality: np.ndarray | None = None,
) -> np.ndarray:
    """Optimal trade vector for one period (closed form).

    Parameters
    ----------
    weights : np.ndarray
        Current portfolio weights, shape (n,).
    alpha : np.ndarray
        Expected-return signal, shape (n,).
    cov : np.ndarray
        Return covariance matrix, shape (n, n).
    risk_aversion : float
        Risk-aversion coefficient ``lam > 0``.
    tcost : float or np.ndarray
        Quadratic transaction-cost coefficient.  A scalar means
        ``Gamma = tcost * I``; a 1-D array gives a diagonal ``Gamma``
        (per-asset cost, e.g. inverse liquidity); a 2-D array is used
        as ``Gamma`` directly.
    neutrality : np.ndarray or None
        Optional constraint matrix ``A`` of shape (k, n).  The executed
        trade is projected so that ``A x = 0`` (e.g. rows of ones for
        dollar neutrality, factor loadings for beta neutrality).

    Returns
    -------
    np.ndarray of shape (n,) -- the trade (metaorder) vector.
    """
    n = len(weights)
    lam = float(risk_aversion)
    gamma = _as_gamma(tcost, n)
    lhs = lam * cov + gamma
    rhs = 0.5 * alpha - lam * cov @ weights
    x = linalg.solve(lhs, rhs, assume_a="pos")
    if neutrality is not None:
        x = _project_neutral(x, np.atleast_2d(neutrality))
    return x


def trading_rate(cov_scale: float, risk_aversion: float, tcost: float) -> float:
    """Scalar-case fraction of the gap to the aim portfolio traded per period.

    For a single asset with variance ``cov_scale`` the partial adjustment
    reduces to ``x = tau * (w_M - w)`` with
    ``tau = lam * sigma^2 / (lam * sigma^2 + tcost)``.  Useful for choosing
    ``tcost`` to hit a desired metaorder duration.
    """
    k = risk_aversion * cov_scale
    return k / (k + tcost)


def _as_gamma(tcost: float | np.ndarray, n: int) -> np.ndarray:
    t = np.asarray(tcost, dtype=float)
    if t.ndim == 0:
        return float(t) * np.eye(n)
    if t.ndim == 1:
        return np.diag(t)
    return t


def _project_neutral(x: np.ndarray, a: np.ndarray) -> np.ndarray:
    """Project ``x`` onto the null space of ``a`` (least-squares correction)."""
    correction = a.T @ linalg.solve(a @ a.T, a @ x)
    return x - correction
