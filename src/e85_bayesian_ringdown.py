#!/usr/bin/env python3
"""E85 - Bayesian ringdown of GW250114: posterior on (f, tau) -> ringdown-only (Mf, af) vs the IMR remnant.
The Bayesian layer over the E83 pipeline (from-scratch: Goodman-Weare ensemble MCMC + a whitened-domain
Gaussian likelihood; the MODEL passes through the IDENTICAL whitening filter as the data). Single damped
sinusoid (the 220 mode), start time t_peak + dt with dt in {3, 5} ms (start-time robustness). The (f, tau)
posterior is mapped through the Berti-Cardoso-Will fits (E74) to a ringdown-ONLY (Mf_det, af) posterior and
compared to the inspiral-derived IMR remnant (NRSur7dq4: Mf_det=68.4 Msun, af=0.679) - the no-hair
consistency test done with our own machinery. CHARACTERIZATION (no prereg; a measurement with credible
intervals, not a locked decision). Seed 85."""
import os, sys, json, math
import numpy as np
from scipy.signal import welch, butter, filtfilt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from src.e83_strain_ringdown import bandpass
from src.e74_gw250114_deepdive import qnm, BCW

STRAIN = os.path.join(ROOT, "data/strain/H-H1_GW250114_4KHZ.hdf5")
FS = 4096.0
IMR = {"Mf_det": 68.4, "af": 0.679}

# ---------- sampler (Goodman-Weare affine-invariant ensemble, stretch move) ----------
def ensemble_sampler(logp, p0, nsteps, rng, a=2.0):
    nw, nd = p0.shape
    chain = np.empty((nsteps, nw, nd)); lp = np.array([logp(x) for x in p0]); p = p0.copy()
    for s in range(nsteps):
        for k in range(nw):
            j = rng.integers(nw - 1); j = j if j < k else j + 1
            z = ((a - 1) * rng.random() + 1) ** 2 / a
            prop = p[j] + z * (p[k] - p[j]); lpp = logp(prop)
            if math.log(rng.random() + 1e-300) < (nd - 1) * math.log(z) + lpp - lp[k]:
                p[k] = prop; lp[k] = lpp
        chain[s] = p
    return chain

# ---------- Kerr inversion: (f, tau) -> (Mf_det, af) via BCW (Q monotone in spin) ----------
def kerr_invert(f_hz, tau_s, mode="220"):
    c = BCW[mode]; Q = math.pi * f_hz * tau_s
    x = ((Q - c["q1"]) / c["q2"])          # = (1-j)^q3
    if x <= 0: return float("nan"), float("nan")
    j = 1.0 - x ** (1.0 / c["q3"])
    if not (0.0 <= j < 0.999): return float("nan"), float("nan")
    MomegaR = c["f1"] + c["f2"] * (1.0 - j) ** c["f3"]
    M_s = MomegaR / (2 * math.pi * f_hz)
    return M_s / 4.925490947e-6, j         # Msun (detector frame), dimensionless spin

# ---------- whitened-domain likelihood with EXACT same filter on the model ----------
class RingdownFit:
    """TRUNCATED time-domain likelihood (pyRing-style): the analysis window [i0, i0+nwin) is compared to
    the damped-sinusoid model under the noise AUTOCOVARIANCE (Toeplitz C from the empirical off-source
    ACF) -- no whitening filter is applied ACROSS the start-time boundary, so the loud merger just before
    the window cannot ring forward into it (the artifact that defeated the whiten-then-window approach:
    fake narrow modes at PSD-structure frequencies). Amplitude+phase are LINEAR (A cos, A sin basis) and
    marginalized analytically; the (f, tau) posterior is computed exactly on a grid."""
    def __init__(self, seg, fs, i0, nwin, hp_hz=25.0, noise_end_s=2.5):
        from scipy.linalg import toeplitz, cho_factor, cho_solve
        self._cho_solve = cho_solve
        self.fs = fs; self.nwin = nwin
        b, a = butter(4, hp_hz, btype="high", fs=fs)
        xhp = filtfilt(b, a, seg)
        self.d = xhp[i0: i0 + nwin].copy()
        noise = xhp[: int(noise_end_s * fs)]                      # off-source, far from the event
        acf = np.array([np.mean(noise[: len(noise) - k] * noise[k:]) for k in range(nwin)])
        acf *= np.linspace(1.0, 0.0, nwin) ** 2                   # taper for positive-definiteness
        C = toeplitz(acf); C[np.diag_indices_from(C)] += 1e-3 * acf[0]
        self.cho = cho_factor(C)
        self.sigma = math.sqrt(acf[0])
        self.tt = np.arange(nwin) / fs

    def _basis(self, f, tau):
        e = np.exp(-self.tt / tau)
        return np.vstack([e * np.cos(2 * math.pi * f * self.tt),
                          e * np.sin(2 * math.pi * f * self.tt)])

    def model(self, f, tau, A, phi):
        B = self._basis(f, tau)
        return A * (math.cos(phi) * B[0] - math.sin(phi) * B[1])

    def marginal_lnL(self, f, tau):
        """amplitude/phase analytically marginalized (flat prior): 0.5 b^T G^-1 b - 0.5 ln det G,
        with inner products under the truncated noise covariance."""
        B = self._basis(f, tau)
        CiB = np.column_stack([self._cho_solve(self.cho, B[0]), self._cho_solve(self.cho, B[1])])
        G = B @ CiB; b = self.d @ CiB
        try:
            Gi = np.linalg.inv(G)
        except np.linalg.LinAlgError:
            return -np.inf
        det = np.linalg.det(G)
        if det <= 0: return -np.inf
        return 0.5 * float(b @ Gi @ b) - 0.5 * math.log(det)

def grid_fit(seg, fs, ipk_in_seg, dt_ms, rng,
             f_grid=np.arange(160, 341, 1.5), tau_grid_ms=np.arange(1.0, 15.1, 0.4)):
    """exact (f, tau) posterior on a grid via analytic linear-amplitude marginalization."""
    i0 = ipk_in_seg + int(dt_ms * 1e-3 * fs)
    fit = RingdownFit(seg, fs, i0, nwin=int(0.040 * fs))
    lnL = np.array([[fit.marginal_lnL(f, tm * 1e-3) for tm in tau_grid_ms] for f in f_grid])
    W = np.exp(lnL - lnL.max()); W /= W.sum()
    idx = rng.choice(W.size, size=4000, p=W.ravel())
    fi, ti = np.unravel_index(idx, W.shape)
    df = f_grid[1] - f_grid[0]; dt = tau_grid_ms[1] - tau_grid_ms[0]
    post = np.column_stack([f_grid[fi] + rng.uniform(-df / 2, df / 2, len(fi)),
                            tau_grid_ms[ti] + rng.uniform(-dt / 2, dt / 2, len(ti))])
    return post, fit.sigma, float(lnL.max())

def ci(v, lo=5, hi=95):
    return [float(np.percentile(v, lo)), float(np.median(v)), float(np.percentile(v, hi))]

def main():
    import h5py
    rng = np.random.default_rng(85)
    with h5py.File(STRAIN, "r") as h:
        strain = np.asarray(h["strain/Strain"]); gps0 = h["meta/GPSstart"][()]
    im = int((1420878141.22 - gps0) * FS)
    fpsd, Pxx = welch(strain[im - 40 * int(FS): im - 8 * int(FS)], fs=FS, nperseg=int(4 * FS))
    seg = strain[im - 4 * int(FS): im + 4 * int(FS)].copy()
    # locate peak with the E83 conditioning
    from src.e83_strain_ringdown import whiten as wtn
    wb = bandpass(wtn(seg, FS, fpsd, Pxx), FS, 30, 400)
    t = (np.arange(len(seg)) - len(seg) // 2) / FS
    ipk = int(np.argmax(np.abs(wb) * (np.abs(t) < 0.1)))

    kerr_f, kerr_tau = qnm(IMR["Mf_det"], IMR["af"], "220")
    out = {"event": "GW250114_082203", "imr_remnant": IMR,
           "kerr_prediction_from_imr": {"f220_Hz": kerr_f, "tau220_ms": kerr_tau * 1e3}, "fits": {}}
    print(f"E85 Bayesian ringdown (GW250114 H1); IMR-Kerr prediction f={kerr_f:.1f} Hz tau={kerr_tau*1e3:.2f} ms")
    for dt in (3.0, 5.0):
        post, sigma, lnmax = grid_fit(seg, FS, ipk, dt, rng)
        f_ci, tau_ci = ci(post[:, 0]), ci(post[:, 1])
        rem = np.array([kerr_invert(f, tau * 1e-3) for f, tau in post[:, :2]])
        ok = np.isfinite(rem[:, 0])
        mf_ci, af_ci = ci(rem[ok, 0]), ci(rem[ok, 1])
        cons_f = f_ci[0] <= kerr_f <= f_ci[2]; cons_m = mf_ci[0] <= IMR["Mf_det"] <= mf_ci[2]
        out["fits"][f"dt_{dt:.0f}ms"] = {"f220_Hz_5_50_95": f_ci, "tau220_ms_5_50_95": tau_ci,
                                          "Mf_det_5_50_95": mf_ci, "af_5_50_95": af_ci,
                                          "frac_kerr_valid": float(ok.mean()),
                                          "imr_within_90": bool(cons_f and cons_m)}
        print(f"  dt={dt:.0f}ms: f220 = {f_ci[1]:.1f} [{f_ci[0]:.1f},{f_ci[2]:.1f}] Hz | "
              f"tau = {tau_ci[1]:.1f} [{tau_ci[0]:.1f},{tau_ci[2]:.1f}] ms")
        print(f"           ringdown-only remnant: Mf_det = {mf_ci[1]:.1f} [{mf_ci[0]:.1f},{mf_ci[2]:.1f}] Msun, "
              f"af = {af_ci[1]:.2f} [{af_ci[0]:.2f},{af_ci[2]:.2f}]  (IMR: 68.4, 0.679)")
        print(f"           IMR remnant inside 90% CI: {cons_f and cons_m} (Kerr-valid fraction {ok.mean()*100:.0f}%)")

    json.dump(out, open(os.path.join(ROOT, "results/e85_bayesian_ringdown_results.json"), "w"), indent=2)
    print("\nwrote results/e85_bayesian_ringdown_results.json")

if __name__ == "__main__":
    main()
