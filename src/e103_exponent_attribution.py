#!/usr/bin/env python3
"""E103 - is the exponent offset 1PN, finite-width, or both?

The referee's decisive test for the attribution inconsistency between Sec IV D and Appendix A:
per-event fitted exponent p*_i vs the per-event 1PN Fisher prediction, and each vs elongation with the
other partialled out. See preregs/E103_exponent_attribution_prereg.md (prior scratch run disclosed;
this is the confirmatory locked run).

Reads the E94 cache. No HDF5. Seed 103.
"""
import json, os, sys
import numpy as np
from scipy.stats import spearmanr, rankdata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from src.e94_build_posterior_cache import load, CACHE
from src.e95_gate_regeneration import primary_rows, AXR_MIN
from src.e101_alternative_curves_and_1pn import (curve_angle_p, fisher_long_axis,
                                                 p_eff_of_angle, P_GRID)
from src.e65_pn_fisher_rotation import adiff

SEED = 103
N_BOOT = 2000
RESULT_JSON = os.path.join(ROOT, "results/e103_exponent_attribution_results.json")


def partial_spearman(x, y, z):
    """Rank-based partial correlation of x and y controlling for z."""
    rx, ry, rz = rankdata(x), rankdata(y), rankdata(z)

    def resid(a, b):
        A = np.vstack([b, np.ones_like(b)]).T
        return a - A @ np.linalg.lstsq(A, a, rcond=None)[0]

    r, p = spearmanr(resid(rx, rz), resid(ry, rz))
    return float(r), float(p)


def main():
    rng = np.random.default_rng(SEED)
    rec = load()
    prim, _ = primary_rows(rec)
    EL = [v for (c, e), v in prim.items() if v["axr"] >= AXR_MIN]

    pstar, ppred, axr = [], [], []
    for v in EL:
        errs = [abs(adiff(curve_angle_p(v["q"], p), v["psi"])) for p in P_GRID]
        pstar.append(float(P_GRID[int(np.argmin(errs))]))
        m1, m2 = float(v["m1m"]), float(v["m2m"])
        ppred.append(p_eff_of_angle(m1, m2, fisher_long_axis(m1, m2, "1PN")))
        axr.append(float(v["axr"]))
    pstar = np.array(pstar); ppred = np.array(ppred); axr = np.array(axr)
    ok = np.isfinite(pstar) & np.isfinite(ppred)
    pstar, ppred, axr = pstar[ok], ppred[ok], axr[ok]
    n = len(pstar)

    # D1: population medians and the bootstrap CI on their difference
    diffs = []
    for _ in range(N_BOOT):
        s = rng.integers(0, n, n)
        diffs.append(float(np.median(pstar[s]) - np.median(ppred[s])))
    d1 = {"median_p_star": float(np.median(pstar)),
          "median_p_pred_1PN": float(np.median(ppred)),
          "median_diff_boot_ci90": [float(np.percentile(diffs, 5)), float(np.percentile(diffs, 95))],
          "medians_consistent": bool(np.percentile(diffs, 5) <= 0 <= np.percentile(diffs, 95))}

    # D2/D3: the correlation structure
    r_pp, p_pp = spearmanr(pstar, ppred)
    r_pa, p_pa = spearmanr(pstar, axr)
    r_qa, p_qa = spearmanr(ppred, axr)
    r_pp_ax, p_pp_ax = partial_spearman(pstar, ppred, axr)
    r_pa_pp, p_pa_pp = partial_spearman(pstar, axr, ppred)

    most_el = axr >= np.median(axr)
    out = {"battery": "E103 exponent attribution", "seed": SEED, "n_elong": int(n),
           "prereg": "preregs/E103_exponent_attribution_prereg.md",
           "provenance": {"cache": os.path.relpath(CACHE, ROOT), "hdf5_accessed": False},
           "D1_median_match": d1,
           "D2_correlations": {
               "pstar_vs_ppred": {"rho": float(r_pp), "p": float(p_pp)},
               "pstar_vs_ppred_partial_axr": {"rho": float(r_pp_ax), "p": float(p_pp_ax)},
               "pstar_vs_axr": {"rho": float(r_pa), "p": float(p_pa)},
               "pstar_vs_axr_partial_ppred": {"rho": float(r_pa_pp), "p": float(p_pa_pp)}},
           "D3_prediction_flat_in_axr": {"rho": float(r_qa), "p": float(p_qa),
                                         "flat": bool(p_qa > 0.05)},
           "most_elongated_half": {"median_p_star": float(np.median(pstar[most_el])),
                                   "median_p_pred": float(np.median(ppred[most_el]))},
           "verdict": {}}

    two_mech = (d1["medians_consistent"]
                and out["D3_prediction_flat_in_axr"]["flat"]
                and r_pa_pp < 0 and p_pa_pp < 0.05)
    out["verdict"] = {
        "two_mechanisms": bool(two_mech),
        "statement": (
            "BOTH mechanisms are real. The 1PN prediction matches the population-level offset "
            f"(median p* = {d1['median_p_star']:.3f} vs predicted {d1['median_p_pred_1PN']:.3f}, "
            "difference consistent with zero), but it is flat in elongation "
            f"(rho = {r_qa:+.2f}, p = {p_qa:.2f}) and therefore cannot carry the elongation trend: "
            f"p* declines with axis ratio even after partialling out the prediction "
            f"(partial rho = {r_pa_pp:+.2f}, p = {p_pa_pp:.3f}). The 1PN term sets the central "
            "displacement of the exponent; a distinct elongation-dependent (finite-width) effect pulls "
            "the most-elongated events back toward 3/5. Neither categorical attribution alone is correct."
            if two_mech else
            "The expected two-mechanism structure did NOT confirm under the locked run; see the "
            "correlation block and report the contradiction.")}

    json.dump(out, open(RESULT_JSON, "w"), indent=1)
    print(f"n={n}")
    print(f"D1 medians: p*={d1['median_p_star']:.3f}  1PN={d1['median_p_pred_1PN']:.3f}  "
          f"diff CI90=[{d1['median_diff_boot_ci90'][0]:+.3f},{d1['median_diff_boot_ci90'][1]:+.3f}]")
    print(f"D2 p* vs pred: rho={r_pp:+.2f}  | partial(axr): {r_pp_ax:+.2f}")
    print(f"   p* vs axr:  rho={r_pa:+.2f}  | partial(pred): {r_pa_pp:+.2f} (p={p_pa_pp:.3f})")
    print(f"D3 pred vs axr: rho={r_qa:+.2f} (p={p_qa:.2f})  flat={out['D3_prediction_flat_in_axr']['flat']}")
    print(f"\nVERDICT: {out['verdict']['statement'][:180]}...")
    print("wrote", RESULT_JSON)


if __name__ == "__main__":
    main()
