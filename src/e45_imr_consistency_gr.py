#!/usr/bin/env python3
"""E45 - strong-gravity IMR-consistency test in the value/shape framework.
Reads LVK GWTC-3 imrct (ΔMf/Mf, Δaf/af) deviation posteriors, per-event + combined GR consistency
+ directional coherence (Rayleigh). Prereg E45. Extracts zip members one at a time (low disk)."""
import os, io, json, math, zipfile, tempfile
import numpy as np
import h5py

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ZIP = os.path.join(ROOT, "data/chains/tgr/IGWN-GWTC3-TGR-v1-imr.zip")

zf = zipfile.ZipFile(ZIP)
members = [m for m in zf.namelist() if m.endswith("_posterior_samples.h5")]
print(f"IMR posterior events: {len(members)}")

GRID = None
rows = []
combined_logpdf = None
for m in sorted(members):
    event = os.path.basename(m).replace("imr_", "").replace("_posterior_samples.h5", "")
    # extract to a temp file (h5py needs seekable)
    with tempfile.NamedTemporaryFile(suffix=".h5", delete=False) as tmp:
        tmp.write(zf.read(m)); tp = tmp.name
    try:
        with h5py.File(tp, "r") as h:
            if "primary/imrct" not in h: continue
            g = h["primary/imrct"]
            fmd = np.asarray(g["final_mass_deviation"], float)
            fsd = np.asarray(g["final_spin_deviation"], float)
            pdf = np.asarray(g["pdf"], float)
    finally:
        os.remove(tp)
    pdf = np.clip(pdf, 0, None)
    if pdf.sum() <= 0: continue
    pdf = pdf / pdf.sum()
    if GRID is None:
        GRID = (fmd, fsd)
        combined_logpdf = np.zeros_like(pdf)
    # accumulate combined (log to avoid underflow); assumes shared grid
    if pdf.shape == combined_logpdf.shape:
        combined_logpdf += np.log(np.clip(pdf, 1e-300, None))
    X, Y = np.meshgrid(fmd, fsd, indexing="ij")
    mx = (pdf * X).sum(); my = (pdf * Y).sum()
    cxx = (pdf * (X - mx) ** 2).sum(); cyy = (pdf * (Y - my) ** 2).sum()
    cxy = (pdf * (X - mx) * (Y - my)).sum()
    rho = cxy / math.sqrt(cxx * cyy)
    psi = 0.5 * math.degrees(math.atan2(2 * cxy, cxx - cyy)) % 180.0
    # GR credible level
    i0 = int(np.argmin(abs(fmd))); j0 = int(np.argmin(abs(fsd)))
    Q = float(pdf[pdf > pdf[i0, j0]].sum())
    # value distance sigma-from-GR (Mahalanobis of (0,0))
    C = np.array([[cxx, cxy], [cxy, cyy]]); mu = np.array([mx, my])
    sig_from_gr = float(math.sqrt(mu @ np.linalg.inv(C) @ mu))
    rows.append({"event": event, "mx": round(mx, 3), "my": round(my, 3),
                 "phi_deg": round(math.degrees(math.atan2(my, mx)), 1),
                 "rho": round(rho, 3), "psi": round(psi, 1),
                 "GR_credible_level": round(Q, 3), "sigma_from_GR": round(sig_from_gr, 2)})

n = len(rows)
print(f"processed {n} events on shared grid {GRID[0].shape if GRID else '?'}")

# ---- D1: combined deviation posterior ----
cl = combined_logpdf - combined_logpdf.max()
cpdf = np.exp(cl); cpdf /= cpdf.sum()
fmd, fsd = GRID
i0 = int(np.argmin(abs(fmd))); j0 = int(np.argmin(abs(fsd)))
Q_comb = float(cpdf[cpdf > cpdf[i0, j0]].sum())
Xc, Yc = np.meshgrid(fmd, fsd, indexing="ij")
cmx = (cpdf * Xc).sum(); cmy = (cpdf * Yc).sum()
D1 = Q_comb < 0.90

# ---- D2: per-event counts ----
consistent = [r for r in rows if r["GR_credible_level"] < 0.90]
discrepant = [r for r in rows if r["GR_credible_level"] > 0.95]

# ---- D3: Rayleigh test on mean-deviation directions ----
phis = np.radians([r["phi_deg"] for r in rows])
C_ = np.cos(phis).sum(); S_ = np.sin(phis).sum()
R = math.sqrt(C_**2 + S_**2) / n
Rayleigh_p = math.exp(-n * R**2) * (1 + (2 * n * R**2 - (n * R**2)**2) / (4 * n))  # approx
mean_dir = math.degrees(math.atan2(S_, C_))
D3_isotropic = Rayleigh_p > 0.05

print(f"\n=== D1 population combined GR test ===")
print(f"combined mean deviation (dMf/Mf, daf/af) = ({cmx:.3f}, {cmy:.3f})")
print(f"GR (0,0) combined credible level Q_comb = {Q_comb:.3f}  -> {'CONSISTENT' if D1 else 'TENSION'}")
print(f"\n=== D2 per-event ===")
print(f"GR-consistent (Q<0.90): {len(consistent)}/{n} | individually discrepant (Q>0.95): {len(discrepant)}")
if discrepant: print("  discrepant:", [(r['event'], r['GR_credible_level']) for r in discrepant])
print(f"\n=== D3 directional coherence ===")
print(f"mean resultant R={R:.3f}, direction={mean_dir:.1f} deg, Rayleigh p={Rayleigh_p:.3f} -> {'ISOTROPIC' if D3_isotropic else 'COHERENT'}")
print(f"\nmost discrepant events (by GR credible level):")
for r in sorted(rows, key=lambda r: -r["GR_credible_level"])[:6]:
    print(f"  {r['event']:14s} Q={r['GR_credible_level']:.3f} sig={r['sigma_from_GR']:.2f} dev=({r['mx']:+.2f},{r['my']:+.2f}) rho={r['rho']:+.2f}")

json.dump({
    "prereg": "preregs/E45_imr_consistency_gr_prereg.md",
    "n_events": n,
    "D1_combined": {"mean_dev": [round(cmx,3), round(cmy,3)], "Q_comb": round(Q_comb,3), "consistent": bool(D1)},
    "D2_per_event": {"n_consistent_Q_lt_0.90": len(consistent), "n_discrepant_Q_gt_0.95": len(discrepant),
                      "discrepant": [r["event"] for r in discrepant]},
    "D3_coherence": {"resultant_R": round(R,3), "mean_direction_deg": round(mean_dir,1),
                      "rayleigh_p": round(Rayleigh_p,4), "isotropic": bool(D3_isotropic)},
    "per_event": sorted(rows, key=lambda r: -r["GR_credible_level"]),
}, open(os.path.join(ROOT, "results/e45_imr_consistency_gr_results.json"), "w"), indent=2)
print("\nwrote results/e45_imr_consistency_gr_results.json")
