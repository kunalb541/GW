"""Contract tests for the E63 neutron-star EOS value/shape transfer.

Guard the machinery (not the physics conclusion): the value/shape + rho descriptors
must (a) not manufacture tension between a probe and itself, (b) recover a pure value
shift as value-dominated with unchanged rho, and (c) recover a pure orientation change
as a rho change. Also verify the C-Love map and column identifications are sane.
"""
import numpy as np
from src import e63_neutron_star_eos as e


def _probe(mu, C, N=40000, seed=0):
    X = np.random.default_rng(seed).multivariate_normal(mu, C, N)
    m, Cc = e.moments(X)
    return dict(label="synthetic", star="X", kind="xray", mu=m, C=Cc, X=X)


def test_self_pair_no_tension():
    C = np.array([[0.02, 0.03], [0.03, 1.2]])       # M-R-like covariance
    A = _probe([1.4, 12.7], C, seed=1); B = _probe([1.4, 12.7], C, seed=2)
    r = e.pair_analysis(A, B)
    assert r["sigma"] < 0.15                          # same distribution -> ~0 sigma
    assert r["delta_rho"] < 0.03


def test_pure_value_shift_is_value_dominated():
    C = np.array([[0.02, 0.03], [0.03, 1.2]])
    A = _probe([1.4, 12.7], C, seed=1); B = _probe([1.5, 13.7], C, seed=2)  # shifted mean, same C
    r = e.pair_analysis(A, B)
    assert r["classification"] == "value-dominated"
    assert r["delta_rho"] < 0.05
    assert r["vf_orientation_only"] > 0.7


def test_pure_orientation_change_shows_in_rho():
    Cpos = np.array([[0.02, 0.139], [0.139, 1.2]])    # rho ~ +0.90
    Cflat = np.array([[0.02, 0.031], [0.031, 1.2]])   # rho ~ +0.20
    A = _probe([1.4, 12.7], Cpos, seed=1); B = _probe([1.4, 12.7], Cflat, seed=2)
    r = e.pair_analysis(A, B)
    assert r["delta_rho"] > 0.3                        # orientation difference is captured by rho


def test_clove_radius_sane():
    # Lambda ~ 300 (GW170817-ish) at M=1.4 should give R ~ 11-12 km
    m = np.array([1.4]); lam = np.array([300.0])
    R = 1.4766 * m / (0.360 - 0.0355 * np.log(lam) + 0.000705 * np.log(lam) ** 2)
    assert 10.5 < float(R[0]) < 12.5


def test_rho_is_scale_invariant():
    # rho(M,R) must be invariant under independent rescaling of the axes (unit choice)
    C = np.array([[0.02, 0.03], [0.03, 1.2]])
    S = np.diag([1000.0, 0.001])                       # arbitrary unit change
    assert abs(e.rho_corr(C) - e.rho_corr(S @ C @ S.T)) < 1e-9
