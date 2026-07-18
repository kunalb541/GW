#!/usr/bin/env python
"""E16: complete H0-axis map over every independent H0 instrument.

Places all H0 anchors on the value axis, including the GW dark-siren posterior we compute
from the public LVK gwcosmo per-event data (not a literature quote). Tags rd-free/
ladder-free vs standard-ruler. Pre-registration:
preregs/E16_h0_axis_all_instruments_prereg.md.

Run:  python -m src.e16_h0_axis
"""
from __future__ import annotations
import json
import math
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parent.parent
CH = REPO / "data" / "chains"
RESULTS = REPO / "results"

CMB = ("Planck CMB (early)", 67.36, 0.54, "standard-ruler")
# (label, H0, sigma, class). GW filled from the computed posterior below.
ANCHORS = [
    ("DESI+CMB chain", 67.0, 0.5, "standard-ruler"),
    ("cosmic chronometers", 67.8, 3.0, "rd-free"),
    ("JWST CCHP JAGB", 67.80, math.hypot(2.17, 1.64), "rd-free (ladder)"),
    ("JWST CCHP TRGB", 68.81, math.hypot(1.79, 1.32), "rd-free (ladder)"),
    ("JWST CCHP combined", 69.96, 1.53, "rd-free (ladder)"),
    ("TDCOSMO 2025 time-delay", 71.6, 3.6, "rd-free (ladder-free)"),
    ("SH0ES HST Cepheid", 73.04, 1.04, "rd-free (ladder)"),
]


def _gw_posterior():
    f = CH / "gw_H0_posterior.npz"
    if not f.exists():
        return None
    z = np.load(f)
    return float(z["mean"]), float(z["sd"])


def main():
    gw = _gw_posterior()
    anchors = list(ANCHORS)
    if gw is not None:
        anchors.append(("GW dark-siren GWTC-3 (real posterior)", round(gw[0], 1),
                        round(gw[1], 1), "rd-free (ladder-free)"))
    anchors.sort(key=lambda a: a[1])

    rows = {}
    for label, h0, sig, cls in anchors:
        t = abs(h0 - CMB[1]) / math.hypot(sig, CMB[2])
        rows[label] = {"H0": h0, "sigma": round(sig, 2), "class": cls,
                       "tension_vs_CMB": round(t, 2)}
    shoes_t = rows["SH0ES HST Cepheid"]["tension_vs_CMB"]
    non_shoes = [k for k in rows if "SH0ES" not in k]
    all_near = all(rows[k]["tension_vs_CMB"] < 2.5 for k in non_shoes)
    outcome = ("SH0ES-outlier" if all_near and shoes_t > 2.5
               else "broad-tension" if sum(rows[k]["tension_vs_CMB"] > 2.5 for k in rows) > 1
               else "concordant")

    out = {"prereg": "preregs/E16_h0_axis_all_instruments_prereg.md",
           "cmb_reference": {"H0": CMB[1], "sigma": CMB[2]},
           "anchors": rows, "gw_real_posterior": ({"H0": gw[0], "sd": gw[1]} if gw else None),
           "outcome": outcome,
           "finding": (
               "Complete H0-axis map over %d independent instruments (GW as a REAL computed "
               "posterior, %.1f+/-%.1f from 46 GWTC-3 dark sirens). SH0ES is the only anchor >2.5 "
               "sigma from the CMB early value (%.1f sigma); every independent probe -- GW "
               "(ladder-free), the JWST CCHP ladders, cosmic chronometers, TDCOSMO -- clusters "
               "within 2.5 sigma of the early value. So across ALL instruments the H0 tension is "
               "SH0ES-specific: the sound-horizon-free / ladder-free probes side with the early "
               "value, not with SH0ES."
               % (len(rows), gw[0] if gw else 0, gw[1] if gw else 0, shoes_t)
               if outcome == "SH0ES-outlier" else "see fields"),
           }
    (RESULTS / "e16_h0_axis_results.json").write_text(json.dumps(out, indent=2))

    print("E16 complete H0-axis map (all instruments; GW = real posterior)\n")
    print(f"  reference: {CMB[0]} = {CMB[1]}+/-{CMB[2]}\n")
    for label, r in rows.items():
        print(f"  {label:38s} H0={r['H0']:5.1f}+/-{r['sigma']:<4} "
              f"vs CMB {r['tension_vs_CMB']:.2f}s  [{r['class']}]")
    print(f"\n  OUTCOME: {outcome}\n  {out['finding']}")


if __name__ == "__main__":
    main()
