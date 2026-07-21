#!/usr/bin/env python3
"""E100 - frames, coordinates and the elongation gate, as a machine-readable artifact.

Every other number in the manuscript regenerates from a committed JSON. These did not. The
frame/coordinate comparison (source vs detector vs log-mass), the paired significance, the median axis
ratios that mediate the frame effect, the matched-axis-ratio control, and the elongation-band
degradation table lived ONLY in docs/GATE_C_FIRST_MEASUREMENT.md as prose. That is the same
prose-only failure mode that made the original gate notes non-reproducible, and the doc had already
drifted: it reports 79 events / 1.04 deg / 0.32 deg, while the cache gives 81 / 1.03 / 0.31.

This battery recomputes all of it from the E94 cache and writes results/e100_frames_and_bands_results.json,
so paper/numbers.tex can source it and the drift cannot recur.

Three coordinate systems, one construction:

  source (m1,m2)      -- the LOCKED PRIMARY score. Everything else here is post-hoc.
  detector (m1,m2)    -- same events, redshift uncertainty removed
  log source          -- (log m1, log m2), a nonlinear reparameterization

The angle is a Euclidean PCA angle in whichever coordinates it is computed in, so it is NOT
reparameterization-invariant and the three answers are expected to differ. That is the point: we
report the dependence rather than assume it away. The curve is mapped through the same coordinate
transform as the data before its angle is taken, so each row is an internally consistent comparison.

The matched-axis-ratio control is what stops "the detector frame is better" being asserted: the
detector frame is also markedly MORE ELONGATED, and orientation is better defined when elongation is
high. Comparing the frames within shared axis-ratio bands separates the two explanations.

Seed 100. Reads the cache only; no HDF5.
"""
import json, os, sys
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from src.e94_build_posterior_cache import load, CACHE
from src.e95_gate_regeneration import primary_rows, AXR_MIN
from src.e71_gwtc5_curved_law import psi_axr_rho, curve_psi
from src.e65_pn_fisher_rotation import adiff, ang_of

SEED = 100
BANDS = ((1.0, 1.5), (1.5, 2.0), (2.0, 3.0), (3.0, 5.0), (5.0, 1e9))
MATCHED = ((3.0, 5.0), (5.0, 10.0), (10.0, 1e9))
THRESHOLDS = (1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0)
RESULT_JSON = os.path.join(ROOT, "results/e100_frames_and_bands_results.json")


def curve_psi_log(mc, qs):
    """Curve orientation in (log m1, log m2). The curve is transformed, then its angle taken -- the
    angle of the transformed curve is NOT the transform of the angle."""
    qs = np.clip(qs[np.isfinite(qs)], 0.02, 1.0)
    m1 = mc * (1 + qs) ** 0.2 * qs ** -0.6
    P = np.column_stack([np.log(m1), np.log(qs * m1)])
    P = P - P.mean(0)
    _, V = np.linalg.eigh(P.T @ P / len(P))
    return ang_of(V[:, 1])


def wilcoxon_p(a, b):
    from scipy.stats import wilcoxon
    d = np.asarray(a) - np.asarray(b)
    d = d[d != 0]
    if len(d) < 6:
        return float("nan")
    return float(wilcoxon(d).pvalue)


def main():
    rec = load()
    prim, _ = primary_rows(rec)

    rows = []
    for (cat, ev), v in sorted(prim.items()):
        d = v["raw"]
        q = d["q"].astype(float)
        m1s, m2s = d["m1s"].astype(float), d["m2s"].astype(float)
        ps, axs, _ = psi_axr_rho(m1s, m2s)
        r = dict(cat=cat, event=ev, axr_source=float(axs),
                 err_source=float(abs(adiff(curve_psi(float(np.median(d["mcs"])), q), ps))))
        pl, axl, _ = psi_axr_rho(np.log(m1s), np.log(m2s))
        r["axr_log"] = float(axl)
        r["err_log"] = float(abs(adiff(curve_psi_log(float(np.median(d["mcs"])), q), pl)))
        if "m1d" in d:
            m1d, m2d = d["m1d"].astype(float), d["m2d"].astype(float)
            pdet, axd, _ = psi_axr_rho(m1d, m2d)
            r["axr_det"] = float(axd)
            r["err_det"] = float(abs(adiff(curve_psi(float(np.median(d["mcd"])), q), pdet)))
        rows.append(r)

    el = [r for r in rows if r["axr_source"] >= AXR_MIN]
    paired = [r for r in el if "err_det" in r]
    med = lambda xs: float(np.median(xs)) if len(xs) else None

    frames = {
        "source_m1_m2": {"n_elong": len(el), "median_err_deg": med([r["err_source"] for r in el]),
                         "median_axr": med([r["axr_source"] for r in el]),
                         "role": "LOCKED PRIMARY -- all other rows are post-hoc"},
        "detector_m1_m2": {"n_elong": len(paired), "median_err_deg": med([r["err_det"] for r in paired]),
                           "median_axr": med([r["axr_det"] for r in paired]), "role": "post-hoc"},
        "log_source_m1_m2": {"n_elong": len(el), "median_err_deg": med([r["err_log"] for r in el]),
                             "median_axr": med([r["axr_log"] for r in el]), "role": "post-hoc"}}

    frames["detector_vs_source_paired"] = {
        "n_paired": len(paired),
        "median_source_deg": med([r["err_source"] for r in paired]),
        "median_detector_deg": med([r["err_det"] for r in paired]),
        "wilcoxon_p": wilcoxon_p([r["err_source"] for r in paired], [r["err_det"] for r in paired]),
        "median_axr_source": med([r["axr_source"] for r in paired]),
        "median_axr_detector": med([r["axr_det"] for r in paired])}

    # Matched-axis-ratio control: within shared bands, does the detector frame still win?
    matched = {}
    for lo, hi in MATCHED:
        s = [r["err_source"] for r in paired if lo <= r["axr_source"] < hi]
        t = [r["err_det"] for r in paired if lo <= r["axr_det"] < hi]
        key = f"{lo:g}-{hi:g}" if hi < 1e8 else f"{lo:g}+"
        matched[key] = {"n_source": len(s), "n_detector": len(t),
                        "median_source_deg": med(s), "median_detector_deg": med(t),
                        "detector_better": (None if not s or not t else bool(med(t) < med(s)))}

    bands = {}
    for lo, hi in BANDS:
        sel = [r for r in rows if lo <= r["axr_source"] < hi]
        key = f"{lo:g}-{hi:g}" if hi < 1e8 else f"{lo:g}+"
        bands[key] = {"n": len(sel), "median_err_deg": med([r["err_source"] for r in sel])}

    thr = {}
    for t in THRESHOLDS:
        sel = [r for r in rows if r["axr_source"] >= t]
        thr[f"{t:g}"] = {"n": len(sel), "median_err_deg": med([r["err_source"] for r in sel])}
    vals = [thr[f"{t:g}"]["median_err_deg"] for t in THRESHOLDS]
    monotone = bool(all(vals[i] >= vals[i + 1] - 1e-12 for i in range(len(vals) - 1)))

    # Chirp-vs-total win fraction, per catalog, over ALL events. Table 1 previously quoted 81% for the
    # training catalog with no artifact behind it; that value equals E65's median_err_curve_elong of
    # 0.806, so it looks like a transcribed degree value, not a fraction. Computed here for all three
    # catalogs by one rule so the row is internally consistent.
    win = {}
    for cat in ("GWTC-3", "O4a", "O4b"):
        w = []
        for (c, ev), v in prim.items():
            if c != cat:
                continue
            d = v["raw"]
            ec = abs(adiff(curve_psi(float(np.median(d["mcs"])), d["q"].astype(float)), v["psi"]))
            w.append(bool(ec < abs(adiff(135.0, v["psi"]))))    # 135 deg = constant-total-mass line
        if w:
            win[cat] = {"n": len(w), "win_fraction": float(np.mean(w))}

    # Arc length vs tangent error. The manuscript quoted (+0.26, +0.02, +0.12) for this, which matched
    # no artifact and did not match its own source note (+0.260, -0.018, -0.416). Measured here.
    # Arc length = length along the constant-Mc curve between the 5th and 95th percentiles of q,
    # normalised by the posterior's own scale so events of different mass are comparable.
    from scipy.stats import spearmanr
    arc = {}
    for cat in ("GWTC-3", "O4a", "O4b"):
        L, E = [], []
        for (c, ev), v in prim.items():
            if c != cat or v["axr"] < AXR_MIN:
                continue
            q = v["q"]
            qq = np.linspace(np.percentile(q, 5), np.percentile(q, 95), 200)
            m1 = v["mc"] * (1 + qq) ** 0.2 * qq ** -0.6
            m2 = qq * m1
            length = float(np.sum(np.hypot(np.diff(m1), np.diff(m2))))
            scale = float(np.hypot(np.std(v["raw"]["m1s"].astype(float)),
                                   np.std(v["raw"]["m2s"].astype(float))))
            L.append(length / max(scale, 1e-9))
            E.append(float(abs(adiff(np.float64(v["psi"]),
                                     np.float64(__import__("src.e71_gwtc5_curved_law", fromlist=["x"])
                                                .tangent_angles(v["m1m"], v["m2m"])[0])))))
        if len(L) >= 5:
            r, p = spearmanr(L, E)
            arc[cat] = {"n": len(L), "spearman_arc_vs_tangent_err": float(r), "p": float(p)}

    out = {"battery": "E100 frames, coordinates and the elongation gate", "seed": SEED,
           "chirp_vs_total_win": win, "arc_length_vs_tangent_error": arc,
           "provenance": {"cache": os.path.relpath(CACHE, ROOT), "hdf5_accessed": False,
                          "supersedes": ("docs/GATE_C_FIRST_MEASUREMENT.md, which carried these numbers "
                                         "as prose only and had drifted (79 events / 1.04 / 0.32 there)")},
           "n_events": len(rows), "axr_min": AXR_MIN,
           "frames": frames, "matched_axis_ratio": matched,
           "axr_bands": bands, "threshold_sweep": thr,
           "threshold_monotone": monotone,
           "random_baseline_deg": 45.0,
           "interpretation": (
               "The angle is coordinate-dependent by construction and the three frames disagree; we "
               "report that rather than claiming invariance. The detector frame scores better AND is "
               "markedly more elongated, and elongation is what makes orientation well defined, so the "
               "matched-axis-ratio rows are the discriminant -- the detector frame is not uniformly "
               "better within matched bands. Nothing distinguishes the locked threshold of 3: the error "
               "falls smoothly and monotonically across the sweep, and degrades toward (but never "
               "reaches) the mod-180 random baseline of 45 deg as posteriors become round.")}
    json.dump(out, open(RESULT_JSON, "w"), indent=1)

    f = out["frames"]
    for k in ("source_m1_m2", "detector_m1_m2", "log_source_m1_m2"):
        v = f[k]
        print(f"{k:>20}: n={v['n_elong']:3d}  err {v['median_err_deg']:.2f} deg  axr {v['median_axr']:.1f}")
    p = f["detector_vs_source_paired"]
    print(f"\npaired n={p['n_paired']}: source {p['median_source_deg']:.2f} vs detector "
          f"{p['median_detector_deg']:.2f}, wilcoxon p={p['wilcoxon_p']:.2e}"
          f"  | axr {p['median_axr_source']:.1f} -> {p['median_axr_detector']:.1f}")
    print("\nmatched axis ratio:")
    for k, v in matched.items():
        print(f"  {k:>7}: source {v['median_source_deg']} (n={v['n_source']})  "
              f"detector {v['median_detector_deg']} (n={v['n_detector']})  det better={v['detector_better']}")
    print("\naxr bands:", {k: round(v["median_err_deg"], 2) for k, v in bands.items() if v["median_err_deg"]})
    print("threshold monotone:", monotone)
    print("wrote", RESULT_JSON)


if __name__ == "__main__":
    main()
