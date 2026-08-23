"""The Kolm-Westray order flow simulator.

Design goals, following the paper: (i) simple to use and integrate,
(ii) computationally efficient across many securities, (iii) simulated flow
statistically similar to real buy-side flow.  The simulator models a
stylized systematic trader: each period a bootstrap alpha vector is drawn,
the trader solves a mean-variance problem with quadratic transaction costs
(closed form, one dense solve per period), and the resulting position
*changes* are recorded as metaorders.  Order-splitting, sign
autocorrelation and realistic size distributions emerge from the optimal
partial adjustment rather than being imposed.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from flowforge.generate.alpha import BootstrapAlpha
from flowforge.generate.market import MarketModel
from flowforge.generate.mvo import partial_adjustment_trades


@dataclass
class SimulationConfig:
    """Configuration of an :class:`OrderFlowSimulator` run.

    Parameters
    ----------
    n_assets, n_periods : problem size.
    rho : information coefficient of the alpha signal; 0 = uninformed flow.
    alpha_half_life : persistence of the signal, in periods (None = iid).
    risk_aversion : MVO risk-aversion coefficient ``lam``.
    tcost : quadratic transaction-cost coefficient (scalar or per-asset).
    book_size : dollar gross book the weights refer to.
    min_order_notional : orders below this dollar size are dropped
        (mirrors the fact that real desks do not send dust orders).
    seed : RNG seed for full reproducibility.
    """

    n_assets: int = 100
    n_periods: int = 500
    rho: float = 0.05
    alpha_half_life: float | None = 5.0
    risk_aversion: float = 5.0
    tcost: float = 5e-3
    book_size: float = 1e9
    min_order_notional: float = 1e4
    seed: int | None = None


class OrderFlowSimulator:
    """Generate labeled metaorder flow from mean-variance optimal trading.

    Examples
    --------
    >>> cfg = SimulationConfig(n_assets=50, n_periods=200, rho=0.05, seed=1)
    >>> sim = OrderFlowSimulator(cfg)
    >>> orders = sim.run()
    >>> set(["period", "asset", "notional", "sign", "participation"]) <= set(orders.columns)
    True
    """

    def __init__(self, config: SimulationConfig, market: MarketModel | None = None) -> None:
        self.config = config
        self.market = market if market is not None else MarketModel(
            n_assets=config.n_assets, seed=config.seed
        )
        self.rng = np.random.default_rng(config.seed)
        self.alpha_model = BootstrapAlpha(
            rho=config.rho,
            vols=self.market.vols,
            half_life=config.alpha_half_life,
            rng=self.rng,
        )

    def run(self) -> pd.DataFrame:
        """Simulate and return the order tape as a long-format DataFrame.

        Columns: ``period, asset, weight_change, notional, sign,
        participation, adv, market_cap, informed, realized_return, alpha``.
        """
        cfg = self.config
        mkt = self.market
        returns = mkt.sample_returns(cfg.n_periods, self.rng)
        weights = np.zeros(cfg.n_assets)
        records: list[pd.DataFrame] = []

        for t in range(cfg.n_periods):
            alpha = self.alpha_model.sample(returns[t])
            trades = partial_adjustment_trades(
                weights, alpha, mkt.cov, cfg.risk_aversion, cfg.tcost
            )
            weights = weights + trades
            notional = trades * cfg.book_size
            mask = np.abs(notional) >= cfg.min_order_notional
            if not mask.any():
                continue
            idx = np.nonzero(mask)[0]
            size_pct_adv = np.abs(notional[idx]) / mkt.adv[idx]
            # Execution participation rate: larger orders (as %ADV) are
            # traded at higher participation (Kolm-Westray validation fact),
            # with log-normal dispersion and a cap at 30% of volume.
            participation = np.minimum(
                0.3,
                0.1 * np.sqrt(size_pct_adv) * np.exp(self.rng.normal(0.0, 0.5, len(idx))),
            )
            records.append(
                pd.DataFrame(
                    {
                        "period": t,
                        "asset": idx,
                        "weight_change": trades[idx],
                        "notional": np.abs(notional[idx]),
                        "sign": np.sign(notional[idx]).astype(int),
                        "participation": participation,
                        "adv": mkt.adv[idx],
                        "market_cap": mkt.market_caps[idx],
                        "informed": self.alpha_model.informed,
                        "realized_return": returns[t, idx],
                        "alpha": alpha[idx],
                    }
                )
            )

        if not records:
            return _empty_orders_frame()
        orders = pd.concat(records, ignore_index=True)
        return orders

    def realized_ic(self, orders: pd.DataFrame) -> float:
        """Cross-sectional correlation between signal and realized return."""
        if len(orders) < 3:
            return float("nan")
        return float(np.corrcoef(orders["alpha"], orders["realized_return"])[0, 1])


def _empty_orders_frame() -> pd.DataFrame:
    cols = [
        "period", "asset", "weight_change", "notional", "sign",
        "participation", "adv", "market_cap", "informed",
        "realized_return", "alpha",
    ]
    return pd.DataFrame(columns=cols)
