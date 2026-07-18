#!/usr/bin/env python3
"""E41 - which GW posterior planes are geometrically lawful?
Test locked a-priori rho-sign predictions (prereg E41, from workflow wf_a602622a-b52, agents
blind to data) against measured within-event rho across 76 LVK events. No RNG, no downloads."""
import json, os
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E38 = json.load(open(os.path.join(ROOT, "results/e38_gw_black_hole_geometry_results.json")))

# LOCKED predictions (prereg E41): plane_key -> (predicted_sign, units_artifact)
PRED = {
    "mass_1_source__mass_2_source":        ("negative", False),
    "chirp_mass_source__mass_ratio":       ("positive", True),
    "mass_ratio__chi_eff":                 ("negative", False),
    "final_mass_source__final_spin":       ("indeterminate", True),
    "luminosity_distance__cos_iota":       ("indeterminate", True),
    "redshift__total_mass_source":         ("positive", True),
}

from collections import defaultdict
P = defaultdict(list)
for e in E38["posterior_chain_geometry"]:
    for k, v in e["planes"].items():
        if v.get("rho") is not None:
            wx = abs(v["x_q16_q84"][1] - v["x_q16_q84"][0])
            wy = abs(v["y_q16_q84"][1] - v["y_q16_q84"][0])
            P[k].append((float(v["rho"]), wx, wy))

def classify(plane, pred_sign):
    rows = P[plane]
    rho = np.array([r[0] for r in rows])
    n = len(rho); med = float(np.median(rho))
    fpos = float((rho > 0).mean()); fneg = float((rho < 0).mean())
    # scale ratio (median Wx/Wy) -> is psi units-dominated?
    ratios = np.array([r[1]/r[2] for r in rows if r[2] != 0])
    wxy = float(np.median(ratios))
    units_pred = "x-dom(~0/180)" if wxy > 3 else ("y-dom(~90)" if wxy < 1/3 else "physical")

    if pred_sign in ("positive", "negative"):
        want_pos = pred_sign == "positive"
        maj = fpos if want_pos else fneg
        if maj >= 0.60 and abs(med) >= 0.15:
            verdict = "HIT"
        elif (want_pos and med < -0.15 and fneg >= 0.60) or ((not want_pos) and med > 0.15 and fpos >= 0.60):
            verdict = "MISS(wrong-sign)"
        else:
            verdict = "WEAK"
    else:  # indeterminate / ~0
        verdict = "HIT" if abs(med) < 0.15 else "SIGNAL-MISSED"
    return {"plane": plane, "n": n, "median_rho": round(med, 3),
            "frac_pos": round(fpos, 2), "frac_neg": round(fneg, 2),
            "median_Wx_Wy": round(wxy, 2), "psi_units": units_pred,
            "predicted": pred_sign, "verdict": verdict}

results = [classify(k, s) for k, (s, _) in PRED.items()]
hits = sum(1 for r in results if r["verdict"] == "HIT")

print(f"{'plane':32s} {'pred':>13} {'med_rho':>7} {'pos/neg':>9} {'Wx/Wy':>7} {'psi':>14} {'verdict':>16}")
for r in results:
    print(f"{r['plane']:32s} {r['predicted']:>13} {r['median_rho']:7.2f} "
          f"{r['frac_pos']:.2f}/{r['frac_neg']:.2f} {r['median_Wx_Wy']:7.1f} {r['psi_units']:>14} {r['verdict']:>16}")
print(f"\nHITs: {hits}/6  | units-artifact psi planes: {sum(1 for r in results if r['psi_units']!='physical')}/6")

json.dump({
    "prereg": "preregs/E41_gw_plane_lawfulness_prereg.md",
    "n_events_max": max(r["n"] for r in results),
    "hits": hits, "planes": results,
    "predictions_source": "workflow wf_a602622a-b52 (agents blind to measured rho)",
}, open(os.path.join(ROOT, "results/e41_gw_plane_lawfulness_results.json"), "w"), indent=2)
print("\nwrote results/e41_gw_plane_lawfulness_results.json")
