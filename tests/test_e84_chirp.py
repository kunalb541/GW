"""E84 contract tests - guard the data-driven chirp machinery (slope inversion, ridge, end-to-end
synthetic recovery). Data-free. Seed 84."""
import numpy as np
import math
from src.e84_data_driven_chirp import mc_from_slope, ridge_points, fit_mc, MSUN

RNG = np.random.default_rng(84)
FS = 4096.0

def _chirp(mc_det_msun, fs, f0=32.0, tend=-0.006):
    """synthetic 0PN chirp: f(t) from f^(-8/3) = K (tc - t); returns (t, x) up to tend before tc."""
    K = (256 / 5) * math.pi ** (8 / 3) * (mc_det_msun * MSUN) ** (5 / 3)
    t0 = -(f0 ** (-8 / 3)) / K                       # time (rel. tc) when f = f0
    t = np.arange(t0, tend, 1 / fs)
    f = (K * (-t)) ** (-3 / 8)
    phase = 2 * np.pi * np.cumsum(f) / fs
    return t, np.cos(phase)

def test_slope_inversion_roundtrip():
    for mc in (2.0, 15.0, 31.0):
        K = (256 / 5) * math.pi ** (8 / 3) * (mc * MSUN) ** (5 / 3)
        assert abs(mc_from_slope(K) - mc) / mc < 1e-9

def test_negative_slope_is_nan():
    assert math.isnan(mc_from_slope(-1.0))

def test_end_to_end_recovery_within_characterized_bias():
    # the ridge estimator recovers the chirp mass within its CHARACTERIZED bias envelope
    # (quantization + window smearing in an accelerating sweep bias it +15-30% high; see E84 report)
    from src.e84_data_driven_chirp import synth_chirp
    mc_true = 15.0
    t, x = synth_chirp(mc_true, FS)
    tt, rf = ridge_points(x, FS, t[0], fmin=32, fmax=200, contrast=4.0)
    pre = tt < -0.010
    mc, n = fit_mc(tt[pre], rf[pre], 32, 200)
    assert n >= 8
    assert 1.00 <= mc / mc_true <= 1.40, mc          # ballpark + known-high bias, never low

def test_bias_grows_with_chirp_mass():
    # mechanism guard: faster sweeps (heavier Mc) -> larger quantization/window bias
    from src.e84_data_driven_chirp import injection_bias
    b = injection_bias()
    assert b["10"] < b["30"], b                       # monotone in Mc
    assert all(1.0 <= v <= 1.45 for v in b.values()), b

def test_ridge_false_positive_rate_in_noise():
    # confident-ridge fraction in pure noise stays a small false-positive rate
    x = RNG.normal(size=int(0.5 * FS))
    tt, rf = ridge_points(x, FS, -0.5, contrast=8.0)
    n_slices = (len(x) - 256) // 16 + 1
    assert len(rf) / n_slices < 0.15, (len(rf), n_slices)
