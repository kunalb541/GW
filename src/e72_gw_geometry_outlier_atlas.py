#!/usr/bin/env python3
"""E72 - GW geometry outlier atlas: where (if anywhere) does the chirp-curve law break?
Prereg E72 (locked 0d1cebf, BEFORE any residual-axis correlation). Sample: the 32 elongated O4b
events (axr>=3) from the LOCKED E71 results. Residual r = err_curve. Correlate r against 9 pre-declared
axes with BH-FDR + partial-Spearman(controlling axr); Tukey outlier fence; E59 coherence lens on flags.
Anomaly atlas, NOT a new-physics claim. Seed 72 (no RNG in main path)."""
import os, sys, json, math
import numpy as np
import h5py

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from src.e65_pn_fisher_rotation import ang_of, adiff
from src.e71_gwtc5_curved_law import psi_axr_rho

GW5 = os.path.join(ROOT, "data/chains/gwtc5")
E71 = os.path.join(ROOT, "results/e71_gwtc5_curved_law_results.json")
AXES = ["chi_p", "abs_chi_eff", "mass_ratio", "redshift", "loudness_snr",
        "chirp_mass_source", "total_mass_source", "mass_2_source", "waveform_disagreement"]

# ---------- stats helpers (independent, pre-declared) ----------
def spearman(x, y):
    from scipy.stats import spearmanr
    s = spearmanr(x, y)
    return float(s.statistic), float(s.pvalue)

def partial_spearman(x, y, z):
    """Spearman partial correlation of x,y controlling z = Pearson partial on ranks."""
    from scipy.stats import rankdata
    rx, ry, rz = rankdata(x), rankdata(y), rankdata(z)
    def pear(a, b): return float(np.corrcoef(a, b)[0, 1])
    rxy, rxz, ryz = pear(rx, ry), pear(rx, rz), pear(ry, rz)
    denom = math.sqrt(max(1e-12, (1 - rxz**2) * (1 - ryz**2)))
    return (rxy - rxz * ryz) / denom

def bh_fdr(pvals, q=0.05):
    """Benjamini-Hochberg: return (reject bool array, qvalues) aligned to input order."""
    p = np.asarray(pvals, float); K = len(p)
    order = np.argsort(p); ranks = np.arange(1, K + 1)
    crit = ranks / K * q
    passed = p[order] <= crit
    kmax = np.max(np.where(passed)[0]) + 1 if passed.any() else 0
    reject = np.zeros(K, bool)
    if kmax > 0: reject[order[:kmax]] = True
    # BH-adjusted q-values (monotone)
    qv = np.empty(K); running = 1.0
    for i in range(K - 1, -1, -1):
        running = min(running, p[order[i]] * K / (i + 1)); qv[order[i]] = running
    return reject, qv

def tukey_upper_fence(v):
    q1, q3 = np.percentile(v, [25, 75]); return float(q3 + 1.5 * (q3 - q1))

# ---------- per-event axis extraction ----------
def load_axes(fp, group):
    with h5py.File(fp, "r") as h:
        ds = h[group]["posterior_samples"]; cols = ds.dtype.names
        def med(c): return float(np.nanmedian(np.asarray(ds[c], float))) if c in cols else float("nan")
        out = {"chi_p": med("chi_p"),
               "abs_chi_eff": abs(med("chi_eff")),
               "mass_ratio": med("mass_ratio"),
               "redshift": med("redshift"),
               "chirp_mass_source": med("chirp_mass_source"),
               "total_mass_source": med("total_mass_source"),
               "mass_2_source": med("mass_2_source")}
        # loudness proxy (record which)
        if "network_matched_filter_snr" in cols:
            out["loudness_snr"] = med("network_matched_filter_snr"); out["_snr_proxy"] = "network_matched_filter_snr"
        elif "network_optimal_snr" in cols:
            out["loudness_snr"] = med("network_optimal_snr"); out["_snr_proxy"] = "network_optimal_snr"
        else:
            dets = [c for c in cols if c.endswith("_optimal_snr")]
            out["loudness_snr"] = math.sqrt(sum(med(c)**2 for c in dets)) if dets else float("nan")
            out["_snr_proxy"] = "quadrature(" + ",".join(dets) + ")" if dets else "none"
        # waveform disagreement: stdev of psi_meas across all waveform families (deg, mod-180 aligned)
        fams = [k for k in h.keys() if isinstance(h[k], h5py.Group) and "posterior_samples" in h[k]]
        psis = []
        for k in fams:
            d = h[k]["posterior_samples"]
            if any(n not in d.dtype.names for n in ["mass_1_source", "mass_2_source"]): continue
            m1 = np.asarray(d["mass_1_source"], float); m2 = np.asarray(d["mass_2_source"], float)
            ok = np.isfinite(m1) & np.isfinite(m2)
            psis.append(psi_axr_rho(m1[ok], m2[ok])[0])
        if len(psis) >= 2:
            base = psis[0]; adj = [p - 180 * round((p - base) / 180) for p in psis]
            out["waveform_disagreement"] = float(np.std(adj)); out["_n_families"] = len(psis)
        else:
            out["waveform_disagreement"] = float("nan"); out["_n_families"] = len(psis)
        return out

def main():
    e71 = json.load(open(E71))
    elong = [r for r in e71["per_event"] if r["axr"] >= 3]
    print(f"E72 sample: {len(elong)} elongated O4b events (axr>=3)")
    rows = []
    for r in elong:
        fp = os.path.join(GW5, f"{r['event']}-combined_PEDataRelease.hdf5")
        ax = load_axes(fp, r["group"])
        rows.append({"event": r["event"], "axr": r["axr"], "r_err_curve": r["err_curve"],
                     "m1": r["m1"], "m2": r["m2"], "group": r["group"], **ax})
    R = np.array([x["r_err_curve"] for x in rows], float)
    AXR = np.array([x["axr"] for x in rows], float)

    # D1: Spearman + BH-FDR + partial(axr)
    d1 = {}; pvals = []; keys = []
    for a in AXES:
        v = np.array([x[a] for x in rows], float)
        m = np.isfinite(v) & np.isfinite(R)
        rho, p = spearman(R[m], v[m])
        rp = partial_spearman(R[m], v[m], AXR[m])
        d1[a] = {"rho": rho, "p": p, "n": int(m.sum()), "rho_partial_axr": rp}
        pvals.append(p); keys.append(a)
    reject, qv = bh_fdr(pvals, 0.05)
    candidates = []
    for i, a in enumerate(keys):
        d1[a]["q_bh"] = float(qv[i]); d1[a]["fdr_reject"] = bool(reject[i])
        if reject[i] and abs(d1[a]["rho_partial_axr"]) >= 0.3 and \
           math.copysign(1, d1[a]["rho"]) == math.copysign(1, d1[a]["rho_partial_axr"]):
            candidates.append(a)

    # D2: Tukey upper fence
    fence = tukey_upper_fence(R)
    outliers = [x for x in rows if x["r_err_curve"] > fence]

    # D3: coherence lens on any outlier (spread across waveforms vs residual)
    for o in outliers:
        o["coherence"] = "SYSTEMATIC(waveform-driven)" if o.get("waveform_disagreement", 0) >= o["r_err_curve"] \
                         else "CANDIDATE-physics"

    print(f"\nD1 correlations (Spearman r vs axis; BH-FDR q=0.05; partial controls axr):")
    print(f"  {'axis':22s} {'rho':>6s} {'p':>7s} {'q_BH':>7s} {'rho|axr':>8s} {'n':>3s} {'FDR':>4s}")
    for a in AXES:
        d = d1[a]
        print(f"  {a:22s} {d['rho']:6.2f} {d['p']:7.3f} {d['q_bh']:7.3f} {d['rho_partial_axr']:8.2f} "
              f"{d['n']:3d} {'YES' if d['fdr_reject'] else '-':>4s}")
    print(f"  CANDIDATE axes (FDR-survive AND |rho_partial|>=0.3 same sign): {candidates or 'NONE'}")
    print(f"\nD2 Tukey upper fence = {fence:.2f} deg; outliers (r>fence): "
          f"{[(o['event'], o['r_err_curve']) for o in outliers] or 'NONE'}")
    if outliers:
        print("D3 coherence lens on outliers:")
        for o in outliers:
            print(f"  {o['event']}: r={o['r_err_curve']} wf_disagree={o['waveform_disagreement']:.2f} -> {o['coherence']}")

    verdict = ("NULL: the curved law holds uniformly across O4b elongated source classes within power "
               "(no axis survives FDR+partial; no Tukey outliers)") if not candidates and not outliers \
              else "FLAGS PRESENT: see candidates/outliers (candidate, not a claim)"
    print(f"\nVERDICT: {verdict}")

    json.dump({"prereg": "preregs/E72_gw_geometry_outlier_atlas_prereg.md",
               "sample": "32 elongated O4b events (axr>=3) from E71", "n": len(rows),
               "snr_proxy": rows[0].get("_snr_proxy") if rows else None,
               "D1_correlations": d1, "D1_candidates": candidates,
               "D2_tukey_fence": fence, "D2_outliers": [o["event"] for o in outliers],
               "D3_coherence": {o["event"]: o["coherence"] for o in outliers},
               "verdict": verdict, "atlas": sorted(rows, key=lambda x: -x["r_err_curve"])},
              open(os.path.join(ROOT, "results/e72_gw_geometry_outlier_atlas_results.json"), "w"), indent=2)
    print("\nwrote results/e72_gw_geometry_outlier_atlas_results.json")

if __name__ == "__main__":
    main()
