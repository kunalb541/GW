"""E83 contract tests - guard the strain pipeline machinery (whiten, bandpass, inst-freq, ringdown fit).
Data-free: synthetic injections. Seed 83."""
import numpy as np
from scipy.signal import welch
from src.e83_strain_ringdown import whiten, bandpass, inst_frequency, ringdown_fit

RNG = np.random.default_rng(83)
FS = 4096.0

def test_ringdown_fit_recovers_injection():
    t = np.arange(0, 0.05, 1 / FS)
    f0, tau0 = 250.0, 4.0e-3
    rd = np.exp(-t / tau0) * np.cos(2 * np.pi * f0 * t)
    fdom, tau = ringdown_fit(rd, FS)
    assert abs(fdom - f0) < 10, fdom            # recovers the QNM frequency
    assert abs(tau - tau0) / tau0 < 0.25, tau   # recovers the damping time

def test_inst_frequency_rises_for_chirp():
    t = np.arange(0, 1, 1 / FS)
    x = np.cos(2 * np.pi * (50 * t + 80 * t ** 2))   # frequency 50 -> 210 Hz
    f = inst_frequency(x, FS)
    assert f[len(f) // 4] < f[3 * len(f) // 4]        # rising

def test_whiten_flattens_colored_noise():
    n = int(16 * FS)
    x = np.cumsum(RNG.normal(size=n)); x -= x.mean()   # red (1/f^2-ish) noise
    fpsd, P = welch(x, fs=FS, nperseg=int(2 * FS))
    w = whiten(x, FS, fpsd, P)
    fw, Pw = welch(w, fs=FS, nperseg=int(2 * FS))
    band = (fw > 30) & (fw < 400)
    # whitened PSD should be far flatter (low/high power ratio near 1) than the red input
    lo, hi = fw < 100, (fw > 200) & (fw < 400)
    assert (Pw[lo & band].mean() / Pw[hi & band].mean()) < (P[lo & band].mean() / P[hi & band].mean())

def test_bandpass_suppresses_out_of_band():
    t = np.arange(0, 4, 1 / FS)
    x = np.cos(2 * np.pi * 100 * t) + np.cos(2 * np.pi * 900 * t)   # in-band 100, out 900
    y = bandpass(x, FS, 30, 400)
    # out-of-band (900 Hz) power strongly suppressed relative to in-band (100 Hz)
    fpsd, P = welch(y, fs=FS, nperseg=int(FS))
    p100 = P[np.argmin(abs(fpsd - 100))]; p900 = P[np.argmin(abs(fpsd - 900))]
    assert p900 / p100 < 1e-3
