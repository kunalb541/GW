#!/usr/bin/env python3
"""E42 - BH population map (Part A, descriptive) + posterior-precision lawfulness (Part B, locked).
Prereg E42. Uses E38 medians/quantiles + GWOSC SNR. No RNG, no downloads (SNR cached to /tmp)."""
import json, os, math
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E38 = json.load(open(os.path.join(ROOT, "results/e38_gw_black_hole_geometry_results.json")))
SNR = json.load(open("/tmp/gw_snr.json"))

def g(e, plane, key):
    p = e["planes"].get(plane)
    return p.get(key) if p else None

ev = []
for e in E38["posterior_chain_geometry"]:
    name = e["event"]
    mp = e["planes"].get("mass_1_source__mass_2_source")
    cp = e["planes"].get("chirp_mass_source__mass_ratio")
    if not (mp and cp): continue
    chirp = cp["x_median"]; cq = cp["x_q16_q84"]
    sig_mc = (cq[1] - cq[0]) / 2.0
    ev.append({
        "event": name, "snr": SNR.get(name),
        "m1": mp["x_median"], "m2": mp["y_median"], "q": cp["y_median"],
        "chirp": chirp, "sig_mc_frac": sig_mc / chirp if chirp else None,
        "chi_eff": g(e, "mass_ratio__chi_eff", "y_median"),
        "Mf": g(e, "final_mass_source__final_spin", "x_median"),
        "af": g(e, "final_mass_source__final_spin", "y_median"),
        "Mtot": g(e, "redshift__total_mass_source", "y_median"),
        "z": g(e, "redshift__total_mass_source", "x_median"),
        "dL": g(e, "luminosity_distance__cos_iota", "x_median"),
        # geometry vector for outlier scoring
        "geom": e["planes"],
    })

# ---------------- Part A: population map ----------------
def arr(k): return np.array([e[k] for e in ev if e[k] is not None])
m1 = arr("m1"); Mtot = arr("Mtot"); chirp = arr("chirp"); q = arr("q")
chi = arr("chi_eff"); Mf = arr("Mf"); af = arr("af"); z = arr("z")
print("=== Part A: BH population (n=%d) ===" % len(ev))
def hist(a, edges):
    h, _ = np.histogram(a, bins=edges); return dict(zip([f"{edges[i]:g}-{edges[i+1]:g}" for i in range(len(edges)-1)], h.tolist()))
print("m1 spectrum:", hist(m1, [0,10,20,30,40,50,70,110]))
print("Mtot spectrum:", hist(Mtot, [0,20,40,60,80,120,200]))
print(f"chi_eff: mean={chi.mean():.3f} median={np.median(chi):.3f} | frac<0 = {(chi<0).mean():.2f} ({int((chi<0).sum())}/{len(chi)})")
print(f"q: median={np.median(q):.3f} | q<0.5 events: {int((q<0.5).sum())}")
print(f"final mass: max={Mf.max():.1f} | Mf>100 (IMBH-scale): {[e['event'] for e in ev if e['Mf'] and e['Mf']>100]}")
print(f"low-mass (Mtot<5, BNS-like): {[e['event'] for e in ev if e['Mtot'] and e['Mtot']<5]}")

# geometric outliers: standardized per-plane (rho, log axis_ratio) across events
planes = list(ev[0]["geom"].keys())
feats = []
for e in ev:
    row = []
    for pl in planes:
        p = e["geom"].get(pl)
        row += [p["rho"], math.log10(p["axis_ratio"])] if p else [np.nan, np.nan]
    feats.append(row)
F = np.array(feats)
mu = np.nanmean(F, 0); sd = np.nanstd(F, 0)
Z = (F - mu) / sd
gdist = np.nansum(Z**2, 1) ** 0.5   # geometric Mahalanobis-ish distance (diagonal)
order = np.argsort(-gdist)
print("\ntop geometric outliers (event, geomdist, m1,q,chi_eff):")
for i in order[:6]:
    e = ev[i]; print(f"  {e['event']:18s} d={gdist[i]:5.1f}  m1={e['m1']:.1f} q={e['q']:.2f} chi_eff={e['chi_eff']:+.2f}")

# ---------------- Part B: precision lawfulness (LOCKED) ----------------
good = [e for e in ev if e["snr"] and e["sig_mc_frac"] and e["sig_mc_frac"] > 0]
x = np.log10(np.array([e["snr"] for e in good]))
y = np.log10(np.array([e["sig_mc_frac"] for e in good]))
lm = np.log10(np.array([e["chirp"] for e in good]))
n = len(good)
r = float(np.corrcoef(x, y)[0, 1])
# OLS slope
b, a = np.polyfit(x, y, 1)
# p-value for r (t-test)
t = r * math.sqrt((n - 2) / (1 - r**2));
# two-sided p via normal approx (n large-ish)
from math import erfc
p = erfc(abs(t) / math.sqrt(2))
# partial corr of y with lm controlling x (D3)
def resid(a_, b_):
    s, i = np.polyfit(a_, b_, 1); return b_ - (s*a_ + i)
ry = resid(x, y); rl = resid(x, lm)
partial = float(np.corrcoef(ry, rl)[0, 1])

D1 = (r < 0) and (abs(r) >= 0.4) and (p < 0.01)
D2 = (-1.5 <= b <= -0.5)
print("\n=== Part B: precision lawfulness (n=%d) ===" % n)
print(f"r(log sigma_Mc/Mc, log SNR) = {r:.3f}  (p={p:.2e})")
print(f"OLS slope b = {b:.3f}  (Fisher predicts -1)")
print(f"partial corr with log Mc | log SNR = {partial:.3f}  (predict positive: cycle-count)")
print(f"D1 (r<0, |r|>=0.4, p<0.01): {'PASS' if D1 else 'FAIL'}")
print(f"D2 (slope in [-1.5,-0.5]):  {'PASS' if D2 else 'FAIL'}")

json.dump({
    "prereg": "preregs/E42_bh_population_precision_prereg.md",
    "n_events": len(ev),
    "population": {
        "m1_spectrum": hist(m1, [0,10,20,30,40,50,70,110]),
        "Mtot_spectrum": hist(Mtot, [0,20,40,60,80,120,200]),
        "chi_eff_mean": round(float(chi.mean()),3), "chi_eff_frac_neg": round(float((chi<0).mean()),3),
        "q_median": round(float(np.median(q)),3),
        "IMBH_Mf_gt100": [e["event"] for e in ev if e["Mf"] and e["Mf"]>100],
        "low_mass_Mtot_lt5": [e["event"] for e in ev if e["Mtot"] and e["Mtot"]<5],
    },
    "geometric_outliers": [{"event": ev[i]["event"], "geomdist": round(float(gdist[i]),2),
                            "m1": ev[i]["m1"], "q": ev[i]["q"], "chi_eff": ev[i]["chi_eff"]} for i in order[:6]],
    "precision": {"n": n, "pearson_r": round(r,3), "p_value": p, "ols_slope": round(b,3),
                  "partial_logMc": round(partial,3), "D1_pass": bool(D1), "D2_pass": bool(D2)},
}, open(os.path.join(ROOT, "results/e42_bh_population_precision_results.json"), "w"), indent=2)
print("\nwrote results/e42_bh_population_precision_results.json")
