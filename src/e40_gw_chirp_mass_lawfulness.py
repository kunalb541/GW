#!/usr/bin/env python3
"""E40 - is the GW (m1,m2) posterior degeneracy the constant-chirp-mass line?
Predict mass-plane orientation from the chirp-mass tangent at median masses; compare to measured
psi (E38), with constant-total-mass as the physical null. Prereg E40. No downloads, no RNG."""
import json, os, math
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E38 = json.load(open(os.path.join(ROOT, "results/e38_gw_black_hole_geometry_results.json")))

def psi_chirp(m1, m2):
    s = m1 + m2
    gx = 0.6/m1 - 0.2/s          # d lnMc / dm1
    gy = 0.6/m2 - 0.2/s          # d lnMc / dm2
    # tangent to constant-Mc curve is perpendicular to grad: t = (-gy, gx) (or its negative)
    return math.degrees(math.atan2(gx, -gy)) % 180.0

def cdist(a, b):
    d = abs(a - b) % 180.0
    return min(d, 180.0 - d)

PSI_TOTAL = 135.0  # constant-total-mass tangent direction (1,-1)

rows = []
for e in E38["posterior_chain_geometry"]:
    pl = e["planes"].get("mass_1_source__mass_2_source")
    if not pl: continue
    m1, m2 = pl["x_median"], pl["y_median"]
    pm = pl["psi"]
    pc = psi_chirp(m1, m2)
    dc, dt = cdist(pc, pm), cdist(PSI_TOTAL, pm)
    rows.append({"event": e["event"], "m1": m1, "m2": m2, "axis_ratio": pl["axis_ratio"],
                 "rho": pl["rho"], "psi_meas": pm, "psi_chirp": round(pc, 2),
                 "psi_total": PSI_TOTAL, "dpsi_chirp": round(dc, 2), "dpsi_total": round(dt, 2),
                 "chirp_wins": dc < dt})

med_c = float(np.median([r["dpsi_chirp"] for r in rows]))
med_t = float(np.median([r["dpsi_total"] for r in rows]))
wins = sum(r["chirp_wins"] for r in rows)
elong = [r for r in rows if r["axis_ratio"] >= 3.0]
med_c_elong = float(np.median([r["dpsi_chirp"] for r in elong])) if elong else None
round_ = [r for r in rows if r["axis_ratio"] < 1.5]
med_c_round = float(np.median([r["dpsi_chirp"] for r in round_])) if round_ else None

# correlation |dpsi_chirp| vs axis_ratio (Spearman via ranks, no scipy dependency assumed)
ar = np.array([r["axis_ratio"] for r in rows]); dd = np.array([r["dpsi_chirp"] for r in rows])
def spearman(x, y):
    rx = np.argsort(np.argsort(x)); ry = np.argsort(np.argsort(y))
    rx = rx - rx.mean(); ry = ry - ry.mean()
    return float((rx@ry)/math.sqrt((rx@rx)*(ry@ry)))
rho_ar = spearman(ar, dd)

D1 = (med_c < med_t) and (wins >= 11)
D2 = (med_c_elong is not None) and (med_c_elong < 12.0)

print(f"{'event':18s} {'m1':>6} {'m2':>6} {'axr':>5} {'psi_m':>7} {'chirp':>7} {'dC':>6} {'dTot':>6} win")
for r in sorted(rows, key=lambda r: -r["axis_ratio"]):
    print(f"{r['event']:18s} {r['m1']:6.2f} {r['m2']:6.2f} {r['axis_ratio']:5.1f} "
          f"{r['psi_meas']:7.2f} {r['psi_chirp']:7.2f} {r['dpsi_chirp']:6.2f} {r['dpsi_total']:6.2f} "
          f"{'Y' if r['chirp_wins'] else '.'}")
print(f"\nmedian|dpsi| chirp={med_c:.2f}  total={med_t:.2f}  | chirp wins {wins}/{len(rows)}")
print(f"elongated (axr>=3, n={len(elong)}): median|dpsi_chirp|={med_c_elong}")
print(f"round (axr<1.5, n={len(round_)}): median|dpsi_chirp|={med_c_round}")
print(f"Spearman(|dpsi_chirp|, axis_ratio) = {rho_ar:.2f} (predict negative)")
print(f"\nD1 (chirp beats total & >=11/14): {'PASS' if D1 else 'FAIL'} (med {med_c:.2f}<{med_t:.2f}, wins {wins})")
print(f"D2 (elongated median|dpsi|<12):   {'PASS' if D2 else 'FAIL'} ({med_c_elong})")

json.dump({
    "prereg": "preregs/E40_gw_chirp_mass_lawfulness_prereg.md",
    "n_events": len(rows),
    "median_dpsi_chirp": round(med_c, 3), "median_dpsi_total": round(med_t, 3),
    "chirp_wins": wins, "n_elong_axr_ge3": len(elong),
    "median_dpsi_chirp_elong": None if med_c_elong is None else round(med_c_elong, 3),
    "median_dpsi_chirp_round": None if med_c_round is None else round(med_c_round, 3),
    "spearman_dpsi_axisratio": round(rho_ar, 3),
    "D1_pass": bool(D1), "D2_pass": bool(D2),
    "per_event": rows,
}, open(os.path.join(ROOT, "results/e40_gw_chirp_mass_lawfulness_results.json"), "w"), indent=2)
print("\nwrote results/e40_gw_chirp_mass_lawfulness_results.json")
