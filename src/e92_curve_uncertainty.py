#!/usr/bin/env python3
"""E92 - uncertainty and permutation layer for the curved chirp-mass law.

Bootstraps the sample-aligned residual psi_curve - psi_meas and builds a permutation null for the
own-q advantage. O4a/O4b are recomputed from local HDF5 chains. GWTC-3 is excluded here because raw
posterior samples are not present in this workspace. Seed 92.
"""
import json
import math
import os
import sys

import h5py
import numpy as np
from scipy.stats import binomtest, spearmanr, wilcoxon

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from src.e65_pn_fisher_rotation import adiff
from src.e91_curve_submission_gates import CATALOGS, aligned_samples, event_name, psi_axr_rho, signed_adiff
from src.e71_gwtc5_curved_law import curve_psi, pick_group

SEED = 92
N_BOOT = 200
N_PERM = 400
RESULT_JSON = os.path.join(ROOT, "results/e92_curve_uncertainty_results.json")


def circular_std_deg(x):
    """Std for mod-180 axis residuals by doubling angles onto the circle."""
    x = np.asarray(x, float)
    rad = np.deg2rad(2.0 * x)
    c, s = np.mean(np.cos(rad)), np.mean(np.sin(rad))
    r = max(math.hypot(c, s), 1e-12)
    return float(np.rad2deg(math.sqrt(-2.0 * math.log(r))) / 2.0)


def load_preferred_samples():
    rows = []
    for cat, data_dir in CATALOGS.items():
        for name in sorted(os.listdir(data_dir)):
            if not (name.startswith("GW") and name.endswith(".hdf5")):
                continue
            fp = os.path.join(data_dir, name)
            with h5py.File(fp, "r") as h:
                g = pick_group(h)
                if g is None:
                    continue
                m1, m2, q, mc = aligned_samples(h[g]["posterior_samples"], "source")
            psi_m, axr, _ = psi_axr_rho(m1, m2)
            psi_c = curve_psi(float(np.median(mc)), q)
            rows.append({
                "catalog": cat,
                "event": event_name(fp),
                "group": g,
                "m1": m1,
                "m2": m2,
                "q": q,
                "mc": mc,
                "psi_meas": psi_m,
                "psi_curve": psi_c,
                "axr": axr,
                "err_curve": adiff(psi_c, psi_m),
                "signed_curve_minus_meas": signed_adiff(psi_c, psi_m),
            })
    return rows


def bootstrap_event(row, rng, n_boot=N_BOOT):
    n = len(row["q"])
    signed = []
    for _ in range(n_boot):
        idx = rng.integers(0, n, n)
        psi_m, _, _ = psi_axr_rho(row["m1"][idx], row["m2"][idx])
        psi_c = curve_psi(float(np.median(row["mc"][idx])), row["q"][idx])
        signed.append(signed_adiff(psi_c, psi_m))
    signed = np.asarray(signed)
    return {
        "event": row["event"],
        "catalog": row["catalog"],
        "group": row["group"],
        "axr": row["axr"],
        "signed_residual": row["signed_curve_minus_meas"],
        "abs_residual": row["err_curve"],
        "boot_sigma_signed": circular_std_deg(signed),
        "boot_ci16": float(np.quantile(signed, 0.16)),
        "boot_ci84": float(np.quantile(signed, 0.84)),
    }


def threshold_curve(rows):
    out = []
    for thr in [1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0]:
        xs = [r for r in rows if r["axr"] >= thr]
        out.append({
            "axr_threshold": thr,
            "n": len(xs),
            "median_curve": None if not xs else float(np.median([r["err_curve"] for r in xs])),
        })
    return out


def permutation_null(rows, rng, n_perm=N_PERM):
    out = {}
    for cat in sorted({r["catalog"] for r in rows}):
        xs = [r for r in rows if r["catalog"] == cat and r["axr"] >= 3.0]
        own = float(np.median([r["err_curve"] for r in xs]))
        errs = []
        for _ in range(n_perm):
            donor = rng.permutation(len(xs))
            pe = []
            for i, j in enumerate(donor):
                r, d = xs[i], xs[j]
                pe.append(adiff(curve_psi(float(np.median(r["mc"])), d["q"]), r["psi_meas"]))
            errs.append(float(np.median(pe)))
        errs = np.asarray(errs)
        out[cat] = {
            "n_elong": len(xs),
            "own_q_median": own,
            "permuted_median_mean": float(np.mean(errs)),
            "permuted_median_ci05_95": [float(np.quantile(errs, 0.05)), float(np.quantile(errs, 0.95))],
            "own_q_percentile_low_is_better": float(np.mean(errs <= own)),
        }
    return out


def main():
    rng = np.random.default_rng(SEED)
    rows = load_preferred_samples()
    elong = [r for r in rows if r["axr"] >= 3.0]
    boot = [bootstrap_event(r, rng) for r in elong]
    z = np.array([b["signed_residual"] / b["boot_sigma_signed"] for b in boot if b["boot_sigma_signed"] > 0])
    signed = np.array([b["signed_residual"] for b in boot])
    positive = int(np.sum(signed > 0))
    signed_by_cat = {}
    for cat in sorted({b["catalog"] for b in boot}):
        xs = [b for b in boot if b["catalog"] == cat]
        pos = int(sum(b["signed_residual"] > 0 for b in xs))
        signed_by_cat[cat] = {
            "n": len(xs),
            "median_signed": float(np.median([b["signed_residual"] for b in xs])),
            "fraction_positive": pos / len(xs),
            "sign_test_p": float(binomtest(pos, len(xs), 0.5).pvalue),
        }
    abs_res = np.array([b["abs_residual"] for b in boot])
    sig = np.array([b["boot_sigma_signed"] for b in boot])
    summary = {
        "battery": "E92 curve uncertainty",
        "seed": SEED,
        "n_boot": N_BOOT,
        "n_perm": N_PERM,
        "inputs": "O4a/O4b local HDF5 only; raw GWTC-3 chains absent",
        "monte_carlo_resolution": {
            "n_elong_axr_ge3": len(boot),
            "median_abs_residual": float(np.median(abs_res)),
            "median_boot_sigma_signed": float(np.median(sig)),
            "median_abs_z": float(np.median(np.abs(z))),
            "fraction_abs_z_lt_1": float(np.mean(np.abs(z) < 1.0)),
            "fraction_abs_z_lt_2": float(np.mean(np.abs(z) < 2.0)),
            "language_guard": "bootstrap measures posterior-sample Monte Carlo resolution, not repeated-experiment coverage",
        },
        "signed_residual": {
            "n": len(boot),
            "median_signed": float(np.median(signed)),
            "fraction_positive": positive / len(boot),
            "sign_test_p": float(binomtest(positive, len(boot), 0.5).pvalue),
            "by_catalog": signed_by_cat,
            "spearman_signed_vs_axr": float(spearmanr([b["axr"] for b in boot], [b["signed_residual"] for b in boot]).statistic),
        },
        "threshold_sensitivity": threshold_curve(rows),
        "permutation_null": permutation_null(rows, rng),
        "per_event_bootstrap": boot,
    }
    json.dump(summary, open(RESULT_JSON, "w"), indent=2)
    print(f"wrote {RESULT_JSON}")


if __name__ == "__main__":
    main()
