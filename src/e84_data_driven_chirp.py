#!/usr/bin/env python3
"""E84 - data-driven chirp mass from strain + the band-resolved feasibility boundary.
CHARACTERIZATION (no prereg; one measurement + one negative result, both honest).
(1) MEASUREMENT: the textbook 0PN law f^(-8/3)(t) = K (tc - t), K = (256/5) pi^(8/3) (G Mc_det/c^3)^(5/3),
    fitted to the spectrogram RIDGE of GW250114's whitened H1 strain -> a template-free, phase-evolution
    chirp mass to compare against the PE value.
(2) NEGATIVE RESULT: the band-resolved version (Mc per frequency band - the E84 'frequency geometry'
    observable) is INFEASIBLE with ridge methods: heavy events sweep the upper bands faster than any
    STFT window (GW250114: 64->200 Hz in <25 ms), light events are too faint per-slice. Exactly the
    E73 anatomy-compression prediction. The real version needs band-limited Bayesian PE (a major build).
Seed 84. Data: data/strain/ (gitignored). Reuses E83's whiten/bandpass."""
import os, sys, json, math
import numpy as np
from scipy.signal import welch, stft

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from src.e83_strain_ringdown import whiten, bandpass

STRAIN = os.path.join(ROOT, "data/strain/H-H1_GW250114_4KHZ.hdf5")
FS = 4096.0
MSUN = 4.925490947e-6
PE_MC_DET = 31.1          # PE: Mc_src ~ 28.7 (m1=33.8, m2=32.2), z ~ 0.086

def mc_from_slope(s):
    """invert K = (256/5) pi^(8/3) (G Mc/c^3)^(5/3): slope of f^(-8/3) vs (tc - t)."""
    return (5 * s / 256) ** (3 / 5) / math.pi ** (8 / 5) / MSUN if s > 0 else float("nan")

def ridge_points(x, fs, t_rel_peak, fmin=32, fmax=200, nperseg=256, contrast=8.0):
    """spectrogram ridge: per-slice peak frequency where peak/median power contrast is high."""
    ff, tt, Z = stft(x, fs=fs, nperseg=nperseg, noverlap=nperseg - 16, boundary=None)
    P = np.abs(Z) ** 2
    band = (ff >= fmin) & (ff <= fmax); ff = ff[band]; P = P[band]
    rf = ff[np.argmax(P, axis=0)]
    good = (P.max(axis=0) / np.median(P, axis=0) > contrast)
    tc = tt + t_rel_peak            # scipy stft times are already window centers (verified)
    return tc[good], rf[good]

def fit_mc(tt, rf, flo, fhi):
    m = (rf >= flo) & (rf < fhi)
    if m.sum() < 4: return float("nan"), int(m.sum())
    s, _ = np.linalg.lstsq(np.vstack([tt[m], np.ones(m.sum())]).T, rf[m] ** (-8 / 3), rcond=None)[0]
    return mc_from_slope(-s), int(m.sum())

def synth_chirp(mc_det_msun, fs, f0=32.0, tend=-0.006, seed=84):
    """physical synthetic 0PN chirp (amplitude ~ f^(2/3)) + mild noise, for bias calibration."""
    rng = np.random.default_rng(seed)
    K = (256 / 5) * math.pi ** (8 / 3) * (mc_det_msun * MSUN) ** (5 / 3)
    t = np.arange(-(f0 ** (-8 / 3)) / K, tend, 1 / fs)
    f = (K * (-t)) ** (-3 / 8)
    x = (f / f0) ** (2 / 3) * np.cos(2 * math.pi * np.cumsum(f) / fs)
    return t, x + 0.05 * rng.normal(size=len(x))

def injection_bias(fs=FS):
    """measured multiplicative bias of the ridge estimator on synthetics (the honesty table)."""
    out = {}
    for mc in (10.0, 15.0, 30.0):
        t, x = synth_chirp(mc, fs)
        tt, rf = ridge_points(x, fs, t[0], contrast=4.0)
        pre = tt < -0.010
        rec, _ = fit_mc(tt[pre], rf[pre], 32, 200)
        out[f"{mc:.0f}"] = round(rec / mc, 3)
    return out

def main():
    import h5py
    with h5py.File(STRAIN, "r") as h:
        strain = np.asarray(h["strain/Strain"]); gps0 = h["meta/GPSstart"][()]
    im = int((1420878141.22 - gps0) * FS)
    fpsd, Pxx = welch(strain[im - 40 * int(FS): im - 8 * int(FS)], fs=FS, nperseg=int(4 * FS))
    seg = strain[im - 4 * int(FS): im + 4 * int(FS)].copy(); N = len(seg)
    wb = bandpass(whiten(seg, FS, fpsd, Pxx), FS, 25, 350)
    t = (np.arange(N) - N // 2) / FS
    ipk = int(np.argmax(np.abs(wb) * (np.abs(t) < 0.1)))

    a = ipk - int(0.25 * FS); b = ipk + int(0.01 * FS)
    tt, rf = ridge_points(wb[a:b], FS, (a - ipk) / FS)
    pre = tt < -0.010; tt, rf = tt[pre], rf[pre]

    mc_all, n_all = fit_mc(tt, rf, 32, 200)
    frac = (mc_all - PE_MC_DET) / PE_MC_DET
    bands = {}
    for flo, fhi in [(32, 64), (64, 110), (110, 200)]:
        mc, n = fit_mc(tt, rf, flo, fhi)
        bands[f"{flo}-{fhi}Hz"] = {"mc": None if mc != mc else round(mc, 1), "n_ridge_points": n}
    bias = injection_bias()

    print(f"E84 data-driven chirp mass (GW250114, H1 ridge, {len(rf)} points)")
    print(f"  full-track fit: Mc_det = {mc_all:.1f} Msun  (PE {PE_MC_DET}) -> {frac*100:+.0f}% raw")
    print(f"  ESTIMATOR BIAS (injections, recovered/true): {bias} -> +15-30%, growing with Mc")
    print(f"  -> the raw few-% agreement is PARTLY FORTUITOUS; honest claim: BALLPARK consistent "
          f"(~20-30% template-free systematic), NOT precision.")
    print(f"  band-resolved attempt: {bands}")
    print(f"  -> upper bands starved of ridge points (GW250114 sweeps 64->200 Hz in <25 ms, faster than")
    print(f"     any STFT window) - the E73 anatomy-compression prediction observed in data. Band-resolved")
    print(f"     frequency geometry needs band-limited Bayesian PE (major build), not a ridge.")

    json.dump({"battery": "E84 data-driven chirp + band-resolved feasibility (characterization)",
               "event": "GW250114_082203",
               "mc_det_strain_ridge_raw": mc_all, "mc_det_pe": PE_MC_DET, "frac_diff_raw": frac,
               "estimator_bias_injections_recovered_over_true": bias,
               "honest_claim": "ballpark-consistent template-free chirp mass (~20-30% systematic from "
                               "frequency quantization + window smearing in an accelerating sweep); the "
                               "raw -3..+6% agreement is partly fortuitous and NOT precision",
               "n_ridge_points": int(len(rf)), "band_resolved_attempt": bands,
               "negative_result": "band-resolved Mc infeasible via ridge: heavy events sweep upper bands "
                                  "faster than STFT resolution (<25 ms for 64-200 Hz); light events too "
                                  "faint per-slice. Matches E73's anatomy compression. Real version needs "
                                  "band-limited Bayesian PE.",
               "pipeline_strands": ["E83 ringdown 241 Hz vs Kerr 248.9 (3.2%)",
                                     "E84 chirp-phase Mc ~ballpark (bias-characterized)"]},
              open(os.path.join(ROOT, "results/e84_data_driven_chirp_results.json"), "w"), indent=2)
    print("\nwrote results/e84_data_driven_chirp_results.json")

if __name__ == "__main__":
    main()
