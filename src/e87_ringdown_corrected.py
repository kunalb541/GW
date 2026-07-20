#!/usr/bin/env python3
"""E87 - the E85 ringdown was PRIOR-DOMINATED: two covariance bugs, 33x of lost sensitivity, and the
corrected measurement of the GW250114 220 mode.

E85 reported f220 = 253.9 [167, 333] Hz and called it "honestly wide" while noting the IMR remnant sat
inside the interval. That reading was wrong in a way width alone cannot expose: the interval WAS the
prior. Two defects in the truncated-likelihood covariance destroyed ~33x in matched-filter SNR --

  (1) `acf *= np.linspace(1, 0, nwin)**2`  -- an ACF taper applied to force positive-definiteness. It
      crushes the off-diagonal correlations while preserving acf[0], driving C toward sigma^2*I with
      sigma = the BROADBAND rms of 25-Hz-high-passed strain (dominated by 25-60 Hz seismic power). A
      matched filter at 250 Hz is then charged the broadband noise instead of the in-band noise. Cost: 8x.
  (2) `C[diag] += 1e-3 * acf[0]`           -- a ridge of 1e-3 x the BROADBAND variance is itself a white
      noise floor far above the true in-band noise at 250 Hz. Cost: a further ~3.5x.

Both are replaced by the textbook construction: the noise ACF is the Wiener-Khinchin transform of a Welch
PSD, which is positive-definite BY CONSTRUCTION (nonnegative spectrum), needs no taper, and preserves the
noise colour exactly. The ridge drops to 1e-6 (converged; see the scan in the report).

CAUTION, learned here: the one-sided Welch PSD must be halved before the inverse FFT
(`irfft(psd*fs/2)`), or the covariance comes out exactly 2x too large -- which tempers the likelihood and
inflates every credible interval by sqrt(2) without moving the peak. Guarded by a contract test.

CHARACTERIZATION (no prereg; a correction + measurement, not a locked decision). Supersedes E85's
numbers; E85's machinery (analytic amplitude/phase marginalization, Kerr inversion, the truncation that
defeats acausal whitening leakage) is retained and reused. Seed 87."""
import os, sys, json, math
import numpy as np
from scipy.signal import butter, filtfilt, welch, sosfiltfilt
from scipy.linalg import toeplitz, cho_factor, cho_solve

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from src.e85_bayesian_ringdown import kerr_invert, IMR      # both correct in E85; reused unchanged

FS = 4096.0
GPS_GW250114 = 1420878141.22
NWIN = int(0.040 * FS)                                       # 40 ms analysis window
F_GRID = np.arange(160.0, 341.0, 1.5)
TAU_GRID_MS = np.arange(1.0, 15.1, 0.4)
DETECTORS = {"H1": "data/strain/H-H1_GW250114_4KHZ.hdf5",
             "L1": "data/strain/L-L1_GW250114_4KHZ.hdf5"}
# LVK's own pyRing Kerr_220 posteriors (Zenodo 17018009) are the comparison standard -- read from the
# release rather than quoted, so no remembered number can slip in unverified.
TGR_TARBALL = os.path.join(ROOT, "data/lvk_tgr/TGR_companion_S250114ax_results.tar.gz")


def acf_from_psd(noise, fs, nwin, hp_hz=25.0, nper_s=0.5):
    """Noise autocovariance via Wiener-Khinchin from a Welch PSD. PD by construction (nonnegative
    spectrum) -- so NO taper is needed, and the noise colour survives intact. The one-sided PSD is
    halved before the inverse FFT; omitting that /2 makes the covariance exactly 2x too large."""
    b, a = butter(4, hp_hz, btype="high", fs=fs)
    nz = filtfilt(b, a, noise)
    nper = int(nper_s * fs)
    fw, Pw = welch(nz, fs=fs, nperseg=nper, noverlap=nper // 2)
    psd = np.interp(np.fft.rfftfreq(nper, 1 / fs), fw, Pw)
    return np.fft.irfft(psd * fs / 2.0)[:nwin]


class RingdownFit:
    """Truncated time-domain likelihood for a single damped sinusoid. Amplitude and phase are linear
    (A cos, A sin basis) and marginalized analytically; (f, tau) is evaluated exactly on a grid. The
    window is compared to the model under the full colored noise covariance -- no whitening filter
    crosses the start-time boundary, so the merger cannot ring forward into the window."""

    def __init__(self, seg, fs, i0, nwin, noise, hp_hz=25.0, ridge=1e-6):
        b, a = butter(4, hp_hz, btype="high", fs=fs)
        self.d = filtfilt(b, a, seg)[i0:i0 + nwin].copy()
        acf = acf_from_psd(noise, fs, nwin, hp_hz=hp_hz)
        C = toeplitz(acf)
        C[np.diag_indices_from(C)] += ridge * acf[0]
        self.cho = cho_factor(C)
        self.nwin = nwin
        self.tt = np.arange(nwin) / fs
        self.lnL0 = -0.5 * self.d @ cho_solve(self.cho, self.d)     # zero-signal reference

    def marginal_lnL(self, f, tau):
        e = np.exp(-self.tt / tau)
        M = np.column_stack([e * np.cos(2 * math.pi * f * self.tt),
                             e * np.sin(2 * math.pi * f * self.tt)])
        G = M.T @ cho_solve(self.cho, M)
        bvec = M.T @ cho_solve(self.cho, self.d)
        _, ld = np.linalg.slogdet(G)
        return 0.5 * bvec @ np.linalg.solve(G, bvec) - 0.5 * ld


def surface(fit, f_grid=F_GRID, tau_grid_ms=TAU_GRID_MS):
    return np.array([[fit.marginal_lnL(f, t * 1e-3) for t in tau_grid_ms] for f in f_grid])


def summarize(lnL, f_grid=F_GRID, tau_grid_ms=TAU_GRID_MS):
    P = np.exp(lnL - lnL.max())
    P /= P.sum()
    cdf = np.cumsum(P.sum(axis=1))
    lo, med, hi = np.interp([0.05, 0.5, 0.95], cdf, f_grid)
    return dict(f_med=float(med), f_lo=float(lo), f_hi=float(hi), width=float(hi - lo),
                f_peak=float(f_grid[int(np.argmax(lnL.max(axis=1)))]),
                tau_peak_ms=float(tau_grid_ms[int(np.argmax(lnL.max(axis=0)))]),
                lnL_range=float(lnL.max() - lnL.min()))


def find_peak(seg, fs, band=(100.0, 400.0), search_s=0.05):
    """Locate the merger peak by bandpassed envelope, centred on the middle of the segment."""
    sos = butter(4, list(band), btype="band", fs=fs, output="sos")
    bp = sosfiltfilt(sos, seg)
    c = len(bp) // 2
    w = int(search_s * fs)
    return int(np.argmax(np.abs(bp[c - w:c + w]))) + c - w


def load_detector(path, gps=GPS_GW250114, fs=FS, pre_s=4.0, noise_lo_s=40.0, noise_hi_s=8.0):
    import h5py
    with h5py.File(path, "r") as h:
        st = np.asarray(h["strain/Strain"])
        gps0 = h["meta/GPSstart"][()]
    im = int((gps - gps0) * fs)
    seg = st[im - int(pre_s * fs): im + int(pre_s * fs)].copy()
    noise = st[im - int(noise_lo_s * fs): im - int(noise_hi_s * fs)].copy()
    return seg, noise


def lvk_pyring_220_scan(tarball=TGR_TARBALL):
    """LVK's OWN pyRing Kerr_220 start-time scan, mapped through the SAME BCW relation this pipeline
    uses. pyRing samples (Mf, af), not (f, tau), so the comparison is made in f220."""
    import tarfile, re
    from src.e74_gw250114_deepdive import qnm
    t = tarfile.open(tarball)
    runs = {}
    for n in t.getnames():
        m = re.search(r"Kerr_220_(\d+)M_weighted_posterior/Nested_sampler/posterior\.dat$", n)
        if m:
            runs[int(m.group(1))] = n
    out = {}
    for M, n in sorted(runs.items()):
        lines = t.extractfile(n).read().decode().strip().split("\n")
        hdr = lines[0].lstrip("#").split()
        arr = np.array([[float(x) for x in l.split()] for l in lines[1:]])
        f220 = np.array([qnm(a, b, "220")[0]
                         for a, b in zip(arr[:, hdr.index("Mf")], arr[:, hdr.index("af")])])
        lo, med, hi = np.percentile(f220, [5, 50, 95])
        out[M] = dict(n=int(len(f220)), f_med=float(med), f_lo=float(lo), f_hi=float(hi),
                      width=float(hi - lo), Mf=float(np.median(arr[:, hdr.index("Mf")])),
                      af=float(np.median(arr[:, hdr.index("af")])))
    return out


def network_lnL(pre, dt_ms):
    """Sum per-detector marginal lnL surfaces. Valid because each detector carries its OWN free
    amplitude and phase, so the analytic marginalization factorizes across detectors."""
    net = None
    for det in DETECTORS:
        seg, noise, ipk = pre[det]
        L = surface(RingdownFit(seg, FS, ipk + int(round(dt_ms * 1e-3 * FS)), NWIN, noise))
        net = L if net is None else net + L
    return net


def main():
    t_M_ms = IMR["Mf_det"] * 4.925490947e-6 * 1e3       # remnant light-crossing time, ms
    pre = {}
    for det, rel in DETECTORS.items():
        seg, noise = load_detector(os.path.join(ROOT, rel))
        pre[det] = (seg, noise, find_peak(seg, FS))

    out = {"t_Mf_ms": t_M_ms, "imr_remnant": IMR, "detectors": {}, "start_time_scan": {},
           "lvk_comparison": {}}

    for dt_ms in (3.0, 5.0):                            # per-detector reference points
        for det in DETECTORS:
            seg, noise, ipk = pre[det]
            out["detectors"][f"{det}_dt{dt_ms}ms"] = summarize(
                surface(RingdownFit(seg, FS, ipk + int(dt_ms * 1e-3 * FS), NWIN, noise)))

    lvk = lvk_pyring_220_scan() if os.path.exists(TGR_TARBALL) else {}
    offs = []
    for M in (0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20):
        s = summarize(network_lnL(pre, M * t_M_ms))
        Mf, af = kerr_invert(s["f_med"], s["tau_peak_ms"] * 1e-3)
        s["kerr_Mf_det"], s["kerr_af"] = float(Mf), float(af)
        out["start_time_scan"][f"{M}M"] = s
        if M in lvk:
            v = lvk[M]
            d = s["f_med"] - v["f_med"]
            out["lvk_comparison"][f"{M}M"] = {
                "ours": {k: s[k] for k in ("f_med", "f_lo", "f_hi", "width")}, "lvk": v,
                "delta_median_hz": float(d),
                "lvk_median_in_our_90ci": bool(s["f_lo"] < v["f_med"] < s["f_hi"])}
            if 2 <= M <= 18:
                offs.append(abs(d))
    if offs:
        out["validation"] = {
            "median_abs_offset_hz_2M_to_18M": float(np.median(offs)),
            "max_abs_offset_hz_2M_to_18M": float(np.max(offs)),
            "n_start_times_with_lvk_median_inside_our_90ci":
                int(sum(v["lvk_median_in_our_90ci"] for v in out["lvk_comparison"].values())),
            "n_start_times_compared": int(len(out["lvk_comparison"]))}
    path = os.path.join(ROOT, "results/e87_ringdown_corrected_results.json")
    json.dump(out, open(path, "w"), indent=1)
    print(json.dumps(out.get("validation", {}), indent=1))
    print("wrote", path)


if __name__ == "__main__":
    main()
