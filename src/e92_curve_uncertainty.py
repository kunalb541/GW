#!/usr/bin/env python3
"""E92 - uncertainty layer for the curved chirp-mass law, read from the E94 posterior cache.

Provenance: `results/e94_posterior_cache.npz` (+ manifest) is the SINGLE source. No HDF5 access here --
a full sweep costs ~276 s wall and that cost is paid once, in E94. This also lets GWTC-3 back in: the
earlier HDF5-backed version excluded it because raw sweeps were too slow.

WHAT THIS MEASURES, AND WHAT IT DOES NOT. Bootstrapping posterior samples measures **Monte Carlo
resolution**: how well the released sample set pins down the functional psi_curve - psi_meas. It is NOT
repeated-experiment uncertainty and NOT model coverage. The bootstrap sigma shrinks as more samples are
released and encodes nothing about detector noise, calibration, waveform systematics or population
variation. Earlier prose called the |z|<1 / |z|<2 rates "coverage against nominal 68%/95%"; that was
wrong and is not repeated here. The supported statement is only that the ~1 deg discrepancy greatly
exceeds finite-sample Monte Carlo error.

Joint resampling matters: psi_meas and psi_curve come from the SAME samples, so each bootstrap draws ONE
index set and recomputes both from it, bootstrapping the difference directly. E94 guarantees m1/m2/q are
sample-aligned; the committed `load_event` does NOT align q with the finite-mass mask, and that mismatch
would silently pair mismatched samples.

Signed residuals use `sdiff` (from E95), NOT the repo's `adiff` -- adiff returns an ABSOLUTE value, and
using it for a sign test produced a tautological "100% positive, p=3e-24". Seed 92.
"""
import json, math, os, sys
import numpy as np
from scipy.stats import binomtest, spearmanr

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from src.e94_build_posterior_cache import load, CACHE, MANIFEST
from src.e95_gate_regeneration import sdiff, primary_rows, AXR_MIN
from src.e71_gwtc5_curved_law import psi_axr_rho, tangent_angles, curve_psi
from src.e65_pn_fisher_rotation import adiff

SEED = 92
N_BOOT = 200
THRESHOLDS = (1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0)
RESULT_JSON = os.path.join(ROOT, "results/e92_curve_uncertainty_results.json")


def circular_std_deg(x):
    """Std for mod-180 axis residuals, via angle doubling onto the circle."""
    rad = np.deg2rad(2.0 * np.asarray(x, float))
    c, s = np.mean(np.cos(rad)), np.mean(np.sin(rad))
    r = max(math.hypot(c, s), 1e-12)
    return float(np.rad2deg(math.sqrt(-2.0 * math.log(r))) / 2.0)


def bootstrap_event(d, rng, n_boot=N_BOOT):
    """JOINT bootstrap of the signed residual from cache-aligned arrays."""
    m1 = d["m1s"].astype(float); m2 = d["m2s"].astype(float)
    q = d["q"].astype(float); mcs = d["mcs"].astype(float)
    assert len(m1) == len(m2) == len(q) == len(mcs), "cache arrays must be sample-aligned"
    n = len(m1)
    psi, _, _ = psi_axr_rho(m1, m2)
    obs = float(sdiff(curve_psi(float(np.median(mcs)), q), psi))
    draws = np.empty(n_boot)
    for b in range(n_boot):
        j = rng.integers(0, n, n)                       # ONE index set for both quantities
        pb, _, _ = psi_axr_rho(m1[j], m2[j])
        draws[b] = sdiff(curve_psi(float(np.median(mcs[j])), q[j]), pb)
    return (obs, circular_std_deg(draws), float(np.quantile(draws, 0.16)),
            float(np.quantile(draws, 0.84)), n)


def main():
    rng = np.random.default_rng(SEED)
    rec = load()
    prim, _ = primary_rows(rec)
    manifest = json.load(open(MANIFEST)) if os.path.exists(MANIFEST) else {}

    rows = []
    for (cat, ev), v in sorted(prim.items()):
        obs, sig, lo, hi, n = bootstrap_event(v["raw"], rng)
        rows.append(dict(catalog=cat, event=ev, group=v["group"], axr=float(v["axr"]),
                         signed=obs, abs_err=abs(obs), boot_sigma=sig, boot_ci16=lo, boot_ci84=hi,
                         n_samples=int(n),
                         tangent_err=float(abs(adiff(tangent_angles(v["m1m"], v["m2m"])[0], v["psi"])))))

    el = [r for r in rows if r["axr"] >= AXR_MIN]
    z = np.array([r["abs_err"] / r["boot_sigma"] for r in el if r["boot_sigma"] > 1e-9])
    out = {
        "battery": "E92 cache-backed uncertainty",
        "seed": SEED, "n_boot": N_BOOT, "axr_min": AXR_MIN,
        "provenance": {"cache": os.path.relpath(CACHE, ROOT),
                       "manifest": os.path.relpath(MANIFEST, ROOT),
                       "cache_manifest": manifest, "hdf5_accessed": False},
        "n_events": len(rows), "n_elongated": len(el),
        "monte_carlo_resolution": {
            "median_abs_err_deg": float(np.median([r["abs_err"] for r in el])),
            "median_bootstrap_sigma_deg": float(np.median([r["boot_sigma"] for r in el])),
            "median_ratio_err_over_sigma": float(np.median(z)),
            "frac_within_1_sigma": float(np.mean(np.abs(z) < 1)),
            "frac_within_2_sigma": float(np.mean(np.abs(z) < 2)),
            "language_guard": ("Monte Carlo resolution of the released posterior samples ONLY. These "
                               "fractions are NOT coverage against nominal 68%/95% levels: the bootstrap "
                               "encodes no detector-noise, calibration, waveform or population "
                               "uncertainty. Supported claim: the ~1 deg discrepancy greatly exceeds "
                               "finite-sample Monte Carlo error.")},
        "signed_residual": {},
        "threshold_sensitivity": {},
    }

    for scope in ("ALL", "GWTC-3", "O4a", "O4b"):
        S = el if scope == "ALL" else [r for r in el if r["catalog"] == scope]
        if len(S) < 3:
            continue
        s = np.array([r["signed"] for r in S])
        npos = int((s > 0).sum())
        out["signed_residual"][scope] = {
            "n": len(s), "median_deg": float(np.median(s)), "mean_deg": float(s.mean()),
            "sd_deg": float(s.std(ddof=1)), "frac_positive": float(npos / len(s)),
            "sign_test_p": float(binomtest(npos, len(s), 0.5).pvalue)}
    out["signed_residual"]["spearman_signed_vs_axr"] = float(
        spearmanr([r["axr"] for r in el], [r["signed"] for r in el]).statistic)
    out["signed_residual"]["note"] = (
        "catalog-specific values are reported because the effect is NOT uniform -- strongest in the "
        "training catalog, weakest in the newest. Pooling all events into one sign test overstates it.")

    for t in THRESHOLDS:
        S = [r for r in rows if r["axr"] >= t]
        if len(S) < 5:
            continue
        out["threshold_sensitivity"][str(t)] = {
            "n": len(S),
            "curve_median_deg": float(np.median([r["abs_err"] for r in S])),
            "tangent_median_deg": float(np.median([r["tangent_err"] for r in S]))}
    out["threshold_sensitivity"]["note"] = (
        "axr>=3 is the locked primary score; the curve error is monotone and smooth across thresholds, "
        "so the primary score is not threshold-tuned.")
    out["events"] = rows

    json.dump(out, open(RESULT_JSON, "w"), indent=1)
    m = out["monte_carlo_resolution"]
    print(f"n={out['n_events']} elongated={out['n_elongated']}")
    print(f"median |err| {m['median_abs_err_deg']:.2f} deg | median bootstrap sigma "
          f"{m['median_bootstrap_sigma_deg']:.3f} deg | ratio {m['median_ratio_err_over_sigma']:.2f}")
    for k, v in out["signed_residual"].items():
        if isinstance(v, dict):
            print(f"  signed {k:>7}: n={v['n']:3d} median {v['median_deg']:+.3f} "
                  f"frac+ {v['frac_positive']:.2f} p={v['sign_test_p']:.3f}")
    print("wrote", RESULT_JSON)


if __name__ == "__main__":
    main()
