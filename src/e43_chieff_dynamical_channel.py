#!/usr/bin/env python3
"""E43 - does the BBH population require negative chi_eff (dynamical channel)?
Reads chi_eff samples from all cached posteriors, computes P(chi_eff<0) + credible intervals.
Prereg E43. No downloads, no RNG."""
import os, sys, json, glob
import numpy as np
import h5py

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
from e38_gw_black_hole_geometry import find_posterior_dataset  # same preferred dataset choice

CACHE = os.path.join(ROOT, "data/chains/gw_posteriors")

rows = []
for path in sorted(glob.glob(os.path.join(CACHE, "*_PE.h5"))):
    event = os.path.basename(path).replace("_PE.h5", "")
    try:
        with h5py.File(path, "r") as h:
            ds = h[find_posterior_dataset(h)]
            names = ds.dtype.names or []
            if "chi_eff" not in names:
                rows.append({"event": event, "note": "no chi_eff column"}); continue
            x = np.asarray(ds["chi_eff"], dtype=float)
    except Exception as e:
        rows.append({"event": event, "note": f"read error: {str(e)[:40]}"}); continue
    x = x[np.isfinite(x)]
    if x.size < 100:
        rows.append({"event": event, "note": "too few samples"}); continue
    p_neg = float((x < 0).mean())
    q = np.percentile(x, [2.5, 5, 50, 95, 97.5])
    rows.append({"event": event, "n": int(x.size), "median": round(float(q[2]), 3),
                 "p_neg": round(p_neg, 3), "q5": round(float(q[1]), 3), "q95": round(float(q[3]), 3),
                 "q2p5": round(float(q[0]), 3), "q97p5": round(float(q[4]), 3),
                 "ci90_all_neg": bool(q[3] < 0), "ci95_all_neg": bool(q[4] < 0)})

good = [r for r in rows if "p_neg" in r]
n = len(good)
p90 = [r for r in good if r["p_neg"] > 0.90]
p95 = [r for r in good if r["p_neg"] > 0.975]
ci95 = [r for r in good if r["ci95_all_neg"]]

D1 = len(p90) >= 2
D2 = len(ci95) >= 1

print(f"events with usable chi_eff: {n} (of {len(rows)})")
print(f"\n{'event':20s} {'median':>7} {'P(<0)':>6} {'90% CI':>16} {'95%CI<0':>7}")
for r in sorted(good, key=lambda r: -r["p_neg"])[:12]:
    print(f"{r['event']:20s} {r['median']:7.3f} {r['p_neg']:6.3f}  [{r['q5']:6.3f},{r['q95']:6.3f}] {str(r['ci95_all_neg']):>7}")
print(f"\nevents P(chi_eff<0) > 0.90: {len(p90)}  -> {[r['event'] for r in p90]}")
print(f"events P(chi_eff<0) > 0.975 (secure): {len(p95)} -> {[r['event'] for r in p95]}")
print(f"events with 95% CI entirely < 0: {len(ci95)} -> {[r['event'] for r in ci95]}")
frac_med_neg = np.mean([r["median"] < 0 for r in good])
print(f"\nfor contrast (E42-style): median chi_eff<0 fraction = {frac_med_neg:.2f}")
print(f"\nD1 (>=2 events P(<0)>0.90): {'PASS' if D1 else 'FAIL'} ({len(p90)})")
print(f"D2 (>=1 event 95% CI all<0): {'PASS' if D2 else 'FAIL'} ({len(ci95)})")

json.dump({
    "prereg": "preregs/E43_chieff_dynamical_channel_prereg.md",
    "n_events": n,
    "n_P_neg_gt_0.90": len(p90), "events_P_neg_gt_0.90": [r["event"] for r in p90],
    "n_P_neg_gt_0.975": len(p95), "events_P_neg_gt_0.975": [r["event"] for r in p95],
    "n_ci95_all_neg": len(ci95), "events_ci95_all_neg": [r["event"] for r in ci95],
    "median_neg_fraction_E42style": round(float(frac_med_neg), 3),
    "D1_pass": bool(D1), "D2_pass": bool(D2),
    "per_event": sorted(good, key=lambda r: r["median"]),
}, open(os.path.join(ROOT, "results/e43_chieff_dynamical_channel_results.json"), "w"), indent=2)
print("\nwrote results/e43_chieff_dynamical_channel_results.json")
