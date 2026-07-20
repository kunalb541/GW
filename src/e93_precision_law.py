#!/usr/bin/env python3
"""E93 - direct precision-law regression, read from the E94 posterior cache.

Model: log(sigma_Mc / Mc) = b0 + b_rho log(rho) + b_mass log(Mc_det), HC1-robust standard errors.
Provenance: `results/e94_posterior_cache.npz` is the SINGLE source; no HDF5 access here.

E42 measured an SNR slope and a partial correlation, never the joint exponents. This fits them.

GATE E IS **NOT PASSED**, and this module refuses to report otherwise. The pooled fit rejects
b_mass = 5/3. Agreement appears only inside a light-chirp-mass band whose edges (20, 40 Msun) were
chosen AFTER seeing the pooled rejection. Failure to reject inside a data-selected subset is not
positive evidence for the predicted exponent. Passing Gate E requires, at minimum:
  (i)   the expected exponent derived from the actual Fisher integral with the detector PSD, the
        event-specific f_low and the mass-dependent upper cutoff -- not the heuristic cycle count;
  (ii)  a continuous transition/interaction model with a physically declared transition variable
        (e.g. in-band inspiral cycles or f_ISCO/f_low) instead of hand-placed bins;
  (iii) an accounting of the non-random SNR availability, showing the missingness does not select
        on mass, SNR or waveform group;
  (iv)  validation on a held-out catalog or a preregistered split.
Until those exist the honest verdict is: b_rho ~ -1 is supported in the selected sample; the mass
exponent is inconsistent with a single 5/3 law and shows an EXPLORATORY mass dependence.

SNR missingness is accounted for explicitly rather than silently dropped: every event lacking a
usable SNR field is recorded with catalog and reason, and the mass distribution of kept vs dropped
events is compared so the selection is visible. Seed 93 (no stochastic estimator).
"""
import json, math, os, sys
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from src.e94_build_posterior_cache import load, CACHE, MANIFEST
from src.e95_gate_regeneration import primary_rows

SEED = 93
GR_MASS_EXPONENT = 5.0 / 3.0
POSTHOC_BANDS = ((0.0, 20.0), (20.0, 40.0), (40.0, float("inf")))
RESULT_JSON = os.path.join(ROOT, "results/e93_precision_law_results.json")


def robust_ols(y, x):
    """OLS with HC1 sandwich standard errors."""
    y = np.asarray(y, float); x = np.asarray(x, float)
    beta = np.linalg.lstsq(x, y, rcond=None)[0]
    resid = y - x @ beta
    n, k = x.shape
    xtx_inv = np.linalg.inv(x.T @ x)
    meat = x.T @ (x * (resid[:, None] ** 2))
    cov = (n / max(n - k, 1)) * xtx_inv @ meat @ xtx_inv
    se = np.sqrt(np.maximum(np.diag(cov), 0.0))
    tss = float(np.sum((y - y.mean()) ** 2))
    r2 = 1.0 - float(np.sum(resid ** 2)) / tss if tss > 0 else float("nan")
    return beta, se, r2


def fit_precision(rows):
    if len(rows) < 8:
        return {"n": len(rows), "note": "too few events to fit"}
    y = np.log([r["sigma_mc_frac"] for r in rows])
    x = np.column_stack([np.ones(len(rows)),
                         np.log([r["rho"] for r in rows]),
                         np.log([r["mc_det"] for r in rows])])
    beta, se, r2 = robust_ols(y, x)
    return {"n": len(rows), "b0": float(beta[0]), "b_rho": float(beta[1]), "b_mass": float(beta[2]),
            "se_b0_hc1": float(se[0]), "se_b_rho_hc1": float(se[1]), "se_b_mass_hc1": float(se[2]),
            "z_b_rho_plus_1": float((beta[1] + 1.0) / se[1]) if se[1] > 0 else None,
            "z_b_mass_minus_5_3": float((beta[2] - GR_MASS_EXPONENT) / se[2]) if se[2] > 0 else None,
            "r2": r2}


def load_rows(prim):
    """Rows with a usable SNR, plus an explicit record of what was dropped and why."""
    rows, missing = [], []
    for (cat, ev), v in sorted(prim.items()):
        d = v["raw"]
        mc_det_med = float(np.median(d["mcd"])) if "mcd" in d else None
        if "mcd" not in d:
            missing.append({"catalog": cat, "event": ev, "group": v["group"],
                            "reason": "no detector-frame chirp mass", "mc_det": None})
            continue
        if "snr" not in d:
            missing.append({"catalog": cat, "event": ev, "group": v["group"],
                            "reason": "no *_optimal_snr field in cached group", "mc_det": mc_det_med})
            continue
        mc = d["mcd"].astype(float); rho = d["snr"].astype(float)
        ok = np.isfinite(mc) & np.isfinite(rho) & (rho > 0)
        if ok.sum() < 200:
            missing.append({"catalog": cat, "event": ev, "group": v["group"],
                            "reason": "too few finite SNR/mass samples", "mc_det": mc_det_med})
            continue
        mc, rho = mc[ok], rho[ok]
        q16, q50, q84 = np.quantile(mc, [0.16, 0.50, 0.84])
        sigma = 0.5 * (q84 - q16)
        rows.append({"catalog": cat, "event": ev, "group": v["group"], "mc_det": float(q50),
                     "sigma_mc_det": float(sigma), "sigma_mc_frac": float(sigma / q50),
                     "rho": float(np.median(rho)), "n_samples": int(ok.sum())})
    return rows, missing


def missingness_report(rows, missing):
    """Is SNR availability selecting on mass? State it rather than assume it away."""
    kept = np.array([r["mc_det"] for r in rows], float)
    drop = np.array([m["mc_det"] for m in missing if m.get("mc_det") is not None], float)
    rep = {"n_kept": len(kept), "n_dropped": len(missing),
           "n_dropped_with_known_mass": int(len(drop)),
           "kept_mc_det_median": float(np.median(kept)) if len(kept) else None,
           "dropped_mc_det_median": float(np.median(drop)) if len(drop) else None,
           "by_catalog_kept": {}, "by_catalog_dropped": {}}
    for c in sorted({r["catalog"] for r in rows} | {m["catalog"] for m in missing}):
        rep["by_catalog_kept"][c] = sum(1 for r in rows if r["catalog"] == c)
        rep["by_catalog_dropped"][c] = sum(1 for m in missing if m["catalog"] == c)
    if len(kept) > 5 and len(drop) > 5:
        from scipy.stats import mannwhitneyu
        rep["mass_selection_test_p"] = float(mannwhitneyu(kept, drop).pvalue)
        rep["interpretation"] = ("a small p indicates SNR availability SELECTS on chirp mass, which "
                                 "would bias the mass exponent; this must be resolved before Gate E "
                                 "can pass")
    return rep


def main():
    rec = load()
    prim, _ = primary_rows(rec)
    rows, missing = load_rows(prim)
    manifest = json.load(open(MANIFEST)) if os.path.exists(MANIFEST) else {}

    bands = {}
    for lo, hi in POSTHOC_BANDS:
        sel = [r for r in rows if lo <= r["mc_det"] < hi]
        key = f"mc_{int(lo)}_{'inf' if math.isinf(hi) else int(hi)}_POSTHOC"
        bands[key] = fit_precision(sel)

    out = {
        "battery": "E93 cache-backed precision law",
        "seed": SEED,
        "model": "log(sigma_Mc/Mc) = b0 + b_rho log(rho) + b_mass log(Mc_detector), HC1 robust SE",
        "mass_exponent_reference": GR_MASS_EXPONENT,
        "provenance": {"cache": os.path.relpath(CACHE, ROOT),
                       "manifest": os.path.relpath(MANIFEST, ROOT),
                       "cache_manifest": manifest, "hdf5_accessed": False},
        "pooled": fit_precision(rows),
        "by_catalog": {c: fit_precision([r for r in rows if r["catalog"] == c])
                       for c in sorted({r["catalog"] for r in rows})},
        "posthoc_mass_bands": bands,
        "snr_missingness": missingness_report(rows, missing),
        "gate_E_status": "NOT PASSED - exploratory",
        "verdict_guard": (
            "b_rho ~ -1 is a supported result IN THE SELECTED SAMPLE. The mass-band edges (20, 40) were "
            "chosen after observing the pooled rejection of 5/3, so the light-band agreement is post-hoc: "
            "failure to reject inside a data-selected subset is NOT positive evidence for the predicted "
            "exponent. Gate E requires a Fisher-integral prediction, a continuous physically-declared "
            "transition model, resolved SNR missingness, and held-out validation."),
        "missing": missing,
        "per_event": rows,
    }
    json.dump(out, open(RESULT_JSON, "w"), indent=1)
    p = out["pooled"]
    print(f"pooled n={p['n']}: b_rho {p['b_rho']:+.3f}+/-{p['se_b_rho_hc1']:.3f} "
          f"(z={p['z_b_rho_plus_1']:+.2f}) | b_mass {p['b_mass']:+.3f}+/-{p['se_b_mass_hc1']:.3f} "
          f"(z={p['z_b_mass_minus_5_3']:+.2f})")
    for k, v in bands.items():
        if "b_mass" in v:
            print(f"  {k:>22}: n={v['n']:3d} b_mass {v['b_mass']:+.3f}+/-{v['se_b_mass_hc1']:.3f} "
                  f"z={v['z_b_mass_minus_5_3']:+.2f}   [POST-HOC]")
    ms = out["snr_missingness"]
    print(f"SNR missingness: kept {ms['n_kept']}, dropped {ms['n_dropped']}; kept/dropped median "
          f"Mc_det {ms['kept_mc_det_median']}/{ms['dropped_mc_det_median']}"
          + (f", selection p={ms['mass_selection_test_p']:.2e}" if "mass_selection_test_p" in ms else ""))
    print(f"GATE E: {out['gate_E_status']}")
    print("wrote", RESULT_JSON)


if __name__ == "__main__":
    main()
