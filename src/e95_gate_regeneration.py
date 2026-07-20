#!/usr/bin/env python3
"""E95 - regenerate the Gate A/C/D numbers from the E94 cache, with a PROPER permutation null.

Answers the reproducibility blocker raised against the Gate A-E measurement notes: those numbers were
committed as prose only, and the first packaging attempt (E91) fell back to re-serializing the committed
E65/E67/E71 result JSONs because a full HDF5 sweep is slow. HDF5 is not broken -- measured 266/266 opens
with 0 failures -- it just costs ~276 s per pass. E94 pays that once; this module runs from the cache in
seconds and writes machine-readable output.

TWO CORRECTIONS TO THE PROSE NOTES, both found by regenerating:

 1. **The single-shuffle baseline was noise.** The notes reported one shuffled-q assignment per catalog
    (9.40 / 3.04 / 6.56). Re-drawing gives wildly different values (9.17 / 8.62 / 4.84). A single
    permutation is not a null distribution. Replaced here by 300 catalog-stratified permutations, which
    make the result STRONGER and properly calibrated: own-q lies below ALL 300 permutations in every
    catalog.
 2. **Subsampling moves the medians at the ~0.1-0.6 deg level.** The notes mixed full-sample and
    2000-sample runs (this is the origin of the 0.96 vs 1.04 discrepancy between the Gate B and Gate C
    notes). Everything here uses one fixed cache subsample, so the numbers are internally consistent.

Preferred-group selection is declared explicitly rather than inherited, and every score is also
available per waveform family from the same cache. Seed 91 (matching the gate work). No HDF5 access.
"""
import os, sys, json
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from src.e94_build_posterior_cache import load
from src.e71_gwtc5_curved_law import psi_axr_rho, tangent_angles, curve_psi
from src.e65_pn_fisher_rotation import adiff

SEED = 91
N_PERM = 300
AXR_MIN = 3.0
PREFERRED = {"GWTC-3": ["C01:Mixed"],
             "O4a": ["C00:Mixed", "C00:Mixed+XO4a"],
             "O4b": ["C00:Mixed", "C00:SEOBNRv5PHM"]}
FAMILY_PAIR = {"GWTC-3": ("C01:IMRPhenomXPHM", "C01:SEOBNRv4PHM"),
               "O4a": ("C00:IMRPhenomXPHM-SpinTaylor", "C00:SEOBNRv5PHM"),
               "O4b": ("C00:IMRPhenomXPHM-SpinTaylor", "C00:SEOBNRv5PHM")}


def sdiff(a, b):
    """SIGNED angular difference in (-90, 90]. NOTE: the repo's adiff() is an ABSOLUTE value; using it
    for a sign test yields a tautology (this actually happened -- see GATE_B note)."""
    return (a - b + 90) % 180 - 90


def _axis(d, frame="source"):
    m1 = d["m1s" if frame == "source" else "m1d"].astype(float)
    m2 = d["m2s" if frame == "source" else "m2d"].astype(float)
    psi, axr, _ = psi_axr_rho(m1, m2)
    return psi, axr, float(np.median(m1)), float(np.median(m2))


def primary_rows(rec):
    """One row per event, using an explicitly declared preferred group."""
    by = {}
    for (c, e, g) in rec:
        by.setdefault((c, e), []).append(g)
    out = {}
    for (c, e), gs in by.items():
        g = next((p for p in PREFERRED[c] if p in gs),
                 max(gs, key=lambda x: len(rec[(c, e, x)]["q"])))
        d = rec[(c, e, g)]
        psi, axr, m1m, m2m = _axis(d)
        out[(c, e)] = dict(group=g, psi=psi, axr=axr, q=d["q"].astype(float),
                           mc=float(np.median(d["mcs"])), m1m=m1m, m2m=m2m, raw=d)
    return out, by


def gate_A(prim, rng):
    res = {}
    for cat in PREFERRED:
        E = [v for (c, _), v in prim.items() if c == cat]
        el = [i for i, v in enumerate(E) if v["axr"] >= AXR_MIN]
        if not el:
            continue
        med = lambda fn: float(np.median([abs(adiff(fn(i), E[i]["psi"])) for i in el]))
        own = med(lambda i: curve_psi(E[i]["mc"], E[i]["q"]))
        pooled_q = np.concatenate([v["q"][rng.integers(0, len(v["q"]), 400)] for v in E])
        null = []
        for _ in range(N_PERM):
            p = rng.permutation(len(E))
            null.append(med(lambda i: curve_psi(E[i]["mc"], E[p[i]]["q"])))
        null = np.array(null)
        res[cat] = {
            "n_elong": len(el), "n_all": len(E),
            "own_q": own,
            "pooled_q": med(lambda i: curve_psi(E[i]["mc"], pooled_q)),
            "tangent": med(lambda i: tangent_angles(E[i]["m1m"], E[i]["m2m"])[0]),
            "total_mass": med(lambda i: 135.0),
            "perm_null": {"n": N_PERM, "mean": float(null.mean()), "sd": float(null.std(ddof=1)),
                          "min": float(null.min()), "p05": float(np.percentile(null, 5)),
                          "p95": float(np.percentile(null, 95)),
                          "own_percentile": float(100 * np.mean(null < own)),
                          "own_below_all": bool(own < null.min())}}
    return res


def gate_A_cross_family(rec, byev):
    """Cross-waveform transfer. Reported in BOTH directions -- a single direction is not the result."""
    rows = []
    for (c, e), gs in byev.items():
        A, B = FAMILY_PAIR[c]
        if A not in gs or B not in gs:
            continue
        da, db = rec[(c, e, A)], rec[(c, e, B)]
        pa, aa, _, _ = _axis(da)
        pb, ab, _, _ = _axis(db)
        rows.append(dict(cat=c, aa=aa, ab=ab, pa=pa, pb=pb,
                         mca=float(np.median(da["mcs"])), qa=da["q"].astype(float),
                         mcb=float(np.median(db["mcs"])), qb=db["q"].astype(float),
                         m1a=float(np.median(da["m1s"])), m2a=float(np.median(da["m2s"]))))
    el = [r for r in rows if r["aa"] >= AXR_MIN and r["ab"] >= AXR_MIN]
    m = lambda v: float(np.median(v))
    return {"n_both": len(rows), "n_elong": len(el),
            "A_to_A": m([abs(adiff(curve_psi(r["mca"], r["qa"]), r["pa"])) for r in el]),
            "B_to_B": m([abs(adiff(curve_psi(r["mcb"], r["qb"]), r["pb"])) for r in el]),
            "A_to_B": m([abs(adiff(curve_psi(r["mca"], r["qa"]), r["pb"])) for r in el]),
            "B_to_A": m([abs(adiff(curve_psi(r["mcb"], r["qb"]), r["pa"])) for r in el]),
            "tangent_A_to_B": m([abs(adiff(tangent_angles(r["m1a"], r["m2a"])[0], r["pb"])) for r in el]),
            "family_axis_disagreement": m([abs(adiff(r["pa"], r["pb"])) for r in el]),
            "note": ("the family disagreement is a REFERENCE SCALE, not an error floor; the two "
                     "families are separately inferred from the same strain, not independent experiments")}


def gate_C_frames(prim):
    src, det, n = [], [], 0
    for v in prim.values():
        d = v["raw"]
        if "m1d" not in d:
            continue
        ps, as_, _, _ = _axis(d, "source")
        if as_ < AXR_MIN:
            continue
        n += 1
        src.append(abs(adiff(curve_psi(float(np.median(d["mcs"])), d["q"].astype(float)), ps)))
        pd_, _, _, _ = _axis(d, "detector")
        det.append(abs(adiff(curve_psi(float(np.median(d["mcd"])), d["q"].astype(float)), pd_)))
    return {"n_elong": n, "source_frame": float(np.median(src)), "detector_frame": float(np.median(det)),
            "note": "difference is CONSISTENT WITH mediation by elongation; mediation not established"}


def gate_D_families(rec):
    out = {}
    for (c, e, g), d in rec.items():
        psi, axr, m1m, m2m = _axis(d)
        if axr < AXR_MIN:
            continue
        k = f"{c}|{g}"
        out.setdefault(k, {"curve": [], "tangent": []})
        out[k]["curve"].append(abs(adiff(curve_psi(float(np.median(d["mcs"])), d["q"].astype(float)), psi)))
        out[k]["tangent"].append(abs(adiff(tangent_angles(m1m, m2m)[0], psi)))
    return {k: {"n": len(v["curve"]), "curve": float(np.median(v["curve"])),
                "tangent": float(np.median(v["tangent"]))}
            for k, v in sorted(out.items()) if len(v["curve"]) >= 5}


def main():
    rng = np.random.default_rng(SEED)
    rec = load()
    prim, byev = primary_rows(rec)
    out = {"battery": "E95 gate regeneration from cache", "seed": SEED, "axr_min": AXR_MIN,
           "cache": "results/e94_posterior_cache.npz", "n_cache_rows": len(rec),
           "n_events": len(prim), "preferred_groups": PREFERRED,
           "gate_A": gate_A(prim, rng),
           "gate_A_cross_family": gate_A_cross_family(rec, byev),
           "gate_C": gate_C_frames(prim),
           "gate_D_families": gate_D_families(rec)}
    p = os.path.join(ROOT, "results/e95_gate_regeneration_results.json")
    json.dump(out, open(p, "w"), indent=1)
    for cat, v in out["gate_A"].items():
        n = v["perm_null"]
        print(f"{cat:>8} n={v['n_elong']:3d}  own-q {v['own_q']:.2f}  tangent {v['tangent']:.2f}  "
              f"| perm null {n['mean']:.2f}+/-{n['sd']:.2f} (min {n['min']:.2f})  "
              f"own below all: {n['own_below_all']}")
    x = out["gate_A_cross_family"]
    print(f"\ncross-family n={x['n_elong']}: A->A {x['A_to_A']:.2f}  A->B {x['A_to_B']:.2f}  "
          f"B->A {x['B_to_A']:.2f}  disagreement {x['family_axis_disagreement']:.2f}")
    print(f"gate C: source {out['gate_C']['source_frame']:.2f}  detector {out['gate_C']['detector_frame']:.2f}")
    print("wrote", p)


if __name__ == "__main__":
    main()
