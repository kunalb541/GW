#!/usr/bin/env python3
"""E46 - parameterized PN-deviation tests (dchi_i) in the value/shape framework.
Per-parameter combined GR bound + cross-event sign coherence. Prereg E46.
Extracts zip members one at a time (low disk). No RNG (binomial is exact)."""
import os, io, json, math, zipfile, tempfile
from collections import defaultdict
import numpy as np
import h5py

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ZIP = os.path.join(ROOT, "data/chains/tgr/IGWN-GWTC3-TGR-v1-par.zip")
zf = zipfile.ZipFile(ZIP)
members = [m for m in zf.namelist() if m.endswith(".h5")]

def dev_col(ds):
    for n in (ds.dtype.names or []):
        if n.lower().startswith("dchi"): return n
    return None

# per (event,param): samples
data = defaultdict(dict)   # param -> event -> samples
for m in sorted(members):
    base = os.path.basename(m).replace("par_", "").replace(".h5", "")  # <event>_seob_<param>
    parts = base.split("_seob_")
    if len(parts) != 2: continue
    event, param = parts
    with tempfile.NamedTemporaryFile(suffix=".h5", delete=False) as tmp:
        tmp.write(zf.read(m)); tp = tmp.name
    try:
        with h5py.File(tp, "r") as h:
            found = []
            h.visititems(lambda n, o: found.append(n) if isinstance(o, h5py.Dataset) and n.endswith("posterior_samples") else None)
            if not found: continue
            ds = h[found[0]]; col = dev_col(ds)
            if not col: continue
            x = np.asarray(ds[col], float)
    finally:
        os.remove(tp)
    x = x[np.isfinite(x)]
    if x.size > 6000: x = x[np.linspace(0, x.size-1, 6000).astype(int)]
    data[param][event] = x

params = sorted(data.keys())
events = sorted({e for p in data for e in data[p]})
print(f"parameters: {len(params)} {params}")
print(f"events: {len(events)}")

def binom_two_sided(k, n, p=0.5):
    from math import comb
    def pmf(i): return comb(n, i) * p**i * (1-p)**(n-i)
    p0 = pmf(k)
    return min(1.0, sum(pmf(i) for i in range(n+1) if pmf(i) <= p0 + 1e-12))

per_param = []
n_evparam_consistent = 0; n_evparam_total = 0
for param in params:
    evs = data[param]
    # common grid from pooled range
    allx = np.concatenate(list(evs.values()))
    lo, hi = np.percentile(allx, 0.5), np.percentile(allx, 99.5)
    pad = 0.2*(hi-lo); grid = np.linspace(lo-pad, hi+pad, 600)
    logcomb = np.zeros_like(grid)
    npos = 0; per_event = []
    for ev, x in evs.items():
        # histogram density on grid
        hh, edges = np.histogram(x, bins=np.linspace(lo-pad, hi+pad, 121), density=True)
        cen = 0.5*(edges[:-1]+edges[1:]); dens = np.interp(grid, cen, hh)
        logcomb += np.log(np.clip(dens, 1e-6, None))
        med = float(np.median(x)); npos += med > 0
        # per-event GR consistency: is 0 within 90% CI
        q5, q95 = np.percentile(x, [5, 95]); inside = (q5 <= 0 <= q95)
        n_evparam_consistent += inside; n_evparam_total += 1
        per_event.append({"event": ev, "median": round(med, 4), "in90": bool(inside)})
    comb = np.exp(logcomb - logcomb.max()); comb /= comb.sum()
    c = np.cumsum(comb)
    cq = lambda q: float(np.interp(q, c, grid))
    clo, cmed, chi = cq(0.05), cq(0.5), cq(0.95)
    gr_inside = (clo <= 0 <= chi)
    n = len(evs); bp = binom_two_sided(npos, n)
    per_param.append({"param": param, "combined_median": round(cmed, 4),
                      "combined_ci90": [round(clo, 4), round(chi, 4)], "GR_inside": bool(gr_inside),
                      "n_events": n, "n_pos": npos, "sign_binom_p": round(bp, 4),
                      "coherent_p05": bool(bp < 0.05), "coherent_bonf": bool(bp < 0.005)})

D1 = all(p["GR_inside"] for p in per_param)
frac_ev = n_evparam_consistent / n_evparam_total
coh05 = [p["param"] for p in per_param if p["coherent_p05"]]
cohB = [p["param"] for p in per_param if p["coherent_bonf"]]

print(f"\n{'param':10s} {'comb_med':>9} {'comb 90% CI':>20} {'GR?':>4} {'+/n':>5} {'signp':>7} {'coh'}")
for p in per_param:
    print(f"{p['param']:10s} {p['combined_median']:9.3f}  [{p['combined_ci90'][0]:7.3f},{p['combined_ci90'][1]:7.3f}] "
          f"{'in' if p['GR_inside'] else 'OUT':>4} {p['n_pos']}/{p['n_events']:>1} {p['sign_binom_p']:7.3f} "
          f"{'*' if p['coherent_p05'] else ''}{'*BONF' if p['coherent_bonf'] else ''}")
print(f"\nD1 (all params GR-consistent combined): {'PASS' if D1 else 'FAIL'} ({sum(p['GR_inside'] for p in per_param)}/{len(per_param)})")
print(f"D2 (per event-param 0 in 90% CI): {frac_ev:.2f} ({n_evparam_consistent}/{n_evparam_total})")
print(f"D3 sign-coherent params p<0.05: {coh05 or 'none'} | Bonferroni p<0.005: {cohB or 'none'}")

json.dump({
    "prereg": "preregs/E46_parameterized_deviations_prereg.md",
    "n_params": len(params), "n_events": len(events),
    "D1_all_GR_consistent": bool(D1),
    "D2_frac_event_param_consistent": round(frac_ev, 3),
    "D3_coherent_p05": coh05, "D3_coherent_bonferroni": cohB,
    "per_parameter": per_param,
}, open(os.path.join(ROOT, "results/e46_parameterized_deviations_results.json"), "w"), indent=2)
print("\nwrote results/e46_parameterized_deviations_results.json")
