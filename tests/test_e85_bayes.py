"""E85 contract tests - guard the Bayesian layer (sampler, Kerr inversion, end-to-end injection).
Data-free. Seed 85."""
import numpy as np
import math
from src.e85_bayesian_ringdown import ensemble_sampler, kerr_invert, RingdownFit
from src.e74_gw250114_deepdive import qnm

RNG = np.random.default_rng(85)

def test_sampler_recovers_gaussian():
    # 2D correlated Gaussian: ensemble MCMC must recover mean and covariance
    mu = np.array([1.0, -2.0]); C = np.array([[2.0, 1.2], [1.2, 1.5]]); Ci = np.linalg.inv(C)
    logp = lambda x: -0.5 * float((x - mu) @ Ci @ (x - mu))
    p0 = RNG.normal(size=(24, 2)) * 3
    ch = ensemble_sampler(logp, p0, 1500, RNG)
    s = ch[750:].reshape(-1, 2)
    assert np.allclose(s.mean(0), mu, atol=0.15), s.mean(0)
    assert np.allclose(np.cov(s.T), C, atol=0.4), np.cov(s.T)

def test_kerr_inversion_roundtrip():
    # (Mf, af) -> (f, tau) via the BCW fits -> invert -> recover (Mf, af)
    for Mf, af in [(68.4, 0.679), (40.0, 0.5), (100.0, 0.9)]:
        f, tau = qnm(Mf, af, "220")
        Mf2, af2 = kerr_invert(f, tau)
        assert abs(Mf2 - Mf) / Mf < 1e-6, (Mf, Mf2)
        assert abs(af2 - af) < 1e-6, (af, af2)

def test_kerr_inversion_rejects_unphysical():
    Mf, af = kerr_invert(250.0, 1e-5)      # absurdly small damping -> Q below Kerr floor
    assert math.isnan(Mf) and math.isnan(af)

def test_end_to_end_injection_recovery_grid():
    # inject a known damped sinusoid into white noise; the grid-marginalized posterior recovers it
    from src.e85_bayesian_ringdown import grid_fit
    fs = 1024.0; N = int(8 * fs)
    noise = RNG.normal(size=N) * 1e-21
    f0, tau0, A0 = 220.0, 6e-3, 20e-21
    i0 = N // 2; tt = np.arange(N - i0) / fs
    sig = np.zeros(N); sig[i0:] = A0 * np.exp(-tt / tau0) * np.cos(2 * math.pi * f0 * tt + 1.0)
    post, sigma, _ = grid_fit(noise + sig, fs, i0, dt_ms=0.0, rng=RNG)
    f_med = np.median(post[:, 0]); tau_med = np.median(post[:, 1]) * 1e-3
    assert abs(f_med - f0) < 5.0, f_med                 # frequency recovered
    assert abs(tau_med - tau0) / tau0 < 0.35, tau_med   # damping recovered

def test_marginal_lnL_peaks_at_injection():
    # the analytic marginal likelihood surface peaks at the injected (f, tau), not elsewhere
    fs = 1024.0; N = int(8 * fs)
    noise = RNG.normal(size=N) * 1e-21
    f0, tau0, A0 = 250.0, 5e-3, 25e-21
    i0 = N // 2; tt = np.arange(N - i0) / fs
    sig = np.zeros(N); sig[i0:] = A0 * np.exp(-tt / tau0) * np.cos(2 * math.pi * f0 * tt + 0.3)
    fit = RingdownFit(noise + sig, fs, i0, nwin=int(0.05 * fs))
    at_true = fit.marginal_lnL(f0, tau0)
    assert at_true > fit.marginal_lnL(f0 + 40, tau0)
    assert at_true > fit.marginal_lnL(f0 - 40, tau0)
    assert at_true > fit.marginal_lnL(f0, tau0 * 3)

def test_pre_window_burst_does_not_leak():
    # THE regression test for the artifact that defeated whiten-then-window: a LOUD transient just
    # BEFORE the analysis window must not manufacture a ringdown detection inside it.
    fs = 1024.0; N = int(8 * fs)
    noise = RNG.normal(size=N) * 1e-21
    i0 = N // 2
    # loud burst ending 1 ms before the window (gaussian-windowed 200 Hz wiggle, ~500x noise)
    tb = np.arange(int(0.02 * fs)) / fs
    burst = 500e-21 * np.exp(-0.5 * ((tb - 0.01) / 0.003) ** 2) * np.cos(2 * math.pi * 200 * tb)
    seg_burst = noise.copy(); jb = i0 - int(0.021 * fs); seg_burst[jb: jb + len(tb)] += burst
    # a genuine in-window ringdown, for contrast
    tt = np.arange(N - i0) / fs
    seg_ring = noise.copy(); seg_ring[i0:] += 20e-21 * np.exp(-tt / 6e-3) * np.cos(2 * math.pi * 220 * tt)
    def contrast(seg):
        fit = RingdownFit(seg, fs, i0, nwin=int(0.05 * fs))
        fgrid = np.arange(160, 341, 6.0)
        vals = np.array([fit.marginal_lnL(f, 6e-3) for f in fgrid])
        return float(vals.max() - np.median(vals))
    c_burst, c_ring = contrast(seg_burst), contrast(seg_ring)
    assert c_burst < 0.25 * c_ring, (c_burst, c_ring)   # burst-only surface is flat vs a real ringdown
