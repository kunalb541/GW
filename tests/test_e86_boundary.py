"""E86 contract tests - guard the boundary machinery (notch conditioning, ridge monotonicity as a
chirp/no-chirp discriminator, injection response). Data-free (synthetic strain). Seed 86."""
import numpy as np
import math
from scipy.signal import welch
from src.e86_band_resolved_boundary import (condition, band_ridge_mc, inject_chirp,
                                            mc_from_slope, FS, MSUN)

RNG = np.random.default_rng(86)

def _noise(dur_s=32.0, amp=1e-21):
    return RNG.normal(size=int(dur_s * FS)) * amp

def _psd(x):
    return welch(x[:int(8 * FS)], fs=FS, nperseg=int(8 * FS))

def test_slope_inversion_roundtrip():
    for mc in (8.0, 10.9, 30.0):
        K = (256 / 5) * math.pi ** (8 / 3) * (mc * MSUN) ** (5 / 3)
        assert abs(mc_from_slope(K) - mc) / mc < 1e-9

def test_notch_suppresses_a_line():
    # a strong 60 Hz line must be suppressed by the conditioning chain
    n = _noise()
    t = np.arange(len(n)) / FS
    x = n + 50e-21 * np.sin(2 * math.pi * 60.0 * t)
    fpsd, Pxx = _psd(x)
    w = condition(x, fpsd, Pxx)
    f, P = welch(w, fs=FS, nperseg=int(4 * FS))
    near = (f > 59.5) & (f < 60.5); away = (f > 70) & (f < 110)
    assert P[near].max() < 5 * np.median(P[away]), (P[near].max(), np.median(P[away]))

def test_monotonicity_discriminates_chirp_from_noise():
    # a real injected chirp -> rising ridge (monotonicity > 0.5); pure noise -> no coherent rise
    noise = _noise()
    fpsd, Pxx = _psd(noise)
    seg, itc = inject_chirp(noise, mc_det=10.9, amp=3e-21)
    _, _, rho_sig = band_ridge_mc(condition(seg, fpsd, Pxx), itc, 2048, 30, 50)
    _, _, rho_noise = band_ridge_mc(condition(noise, fpsd, Pxx), itc, 2048, 30, 50)
    assert rho_sig > 0.5, rho_sig
    assert (rho_noise != rho_noise) or rho_noise < rho_sig, (rho_noise, rho_sig)

def test_injection_recovers_low_mass_chirp():
    # in the regime where the long window IS adequate (light, slow sweep) the estimator is ~unbiased
    noise = _noise()
    fpsd, Pxx = _psd(noise)
    seg, itc = inject_chirp(noise, mc_det=8.0, amp=3e-21)
    mc, n, rho = band_ridge_mc(condition(seg, fpsd, Pxx), itc, 2048, 30, 50)
    assert n >= 6 and rho > 0.5
    assert 0.7 < mc / 8.0 < 1.3, mc

def test_response_slope_is_compressed_at_higher_mass():
    # THE boundary result: the estimator's response to true Mc is compressed (little information).
    # A 36% increase in true Mc must NOT produce a proportionate increase in the recovered value.
    noise = _noise()
    fpsd, Pxx = _psd(noise)
    recs = []
    for mc_true in (8.0, 10.9):
        seg, itc = inject_chirp(noise, mc_det=mc_true, amp=3e-21)
        mc, _, _ = band_ridge_mc(condition(seg, fpsd, Pxx), itc, 2048, 30, 50)
        recs.append(mc)
    slope = ((recs[1] - recs[0]) / recs[0]) / ((10.9 - 8.0) / 8.0)
    assert slope < 0.75, slope        # far below 1.0 = the degeneracy that closes the method
