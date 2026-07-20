"""E87 contract tests - guard the corrected ringdown covariance. Every test here encodes a defect that
actually occurred and cost real sensitivity (or, in the null/leak cases, would have manufactured a fake
detection). Data-free (synthetic colored noise). Seed 87."""
import numpy as np
import math
from scipy.signal import butter, filtfilt
from scipy.linalg import toeplitz, cho_factor, cho_solve
from src.e87_ringdown_corrected import (RingdownFit, acf_from_psd, surface, summarize,
                                        kerr_invert, find_peak)

RNG = np.random.default_rng(87)
FS = 4096.0
NWIN = int(0.040 * FS)
F_GRID = np.arange(200.0, 301.0, 4.0)          # coarse grids keep the suite fast
TAU_GRID = np.arange(2.0, 9.1, 1.0)


def _colored_noise(dur_s=40.0, amp=2.3e-22):
    """Noise with a realistically STEEP red wall below ~30 Hz plus a flat mid band. The steepness is
    calibrated, not arbitrary: a gentle 60x step reproduces only a 1.8x taper penalty, whereas real H1
    strain shows ~20x. These filter settings reproduce ~40x, i.e. the regime the bug actually lived in."""
    w = RNG.normal(size=int(dur_s * FS))
    b, a = butter(6, 30.0, btype="low", fs=FS)
    return (amp * w + 3000.0 * amp * filtfilt(b, a, w))


def _ringdown(n, i0, f, tau, amp, phi=0.7):
    s = np.zeros(n)
    t = np.arange(n - i0) / FS
    s[i0:] = amp * np.exp(-t / tau) * np.cos(2 * math.pi * f * t + phi)
    return s


# ---------------------------------------------------------------- the factor-2 bug
def test_wiener_khinchin_normalization_matches_empirical_autocovariance():
    """THE bug that a one-sided PSD invites: irfft(psd*fs) is exactly 2x too large, which tempers the
    likelihood and inflates every credible interval by sqrt(2) WITHOUT moving the peak - invisible to
    any peak-location check. acf[0] must equal the variance of the high-passed noise."""
    noise = _colored_noise()
    acf = acf_from_psd(noise, FS, NWIN)
    b, a = butter(4, 25.0, btype="high", fs=FS)
    nz = filtfilt(b, a, noise)
    assert abs(acf[0] / np.var(nz) - 1.0) < 0.05, acf[0] / np.var(nz)
    # and the off-diagonal structure must track the empirical ACF, not be tapered away
    for k in (1, 5, 20, 100):
        emp = np.mean(nz[:len(nz) - k] * nz[k:])
        assert abs(acf[k] - emp) < 0.25 * acf[0], (k, acf[k], emp)


def test_acf_is_positive_definite_without_a_taper():
    """The Wiener-Khinchin ACF of a nonnegative spectrum is PD by construction - so the destructive
    E85 taper (which is what crushed the noise colour) is never needed."""
    acf = acf_from_psd(_colored_noise(), FS, NWIN)
    cho_factor(toeplitz(acf))          # raises LinAlgError if not PD


def test_corrected_covariance_is_far_more_sensitive_than_the_e85_construction():
    """The E85 regression: a tapered ACF + a 1e-3 broadband ridge charges an in-band matched filter the
    BROADBAND noise. Recovering that sensitivity is the whole point of E87."""
    noise = _colored_noise()
    b, a = butter(4, 25.0, btype="high", fs=FS)
    nz = filtfilt(b, a, noise)
    tt = np.arange(NWIN) / FS
    tmpl = np.exp(-tt / 4.2e-3) * np.cos(2 * math.pi * 252 * tt)

    def snr_per_amp(acf, ridge):
        C = toeplitz(acf)
        C[np.diag_indices_from(C)] += ridge * acf[0]
        return math.sqrt(tmpl @ cho_solve(cho_factor(C), tmpl))

    emp = np.array([np.mean(nz[:len(nz) - k] * nz[k:]) for k in range(NWIN)])
    e85 = snr_per_amp(emp * np.linspace(1.0, 0.0, NWIN) ** 2, 1e-3)
    e87 = snr_per_amp(acf_from_psd(noise, FS, NWIN), 1e-6)
    assert e87 / e85 > 5.0, e87 / e85


# ---------------------------------------------------------------- null behaviour
def test_pure_noise_gives_an_UNINFORMATIVE_posterior():
    """E85's real-data result was statistically indistinguishable from no signal: the '90% CI' was the
    grid. With no signal the posterior MUST stay flat - so that a narrow interval means something."""
    noise = _colored_noise()
    fit = RingdownFit(noise, FS, len(noise) // 2, NWIN, noise)
    lnL = surface(fit, F_GRID, TAU_GRID)
    s = summarize(lnL, F_GRID, TAU_GRID)
    span = F_GRID[-1] - F_GRID[0]
    assert s["width"] > 0.6 * span, s          # essentially the prior
    assert lnL.max() - lnL.min() < 15.0, lnL.max() - lnL.min()


def test_pre_window_burst_does_not_leak_into_the_window():
    """Inherited E85 guard: the truncated likelihood must not let a loud transient BEFORE the window
    ring forward into it (the acausal-whitening artifact that produced fake narrow modes)."""
    noise = _colored_noise()
    i0 = len(noise) // 2
    burst = np.zeros(len(noise))
    j = i0 - int(0.010 * FS)
    tb = np.arange(int(0.008 * FS)) / FS
    burst[j:j + len(tb)] = 3e-19 * np.exp(-tb / 1e-3) * np.cos(2 * math.pi * 250 * tb)
    s = summarize(surface(RingdownFit(noise + burst, FS, i0, NWIN, noise), F_GRID, TAU_GRID),
                  F_GRID, TAU_GRID)
    span = F_GRID[-1] - F_GRID[0]
    assert s["width"] > 0.5 * span, s          # a pre-window burst must NOT create a confident mode


# ---------------------------------------------------------------- signal behaviour
def test_injected_ringdown_is_recovered_at_realistic_amplitude():
    noise = _colored_noise()
    i0 = len(noise) // 2
    d = noise + _ringdown(len(noise), i0, 252.0, 4.2e-3, 2.5e-21)
    s = summarize(surface(RingdownFit(d, FS, i0, NWIN, noise), F_GRID, TAU_GRID), F_GRID, TAU_GRID)
    assert s["f_lo"] < 252.0 < s["f_hi"], s    # truth inside the 90% CI
    assert s["width"] < 0.4 * (F_GRID[-1] - F_GRID[0]), s


def test_adding_a_second_detector_must_not_broaden_the_posterior():
    """The failure that exposed E85: summing two independent detectors' lnL surfaces LEFT the width
    unchanged (162 vs 160 Hz), which is impossible for genuine information. It must tighten."""
    i0 = None
    widths, lnLs = [], []
    for _ in range(2):
        noise = _colored_noise()
        i0 = len(noise) // 2
        d = noise + _ringdown(len(noise), i0, 252.0, 4.2e-3, 2.5e-21)
        lnL = surface(RingdownFit(d, FS, i0, NWIN, noise), F_GRID, TAU_GRID)
        lnLs.append(lnL)
        widths.append(summarize(lnL, F_GRID, TAU_GRID)["width"])
    net = summarize(lnLs[0] + lnLs[1], F_GRID, TAU_GRID)["width"]
    assert net <= min(widths) + 1e-9, (net, widths)


def test_kerr_inversion_roundtrip():
    """(f, tau) -> (Mf, af) must invert the BCW fit self-consistently."""
    from src.e74_gw250114_deepdive import qnm
    for Mf, af in ((68.4, 0.679), (60.0, 0.5), (80.0, 0.8)):
        f, tau = qnm(Mf, af, "220")
        Mf2, af2 = kerr_invert(f, tau)
        assert abs(Mf2 - Mf) / Mf < 1e-6, (Mf, Mf2)
        assert abs(af2 - af) < 1e-6, (af, af2)


def test_find_peak_locates_an_injected_transient():
    noise = _colored_noise(dur_s=8.0)
    i0 = len(noise) // 2 + int(0.013 * FS)
    d = noise + _ringdown(len(noise), i0, 252.0, 4.2e-3, 5e-20)
    assert abs(find_peak(d, FS) - i0) < int(0.003 * FS), (find_peak(d, FS), i0)
