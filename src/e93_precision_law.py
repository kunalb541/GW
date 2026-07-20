#!/usr/bin/env python3
"""E93 - direct precision-law regression for chirp-mass posterior width.

Fits log(sigma_Mc/Mc) = b0 + b_rho log(rho) + b_M log(Mc_det) with robust uncertainties and records
the post-hoc nature of mass-band splits. O4a/O4b only: GWTC-3 was the E42 discovery sample and the
local O4 files expose network_optimal_snr inconsistently. Seed 93 (no stochastic estimator).
"""
import json
import math
import os
import sys

import h5py
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from src.e91_curve_submission_gates import CATALOGS, aligned_samples, event_name
from src.e71_gwtc5_curved_law import pick_group

RESULT_JSON = os.path.join(ROOT, "results/e93_precision_law_results.json")
GR_MASS_EXPONENT = 5.0 / 3.0


def robust_ols(y, x):
    y = np.asarray(y, float)
    x = np.asarray(x, float)
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
    y = np.log([r["sigma_mc_frac"] for r in rows])
    x = np.column_stack([
        np.ones(len(rows)),
        np.log([r["rho"] for r in rows]),
        np.log([r["mc_det"] for r in rows]),
    ])
    beta, se, r2 = robust_ols(y, x)
    return {
        "n": len(rows),
        "b0": float(beta[0]),
        "b_rho": float(beta[1]),
        "b_mass": float(beta[2]),
        "se_b0_hc1": float(se[0]),
        "se_b_rho_hc1": float(se[1]),
        "se_b_mass_hc1": float(se[2]),
        "z_b_rho_plus_1": float((beta[1] + 1.0) / se[1]) if se[1] > 0 else None,
        "z_b_mass_minus_5_3": float((beta[2] - GR_MASS_EXPONENT) / se[2]) if se[2] > 0 else None,
        "r2": r2,
    }


def load_rows():
    rows, missing = [], []
    for cat, data_dir in CATALOGS.items():
        for name in sorted(os.listdir(data_dir)):
            if not (name.startswith("GW") and name.endswith(".hdf5")):
                continue
            fp = os.path.join(data_dir, name)
            ev = event_name(fp)
            with h5py.File(fp, "r") as h:
                g = pick_group(h)
                if g is None:
                    missing.append({"catalog": cat, "event": ev, "reason": "no preferred group"})
                    continue
                ds = h[g]["posterior_samples"]
                cols = ds.dtype.names or []
                if "network_optimal_snr" not in cols or "chirp_mass" not in cols:
                    missing.append({"catalog": cat, "event": ev, "group": g, "reason": "missing network_optimal_snr or chirp_mass"})
                    continue
                _, _, _, mc_src = aligned_samples(ds, "source")
                mc_det = np.asarray(ds["chirp_mass"], float)
                rho = np.asarray(ds["network_optimal_snr"], float)
            ok = np.isfinite(mc_det) & np.isfinite(rho) & (rho > 0)
            mc_det = mc_det[ok]
            rho = rho[ok]
            if len(mc_det) < 20 or len(rho) < 20:
                missing.append({"catalog": cat, "event": ev, "group": g, "reason": "too few finite samples"})
                continue
            q16, q50, q84 = np.quantile(mc_det, [0.16, 0.50, 0.84])
            sigma = 0.5 * (q84 - q16)
            rows.append({
                "catalog": cat,
                "event": ev,
                "group": g,
                "mc_det": float(q50),
                "sigma_mc_det": float(sigma),
                "sigma_mc_frac": float(sigma / q50),
                "rho": float(np.median(rho)),
                "n_samples": int(len(mc_det)),
            })
    return rows, missing


def band_rows(rows, lo, hi):
    return [r for r in rows if lo <= r["mc_det"] < hi]


def main():
    rows, missing = load_rows()
    by_catalog = {cat: fit_precision([r for r in rows if r["catalog"] == cat]) for cat in sorted({r["catalog"] for r in rows})}
    bands = {
        "mc_0_20_posthoc": band_rows(rows, 0.0, 20.0),
        "mc_20_40_posthoc": band_rows(rows, 20.0, 40.0),
        "mc_40_inf_posthoc": band_rows(rows, 40.0, float("inf")),
    }
    out = {
        "battery": "E93 precision law",
        "model": "log(sigma_Mc/Mc) = b0 + b_rho log(network_optimal_snr) + b_mass log(Mc_detector)",
        "mass_exponent_reference": GR_MASS_EXPONENT,
        "n_used": len(rows),
        "n_missing_snr_or_required_fields": len(missing),
        "missing": missing,
        "pooled": fit_precision(rows),
        "by_catalog": by_catalog,
        "posthoc_mass_bands": {k: fit_precision(v) for k, v in bands.items() if len(v) >= 8},
        "verdict_guard": (
            "b_rho near -1 is a supported selected-sample result. The mass-band split is post-hoc; "
            "failure of the light band to reject 5/3 is not by itself confirmation."
        ),
        "per_event": rows,
    }
    json.dump(out, open(RESULT_JSON, "w"), indent=2)
    print(f"wrote {RESULT_JSON}")


if __name__ == "__main__":
    main()
