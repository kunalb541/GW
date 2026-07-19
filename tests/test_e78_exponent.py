"""E78 contract tests - guard the geometric-exponent machinery.
Data-free; synthetic q-marginals. Seed 78."""
import numpy as np
from src.e78_geometric_gr_exponent import curve_pts, curve_psi_p, fit_p, psi_of
from src.e71_gwtc5_curved_law import curve_psi as e71_curve_psi

RNG = np.random.default_rng(78)
Q = np.clip(RNG.uniform(0.3, 1.0, 4000), 0.02, 1.0)   # a spread mass-ratio marginal

def test_p06_matches_e71_curve_law():
    # the generalized curve at p=0.6 must reproduce the E71 constant-Mc curve orientation exactly
    # (E71's curve_psi(mc, qs) is scale-free in mc, so any mc works)
    a = curve_psi_p(Q, 0.6)
    b = e71_curve_psi(30.0, Q)
    assert abs((a - b + 90) % 180 - 90) < 1e-6

def test_scale_invariance():
    # orientation is independent of the mass-scale prefactor (that is why p is isolated)
    P = curve_pts(Q, 0.6)
    assert abs((psi_of(P) - psi_of(P * 7.3) + 90) % 180 - 90) < 1e-9

def test_injection_recovers_known_p():
    for p_true in (0.50, 0.55, 0.60, 0.65, 0.70):
        psi = curve_psi_p(Q, p_true)      # noiseless: fit must return p_true
        assert abs(fit_p(Q, psi) - p_true) < 0.01, p_true

def test_sensitivity_monotone_in_p():
    # predicted orientation moves monotonically with p (non-degenerate -> test has power)
    psis = [curve_psi_p(Q, p) for p in np.linspace(0.45, 0.75, 7)]
    d = np.diff(psis)
    assert np.all(d > 0) or np.all(d < 0)
    assert abs(psis[-1] - psis[0]) > 3.0     # >3 deg across the range -> constrainable

def test_fit_is_deterministic():
    psi = curve_psi_p(Q, 0.6)
    assert fit_p(Q, psi) == fit_p(Q, psi)
