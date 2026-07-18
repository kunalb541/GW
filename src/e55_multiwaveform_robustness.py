#!/usr/bin/env python3
"""E55 - multi-waveform robustness of E40 (chirp-mass mass-plane lawfulness).
Recompute the (m1,m2) orientation + chirp-mass prediction with IMRPhenomXPHM vs SEOBNRv4PHM
(two independent waveform families) per event; test whether the positive E40 result is
waveform-robust. Prereg E55. (The E45/E46 GR-test systematic multi-waveform check is DATA-BLOCKED:
GWTC-3 par is FTI/SEOBNR-only, IMR single-waveform -- see report.) No downloads, no RNG."""
import os, sys, json, math, glob
import numpy as np
import h5py

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, "data/chains/gw_posteriors")
WAVEFORMS = ["C01:IMRPhenomXPHM", "C01:SEOBNRv4PHM"]

def psi_chirp(m1, m2):
    s = m1 + m2
    gx = 0.6/m1 - 0.2/s; gy = 0.6/m2 - 0.2/s
    return math.degrees(math.atan2(gx, -gy)) % 180.0
def cdist(a, b):
    d = abs(a - b) % 180.0; return min(d, 180.0 - d)

def mass_psi(ds):
    m1 = np.asarray(ds["mass_1_source"], float); m2 = np.asarray(ds["mass_2_source"], float)
    ok = np.isfinite(m1) & np.isfinite(m2); m1, m2 = m1[ok], m2[ok]
    if m1.size < 200: return None
    C = np.cov(m1, m2)
    psi = 0.5 * math.degrees(math.atan2(2*C[0,1], C[0,0]-C[1,1])) % 180.0
    ar = math.sqrt(np.linalg.eigvalsh(C)[-1]/np.linalg.eigvalsh(C)[0])
    return {"psi": psi, "axr": ar, "m1med": float(np.median(m1)), "m2med": float(np.median(m2))}

rows = []
for f in sorted(glob.glob(os.path.join(CACHE, "*_PE.h5"))):
    event = os.path.basename(f).replace("_PE.h5", "")
    try:
        h = h5py.File(f, "r")
    except Exception:
        continue
    per = {}
    for wf in WAVEFORMS:
        try:
            ds = h[wf + "/posterior_samples"]
            if "mass_1_source" not in (ds.dtype.names or []): continue
            per[wf] = mass_psi(ds)
        except Exception:
            pass
    h.close()
    if len(per) < 2 or any(v is None for v in per.values()): continue
    xp = per["C01:IMRPhenomXPHM"]; sb = per["C01:SEOBNRv4PHM"]
    rows.append({"event": event,
                 "psi_phenom": round(xp["psi"], 2), "psi_seob": round(sb["psi"], 2),
                 "interwaveform_dpsi": round(cdist(xp["psi"], sb["psi"]), 2),
                 "axr_phenom": round(xp["axr"], 2), "axr_seob": round(sb["axr"], 2),
                 "dpsi_chirp_phenom": round(cdist(xp["psi"], psi_chirp(xp["m1med"], xp["m2med"])), 2),
                 "dpsi_chirp_seob": round(cdist(sb["psi"], psi_chirp(sb["m1med"], sb["m2med"])), 2)})

n = len(rows)
# elongated subset (well-defined orientation) per E40
elong = [r for r in rows if r["axr_phenom"] >= 3 and r["axr_seob"] >= 3]
med_chirp_ph = float(np.median([r["dpsi_chirp_phenom"] for r in rows]))
med_chirp_sb = float(np.median([r["dpsi_chirp_seob"] for r in rows]))
med_inter = float(np.median([r["interwaveform_dpsi"] for r in rows]))
med_inter_el = float(np.median([r["interwaveform_dpsi"] for r in elong])) if elong else None
med_chirp_ph_el = float(np.median([r["dpsi_chirp_phenom"] for r in elong])) if elong else None
med_chirp_sb_el = float(np.median([r["dpsi_chirp_seob"] for r in elong])) if elong else None

# Decisions: E40 holds for BOTH waveforms, and orientation is waveform-robust
D1 = med_chirp_ph < 12 and med_chirp_sb < 12          # chirp-mass law holds both waveforms (all)
D2 = (med_inter_el is not None) and (med_inter_el < 8) # orientation agrees across waveforms (elongated)

print(f"events with BOTH IMRPhenomXPHM and SEOBNRv4PHM: {n} (elongated axr>=3: {len(elong)})")
print(f"median |dpsi_chirp|  phenom={med_chirp_ph:.2f}  seob={med_chirp_sb:.2f}  (E40 all-events was 7.49)")
if elong:
    print(f"  elongated subset:  phenom={med_chirp_ph_el:.2f}  seob={med_chirp_sb_el:.2f}")
print(f"median inter-waveform |dpsi|: all={med_inter:.2f}  elongated={med_inter_el}")
print(f"\nD1 (chirp-mass law holds for BOTH waveforms, median|dpsi|<12): {'PASS' if D1 else 'FAIL'}")
print(f"D2 (orientation waveform-robust, elongated inter-wf |dpsi|<8): {'PASS' if D2 else 'FAIL'}")

json.dump({"prereg": "preregs/E55_multiwaveform_robustness_prereg.md",
           "n_events_both_waveforms": n, "n_elongated": len(elong),
           "median_dpsi_chirp_phenom": round(med_chirp_ph, 2), "median_dpsi_chirp_seob": round(med_chirp_sb, 2),
           "median_dpsi_chirp_phenom_elong": None if med_chirp_ph_el is None else round(med_chirp_ph_el,2),
           "median_dpsi_chirp_seob_elong": None if med_chirp_sb_el is None else round(med_chirp_sb_el,2),
           "median_interwaveform_dpsi": round(med_inter, 2),
           "median_interwaveform_dpsi_elong": None if med_inter_el is None else round(med_inter_el, 2),
           "D1_chirp_law_both_waveforms": bool(D1), "D2_orientation_waveform_robust": bool(D2),
           "E45_E46_multiwaveform": "DATA-BLOCKED: GWTC-3 par is FTI/SEOBNR-only (TIGER/IMRPhenom delayed); imr single-waveform",
           "per_event": rows},
          open(os.path.join(ROOT, "results/e55_multiwaveform_robustness_results.json"), "w"), indent=2)
print("\nwrote results/e55_multiwaveform_robustness_results.json")
