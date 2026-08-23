"""FlowForge: metaorder simulation and market impact research.

Two engines:

- ``flowforge.generate``  -- forward-simulates institutional order flow by
  feeding bootstrap alpha signals into mean-variance optimization with
  quadratic transaction costs (Kolm & Westray, JPM 2022).
- ``flowforge.reconstruct`` -- builds synthetic metaorders from public trade
  data via randomized trader-mapping functions
  (Maitrier, Loeper & Bouchaud, 2025, arXiv:2503.18199).

A shared ``flowforge.diagnostics`` module validates the stylized facts of
both order flow (sign autocorrelation, participation) and impact
(Square Root Law, concave execution profile, post-execution decay).
"""

from flowforge.generate import (
    BootstrapAlpha,
    MarketModel,
    OrderFlowSimulator,
    SimulationConfig,
    markowitz_target,
    partial_adjustment_trades,
)
from flowforge.reconstruct import (
    MappingConfig,
    build_metaorders,
    sample_trader_frequencies,
    synthetic_tape,
)
from flowforge.diagnostics import (
    execution_profile,
    impact_decay,
    participation_stats,
    sign_autocorrelation,
    square_root_law,
)

__version__ = "0.1.0"

__all__ = [
    "BootstrapAlpha",
    "MarketModel",
    "OrderFlowSimulator",
    "SimulationConfig",
    "markowitz_target",
    "partial_adjustment_trades",
    "MappingConfig",
    "build_metaorders",
    "sample_trader_frequencies",
    "synthetic_tape",
    "square_root_law",
    "execution_profile",
    "impact_decay",
    "sign_autocorrelation",
    "participation_stats",
]
