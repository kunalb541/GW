#!/usr/bin/env python3
"""E58 - massive-graviton / Lorentz-violation from GWTC-3 modified-dispersion posteriors.
Robust PER-EVENT bounds on log10(lambda_eff); alpha=0 -> graviton mass. GR-consistency check.
The COMBINED bound is prior-dependent (LVK use flat-in-A, not flat-in-log10lambda; prior samples are
empty in the release) -> reported with that caveat, NOT as the headline. Prereg E58. No RNG."""
import os, re, json, math, zipfile, tempfile
from collections import defaultdict
import numpy as np
import h5py

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ZIP = os.path.join(ROOT, "data/chains/tgr/IGWN-GWTC3-TGR-v1-liv.zip")
zf = zipfile.ZipFile(ZIP)
members = [m for m in zf.namelist() if m.endswith(".h5")]
HC_OVER_E = 1.2398419e-6  # eV*m -> m_g c^2 [eV] = HC_OVER_E / lambda_g[m]

def read_liv(member):
    with tempfile.NamedTemporaryFile(suffix=".h5", delete=False) as t:
        t.write(zf.read(member)); tp = t.name
    try:
        with h5py.File(tp, "r") as h:
            found = []
            h.visititems(lambda n, o: found.append(n) if isinstance(o, h5py.Dataset) and n.endswith("posterior_samples") else None)
            x = np.asarray(h[found[0]]["log10lambda_eff"], float)
    finally:
        os.remove(tp)
    return x[np.isfinite(x)]

def parse(m):
    mt = re.match(r"liv_(.+?)_(Aplus|Aminus)_alpha([0-9p]+)\.h5", os.path.basename(m))
    if not mt: return None
    ev, sign, a = mt.groups(); return ev, sign, a.replace("p", ".")

files = defaultdict(dict)
for m in sorted(members):
    p = parse(m)
    if p: files[(p[1], p[2])][p[0]] = m

# ---- per-event graviton (alpha=0, Aplus branch physical) ----
g_per = {}; prior_edges = []
for ev, mem in files[("Aplus", "0")].items():
    x = read_liv(mem)
    if x.size < 200: continue
    q5 = float(np.percentile(x, 5)); q95 = float(np.percentile(x, 95)); mx = float(x.max())
    prior_edges.append(mx)
    g_per[ev] = {"log10lambda_g_lower_90": round(q5, 2), "q95": round(q95, 2), "max": round(mx, 2),
                 "m_g_upper_eV": HC_OVER_E / 10**q5}
prior_edge = float(np.median(prior_edges))
# GR-consistency: q95 reaches near the prior edge (GR/large-lambda not excluded) for every event
gr_ok = all(v["q95"] >= prior_edge - 1.5 for v in g_per.values())
best = max(g_per.values(), key=lambda v: v["log10lambda_g_lower_90"])   # best single-event bound
best_mg = best["m_g_upper_eV"]; median_mg = float(np.median([v["m_g_upper_eV"] for v in g_per.values()]))

# naive flat-in-log10lambda combined bound (PRIOR-DEPENDENT, caveated -- not the LVK number)
grid = np.linspace(min(prior_edges) - 6, prior_edge + 0.5, 500)
edges = np.concatenate([[grid[0]-1], 0.5*(grid[1:]+grid[:-1]), [grid[-1]+1]])
logc = np.zeros(len(grid))
for ev, mem in files[("Aplus", "0")].items():
    x = read_liv(mem)
    if x.size < 200: continue
    hh, _ = np.histogram(x, bins=edges, density=True); logc += np.log(np.clip(hh, 1e-12, None))
c = np.exp(logc - logc.max()); c /= c.sum()
naive_comb_q5 = float(np.interp(0.05, np.cumsum(c), grid))
naive_comb_mg = HC_OVER_E / 10**naive_comb_q5

# ---- LIV per alpha: per-event MEDIAN q5 bound (robust; combination skipped due to prior/grid) ----
alphas = sorted({a for (s, a) in files}, key=float)
liv_per_alpha = {}
for a in alphas:
    row = {}
    for sign in ("Aplus", "Aminus"):
        if (sign, a) not in files: continue
        q5s = []
        for ev, mem in files[(sign, a)].items():
            x = read_liv(mem)
            if x.size >= 200: q5s.append(float(np.percentile(x, 5)))
        if q5s: row[sign] = {"median_event_log10lambda_lower_90": round(float(np.median(q5s)), 2),
                              "best_event": round(float(np.max(q5s)), 2)}
    liv_per_alpha[f"alpha={a}"] = row

D1 = gr_ok
D2 = best_mg < 1e-22   # robust per-event graviton bound order of magnitude
print(f"=== D1 GR-consistency (no LIV detection) ===")
print(f"prior edge log10lambda ~ {prior_edge:.1f}; all events q95 near edge = {gr_ok}")
print(f"\n=== D2 GRAVITON MASS (alpha=0), PER-EVENT robust bounds ===")
print(f"{'event':12s} {'log10(lambda_g/m)>':>18} {'m_g < [eV/c^2]':>16}")
for ev, v in sorted(g_per.items(), key=lambda kv: -kv[1]["log10lambda_g_lower_90"]):
    print(f"{ev:12s} {v['log10lambda_g_lower_90']:18.2f} {v['m_g_upper_eV']:16.2e}")
print(f"\nbest single-event: m_g < {best_mg:.2e} eV/c^2 | median event: m_g < {median_mg:.2e}")
print(f"naive flat-in-log10lambda combined (PRIOR-DEPENDENT, NOT the LVK bound): m_g < {naive_comb_mg:.2e}")
print(f"  [LVK GWTC-3 flat-in-A combined = 1.27e-23 eV/c^2; my naive product assumes a different prior]")
print(f"\n=== D3 LIV per order (per-event median / best log10lambda lower bound) ===")
for a, row in liv_per_alpha.items():
    print(f"  {a:10s} " + "  ".join(f"{s}: med {d['median_event_log10lambda_lower_90']} best {d['best_event']}" for s, d in row.items()))
print(f"\nD1 (GR-consistent, no LIV detection): {'PASS' if D1 else 'FAIL'}")
print(f"D2 (per-event graviton bound < 1e-22 eV): {'PASS' if D2 else 'FAIL'} (best {best_mg:.2e})")

json.dump({"prereg": "preregs/E58_massive_graviton_liv_prereg.md", "n_events": len(g_per),
           "graviton_per_event": g_per,
           "best_single_event_m_g_eV": best_mg, "median_event_m_g_eV": median_mg,
           "naive_combined_m_g_eV_PRIOR_DEPENDENT": naive_comb_mg,
           "LVK_GWTC3_combined_m_g_eV": 1.27e-23,
           "GR_consistent_no_LIV": bool(gr_ok),
           "liv_per_alpha": liv_per_alpha,
           "D1_GR_consistent": bool(D1), "D2_graviton_bound_order": bool(D2),
           "combination_caveat": "LVK use flat-in-A prior; prior samples empty in release; naive posterior-product assumes flat-in-log10lambda and is NOT the LVK combined bound"},
          open(os.path.join(ROOT, "results/e58_massive_graviton_liv_results.json"), "w"), indent=2)
print("\nwrote results/e58_massive_graviton_liv_results.json")
