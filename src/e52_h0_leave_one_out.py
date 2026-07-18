#!/usr/bin/env python3
"""E52 - H0 anchor leave-one-out / leave-two-out: is the H0 tension SH0ES-sensitive?
Inverse-variance consensus of independent late-time H0 anchors, LOO/LTO tension vs the CMB/early
value. Prereg E52. Inputs from E16 (no anchor re-derived). No RNG."""
import os, json, math, itertools
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CMB = (67.36, 0.54)          # early-universe reference (Planck)
EARLY_RULER = (67.0, 0.5)    # DESI+CMB (shown for context, not in late-time consensus)

# Non-redundant INDEPENDENT late-time anchors (JWST-CCHP combined used once; JAGB/TRGB are its
# components and are NOT added separately to avoid double-counting).
LATE = {
    "cosmic chronometers": (67.80, 3.00),
    "JWST-CCHP combined":  (69.96, 1.53),
    "GW dark sirens":      (69.30, 12.90),
    "TDCOSMO time-delay":  (71.60, 3.60),
    "SH0ES Cepheid":       (73.04, 1.04),
}

def consensus(anchors):
    """inverse-variance-weighted mean + its sigma."""
    w = np.array([1/s**2 for _, s in anchors.values()])
    x = np.array([h for h, _ in anchors.values()])
    mu = float(np.sum(w*x)/np.sum(w)); sig = float(1/math.sqrt(np.sum(w)))
    return mu, sig

def tens(a, b):  # a,b = (val,sig)
    return abs(a[0]-b[0])/math.sqrt(a[1]**2+b[1]**2)

def chi2_around(anchors, center):
    return float(sum(((h-center)/s)**2 for h, s in anchors.values()))

# D1: individual anchor tensions vs CMB
indiv = {k: round(tens(v, CMB), 2) for k, v in LATE.items()}
outliers = [k for k, t in indiv.items() if t > 2.5]

# Full late-time consensus + tension vs CMB
mu_all, sig_all = consensus(LATE)
t_all = tens((mu_all, sig_all), CMB)
chi2_all = chi2_around(LATE, mu_all); dof_all = len(LATE)-1

# Leave-one-out
loo = {}
for drop in LATE:
    sub = {k: v for k, v in LATE.items() if k != drop}
    mu, sig = consensus(sub)
    loo[drop] = {"consensus_H0": round(mu, 2), "sigma": round(sig, 2),
                 "tension_vs_CMB": round(tens((mu, sig), CMB), 2)}

# Leave-two-out (always dropping SH0ES + one more)
lto = {}
for drop in [k for k in LATE if k != "SH0ES Cepheid"]:
    sub = {k: v for k, v in LATE.items() if k not in ("SH0ES Cepheid", drop)}
    mu, sig = consensus(sub)
    lto[f"SH0ES+{drop}"] = {"consensus_H0": round(mu, 2), "tension_vs_CMB": round(tens((mu, sig), CMB), 2)}

# Mutual consistency of the non-SH0ES late-time anchors
noSH = {k: v for k, v in LATE.items() if k != "SH0ES Cepheid"}
mu_no, sig_no = consensus(noSH)
chi2_no = chi2_around(noSH, mu_no); dof_no = len(noSH)-1
maxpair_no = max(tens(a, b) for a, b in itertools.combinations(noSH.values(), 2))

D1 = (outliers == ["SH0ES Cepheid"])
D2 = (t_all > 2.5) and (loo["SH0ES Cepheid"]["tension_vs_CMB"] < 2.0)
D3 = (chi2_no/dof_no < 2.0) and (maxpair_no < 2.5)

print(f"individual tension vs CMB: {indiv}")
print(f"  >2.5sigma outliers: {outliers}")
print(f"\nfull late-time consensus H0 = {mu_all:.2f} +/- {sig_all:.2f}  (tension vs CMB {t_all:.2f}sigma; chi2/dof {chi2_all:.1f}/{dof_all})")
print(f"\nLEAVE-ONE-OUT (consensus + tension vs CMB):")
for k, v in loo.items():
    print(f"  drop {k:22s} -> H0 {v['consensus_H0']:.2f}+/-{v['sigma']:.2f}  tension {v['tension_vs_CMB']:.2f}")
print(f"\nno-SH0ES late-time anchors: consensus {mu_no:.2f}+/-{sig_no:.2f}, tension {tens((mu_no,sig_no),CMB):.2f}, "
      f"chi2/dof {chi2_no:.1f}/{dof_no}, max pairwise {maxpair_no:.2f}sigma")
print(f"\nD1 (SH0ES sole >2.5sigma outlier): {'PASS' if D1 else 'FAIL'} ({outliers})")
print(f"D2 (dropping SH0ES collapses tension >2.5 -> <2.0): {'PASS' if D2 else 'FAIL'} ({t_all:.2f} -> {loo['SH0ES Cepheid']['tension_vs_CMB']:.2f})")
print(f"D3 (non-SH0ES anchors mutually consistent): {'PASS' if D3 else 'FAIL'} (chi2/dof {chi2_no/dof_no:.2f}, maxpair {maxpair_no:.2f})")

json.dump({"prereg": "preregs/E52_h0_leave_one_out_prereg.md",
           "cmb_ref": CMB, "individual_tension_vs_CMB": indiv, "outliers_gt_2.5sigma": outliers,
           "full_consensus": {"H0": round(mu_all,2), "sigma": round(sig_all,2), "tension_vs_CMB": round(t_all,2),
                               "chi2": round(chi2_all,2), "dof": dof_all},
           "leave_one_out": loo, "leave_two_out_with_SH0ES": lto,
           "no_SH0ES": {"consensus_H0": round(mu_no,2), "sigma": round(sig_no,2),
                        "tension_vs_CMB": round(tens((mu_no,sig_no),CMB),2),
                        "chi2_over_dof": round(chi2_no/dof_no,2), "max_pairwise_sigma": round(maxpair_no,2)},
           "D1_SH0ES_sole_outlier": bool(D1), "D2_SH0ES_drives_tension": bool(D2), "D3_others_consistent": bool(D3)},
          open(os.path.join(ROOT, "results/e52_h0_leave_one_out_results.json"), "w"), indent=2)
print("\nwrote results/e52_h0_leave_one_out_results.json")
