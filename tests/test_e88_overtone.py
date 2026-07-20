"""E88 contract tests - guard the overtone-evidence machinery. Each test encodes something that was
actually measured during E88, including two designs that FAILED and must not silently return.
Data-free (synthetic colored noise). Seed 88."""
import numpy as np
import math
import pytest
from scipy.signal import butter, filtfilt
from src.e88_overtone_evidence import (kerr_basis, gb, kmats, rho_grid, ln_eff_stack, evidence,
                                       snr_perp, MODES, SIGMA_A_DEFAULT, RHO_MAX_DEFAULT)
from src.e87_ringdown_corrected import RingdownFit
from src.e74_gw250114_deepdive import qnm
import src.e88_overtone_evidence as E

RNG = np.random.default_rng(88)
FS = 4096.0
NWIN = int(0.040 * FS)
MF_T, AF_T = 68.4, 0.679
A_PEAK = 1.95e-21


@pytest.fixture(autouse=True)
def _small_grid(monkeypatch):
    """Keep the suite fast: a coarse (Mf, af) grid. E88 verified the evidence integral is converged
    at 1.0 Msun / 0.025, so a coarser grid changes absolute lnZ slightly but not any behaviour here."""
    monkeypatch.setattr(E, "MF_GRID", np.arange(52.0, 92.1, 4.0))
    monkeypatch.setattr(E, "AF_GRID", np.arange(0.05, 0.901, 0.05))
    monkeypatch.setattr(E, "RHO_N", 13)


def _noise(dur_s=40.0, amp=2.3e-22):
    w = RNG.normal(size=int(dur_s * FS))
    b, a = butter(6, 30.0, btype="low", fs=FS)
    return amp * w + 3000.0 * amp * filtfilt(b, a, w)


def _inject(base, i0, rho, phi=1.1, amp=A_PEAK):
    f0, t0 = qnm(MF_T, AF_T, "220")
    f1, t1 = qnm(MF_T, AF_T, "221")
    t = np.arange(len(base) - i0) / FS
    x = base.copy()
    x[i0:] += amp * (np.exp(-t / t0) * np.cos(2 * math.pi * f0 * t)
                     + rho * np.exp(-t / t1) * np.cos(2 * math.pi * f1 * t + phi))
    return x


def _fits(rho, n_det=2):
    out = []
    for _ in range(n_det):
        nz = _noise()
        i0 = len(nz) // 2
        out.append(RingdownFit(_inject(nz, i0, rho), FS, i0, NWIN, nz))
    return out


# ------------------------------------------------- the physical model reduction
def test_K_reduction_reproduces_the_physical_model_exactly():
    """The shared-rho model Re[A(T220 + rho T221)] must equal M_full @ K(rho) @ [u, v]. This is what
    lets one complex ratio be shared across detectors while each keeps a free complex amplitude."""
    t = np.arange(200) / FS
    M = kerr_basis(t, MF_T, AF_T)
    f0, t0 = qnm(MF_T, AF_T, "220")
    f1, t1 = qnm(MF_T, AF_T, "221")
    e0, e1 = np.exp(-t / t0), np.exp(-t / t1)
    w0, w1 = 2 * math.pi * f0, 2 * math.pi * f1
    for _ in range(50):
        u, v = RNG.normal(size=2)
        rho = complex(*RNG.normal(size=2))
        direct = np.real(complex(u, v) * (e0 * np.exp(1j * w0 * t) + rho * e1 * np.exp(1j * w1 * t)))
        K = kmats(np.array([rho.real]), np.array([rho.imag]))[0]
        assert np.allclose(M @ (K @ np.array([u, v])), direct, rtol=1e-10, atol=1e-14)


def test_rho_zero_reduces_to_the_220_only_model():
    K = kmats(np.zeros(1), np.zeros(1))[0]
    assert np.allclose(np.abs(K), np.array([[1., 0.], [0., 1.], [0., 0.], [0., 0.]]))


def test_marginal_evidence_matches_brute_force_integration():
    """The Gaussian-amplitude-prior evidence must equal direct numerical integration over the
    amplitudes. A flat/improper prior (what E85 and E87 used) makes a Bayes factor undefined."""
    from scipy.linalg import cho_factor, cho_solve
    n = 40
    L = np.tril(RNG.normal(size=(n, n))) * 0.1 + np.eye(n)
    cho = cho_factor(L @ L.T)
    d = RNG.normal(size=n)
    M = RNG.normal(size=(n, 2))
    sig = 0.7
    G = M.T @ cho_solve(cho, M)
    b = M.T @ cho_solve(cho, d)
    analytic = ln_eff_stack(G[None], b[None], sig)[0]
    g = np.linspace(-6 * sig, 6 * sig, 701)
    X, Y = np.meshgrid(g, g, indexing="ij")
    aa = np.stack([X, Y], -1)
    integ = (aa @ b - 0.5 * np.einsum("...i,ij,...j->...", aa, G, aa)
             - 0.5 * (X ** 2 + Y ** 2) / sig ** 2 - math.log(2 * math.pi * sig ** 2))
    m = integ.max()
    brute = m + math.log(np.exp(integ - m).sum() * (g[1] - g[0]) ** 2)
    assert abs(analytic - brute) < 1e-6, (analytic, brute)


# ------------------------------------------------- the design that FAILED
def test_shared_rho_keeps_the_noise_occam_penalty_small():
    """THE design result. Giving each detector its own free 221 amplitude (4 extra linear parameters)
    costs ~11 lnB of pure Occam penalty on signal-free data and destroys the test. Sharing rho makes
    both models carry the same linear dimension, so signal-free dlnB must sit near zero."""
    nz1, nz2 = _noise(), _noise()
    i1, i2 = len(nz1) // 2, len(nz2) // 2
    fits = [RingdownFit(nz1, FS, i1, NWIN, nz1), RingdownFit(nz2, FS, i2, NWIN, nz2)]
    ev, _ = evidence(fits)
    assert abs(ev[(SIGMA_A_DEFAULT, RHO_MAX_DEFAULT)]["dlnB"]) < 4.0, ev


def test_amplitude_prior_width_nearly_cancels():
    """Because both models carry two linear amplitudes per detector, sigma_A must almost cancel in the
    Bayes factor. Measured spread on real data was < 0.3 over a 33x range."""
    fits = _fits(1.0)
    ev, _ = evidence(fits, sigmas=(3e-21, 1e-20, 1e-19), rho_maxes=(RHO_MAX_DEFAULT,))
    vals = [ev[(s, RHO_MAX_DEFAULT)]["dlnB"] for s in (3e-21, 1e-20, 1e-19)]
    assert max(vals) - min(vals) < 2.0, vals


def test_rho_prior_volume_costs_about_log_area():
    """The only Occam cost of the overtone is the rho prior volume, so widening the disc must reduce
    dlnB by roughly ln(area ratio) -- a sanity check that the penalty is the prior, not a bug.

    The truth must lie INSIDE every disc tested: with |rho| = 2 injected, widening from R=1 to R=3
    both dilutes the prior AND newly captures the truth, and the two effects cancel (measured -0.56).
    Injected here at |rho| = 0.8, loud, so the rho posterior is contained and the cost is pure volume."""
    fits = []
    for _ in range(2):
        nz = _noise()
        i0 = len(nz) // 2
        fits.append(RingdownFit(_inject(nz, i0, 0.8, amp=3.0 * A_PEAK), FS, i0, NWIN, nz))
    ev, _ = evidence(fits, sigmas=(SIGMA_A_DEFAULT,), rho_maxes=(1.0, 3.0))
    drop = ev[(SIGMA_A_DEFAULT, 1.0)]["dlnB"] - ev[(SIGMA_A_DEFAULT, 3.0)]["dlnB"]
    assert 0.5 * math.log(9.0) < drop < 1.5 * math.log(9.0), drop


# ------------------------------------------------- feasibility & detection
def test_overtone_is_largely_collinear_with_the_220_basis():
    """The fact that governs everything: over a 40 ms window the 221 is ~76% absorbable by the 220
    basis even at a FIXED remnant, so only SNR_perp is available for detection."""
    nz = _noise()
    i0 = len(nz) // 2
    fit = RingdownFit(nz, FS, i0, NWIN, nz)
    s0, s1, sp = snr_perp(fit, MF_T, AF_T, A_PEAK, A_PEAK)
    assert sp < 0.7 * s1, (sp, s1)          # most of the overtone is mimicked by the 220
    assert sp > 0.05 * s1, (sp, s1)         # but not all of it


def test_a_loud_overtone_is_detected():
    fits = _fits(3.0)
    ev, _ = evidence(fits)
    assert ev[(SIGMA_A_DEFAULT, RHO_MAX_DEFAULT)]["dlnB"] > 5.0, ev


def test_pure_220_does_not_fake_an_overtone():
    """The correct null: a loud 220 with NO overtone must not produce two-mode preference."""
    fits = _fits(0.0)
    ev, _ = evidence(fits)
    assert ev[(SIGMA_A_DEFAULT, RHO_MAX_DEFAULT)]["dlnB"] < 4.0, ev


def test_a_genuine_overtone_DECAYS_with_start_time():
    """THE discriminator that decided E88. A real 221 fades with a ~2 ms e-folding, so its dlnB must
    collapse by a few M_f. The observed GW250114 preference does NOT decay this way, which is why it
    cannot be attributed to the overtone. Guards the shape test itself."""
    f0, t0 = qnm(MF_T, AF_T, "220")
    dl = []
    for shift_ms in (0.0, 3.0):
        fits = []
        for _ in range(2):
            nz = _noise()
            i0 = len(nz) // 2
            d = _inject(nz, i0, 3.0)
            fits.append(RingdownFit(d, FS, i0 + int(shift_ms * 1e-3 * FS), NWIN, nz))
        ev, _ = evidence(fits)
        dl.append(ev[(SIGMA_A_DEFAULT, RHO_MAX_DEFAULT)]["dlnB"])
    assert dl[0] - dl[1] > 2.0, dl          # must fall substantially once the 221 has decayed
