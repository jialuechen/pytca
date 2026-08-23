"""FlowForge quickstart: run both engines end to end.

Engine 1 (generate): simulate informed and uninformed institutional flow
via mean-variance optimization on bootstrap alphas, and check the flow
stylized facts.

Engine 2 (reconstruct): build synthetic metaorders from a (synthetic)
public tape via randomized trader mapping, and check the impact stylized
facts: Square Root Law, concave execution profile, post-execution decay.
"""

import numpy as np

from flowforge import (
    MappingConfig,
    OrderFlowSimulator,
    SimulationConfig,
    build_metaorders,
    execution_profile,
    impact_decay,
    participation_stats,
    sign_autocorrelation,
    square_root_law,
    synthetic_tape,
)


def main() -> None:
    print("=" * 68)
    print("Engine 1 - order flow generation (Kolm-Westray)")
    print("=" * 68)
    informed = OrderFlowSimulator(
        SimulationConfig(n_assets=100, n_periods=750, rho=0.05, seed=7)
    )
    orders = informed.run()
    print(f"informed orders generated : {len(orders):,}")
    print(f"realized IC               : {informed.realized_ic(orders):.4f} (target 0.05)")

    uninformed = OrderFlowSimulator(
        SimulationConfig(n_assets=100, n_periods=750, rho=0.0, seed=7)
    )
    rand_orders = uninformed.run()
    print(f"uninformed orders         : {len(rand_orders):,}")
    print(f"uninformed realized IC    : {uninformed.realized_ic(rand_orders):.4f} (target 0)")

    acf = sign_autocorrelation(orders, max_lag=5)
    print("\nsign autocorrelation (order splitting):")
    for _, row in acf.iterrows():
        print(f"  lag {int(row['lag'])}: {row['autocorr']:+.3f}")
    stats = participation_stats(orders)
    print(f"\ncorr(size %ADV, participation) : {stats['corr_size_participation']:+.3f}")
    print(f"corr(size %ADV, market cap)    : {stats['corr_size_marketcap']:+.3f}")
    print(f"participation tail exponent    : {stats['participation_tail_exponent']:.2f}")

    print()
    print("=" * 68)
    print("Engine 2 - metaorder reconstruction (Maitrier-Loeper-Bouchaud)")
    print("=" * 68)
    tape = synthetic_tape(n_sessions=40, trades_per_session=3000, seed=11)
    print(f"public tape               : {len(tape):,} trades / {tape['date'].nunique()} sessions")

    meta, children = build_metaorders(
        tape, MappingConfig(n_traders=20, freq_dist="homogeneous"), seed=11
    )
    print(f"synthetic metaorders      : {len(meta):,} "
          f"(mean children {meta['n_children'].mean():.1f}, "
          f"mean duration {meta['duration'].mean():.0f}s)")

    sql = square_root_law(meta)
    print(f"\nSquare Root Law fit       : I/sigma = {sql['Y']:.2f} * (Q/V)^{sql['exponent']:.2f}")
    print(f"  (benchmarks: exponent ~ 0.5, Y in [0.5, 1]; R = {sql['r_value']:.3f})")

    profile = execution_profile(children, n_bins=10)
    ratio = profile["impact"] / np.sqrt(profile["phi"])
    print("\nexecution profile I(phi)/sqrt(phi) by phi bin (flat = sqrt profile):")
    print("  " + "  ".join(f"{v:.2f}" for v in ratio.round(2)))

    decay = impact_decay(meta, tape, min_duration=60.0)
    print("\npost-execution decay (rescaled impact at z = 1 + dt/T):")
    for _, row in decay.iterrows():
        print(f"  z = {row['z']:.2f}: {row['impact']:+.3f}  (n={int(row['count']):,})")


if __name__ == "__main__":
    main()
