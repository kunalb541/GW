#!/usr/bin/env python3
"""E44 - hierarchical chi_eff population: does it require support below zero?
Gaussian population fit (Roulet-Zaldarriaga/LVK) via MC hierarchical likelihood over 74 events'
posterior samples + a positive-truncation model comparison. Prereg E44. No downloads, no RNG."""
import os, sys, json, glob, math
import numpy as np
import h5py

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
from e38_gw_black_hole_geometry import find_posterior_dataset
CACHE = os.path.join(ROOT, "data/chains/gw_posteriors")

# ---- load chi_eff samples + median mass_ratio per event (deterministic subsample) ----
events = []      # chi_eff sample arrays
qmeds = []       # per-event median mass_ratio (for the induced chi_eff prior)
for path in sorted(glob.glob(os.path.join(CACHE, "*_PE.h5"))):
    try:
        with h5py.File(path, "r") as h:
            ds = h[find_posterior_dataset(h)]
            names = ds.dtype.names or []
            if "chi_eff" not in names: continue
            x = np.asarray(ds["chi_eff"], dtype=float)
            q = np.asarray(ds["mass_ratio"], dtype=float) if "mass_ratio" in names else None
    except Exception:
        continue
    m = np.isfinite(x); x = x[m]
    if x.size < 200: continue
    idx = np.linspace(0, x.size - 1, min(x.size, 3000)).astype(int)
    events.append(x[idx])
    qmeds.append(float(np.median(q[np.isfinite(q)])) if q is not None else 0.7)
n_ev = len(events)
print(f"events with chi_eff: {n_ev}")

# ---- induced chi_eff prior via seeded simulation of the standard spin prior ----
# isotropic spins, magnitude ~ Uniform(0, 0.99); chi_eff = (a1 cos t1 + q a2 cos t2)/(1+q).
# Reweight posterior samples by 1/p_prior(chi_eff|q). Seeded -> deterministic/reproducible.
rng = np.random.default_rng(44)
NSIM = 400000
_edges = np.linspace(-1, 1, 401)
_cen = 0.5 * (_edges[:-1] + _edges[1:])
def prior_interp(q):
    a1 = rng.uniform(0, 0.99, NSIM); a2 = rng.uniform(0, 0.99, NSIM)
    c1 = rng.uniform(-1, 1, NSIM); c2 = rng.uniform(-1, 1, NSIM)
    chi = (a1 * c1 + q * a2 * c2) / (1 + q)
    hh, _ = np.histogram(chi, bins=_edges, density=True)
    hh = np.clip(hh, 1e-6, None)
    return lambda v: np.interp(v, _cen, hh)
weights = []
for x, q in zip(events, qmeds):
    p = prior_interp(q)(x)
    w = 1.0 / np.clip(p, 1e-6, None)
    weights.append(w / w.sum())

# ---- grid hierarchical likelihood (weighted) ----
mus = np.linspace(-0.20, 0.30, 101)
sigs = np.linspace(0.01, 0.40, 101)
INV_SQRT_2PI = 1.0 / math.sqrt(2 * math.pi)
def norm_pdf(x, mu, s): return INV_SQRT_2PI / s * np.exp(-0.5 * ((x - mu) / s) ** 2)

def cred(vals, w, qs=(0.05, 0.5, 0.95)):
    order = np.argsort(vals); v = vals[order]; ww = w[order]; c = np.cumsum(ww) / ww.sum()
    return [float(np.interp(q, c, v)) for q in qs]

def fit(evs, wts):
    """wts: per-event sample weights (or None for flat). Returns results dict."""
    logL = np.zeros((len(mus), len(sigs)))
    for x, w in zip(evs, wts):
        for js, s in enumerate(sigs):
            z = (x[None, :] - mus[:, None]) / s
            pdf = INV_SQRT_2PI / s * np.exp(-0.5 * z * z)     # (nmu, nsamp)
            m = (pdf * w[None, :]).sum(axis=1)                # weighted mean (w normalized)
            logL[:, js] += np.log(np.clip(m, 1e-300, None))
    off = logL.max(); post = np.exp(logL - off); post /= post.sum()
    p_mu = post.sum(1); p_sig = post.sum(0)
    mu_lo, mu_med, mu_hi = cred(mus, p_mu)
    sig_lo, sig_med, sig_hi = cred(sigs, p_sig)
    MU, SIG = np.meshgrid(mus, sigs, indexing="ij")
    FNEG = 0.5 * (1 + np.vectorize(math.erf)(-MU / (SIG * math.sqrt(2))))
    fn_lo, fn_med, fn_hi = cred(FNEG.ravel(), post.ravel())
    imu, isig = np.unravel_index(np.argmax(logL), logL.shape)
    mu_map, sig_map = mus[imu], sigs[isig]
    # free vs positive-truncated max-lnL
    def free_lnL(mu, s):
        return sum(math.log(max((norm_pdf(x, mu, s) * w).sum(), 1e-300)) for x, w in zip(evs, wts))
    lnL_free = free_lnL(mu_map, sig_map)
    best_tr = -1e18; best_pt = None
    for mu in mus[mus >= 0]:
        for s in sigs:
            Z = 0.5 * math.erfc(-mu / (s * math.sqrt(2)))
            tot = 0.0
            for x, w in zip(evs, wts):
                pos = x >= 0
                m = (norm_pdf(x[pos], mu, s) * w[pos]).sum() / Z if pos.any() else 1e-300
                tot += math.log(max(m, 1e-300))
            if tot > best_tr: best_tr = tot; best_pt = (float(mu), float(s))
    return {"mu": {"map": round(mu_map,3), "ci90": [round(mu_lo,3), round(mu_hi,3)], "median": round(mu_med,3)},
            "sigma": {"map": round(sig_map,3), "ci90": [round(sig_lo,3), round(sig_hi,3)], "median": round(sig_med,3)},
            "f_neg": {"ci90": [round(fn_lo,3), round(fn_hi,3)], "median": round(fn_med,3)},
            "truncated_best": {"mu": round(best_pt[0],3), "sigma": round(best_pt[1],3)},
            "delta_lnL": round(lnL_free - best_tr, 2),
            "D1_pass": bool(sig_lo > 0.05), "D2_pass": bool(fn_lo > 0.05), "D3_pass": bool(lnL_free - best_tr >= 3.0)}

flat_w = [np.full(x.size, 1.0/x.size) for x in events]
res_flat = fit(events, flat_w)
res_rw = fit(events, weights)

def show(tag, r):
    print(f"\n=== {tag} ===")
    print(f"  mu    = {r['mu']['map']}  90% CI {r['mu']['ci90']}")
    print(f"  sigma = {r['sigma']['map']}  90% CI {r['sigma']['ci90']}")
    print(f"  f_neg = {r['f_neg']['median']}  90% CI {r['f_neg']['ci90']}")
    print(f"  free-vs-truncated delta lnL = {r['delta_lnL']}  (truncated best mu={r['truncated_best']['mu']})")
    print(f"  D1(sigma>0.05):{'PASS' if r['D1_pass'] else 'FAIL'}  D2(f_neg>0.05):{'PASS' if r['D2_pass'] else 'FAIL'}  D3(dlnL>=3):{'PASS' if r['D3_pass'] else 'FAIL'}")
show("FLAT effective prior (locked primary, conservative)", res_flat)
show("PRIOR-REWEIGHTED (induced chi_eff prior divided out)", res_rw)

json.dump({
    "prereg": "preregs/E44_chieff_hierarchical_prereg.md",
    "n_events": n_ev,
    "flat_effective_prior": res_flat,
    "prior_reweighted": res_rw,
    "note": "flat = locked primary (conservative, biases sigma low); reweighted = pre-anticipated proper analysis (seed 44)",
}, open(os.path.join(ROOT, "results/e44_chieff_hierarchical_results.json"), "w"), indent=2)
print("\nwrote results/e44_chieff_hierarchical_results.json")
