"""Tests for FlowForge: both engines plus diagnostics."""

import numpy as np
import pandas as pd
import pytest

from flowforge import (
    BootstrapAlpha,
    MappingConfig,
    MarketModel,
    OrderFlowSimulator,
    SimulationConfig,
    build_metaorders,
    execution_profile,
    impact_decay,
    markowitz_target,
    participation_stats,
    partial_adjustment_trades,
    sign_autocorrelation,
    square_root_law,
    synthetic_tape,
)
from flowforge.generate.mvo import trading_rate
from flowforge.reconstruct.mapping import assign_traders, sample_trader_frequencies


# ---------------------------------------------------------------- generate

def test_bootstrap_alpha_ic():
    rng = np.random.default_rng(0)
    vols = np.full(500, 0.02)
    model = BootstrapAlpha(rho=0.1, vols=vols, half_life=None, rng=rng)
    r = rng.normal(0, 0.02, (400, 500))
    ics = [np.corrcoef(model.sample(r[t]), r[t])[0, 1] for t in range(400)]
    assert abs(np.mean(ics) - 0.1) < 0.01


def test_uninformed_alpha_has_zero_ic():
    rng = np.random.default_rng(1)
    vols = np.full(500, 0.02)
    model = BootstrapAlpha(rho=0.0, vols=vols, rng=rng)
    r = rng.normal(0, 0.02, (200, 500))
    ics = [np.corrcoef(model.sample(r[t]), r[t])[0, 1] for t in range(200)]
    assert abs(np.mean(ics)) < 0.01


def test_partial_adjustment_matches_foc():
    rng = np.random.default_rng(2)
    n = 10
    a = rng.normal(size=(n, n))
    cov = a @ a.T / n + np.eye(n) * 0.01
    alpha, w = rng.normal(0, 0.01, n), rng.normal(0, 0.05, n)
    lam, tc = 4.0, 1e-2
    x = partial_adjustment_trades(w, alpha, cov, lam, tc)
    foc = alpha - 2 * lam * cov @ (w + x) - 2 * tc * x
    assert np.allclose(foc, 0, atol=1e-10)


def test_zero_tcost_reaches_markowitz():
    rng = np.random.default_rng(3)
    n = 5
    a = rng.normal(size=(n, n))
    cov = a @ a.T / n + np.eye(n) * 0.01
    alpha, w = rng.normal(0, 0.01, n), rng.normal(0, 0.05, n)
    x = partial_adjustment_trades(w, alpha, cov, 4.0, 0.0)
    assert np.allclose(w + x, markowitz_target(alpha, cov, 4.0), atol=1e-10)


def test_neutrality_projection():
    rng = np.random.default_rng(4)
    n = 8
    a = rng.normal(size=(n, n))
    cov = a @ a.T / n + np.eye(n) * 0.01
    ones = np.ones((1, n))
    x = partial_adjustment_trades(
        np.zeros(n), rng.normal(0, 0.01, n), cov, 4.0, 1e-2, neutrality=ones
    )
    assert abs(x.sum()) < 1e-10


def test_trading_rate_bounds():
    assert 0 < trading_rate(0.02**2, 5.0, 1e-2) < 1


def test_simulator_runs_and_labels():
    orders = OrderFlowSimulator(
        SimulationConfig(n_assets=40, n_periods=150, rho=0.05, seed=5)
    ).run()
    assert len(orders) > 100
    assert orders["informed"].all()
    assert set(orders["sign"].unique()) <= {-1, 1}
    assert (orders["notional"] > 0).all()


def test_simulator_sign_autocorrelation_positive():
    orders = OrderFlowSimulator(
        SimulationConfig(n_assets=60, n_periods=400, rho=0.05, seed=6)
    ).run()
    acf = sign_autocorrelation(orders, max_lag=3)
    assert acf.loc[acf["lag"] == 1, "autocorr"].iloc[0] > 0.05


def test_participation_stats_relations():
    orders = OrderFlowSimulator(
        SimulationConfig(n_assets=80, n_periods=300, rho=0.05, seed=7)
    ).run()
    stats = participation_stats(orders)
    assert stats["corr_size_participation"] > 0.5
    assert stats["corr_size_marketcap"] < 0


# ------------------------------------------------------------- reconstruct

def test_frequency_sampling():
    rng = np.random.default_rng(8)
    p_hom = sample_trader_frequencies(MappingConfig(n_traders=10), rng)
    assert np.allclose(p_hom.sum(), 1.0) and np.allclose(p_hom, 0.1)
    p_pl = sample_trader_frequencies(
        MappingConfig(n_traders=100, freq_dist="powerlaw", exponent=2.0), rng
    )
    assert np.allclose(p_pl.sum(), 1.0) and p_pl.max() > p_pl.min()


def test_assignment_covers_all_trades():
    rng = np.random.default_rng(9)
    p = sample_trader_frequencies(MappingConfig(n_traders=5), rng)
    ids = assign_traders(10000, p, rng)
    assert ids.min() >= 0 and ids.max() <= 4 and len(ids) == 10000


def test_build_metaorders_consistency():
    tape = synthetic_tape(n_sessions=3, trades_per_session=500, seed=10)
    meta, children = build_metaorders(tape, MappingConfig(n_traders=8), seed=10)
    assert len(meta) > 0
    assert (meta["n_children"] >= 2).all()
    assert (meta["volume"] > 0).all()
    assert (meta["q_frac"] <= 1.0).all()
    # children phi in (0, 1], last child of each metaorder ends at phi == 1
    assert (children["phi"] > 0).all() and (children["phi"] <= 1 + 1e-12).all()
    last_phi = children.groupby("meta_id")["phi"].max()
    assert np.allclose(last_phi, 1.0)
    # metaorder volume equals sum of member trade sizes: verify via q_frac * v_d
    assert np.allclose(meta["volume"], meta["q_frac"] * meta["v_d"])


def test_metaorders_require_valid_tape():
    bad = pd.DataFrame({"timestamp": [1, 2], "price": [1.0, 1.0], "size": [1, 1]})
    with pytest.raises(ValueError):
        build_metaorders(bad)


def test_square_root_law_recovery():
    tape = synthetic_tape(n_sessions=40, trades_per_session=3000, seed=11)
    meta, _ = build_metaorders(tape, MappingConfig(n_traders=20), seed=11)
    sql = square_root_law(meta)
    assert 0.2 < sql["exponent"] < 0.8
    assert sql["Y"] > 0


def test_execution_profile_concave():
    tape = synthetic_tape(n_sessions=30, trades_per_session=3000, seed=12)
    _, children = build_metaorders(tape, MappingConfig(n_traders=20), seed=12)
    profile = execution_profile(children, n_bins=10)
    first, last = profile.iloc[0], profile.iloc[-1]
    slope_early = first["impact"] / max(first["phi"], 1e-9)
    slope_avg = last["impact"] / max(last["phi"], 1e-9)
    assert slope_early > slope_avg  # early children impact more: concavity


def test_impact_decay_runs():
    tape = synthetic_tape(n_sessions=30, trades_per_session=3000, seed=13)
    meta, _ = build_metaorders(tape, MappingConfig(n_traders=20), seed=13)
    decay = impact_decay(meta, tape, min_duration=60.0)
    assert len(decay) >= 3
    peak = decay.loc[decay["z"] == 1.0, "impact"].iloc[0]
    tail = decay.loc[decay["z"] == decay["z"].max(), "impact"].iloc[0]
    assert peak > 0 and tail < peak  # impact decays after execution


def test_sign_flip_kills_impact():
    """Paper's sanity check: randomly flipping trade signs must give ~zero impact."""
    tape = synthetic_tape(n_sessions=30, trades_per_session=3000, seed=14)
    rng = np.random.default_rng(14)
    tape_flipped = tape.copy()
    tape_flipped["sign"] = rng.choice([-1, 1], size=len(tape))
    meta, _ = build_metaorders(tape_flipped, MappingConfig(n_traders=20), seed=14)
    mean_impact = meta["norm_impact"].mean()
    assert abs(mean_impact) < 0.1
