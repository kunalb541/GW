#!/usr/bin/env python3
"""E65 - derive the E40 mass-plane law from PN Fisher geometry: the chirp->total rotation.
Prereg E65 (locked). Two-direction Fisher mixture; kappa fit on the 14 E40-prereg events only;
out-of-sample D1/D2 on the remaining 61; parameter-free sign test D3 on all. Seed 65 (no RNG)."""
import os, sys, json, glob, math
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from src.e38_gw_black_hole_geometry import find_posterior_dataset
import h5py

GW = os.path.join(ROOT, "data/chains/gw_posteriors")

# the 14 locked E40-prereg events (calibration set; from REPORT_E40 table)
PREREG14 = {"GW190814", "GW190425", "GW190924_021846", "GW190728_064510", "GW190708_232457",
            "GW190513_205428", "GW190620_030421", "GW190803_022701", "GW190706_222641",
            "GW190910_112807", "GW190731_140936", "GW190521_074359", "GW190727_060333",
            "GW190519_153544"}

# ---------- analytic aLIGO PSD (Ajith 2011 fit; locked in prereg) ----------
def Sn(f):
    x = f / 215.0
    return 1e-49 * (x ** -4.14 - 5 * x ** -2 + 111 * (1 - x ** 2 + x ** 4 / 2) / (1 + x ** 2 / 2))

TSUN = 4.925491e-6  # GM_sun/c^3 [s]

def weights(mc_det, mt_det):
    """W_c: 0PN lnMc phase Fisher over inspiral band; W_t: merger-band SNR^2 (prereg formulas)."""
    fisco = 4397.0 / mt_det
    f1 = np.geomspace(20.0, max(fisco, 21.0), 400)
    dpsi_dlnmc = (5.0 / 3.0) * (3.0 / 128.0) * (math.pi * mc_det * TSUN * f1) ** (-5.0 / 3.0)
    Wc = np.trapezoid(dpsi_dlnmc ** 2 * f1 ** (-7.0 / 3.0) / Sn(f1), f1)
    f2hi = min(4 * fisco, 1024.0)
    if f2hi > fisco * 1.01:
        f2 = np.geomspace(fisco, f2hi, 200)
        Wt = np.trapezoid(f2 ** (-7.0 / 3.0) / Sn(f2), f2)
    else:
        Wt = 0.0
    return float(Wc), float(Wt)

# ---------- angles ----------
def ang_of(v):
    return math.degrees(math.atan2(v[1], v[0])) % 180.0

def adiff(a, b):
    return abs((a - b + 90) % 180 - 90)

def psi_pred(m1, m2, Wc, Wt, kappa):
    """long axis of C from Gamma = Wc*g_c g_c^T + kappa*Wt*g_t g_t^T (grads of ln Mc, ln Mtot)."""
    # d lnMc/dm = (1/Mc) dMc/dm; Mc=(m1 m2)^(3/5) (m1+m2)^(-1/5)
    M = m1 + m2
    g_c = np.array([0.6 / m1 - 0.2 / M, 0.6 / m2 - 0.2 / M])   # grad ln Mc
    g_t = np.array([1.0 / M, 1.0 / M])                          # grad ln Mtot
    G = Wc * np.outer(g_c, g_c) + kappa * Wt * np.outer(g_t, g_t) + 1e-30 * np.eye(2)
    w, V = np.linalg.eigh(G)
    return ang_of(V[:, 0])       # smallest-eigenvalue direction of Gamma = long axis of C

def between_frac(psi_m, psi_c, psi_t):
    """where psi_m sits on the shortest arc psi_c -> psi_t: 0 = at chirp, 1 = at total (clipped)."""
    span = (psi_t - psi_c + 90) % 180 - 90
    off = (psi_m - psi_c + 90) % 180 - 90
    if abs(span) < 1e-9: return float("nan"), False
    fr = off / span
    return fr, (0.0 <= fr <= 1.0)

def main():
    d40 = json.load(open(os.path.join(ROOT, "results/e40_gw_chirp_mass_lawfulness_results.json")))
    ev40 = {e["event"]: e for e in d40["per_event"]}

    # detector-frame medians from local PE files
    rows = []
    for name, e in sorted(ev40.items()):
        fp = os.path.join(GW, f"{name}_PE.h5")
        if not os.path.exists(fp): continue
        for attempt in range(4):                       # transient errno-60 disk stalls: retry
            try:
                with h5py.File(fp, "r") as h:
                    ds = h[find_posterior_dataset(h)]
                    mc_det = float(np.median(ds["chirp_mass"]))
                    mt_det = float(np.median(ds["total_mass"]))
                    mc_src = float(np.median(ds["chirp_mass_source"]))
                    qs = np.asarray(ds["mass_ratio"], float)    # for the post-hoc chord test
                break
            except (TimeoutError, OSError):
                if attempt == 3: raise
                import time; time.sleep(3 * (attempt + 1))
        # POST-HOC (exploratory, labelled): psi of the constant-Mc CURVE sampled over the
        # event's own q posterior — the "curved-law" prediction (no free parameters).
        qs = np.clip(qs[np.isfinite(qs)], 0.02, 1.0)
        m1c = mc_src * (1 + qs) ** 0.2 * qs ** -0.6
        m2c = qs * m1c
        P = np.column_stack([m1c, m2c]); P = P - P.mean(0)
        _, Vc = np.linalg.eigh(P.T @ P / len(P))
        psi_curve = ang_of(Vc[:, 1])                    # largest-eigenvalue direction
        Wc, Wt = weights(mc_det, mt_det)
        rows.append(dict(event=name, m1=e["m1"], m2=e["m2"], axr=e["axis_ratio"],
                         psi_meas=e["psi_meas"], psi_chirp=e["psi_chirp"], psi_total=e["psi_total"],
                         psi_curve=psi_curve, mc_det=mc_det, mt_det=mt_det,
                         mt_src=e["m1"] + e["m2"], Wc=Wc, Wt=Wt))
    print(f"events with PE + e40 geometry: {len(rows)}")

    cal = [r for r in rows if r["event"] in PREREG14]
    test = [r for r in rows if r["event"] not in PREREG14]
    print(f"calibration (E40 prereg): {len(cal)}   test (out-of-sample): {len(test)}")

    # ---- fit kappa on calibration set only ----
    def med_err(rs, kappa):
        return float(np.median([adiff(psi_pred(r["m1"], r["m2"], r["Wc"], r["Wt"], kappa),
                                      r["psi_meas"]) for r in rs]))
    grid = np.geomspace(1e-6, 1e6, 241)
    errs = [med_err(cal, k) for k in grid]
    kappa = float(grid[int(np.argmin(errs))])
    print(f"kappa* = {kappa:.3e}  (cal median err {min(errs):.2f} vs pure-chirp "
          f"{np.median([adiff(r['psi_chirp'], r['psi_meas']) for r in cal]):.2f})")

    # ---- D1: out-of-sample ----
    for r in rows:
        r["psi_mix"] = psi_pred(r["m1"], r["m2"], r["Wc"], r["Wt"], kappa)
        r["err_mix"] = adiff(r["psi_mix"], r["psi_meas"])
        r["err_chirp"] = adiff(r["psi_chirp"], r["psi_meas"])
    d1_mix = float(np.median([r["err_mix"] for r in test]))
    d1_chp = float(np.median([r["err_chirp"] for r in test]))
    D1 = d1_mix < d1_chp

    # ---- D2: heavy test events (Mtot_source > 60) ----
    heavy = [r for r in test if r["mt_src"] > 60]
    d2_mix = float(np.median([r["err_mix"] for r in heavy])) if heavy else float("nan")
    d2_chp = float(np.median([r["err_chirp"] for r in heavy])) if heavy else float("nan")
    D2 = bool(heavy) and d2_mix < 0.7 * d2_chp

    # ---- D3: parameter-free sign test (all events, gated) ----
    gated = [r for r in rows if r["axr"] >= 1.5 and adiff(r["psi_chirp"], r["psi_total"]) > 10]
    fr_ok = 0; frs = []; mts = []
    for r in gated:
        fr, ok = between_frac(r["psi_meas"], r["psi_chirp"], r["psi_total"])
        r["rot_frac"] = fr
        if ok: fr_ok += 1
        if np.isfinite(fr): frs.append(np.clip(fr, -1, 2)); mts.append(r["mt_det"])
    frac_between = fr_ok / len(gated) if gated else float("nan")
    from scipy.stats import spearmanr
    sp = spearmanr(mts, frs) if len(frs) > 4 else None
    D3 = (frac_between >= 0.70) and (sp is not None and sp.statistic > 0.3)

    print(f"\nD1 out-of-sample (n={len(test)}): mixture {d1_mix:.2f} vs chirp {d1_chp:.2f} deg "
          f"-> {'PASS' if D1 else 'FAIL'}")
    print(f"D2 heavy test (n={len(heavy)}): mixture {d2_mix:.2f} vs chirp {d2_chp:.2f} deg "
          f"(need >30% cut) -> {'PASS' if D2 else 'FAIL'}")
    print(f"D3 sign test (n={len(gated)}): between-fraction {frac_between:.2f} (need >=0.70), "
          f"Spearman(rot_frac, Mtot_det) = {sp.statistic:.2f} (p={sp.pvalue:.3g}, need >0.3) "
          f"-> {'PASS' if D3 else 'FAIL'}")

    # rotation-fraction vs mass table (descriptive)
    gated_sorted = sorted(gated, key=lambda r: r["mt_det"])
    print("\n  event                Mt_det  axr   psi_meas  psi_chirp  psi_total  rot_frac")
    for r in gated_sorted[:40]:
        print(f"  {r['event']:20s} {r['mt_det']:6.1f} {r['axr']:5.1f}  {r['psi_meas']:7.2f}  "
              f"{r['psi_chirp']:7.2f}  {r['psi_total']:7.2f}  {r['rot_frac']:+.2f}")

    # ---- POST-HOC exploratory: the curved-law (constant-Mc CURVE chord) vs tangent ----
    for r in rows:
        r["err_curve"] = adiff(r["psi_curve"], r["psi_meas"])
    ph_curve_all = float(np.median([r["err_curve"] for r in rows]))
    ph_chirp_all = float(np.median([r["err_chirp"] for r in rows]))
    elong = [r for r in rows if r["axr"] >= 3]
    ph_curve_el = float(np.median([r["err_curve"] for r in elong]))
    ph_chirp_el = float(np.median([r["err_chirp"] for r in elong]))
    curve_wins = sum(1 for r in rows if r["err_curve"] < r["err_chirp"])
    # signed residual vs elongation (the curvature-bias signature)
    def sgn(a, b): return (a - b + 90) % 180 - 90
    sres = [sgn(r["psi_meas"], r["psi_chirp"]) for r in rows]
    sp2 = spearmanr([r["axr"] for r in rows], np.abs(sres))
    print(f"\n=== POST-HOC (exploratory, NOT preregistered): curved-law test ===")
    print(f"  all 75:      curve {ph_curve_all:.2f} vs tangent {ph_chirp_all:.2f} deg ; curve wins {curve_wins}/75")
    print(f"  elongated (axr>=3, n={len(elong)}): curve {ph_curve_el:.2f} vs tangent {ph_chirp_el:.2f} deg")
    print(f"  Spearman(|signed residual|, axr) = {sp2.statistic:.2f} (p={sp2.pvalue:.3g})")

    json.dump({"prereg": "preregs/E65_pn_fisher_rotation_prereg.md",
               "posthoc_curved_law": {"label": "EXPLORATORY post-hoc, not preregistered",
                   "median_err_curve_all": ph_curve_all, "median_err_tangent_all": ph_chirp_all,
                   "median_err_curve_elong": ph_curve_el, "median_err_tangent_elong": ph_chirp_el,
                   "curve_wins": curve_wins, "n": len(rows),
                   "spearman_absres_axr": float(sp2.statistic), "p": float(sp2.pvalue)},
               "kappa": kappa, "n_cal": len(cal), "n_test": len(test),
               "D1": {"median_err_mixture_test": d1_mix, "median_err_chirp_test": d1_chp, "pass": bool(D1)},
               "D2": {"n_heavy": len(heavy), "median_err_mixture": d2_mix, "median_err_chirp": d2_chp, "pass": bool(D2)},
               "D3": {"n_gated": len(gated), "frac_between": frac_between,
                      "spearman_rotfrac_mtdet": float(sp.statistic), "p": float(sp.pvalue), "pass": bool(D3)},
               "per_event": [{k: (round(v, 4) if isinstance(v, float) else v) for k, v in r.items()}
                             for r in rows]},
              open(os.path.join(ROOT, "results/e65_pn_fisher_rotation_results.json"), "w"), indent=2)
    print("\nwrote results/e65_pn_fisher_rotation_results.json")

if __name__ == "__main__":
    main()
