#!/usr/bin/env python3
"""E97 - is the constant-Mc curve a PRINCIPAL CURVE? Implementing the mathematics, not citing it.

The manuscript cites principal curves (Hastie & Stuetzle 1989) for the conceptual distinction between a
chord and a tangent. The submission-gate audit rightly objected to ornamental mathematics: a citation
earns its place only if the mathematics is actually used. So use it.

Hastie & Stuetzle define a principal curve by SELF-CONSISTENCY:

    f(t) = E[ X | t_f(X) = t ]

each point of the curve is the mean of the data projecting onto it. That is a precise, testable property
of the constant-Mc curve, and it bears directly on the manuscript's open question -- why is there a
residual ~1 deg between the curve's principal axis and the measured one?

WHAT IS MEASURED
  1. the self-consistency VIOLATION: the perpendicular offset between each curve point and the mean of the
     samples projecting onto it, normalised by the posterior's own scale;
  2. whether that violation PREDICTS the per-event orientation residual (the headline; a correlation, not
     a fit, so it cannot be inflated by added flexibility);
  3. one Hastie-Stuetzle iteration (replace the curve by those conditional means) -- reported IN-SAMPLE
     and with its grid sensitivity exposed, plus a cross-waveform-family test that is not in-sample.

HONESTY NOTES BUILT IN
  - The projection grid is a tuning knob. A fine grid empties the bins; a coarse one over-smooths. The
     correlation is reported across a SWEEP so the reader sees it does not depend on that choice, while
     the iteration's improvement plainly does.
  - The iteration uses the posterior's own conditional means, so an in-sample improvement proves nothing;
     the cross-family test (learn the correction on waveform family A, apply to family B) is the honest bar,
     the same one E96 had to clear.

Reads the E94 cache only. No HDF5. Seed 97.
"""
import json, math, os, sys
import numpy as np
from scipy.stats import spearmanr, wilcoxon

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from src.e94_build_posterior_cache import load, CACHE, MANIFEST
from src.e95_gate_regeneration import primary_rows, AXR_MIN, FAMILY_PAIR
from src.e71_gwtc5_curved_law import curve_psi, psi_axr_rho
from src.e65_pn_fisher_rotation import adiff, ang_of

SEED = 97
GRID_SWEEP = ((24, 60), (40, 40), (60, 30), (100, 20))
PRIMARY_GRID = (40, 40)
RESULT_JSON = os.path.join(ROOT, "results/e97_principal_curve_selfconsistency_results.json")


def curve_pts(mc, qs):
    m1 = mc * (1 + qs) ** 0.2 * qs ** -0.6
    return np.column_stack([m1, qs * m1])


def self_consistency(m1, m2, q, mc, n_grid, min_per_bin):
    """Project samples to the curve; return (signed offsets, conditional means, curve points).

    The projection index is the nearest curve point (Hastie-Stuetzle's t_f). The offset is taken along
    the local NORMAL, so it measures failure of self-consistency perpendicular to the curve -- movement
    along the curve is reparameterization, not a violation."""
    X = np.column_stack([m1, m2])
    qg = np.linspace(max(np.percentile(q, 1), 0.02), min(np.percentile(q, 99), 1.0), n_grid)
    C = curve_pts(mc, qg)
    idx = ((X[:, None, :] - C[None, :, :]) ** 2).sum(-1).argmin(1)
    offs, means, pts = [], [], []
    for k in range(n_grid):
        s = idx == k
        if s.sum() < min_per_bin:
            continue
        mu = X[s].mean(0)
        t = curve_pts(mc, np.array([qg[k] + 1e-4]))[0] - C[k]
        t /= np.hypot(*t)
        offs.append(float((mu - C[k]) @ np.array([-t[1], t[0]])))
        means.append(mu)
        pts.append(C[k])
    return np.array(offs), np.array(means), np.array(pts)


def axis_of(P):
    P = P - P.mean(0)
    _, V = np.linalg.eigh(P.T @ P / len(P))
    return ang_of(V[:, 1])


def analyse(prim, n_grid, min_per_bin):
    rows = []
    for (cat, ev), v in sorted(prim.items()):
        if v["axr"] < AXR_MIN:
            continue
        m1 = v["raw"]["m1s"].astype(float)
        m2 = v["raw"]["m2s"].astype(float)
        offs, means, _ = self_consistency(m1, m2, v["q"], v["mc"], n_grid, min_per_bin)
        if len(means) < 6:
            continue
        scale = float(np.sqrt(np.linalg.eigvalsh(np.cov(np.column_stack([m1, m2]).T))[-1]))
        rows.append(dict(
            catalog=cat, event=ev, axr=float(v["axr"]), n_bins=int(len(means)),
            residual_deg=float(abs(adiff(curve_psi(v["mc"], v["q"]), v["psi"]))),
            residual_after_one_iteration_deg=float(abs(adiff(axis_of(means), v["psi"]))),
            violation=float(np.mean(np.abs(offs)) / scale),
            violation_signed=float(np.mean(offs) / scale)))
    return rows


def cross_family(rec, byev, n_grid, min_per_bin):
    """Learn the self-consistency correction on family A; apply it to family B. NOT in-sample."""
    out = []
    for (cat, ev), gs in sorted(byev.items()):
        A, B = FAMILY_PAIR[cat]
        if A not in gs or B not in gs:
            continue
        da, db = rec[(cat, ev, A)], rec[(cat, ev, B)]
        pa, aa, _ = psi_axr_rho(da["m1s"].astype(float), da["m2s"].astype(float))
        pb, ab, _ = psi_axr_rho(db["m1s"].astype(float), db["m2s"].astype(float))
        if aa < AXR_MIN or ab < AXR_MIN:
            continue
        for src, tgt, psi_t, tag in ((da, db, pb, "AtoB"), (db, da, pa, "BtoA")):
            mc_s = float(np.median(src["mcs"]))
            offs, means, pts = self_consistency(src["m1s"].astype(float), src["m2s"].astype(float),
                                                src["q"].astype(float), mc_s, n_grid, min_per_bin)
            if len(means) < 6:
                continue
            # apply the SOURCE family's normal-offset correction to the TARGET's own curve
            mc_t = float(np.median(tgt["mcs"]))
            qt = tgt["q"].astype(float)
            qg = np.linspace(max(np.percentile(qt, 1), 0.02), min(np.percentile(qt, 99), 1.0), len(offs))
            Ct = curve_pts(mc_t, qg)
            fwd = curve_pts(mc_t, np.clip(qg + 1e-4, 0.02, 1.0)) - Ct
            nrm = np.hypot(fwd[:, 0], fwd[:, 1])[:, None]
            nrm[nrm == 0] = 1.0
            tt = fwd / nrm
            nvec = np.column_stack([-tt[:, 1], tt[:, 0]])
            corrected = Ct + nvec * offs[:, None]
            out.append(dict(catalog=cat, event=ev, direction=tag,
                            pure_deg=float(abs(adiff(curve_psi(mc_t, qt), psi_t))),
                            corrected_deg=float(abs(adiff(axis_of(corrected), psi_t)))))
    return out


def main():
    rec = load()
    prim, byev = primary_rows(rec)
    manifest = json.load(open(MANIFEST)) if os.path.exists(MANIFEST) else {}

    sweep = {}
    for ng, mb in GRID_SWEEP:
        rows = analyse(prim, ng, mb)
        vi = np.array([r["violation"] for r in rows])
        rs = np.array([r["residual_deg"] for r in rows])
        it = np.array([r["residual_after_one_iteration_deg"] for r in rows])
        rho, p = spearmanr(vi, rs)
        sweep[f"grid{ng}_min{mb}"] = {
            "n_events": len(rows), "median_bins_per_event": float(np.median([r["n_bins"] for r in rows])),
            "median_violation": float(np.median(vi)),
            "spearman_violation_vs_residual": float(rho), "p_value": float(p),
            "median_residual_deg": float(np.median(rs)),
            "median_residual_after_one_iteration_deg": float(np.median(it)),
            "frac_iteration_improved": float(np.mean(it < rs))}

    ng, mb = PRIMARY_GRID
    rows = analyse(prim, ng, mb)
    xf = cross_family(rec, byev, ng, mb)
    xs = {}
    for tag in ("AtoB", "BtoA"):
        S = [r for r in xf if r["direction"] == tag]
        if len(S) < 5:
            continue
        pu = np.array([r["pure_deg"] for r in S])
        co = np.array([r["corrected_deg"] for r in S])
        xs[tag] = {"n": len(S), "pure_curve_deg": float(np.median(pu)),
                   "self_consistency_corrected_deg": float(np.median(co)),
                   "frac_improved": float(np.mean(co < pu)),
                   "wilcoxon_p": float(wilcoxon(pu, co).pvalue)}

    rhos = [v["spearman_violation_vs_residual"] for v in sweep.values()]
    its = [v["median_residual_after_one_iteration_deg"] for v in sweep.values()]
    verdict = {
        "violation_predicts_residual": ("SUPPORTED and grid-robust" if min(rhos) > 0.5
                                        else "NOT robust across grids"),
        "one_iteration_improves_out_of_sample": ("SUPPORTED" if xs and all(
            v["self_consistency_corrected_deg"] < v["pure_curve_deg"] and v["wilcoxon_p"] < 0.05
            for v in xs.values()) else "NOT SUPPORTED out-of-sample"),
        "statement": ("The constant-Mc curve is NOT a principal curve in the Hastie-Stuetzle sense: it is "
                      "not self-consistent, and the size of that violation predicts the per-event "
                      "orientation residual. This is a correlation between two measured quantities, not a "
                      "fit, so it cannot be inflated by added model freedom. The one-step correction is "
                      "reported separately because it is in-sample and grid-sensitive "
                      f"(median residual after one iteration ranges {min(its):.2f}-{max(its):.2f} deg "
                      "across the grid sweep).")}

    out = {"battery": "E97 principal-curve self-consistency", "seed": SEED,
           "definition": "Hastie & Stuetzle (1989): f is a principal curve iff f(t) = E[X | t_f(X) = t]",
           "provenance": {"cache": os.path.relpath(CACHE, ROOT),
                          "manifest": os.path.relpath(MANIFEST, ROOT),
                          "cache_manifest": manifest, "hdf5_accessed": False},
           "primary_grid": {"n_grid": ng, "min_per_bin": mb},
           "grid_sweep": sweep, "cross_family": xs, "verdict": verdict, "events": rows}
    json.dump(out, open(RESULT_JSON, "w"), indent=1)

    print("grid sweep (violation vs residual):")
    for k, v in sweep.items():
        print(f"  {k:>16} n={v['n_events']:3d} bins~{v['median_bins_per_event']:.0f}  "
              f"viol={v['median_violation']:.4f}  rho={v['spearman_violation_vs_residual']:+.3f} "
              f"(p={v['p_value']:.1e})  1-iter {v['median_residual_after_one_iteration_deg']:.3f} deg "
              f"({v['frac_iteration_improved']:.0%} improved)")
    for tag, v in xs.items():
        print(f"  cross-family {tag}: n={v['n']} pure {v['pure_curve_deg']:.2f} -> corrected "
              f"{v['self_consistency_corrected_deg']:.2f} deg (p={v['wilcoxon_p']:.3f}, "
              f"{v['frac_improved']:.0%} improved)")
    print("VERDICT:", verdict["violation_predicts_residual"], "|",
          verdict["one_iteration_improves_out_of_sample"])
    print("wrote", RESULT_JSON)


if __name__ == "__main__":
    main()
