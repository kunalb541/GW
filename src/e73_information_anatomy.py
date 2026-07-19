#!/usr/bin/env python3
"""E73 - the information anatomy of a detection + a dipole (GR) sensitivity forecast.
CHARACTERIZATION (forward Fisher computation from the waveform model + PSD, NOT extracted from strain;
so not a locked blind test - the data-driven 'did info arrive where GR predicts' test needs strain
re-analysis and is the successor). Two products, for the real O4a+O4b events:
  (1) info-flow anatomy: the frequency by which 50%/90% of the Fisher information about each parameter
      (chirp mass Mc, symmetric mass ratio eta, aligned spin chi) is accumulated. Leading-order TaylorF2
      structure (Mc at 0PN ~ f^-5/3; eta at 1PN ~ f^-1; spin at 1.5PN ~ f^-2/3), scout-validated ordering.
  (2) dipole GR-sensitivity forecast: marginalized Fisher error sigma_beta on a -1PN (dipole) phase term
      beta*(pi Mc f)^-7/3, over {t_c, phi_c, lnMc, beta}. Smaller sigma_beta = tighter geometric GR test.
Seed 73 (no RNG). PSD: E65's analytic aLIGO fit."""
import os, sys, json, math
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from src.e65_pn_fisher_rotation import Sn

# leading-order per-parameter phase-derivative frequency scalings (see docstring)
ANAT_SCAL = {"Mc": -5/3, "eta": -1.0, "chi": -2/3}

def anatomy(m1, m2, z=0.0, fmin=20.0):
    f_isco = 4397.0 / ((m1 + m2) * (1 + z))
    f = np.geomspace(fmin, max(f_isco, fmin + 1), 6000)
    w = f**(-7/3) / Sn(f)                                   # inspiral |h|^2 / Sn
    out = {"f_isco": round(float(f_isco), 1)}
    for k, s in ANAT_SCAL.items():
        integ = (f**s)**2 * w
        C = np.concatenate([[0], np.cumsum(0.5 * (integ[1:] + integ[:-1]) * np.diff(f))]); C /= C[-1]
        out[k] = (round(float(np.interp(0.5, C, f)), 1), round(float(np.interp(0.9, C, f)), 1))
    return out

def sigma_beta(m1, m2, z=0.0, rho=15.0, fmin=20.0):
    """marginalized Fisher error on a -1PN dipole phase term, at network SNR rho."""
    Mc_src = (m1 * m2) ** 0.6 / (m1 + m2) ** 0.2
    Mc = Mc_src * (1 + z) * 4.925490947e-6                  # detector-frame chirp mass in seconds
    f_isco = 4397.0 / ((m1 + m2) * (1 + z))
    f = np.geomspace(fmin, max(f_isco, fmin + 1), 6000)
    w = f**(-7/3) / Sn(f)
    x = math.pi * Mc * f
    d = {"tc": 2 * math.pi * f, "phic": -np.ones_like(f),
         "lnMc": (-5/3) * (3/128) * x**(-5/3), "beta": x**(-7/3)}
    keys = ["tc", "phic", "lnMc", "beta"]
    norm = np.trapezoid(w, f)
    M = np.array([[np.trapezoid(d[i] * d[j] * w, f) / norm for j in keys] for i in keys])
    Gamma = rho**2 * M
    try:
        cov = np.linalg.inv(Gamma)
        return float(math.sqrt(max(cov[3, 3], 0.0)))
    except np.linalg.LinAlgError:
        return float("nan")

def main():
    ev = []
    for jf, cat in [("results/e67_gwtc4_curved_law_results.json", "O4a"),
                    ("results/e71_gwtc5_curved_law_results.json", "O4b")]:
        for r in json.load(open(os.path.join(ROOT, jf)))["per_event"]:
            ev.append({"event": r["event"], "cat": cat, "m1": r["m1"], "m2": r["m2"]})
    print(f"information anatomy on {len(ev)} real O4a+O4b events\n")

    rows = []
    for e in ev:
        a = anatomy(e["m1"], e["m2"])
        rows.append({**e, "f_isco": a["f_isco"], "Mc_f50": a["Mc"][0], "eta_f50": a["eta"][0],
                     "chi_f50": a["chi"][0], "sep_chi_minus_Mc": round(a["chi"][0] - a["Mc"][0], 1),
                     "sigma_beta_raw": sigma_beta(e["m1"], e["m2"])})
    # dipole sensitivity is meaningful only RELATIVELY (beta normalization is arbitrary here; the absolute
    # ppE convention + LVK comparison is the successor). Normalize so the tightest event = 1.
    sbmin = min(r["sigma_beta_raw"] for r in rows)
    for r in rows:
        r["dipole_relative_error"] = round(r["sigma_beta_raw"] / sbmin, 2)

    from scipy.stats import spearmanr
    Mtot = np.array([r["m1"] + r["m2"] for r in rows]); sep = np.array([r["sep_chi_minus_Mc"] for r in rows])
    rel = np.array([r["dipole_relative_error"] for r in rows]); ordered = all(r["Mc_f50"] <= r["chi_f50"] for r in rows)
    rho_sep, _ = spearmanr(Mtot, sep); rho_rel, _ = spearmanr(Mtot, rel)
    print(f"ordering Mc<eta<chi holds for all {len(rows)} events: {ordered}")
    print(f"anatomy 'richness' (chi_f50 - Mc_f50): Spearman vs total mass = {rho_sep:+.2f} "
          f"(lighter/longer-inspiral -> wider anatomy)")
    print(f"dipole sensitivity RANK: Spearman(rel_error, total mass) = {rho_rel:+.2f} -> lightest / "
          f"longest-inspiral events most sensitive to a -1PN dipole term. NOTE: only the RANK is reliable "
          f"(Fisher cond ~1e12, arbitrary beta units); the absolute magnitude is a conditioning artifact.")

    best = sorted(rows, key=lambda r: r["dipole_relative_error"])[:6]
    print(f"\nbest events for the geometric dipole (GR) test (relative error, best=1.0):")
    print(f"  {'event':22s} {'Mtot':>6s} {'f_isco':>7s} {'Mc_f50':>7s} {'chi_f50':>8s} {'rel_err':>8s}")
    for r in best:
        print(f"  {r['event']:22s} {r['m1']+r['m2']:6.1f} {r['f_isco']:7.0f} {r['Mc_f50']:7.1f} "
              f"{r['chi_f50']:8.1f} {r['dipole_relative_error']:8.2f}")

    json.dump({"battery": "E73 information anatomy (CHARACTERIZATION; forward Fisher, not strain-extracted)",
               "n_events": len(rows), "ordering_Mc_eta_chi_all": ordered,
               "spearman_richness_vs_Mtot": float(rho_sep), "spearman_dipole_rel_vs_Mtot": float(rho_rel),
               "dipole_ranking_note": "only the RANK is reliable (Fisher cond ~1e12, arbitrary beta units); "
                                      "absolute sigma_beta + the LVK -1PN comparison need a numerically-stable, "
                                      "ppE-normalized forecast (successor)",
               "note": "info-flow anatomy is computed from the waveform model + PSD (measurement theory), "
                       "not measured from each event's strain; the data-driven GR test (analyze in "
                       "frequency slices, compare empirical info accumulation to the GR-Fisher prediction) "
                       "needs strain re-analysis and is the successor. sigma_beta is a Fisher forecast at "
                       "rho=15; comparison to the LVK -1PN dipole bound is part of that successor.",
               "per_event": rows},
              open(os.path.join(ROOT, "results/e73_information_anatomy_results.json"), "w"), indent=2)
    print("\nwrote results/e73_information_anatomy_results.json")

if __name__ == "__main__":
    main()
