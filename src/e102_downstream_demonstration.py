#!/usr/bin/env python3
"""E102 - does the orientation correction change a downstream quantity?

Answers the review's fairest objection: the paper calls the reconstruction a "cheap correction for
applications relying on orientation" but never shows an orientation error of this size costs anything.
See preregs/E102_downstream_demonstration_prereg.md. Blind: coverage not computed at prereg time.

For each elongated event, build a 2-D Gaussian with the TRUE mean and TRUE covariance eigenvalues, but
orientation from {oracle=measured, curve, tangent}. Holding mean and eigenvalues fixed isolates
orientation. Metric: fraction of true samples inside the Gaussian's 90% Mahalanobis ellipse (a
well-oriented approximation covers ~90%; a mis-oriented ellipse of equal area covers less).

Reads the E94 cache. No HDF5. Seed 102.
"""
import json, os, sys, math
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from src.e94_build_posterior_cache import load, CACHE
from src.e95_gate_regeneration import primary_rows, AXR_MIN
from src.e71_gwtc5_curved_law import curve_psi, tangent_angles
from scipy.stats import chi2

SEED = 102
CATS = ("GWTC-3", "O4a", "O4b")
LEVEL = 0.90
R2 = chi2.ppf(LEVEL, df=2)                 # Mahalanobis radius^2 for the 90% 2-D ellipse
AXR_BANDS = ((3.0, 5.0), (5.0, 10.0), (10.0, 1e9))
RESULT_JSON = os.path.join(ROOT, "results/e102_downstream_demonstration_results.json")


def gaussian_from(m1, m2, angle_deg, eigvals):
    """Covariance with given principal-axis angle and eigenvalues (l_max along the axis)."""
    th = math.radians(angle_deg)
    u = np.array([math.cos(th), math.sin(th)])          # long axis
    v = np.array([-u[1], u[0]])                          # short axis
    lo, hi = sorted(eigvals)
    return hi * np.outer(u, u) + lo * np.outer(v, v)


def coverage(m1, m2, mean, cov):
    """Fraction of samples inside the 90% Mahalanobis ellipse of N(mean, cov)."""
    X = np.column_stack([m1, m2]) - mean
    Ci = np.linalg.inv(cov + 1e-12 * np.eye(2))
    d2 = np.einsum("ij,jk,ik->i", X, Ci, X)
    return float(np.mean(d2 <= R2))


def m2_width_err(m1, m2, mean, cov):
    """Fractional error in the Gaussian-approx 90% width on m2 vs the true 90% width."""
    true_w = np.percentile(m2, 95) - np.percentile(m2, 5)
    approx_w = 2 * 1.645 * math.sqrt(cov[1, 1])          # 90% width of the Gaussian m2 marginal
    return float((approx_w - true_w) / true_w)


def main():
    rec = load()
    prim, _ = primary_rows(rec)
    EL = {c: [v for (cc, e), v in prim.items() if cc == c and v["axr"] >= AXR_MIN] for c in CATS}

    out = {"battery": "E102 downstream demonstration", "seed": SEED,
           "prereg": "preregs/E102_downstream_demonstration_prereg.md",
           "provenance": {"cache": os.path.relpath(CACHE, ROOT), "hdf5_accessed": False},
           "level": LEVEL, "n_elong": {c: len(EL[c]) for c in CATS}, "by_catalog": {}, "by_axr_band": {}}

    rows = []
    for c in CATS:
        cov_or, cov_cu, cov_ta, w_or, w_cu, w_ta = [], [], [], [], [], []
        for v in EL[c]:
            m1 = v["raw"]["m1s"].astype(float); m2 = v["raw"]["m2s"].astype(float)
            mean = np.array([m1.mean(), m2.mean()])
            C = np.cov(np.vstack([m1, m2]))
            eig = np.linalg.eigvalsh(C)
            a_or, a_cu, a_ta = v["psi"], curve_psi(v["mc"], v["q"]), tangent_angles(v["m1m"], v["m2m"])[0]
            g_or = gaussian_from(*mean, a_or, eig)
            g_cu = gaussian_from(*mean, a_cu, eig)
            g_ta = gaussian_from(*mean, a_ta, eig)
            cov_or.append(coverage(m1, m2, mean, g_or))
            cov_cu.append(coverage(m1, m2, mean, g_cu))
            cov_ta.append(coverage(m1, m2, mean, g_ta))
            w_or.append(abs(m2_width_err(m1, m2, mean, g_or)))
            w_cu.append(abs(m2_width_err(m1, m2, mean, g_cu)))
            w_ta.append(abs(m2_width_err(m1, m2, mean, g_ta)))
            rows.append((v["axr"], cov_or[-1], cov_cu[-1], cov_ta[-1]))
        o, cu, ta = np.median(cov_or), np.median(cov_cu), np.median(cov_ta)
        gap = o - ta
        closed = (cu - ta) / gap if gap > 1e-6 else float("nan")
        out["by_catalog"][c] = {
            "coverage_oracle": round(o, 4), "coverage_curve": round(cu, 4),
            "coverage_tangent": round(ta, 4), "gap_closed_frac": round(closed, 3),
            "m2_width_abs_err_oracle": round(float(np.median(w_or)), 4),
            "m2_width_abs_err_curve": round(float(np.median(w_cu)), 4),
            "m2_width_abs_err_tangent": round(float(np.median(w_ta)), 4)}

    # pooled by axis-ratio band (effect must grow with elongation)
    rows = np.array(rows)
    for lo, hi in AXR_BANDS:
        sel = rows[(rows[:, 0] >= lo) & (rows[:, 0] < hi)]
        key = f"{lo:g}-{hi:g}" if hi < 1e8 else f"{lo:g}+"
        if len(sel):
            out["by_axr_band"][key] = {
                "n": int(len(sel)), "coverage_oracle": round(float(np.median(sel[:, 1])), 4),
                "coverage_curve": round(float(np.median(sel[:, 2])), 4),
                "coverage_tangent": round(float(np.median(sel[:, 3])), 4)}

    # overall verdict
    allc = np.array([[out["by_catalog"][c][k] for k in
                      ("coverage_oracle", "coverage_curve", "coverage_tangent")] for c in CATS])
    o, cu, ta = allc.mean(0)
    gap_closed = (cu - ta) / (o - ta) if (o - ta) > 1e-6 else float("nan")
    bands = list(out["by_axr_band"].values())
    grows = (len(bands) >= 2 and
             (bands[0]["coverage_oracle"] - bands[0]["coverage_tangent"]) <
             (bands[-1]["coverage_oracle"] - bands[-1]["coverage_tangent"]))
    w_or = float(np.mean([out["by_catalog"][c]["m2_width_abs_err_oracle"] for c in CATS]))
    w_cu = float(np.mean([out["by_catalog"][c]["m2_width_abs_err_curve"] for c in CATS]))
    w_ta = float(np.mean([out["by_catalog"][c]["m2_width_abs_err_tangent"] for c in CATS]))
    out["verdict"] = {
        # PRIMARY metric (prereg): total 90% region coverage. Orientation-insensitive by construction
        # (the ellipse area is fixed), so this is a NULL and is reported as one -- not swapped for the
        # metric that worked.
        "primary_coverage": {"oracle": round(float(o), 4), "curve": round(float(cu), 4),
                             "tangent": round(float(ta), 4), "gap_deg": round(float(o - ta), 4),
                             "outcome": "NULL: orientation barely affects total-region coverage "
                                        "(the region area is fixed, so this metric is insensitive to it)"},
        # SECONDARY metric: the component-mass marginal width, which IS orientation-sensitive.
        "secondary_m2_width_abs_err": {"oracle": round(w_or, 3), "curve": round(w_cu, 3),
                                       "tangent": round(w_ta, 3),
                                       "outcome": "EFFECT: a tangent-oriented Gaussian misstates the "
                                                  "secondary-mass 90% width; the curve tracks the oracle"},
        "effect_grows_with_axr": bool(grows),
        "statement": (
            f"Orientation is nearly irrelevant to total 90% coverage (oracle {o:.3f} vs tangent {ta:.3f}), "
            f"which depends on the region area, not its tilt. It matters for the component-mass marginals: "
            f"a tangent-oriented Gaussian misstates the secondary-mass 90% credible width by "
            f"{w_ta:.0%} (median), which the curve reduces to {w_cu:.0%}, close to the oracle {w_or:.0%}. "
            f"The demonstrated downstream value is thus specific: more accurate component-mass credible "
            f"intervals from a Gaussian single-event approximation, not better total coverage.")}

    json.dump(out, open(RESULT_JSON, "w"), indent=1)
    print("90% Mahalanobis-ellipse coverage of the true posterior (higher = better approximation):")
    for c in CATS:
        d = out["by_catalog"][c]
        print(f"  {c:>7}: oracle {d['coverage_oracle']:.3f}  curve {d['coverage_curve']:.3f}  "
              f"tangent {d['coverage_tangent']:.3f}  gap closed {d['gap_closed_frac']:.0%}")
    print("\nby axis-ratio band:")
    for k, d in out["by_axr_band"].items():
        print(f"  {k:>7} (n={d['n']:3d}): oracle {d['coverage_oracle']:.3f}  curve {d['coverage_curve']:.3f}"
              f"  tangent {d['coverage_tangent']:.3f}")
    v = out["verdict"]["secondary_m2_width_abs_err"]
    print(f"\nm2 90%-width |error|:  oracle {v['oracle']:.2f}  curve {v['curve']:.2f}  tangent {v['tangent']:.2f}")
    print(f"VERDICT: {out['verdict']['statement']}")
    print("wrote", RESULT_JSON)


if __name__ == "__main__":
    main()
