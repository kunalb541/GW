#!/usr/bin/env python3
"""E69 - the ruler dichotomy: does the arbiter class (ruler-free AND ladder-free H0) side with
the sound-horizon ruler (-> ladder systematic) or the ladder (-> early ingredient)? Prereg E69.
All inputs are published Gaussian summaries vetted in E16/E52 (+ masers, BAO+BBN, cited). No RNG."""
import os, json, math
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CLASSES = {
    "R (sound-horizon ruler)": {
        "Planck CMB": (67.36, 0.54),
        "DESI DR2 BAO + BBN": (68.51, 0.58),
    },
    "L (distance ladder)": {
        "SH0ES Cepheid": (73.04, 1.04),
        "JWST-CCHP (TRGB/JAGB)": (69.96, 1.53),
    },
    "F (arbiters: ruler-free & ladder-free)": {
        "cosmic chronometers": (67.80, 3.00),
        "TDCOSMO time-delay": (71.60, 3.60),
        "MCP megamasers": (73.90, 3.00),
        "GW sirens": (69.30, 12.90),
    },
}
SH0ES = CLASSES["L (distance ladder)"]["SH0ES Cepheid"]

def consensus(ms):
    w = np.array([1 / s ** 2 for _, s in ms.values()])
    x = np.array([h for h, _ in ms.values()])
    mu = float((w * x).sum() / w.sum()); sig = float(1 / math.sqrt(w.sum()))
    chi2 = float(sum(((h - mu) / s) ** 2 for h, s in ms.values()))
    return mu, sig, chi2, len(ms) - 1

def tens(a, b):
    return abs(a[0] - b[0]) / math.sqrt(a[1] ** 2 + b[1] ** 2)

def main():
    out = {"prereg": "preregs/E69_ruler_dichotomy_prereg.md", "classes": {}, }
    cons = {}
    print("=== class consensuses ===")
    for cname, ms in CLASSES.items():
        mu, sig, chi2, dof = consensus(ms)
        cons[cname] = (mu, sig)
        out["classes"][cname] = {"members": {k: {"H0": v[0], "sigma": v[1]} for k, v in ms.items()},
                                 "consensus_H0": round(mu, 2), "sigma": round(sig, 2),
                                 "chi2": round(chi2, 2), "dof": dof}
        print(f"  {cname:42s} H0 = {mu:6.2f} +/- {sig:.2f}   (chi2/dof {chi2:.1f}/{dof})")

    R = cons["R (sound-horizon ruler)"]; F = cons["F (arbiters: ruler-free & ladder-free)"]
    L = cons["L (distance ladder)"]

    tFR = tens(F, R); tFS = tens(F, SH0ES); tFL = tens(F, L); tRL = tens(R, L); tRS = tens(R, SH0ES)
    print(f"\n  t(F,R) = {tFR:.2f}   t(F,SH0ES) = {tFS:.2f}   t(F,L) = {tFL:.2f}   "
          f"t(R,L) = {tRL:.2f}   t(R,SH0ES) = {tRS:.2f}")

    # ---- D1 fork ----
    if tFR >= 2 and tFS < 1:
        d1 = "RULER IMPLICATED (early ingredient)"
    elif tFR < 1 and tFS >= 2:
        d1 = "LADDER IMPLICATED (SH0ES systematic)"
    else:
        d1 = "UNDERPOWERED/INCONCLUSIVE at current precision"
    print(f"\nD1 fork -> {d1}")

    # ---- leave-one-out within F ----
    print("\n  F leave-one-out:")
    floo = {}
    Fm = CLASSES["F (arbiters: ruler-free & ladder-free)"]
    for drop in Fm:
        sub = {k: v for k, v in Fm.items() if k != drop}
        mu, sig, _, _ = consensus(sub)
        floo[drop] = {"F_consensus": round(mu, 2), "sigma": round(sig, 2),
                      "t_vs_R": round(tens((mu, sig), R), 2), "t_vs_SH0ES": round(tens((mu, sig), SH0ES), 2)}
        print(f"    drop {drop:22s} -> F = {mu:6.2f} +/- {sig:.2f}  t(R)={floo[drop]['t_vs_R']:.2f} "
              f"t(SH0ES)={floo[drop]['t_vs_SH0ES']:.2f}")

    # ---- D2 required precision ----
    # sigma_F needed so that |mu_F - center| = 3 * sqrt(sig_F^2 + sig_center^2) for the FARTHER center
    # (i.e. F discriminates the two hypotheses at 3 sigma), holding current mu_F.
    def need_sig(center):
        gap = abs(F[0] - center[0])
        val = (gap / 3.0) ** 2 - center[1] ** 2
        return math.sqrt(val) if val > 0 else float("nan")
    sig_need_R = need_sig(R); sig_need_S = need_sig(SH0ES)
    d2 = {"current_sigma_F": round(F[1], 2),
          "sigma_F_to_reject_R_at_3sig": None if math.isnan(sig_need_R) else round(sig_need_R, 2),
          "sigma_F_to_reject_SH0ES_at_3sig": None if math.isnan(sig_need_S) else round(sig_need_S, 2),
          "note": "computed holding the current F central value fixed"}
    print(f"\nD2: sigma(F) now {F[1]:.2f}; to reject R at 3sig need <= {d2['sigma_F_to_reject_R_at_3sig']}; "
          f"to reject SH0ES at 3sig need <= {d2['sigma_F_to_reject_SH0ES_at_3sig']}")

    # ---- D3 sanity ----
    d3 = {"chi2_ok": {c: bool(out['classes'][c]['chi2'] / max(out['classes'][c]['dof'], 1) < 3)
                      for c in CLASSES},
          "R_internal_split_sigma": round(tens((67.36, 0.54), (68.51, 0.58)), 2)}
    print(f"D3: class chi2 gates {d3['chi2_ok']}; R-internal Planck-vs-BAO+BBN split = "
          f"{d3['R_internal_split_sigma']} sigma")

    out.update({"pairwise_tensions": {"F_vs_R": round(tFR, 2), "F_vs_SH0ES": round(tFS, 2),
                                      "F_vs_L": round(tFL, 2), "R_vs_L": round(tRL, 2),
                                      "R_vs_SH0ES": round(tRS, 2)},
                "D1_verdict": d1, "F_leave_one_out": floo, "D2_required_precision": d2, "D3": d3})
    json.dump(out, open(os.path.join(ROOT, "results/e69_ruler_dichotomy_results.json"), "w"), indent=2)
    print("\nwrote results/e69_ruler_dichotomy_results.json")

if __name__ == "__main__":
    main()
