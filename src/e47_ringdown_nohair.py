#!/usr/bin/env python3
"""E47 - ringdown 221-overtone no-hair test (domega_221, dtau_221) in the value/shape framework.
Per-event + combined GR consistency + directional coherence. Prereg E47. Extracts zip members one
at a time (low disk). No RNG (Rayleigh analytic)."""
import os, json, math, zipfile, tempfile
import numpy as np
import h5py

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ZIP = os.path.join(ROOT, "data/chains/tgr/IGWN-GWTC3-TGR-v2-rin.zip")
zf = zipfile.ZipFile(ZIP)
members = [m for m in zf.namelist() if "Kerr_221_domega_dtau_221_0M" in m and m.endswith(".h5")]
print(f"221 joint (domega,dtau) events: {len(members)}")

# Robust Gaussian statistics per event (histogram density is too noisy for a 22-way product).
# GR credible level for a 2D Gaussian at Mahalanobis distance d: Q = 1 - exp(-d^2/2).
def gr_Q(sig): return 1.0 - math.exp(-0.5 * sig * sig)

rows = []
means = []; precisions = []   # for the Gaussian-product combination
for m in sorted(members):
    event = os.path.basename(m).split("_pyring_")[0].replace("rin_", "")
    with tempfile.NamedTemporaryFile(suffix=".h5", delete=False) as tmp:
        tmp.write(zf.read(m)); tp = tmp.name
    try:
        with h5py.File(tp, "r") as h:
            found = []
            h.visititems(lambda n, o: found.append(n) if isinstance(o, h5py.Dataset) and n.endswith("posterior_samples") else None)
            ds = h[found[0]]
            dfx = np.asarray(ds["domega_221"], float); dty = np.asarray(ds["dtau_221"], float)
    finally:
        os.remove(tp)
    ok = np.isfinite(dfx) & np.isfinite(dty)
    dfx, dty = dfx[ok], dty[ok]
    if dfx.size < 200: continue
    mu = np.array([float(np.mean(dfx)), float(np.mean(dty))])
    C = np.cov(dfx, dty)
    rho = C[0, 1] / math.sqrt(C[0, 0] * C[1, 1])
    psi = 0.5 * math.degrees(math.atan2(2 * C[0, 1], C[0, 0] - C[1, 1])) % 180.0
    Cinv = np.linalg.inv(C)
    sig = float(math.sqrt(mu @ Cinv @ mu))
    means.append(mu); precisions.append(Cinv)
    rows.append({"event": event, "domega_mean": round(float(mu[0]), 3), "dtau_mean": round(float(mu[1]), 3),
                 "phi_deg": round(math.degrees(math.atan2(mu[1], mu[0])), 1), "rho": round(rho, 3),
                 "psi": round(psi, 1), "GR_credible_level": round(gr_Q(sig), 3), "sigma_from_GR": round(sig, 2)})

n = len(rows)
# D1 combined via Gaussian product (inverse-covariance weighting) -- robust, no histogram noise
P = sum(precisions); Ccomb = np.linalg.inv(P)
mu_comb = Ccomb @ sum(Pi @ mi for Pi, mi in zip(precisions, means))
cmx, cmy = float(mu_comb[0]), float(mu_comb[1])
sig_comb = float(math.sqrt(mu_comb @ P @ mu_comb))
Q_comb = gr_Q(sig_comb)
D1 = Q_comb < 0.90
# D2
consistent = [r for r in rows if r["GR_credible_level"] < 0.90]
discrepant = [r for r in rows if r["GR_credible_level"] > 0.95]
# D3 Rayleigh
phis = np.radians([r["phi_deg"] for r in rows])
Cc, Ss = np.cos(phis).sum(), np.sin(phis).sum()
R = math.sqrt(Cc**2 + Ss**2) / n
Z = n * R**2
Ray_p = math.exp(-Z) * (1 + (2*Z - Z**2) / (4*n))
mean_dir = math.degrees(math.atan2(Ss, Cc))
D3_iso = Ray_p > 0.05

print(f"\n=== D1 combined no-hair test (Gaussian product) ===")
print(f"combined mean deviation (domega, dtau) = ({cmx:.3f}, {cmy:.3f}); combined sigma-from-GR = {sig_comb:.2f}; Q_comb = {Q_comb:.3f} -> {'CONSISTENT' if D1 else 'TENSION'}")
print(f"=== D2 per-event ===")
print(f"consistent (Q<0.90): {len(consistent)}/{n} | discrepant (Q>0.95): {len(discrepant)} {[r['event'] for r in discrepant]}")
print(f"=== D3 directional coherence ===")
print(f"R={R:.3f}, mean dir={mean_dir:.1f} deg, Rayleigh p={Ray_p:.3f} -> {'ISOTROPIC' if D3_iso else 'COHERENT'}")
print("\nmost discrepant:")
for r in sorted(rows, key=lambda r: -r["GR_credible_level"])[:6]:
    print(f"  {r['event']:14s} Q={r['GR_credible_level']:.3f} sig={r['sigma_from_GR']:.2f} dev=({r['domega_mean']:+.2f},{r['dtau_mean']:+.2f})")

json.dump({
    "prereg": "preregs/E47_ringdown_nohair_prereg.md", "n_events": n,
    "D1_combined": {"mean_dev": [round(cmx, 3), round(cmy, 3)], "sigma_from_GR": round(sig_comb,2), "Q_comb": round(Q_comb, 3), "consistent": bool(D1)},
    "D2_per_event": {"n_consistent": len(consistent), "n_discrepant": len(discrepant), "discrepant": [r["event"] for r in discrepant]},
    "D3_coherence": {"resultant_R": round(R, 3), "mean_direction_deg": round(mean_dir, 1), "rayleigh_p": round(Ray_p, 4), "isotropic": bool(D3_iso)},
    "per_event": sorted(rows, key=lambda r: -r["GR_credible_level"]),
}, open(os.path.join(ROOT, "results/e47_ringdown_nohair_results.json"), "w"), indent=2)
print("\nwrote results/e47_ringdown_nohair_results.json")
