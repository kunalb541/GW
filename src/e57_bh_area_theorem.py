#!/usr/bin/env python3
"""E57 - black-hole area theorem (Hawking's 2nd law) from GWTC-3 mergers.
A_initial from the INSPIRAL segment (progenitor masses/spins), A_final from the POSTINSPIRAL
(ringdown) segment (remnant) -- disjoint data, independent. Test P(A_final > A_initial). Prereg E57.
Seed 57 (random pairing of the two independent posteriors)."""
import os, json, math, zipfile, tempfile
import numpy as np
import h5py

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ZIP = os.path.join(ROOT, "data/chains/tgr/IGWN-GWTC3-TGR-v1-imr.zip")
zf = zipfile.ZipFile(ZIP)
members = [m for m in zf.namelist() if m.endswith("_posterior_samples.h5")]
rng = np.random.default_rng(57)

def kerr_area(M, a):
    a = np.clip(np.abs(a), 0.0, 0.9999)
    return 8 * math.pi * M**2 * (1.0 + np.sqrt(1.0 - a**2))

rows = []
stacked_z = []   # per-event standardized delta_A for a stacked meta-test
for m in sorted(members):
    event = os.path.basename(m).replace("imr_", "").replace("_posterior_samples.h5", "")
    with tempfile.NamedTemporaryFile(suffix=".h5", delete=False) as tmp:
        tmp.write(zf.read(m)); tp = tmp.name
    skip = None
    try:
        with h5py.File(tp, "r") as h:
            if "primary/posterior_samples" not in h: skip = "no posterior_samples"; raise KeyError
            ins = h["primary/posterior_samples/inspiral"]; pos = h["primary/posterior_samples/postinspiral"]
            iN = set(ins.dtype.names or []); pN = set(pos.dtype.names or [])
            need_i = {"mass_1_source", "mass_2_source", "a_1", "a_2"}; need_f = {"final_mass_source", "final_spin"}
            if not need_i <= iN: skip = f"inspiral missing {need_i - iN}"; raise KeyError
            if not need_f <= pN: skip = f"postinspiral missing {need_f - pN}"; raise KeyError
            m1 = np.asarray(ins["mass_1_source"], float); m2 = np.asarray(ins["mass_2_source"], float)
            a1 = np.asarray(ins["a_1"], float); a2 = np.asarray(ins["a_2"], float)
            Mf = np.asarray(pos["final_mass_source"], float); af = np.asarray(pos["final_spin"], float)
    except (KeyError, Exception):
        if skip: print(f"  skip {event}: {skip}")
        os.remove(tp) if os.path.exists(tp) else None; continue
    os.remove(tp)
    okI = np.isfinite(m1) & np.isfinite(m2) & np.isfinite(a1) & np.isfinite(a2)
    okF = np.isfinite(Mf) & np.isfinite(af)
    m1, m2, a1, a2 = m1[okI], m2[okI], a1[okI], a2[okI]
    Mf, af = Mf[okF], af[okF]
    if min(m1.size, Mf.size) < 200: continue
    A_init = kerr_area(m1, a1) + kerr_area(m2, a2)     # inspiral segment
    A_fin = kerr_area(Mf, af)                           # postinspiral segment
    # independent random pairing to N = min sizes
    N = min(A_init.size, A_fin.size)
    Ai = rng.permutation(A_init)[:N]; Af = rng.permutation(A_fin)[:N]
    dA = Af - Ai
    p_hold = float((dA > 0).mean())
    frac = float(np.median(dA / Ai))
    # standardized delta_A for stacking (mean / std of the paired difference)
    z = float(np.mean(dA) / (np.std(dA) + 1e-30))
    stacked_z.append(z)
    rows.append({"event": event, "P_area_theorem_holds": round(p_hold, 4),
                 "median_frac_area_increase": round(frac, 3),
                 "A_init_median": round(float(np.median(A_init)), 1),
                 "A_final_median": round(float(np.median(A_fin)), 1),
                 "z_deltaA": round(z, 2), "n_pairs": N})

n = len(rows)
violations = [r for r in rows if r["P_area_theorem_holds"] < 0.05]
strong = [r for r in rows if r["P_area_theorem_holds"] > 0.90]
# stacked meta-significance (independent events): combined z = sum(z)/sqrt(n)
comb_z = float(np.sum(stacked_z) / math.sqrt(n)) if n else 0.0

D1 = len(violations) == 0
D2 = len(strong) >= 1
print(f"events: {n}")
print(f"{'event':16s} {'P(dA>0)':>8} {'frac_incr':>9} {'A_init':>9} {'A_final':>9} {'z':>6}")
for r in sorted(rows, key=lambda r: r["P_area_theorem_holds"]):
    print(f"{r['event']:16s} {r['P_area_theorem_holds']:8.3f} {r['median_frac_area_increase']:9.2f} "
          f"{r['A_init_median']:9.1f} {r['A_final_median']:9.1f} {r['z_deltaA']:6.2f}")
print(f"\nP(dA>0)>0.90 (strong): {len(strong)} | violations P<0.05: {len(violations)} {[r['event'] for r in violations]}")
print(f"stacked combined z (area increase): {comb_z:.2f}sigma")
print(f"\nD1 (no violation P<0.05): {'PASS' if D1 else 'FAIL'}")
print(f"D2 (>=1 strong confirmation P>0.90): {'PASS' if D2 else 'FAIL'} ({len(strong)})")

json.dump({"prereg": "preregs/E57_bh_area_theorem_prereg.md", "n_events": n,
           "n_strong_confirm": len(strong), "n_violations": len(violations),
           "violation_events": [r["event"] for r in violations],
           "stacked_combined_z_sigma": round(comb_z, 2),
           "D1_no_violation": bool(D1), "D2_strong_confirmation": bool(D2),
           "per_event": sorted(rows, key=lambda r: -r["P_area_theorem_holds"])},
          open(os.path.join(ROOT, "results/e57_bh_area_theorem_results.json"), "w"), indent=2)
print("\nwrote results/e57_bh_area_theorem_results.json")
