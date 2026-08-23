# FlowForge

Python package pairing two engines for metaorder research: a **generation
engine** that forward-simulates institutional order flow via mean-variance
optimization on tunable alpha signals,
producing millions of labeled orders switchable between informed and
uninformed flow for execution algo testing and causal A/B experiments at
zero trading cost; and an **impact engine** that reconstructs realistic
metaorders from public trade data via randomized trader mapping, recovering
proprietary-grade stylized facts (Square Root Law, concave execution
profiles, impact decay) and removing the proprietary-data barrier to
impact research.

## Install

```bash
pip install -e .
```

Dependencies: numpy, pandas, scipy.

## Engine 1 — order flow generation (`flowforge.generate`)

Each period a bootstrap alpha vector `alpha = rho * r + sqrt(1-rho^2) * z`
(information coefficient ≈ `rho` by construction) feeds a mean-variance
problem with quadratic transaction costs. The closed-form solution is a
Garleanu-Pedersen partial adjustment toward the Markowitz target, so
order splitting and sign autocorrelation emerge endogenously. Setting
`rho=0` flips the same machinery to uninformed (randomized) flow — the
switch used for interventional data in causal A/B testing of impact models.

```python
from flowforge import OrderFlowSimulator, SimulationConfig

sim = OrderFlowSimulator(SimulationConfig(
    n_assets=100, n_periods=750,
    rho=0.05,             # information coefficient; 0 = uninformed flow
    alpha_half_life=5.0,  # signal persistence, periods
    risk_aversion=5.0,
    tcost=5e-3,           # quadratic transaction cost -> trading rate
    seed=7,
))
orders = sim.run()        # long-format tape: period, asset, notional, sign,
                          # participation, adv, market_cap, informed, ...
print(sim.realized_ic(orders))
```

Flow diagnostics:

```python
from flowforge import sign_autocorrelation, participation_stats

sign_autocorrelation(orders, max_lag=10)   # order-splitting persistence
participation_stats(orders)                # size/participation/cap relations
```

## Engine 2 — metaorder reconstruction (`flowforge.reconstruct`)

Takes any public tape (`timestamp, price, size, sign`, plus a session
column), randomly assigns trades to `n_traders` synthetic traders drawn
from a homogeneous or power-law frequency distribution (the mapping's only
two degrees of freedom), and defines a metaorder as a same-trader,
same-sign run of trades. Impact is measured from the trade before the
first child to the trade after the last child, normalized by daily
volatility and volume.

```python
from flowforge import build_metaorders, MappingConfig, synthetic_tape

tape = synthetic_tape(n_sessions=40, trades_per_session=3000, seed=11)
# or your own data: DataFrame with date, timestamp, price, size, sign

meta, children = build_metaorders(
    tape, MappingConfig(n_traders=20, freq_dist="homogeneous"), seed=11
)
```

Impact diagnostics:

```python
from flowforge import square_root_law, execution_profile, impact_decay

sql = square_root_law(meta)          # fits I/sigma = Y * (Q/V)^gamma
profile = execution_profile(children)  # vs sqrt(phi) concave benchmark
decay = impact_decay(meta, tape)     # rescaled impact at z = 1 + dt/T
```

Benchmarks from the literature: exponent ≈ 0.5 with prefactor
Y ∈ [0.5, 1]; concave `sqrt(phi)` in-execution profile; impact decaying
after execution on the timescale of the metaorder itself.

## Quickstart

```bash
python examples/quickstart.py
python -m pytest tests/
```

## Package layout

```
flowforge/
├── generate/       Kolm-Westray engine: alpha.py, mvo.py, market.py, simulator.py
├── reconstruct/    Maitrier-Bouchaud engine: mapping.py, metaorders.py, tape.py
└── diagnostics/    shared stylized-fact tests: impact.py, flow.py
```

## Disclaimer

Research software for simulation and diagnostics; not investment advice.
