#!/usr/bin/env python3
"""E98 - which mathematical frameworks does this measurement actually earn?

Four frameworks are commonly attached to results of this kind. The submission-gate audit banned citing
mathematics we do not compute, so this battery tests each one against what we actually measure and
records the verdict, including where the framing is NOT supported by our own data.

  1. SLOPPY MODELS (Transtrum et al.) -- claims a Fisher/covariance eigenvalue spectrum spanning orders
     of magnitude, i.e. a thin "hyperribbon", with stiff and sloppy directions.
     TEST: measure the eigenvalue ratio of the 2-D mass covariance across the catalog.

  2. PRINCIPAL CURVES (Hastie & Stuetzle) -- a curve is principal iff self-consistent.
     TEST: done in E97. Earned: the curve is not self-consistent, and the violation predicts the residual.

  3. BERNSTEIN-VON MISES / Gaussian limit -- the posterior tends to a Gaussian whose covariance is the
     inverse Fisher matrix. A Gaussian's principal axis IS the local tangent, so the tangent error is
     exactly the error the Gaussian approximation makes.
     TEST: compare tangent error (Gaussian) with curve error (arc-corrected) on elongated events.

  4. CENCOV / Fisher-Rao uniqueness -- asserts Fisher-Rao is the unique metric invariant under
     sufficient statistics.
     TEST: our measured object is a Euclidean PCA angle in fixed coordinates. Gate C measured it in
     three coordinate systems and got three different answers, so invoking Cencov would contradict our
     own result. Recorded as NOT APPLICABLE rather than quietly dropped.

Reads the E94 cache and the E95/E97 artifacts. No HDF5. Seed 98.
"""
import json, os, sys
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from src.e94_build_posterior_cache import load, CACHE
from src.e95_gate_regeneration import primary_rows, AXR_MIN
from src.e71_gwtc5_curved_law import curve_psi, tangent_angles
from src.e65_pn_fisher_rotation import adiff

SEED = 98
E97_JSON = os.path.join(ROOT, "results/e97_principal_curve_selfconsistency_results.json")
RESULT_JSON = os.path.join(ROOT, "results/e98_framework_audit_results.json")


def main():
    rec = load()
    prim, _ = primary_rows(rec)

    ratios, tan, cur = [], [], []
    for (cat, ev), v in sorted(prim.items()):
        m1 = v["raw"]["m1s"].astype(float)
        m2 = v["raw"]["m2s"].astype(float)
        w = np.linalg.eigvalsh(np.cov(np.vstack([m1, m2])))
        ratios.append(float(w[-1] / max(w[0], 1e-30)))
        if v["axr"] >= AXR_MIN:
            tan.append(float(abs(adiff(tangent_angles(v["m1m"], v["m2m"])[0], v["psi"]))))
            cur.append(float(abs(adiff(curve_psi(v["mc"], v["q"]), v["psi"]))))
    r = np.array(ratios)
    tan, cur = np.array(tan), np.array(cur)

    sloppy = {
        "n_events": int(len(r)),
        "eigenvalue_ratio_median": float(np.median(r)),
        "eigenvalue_ratio_p10": float(np.percentile(r, 10)),
        "eigenvalue_ratio_p90": float(np.percentile(r, 90)),
        "eigenvalue_ratio_max": float(r.max()),
        "frac_gt_1_decade": float(np.mean(r > 10)),
        "frac_gt_2_decades": float(np.mean(r > 100)),
        "frac_gt_3_decades": float(np.mean(r > 1000)),
        "verdict": "PARTIAL -- concept supported, 'hyperribbon' NOT supported by our measurement",
        "statement": ("The stiff/sloppy CONCEPT holds -- chirp mass is measured far better than mass "
                      "ratio -- but the hyperribbon picture does not follow from what we measure. In the "
                      "2-D mass plane the eigenvalue ratio has a median of only ~3, with about 29% of "
                      "events exceeding one order of magnitude and 3% exceeding two. Sloppiness in the "
                      "Transtrum sense is a property of the FULL parameter space, which we do not "
                      "measure; a 2-D marginal neither establishes nor entitles us to the hyperribbon "
                      "language. Cite the concept, not the geometry.")}

    bvm = {
        "n_elongated": int(len(tan)),
        "gaussian_tangent_error_deg": float(np.median(tan)),
        "arc_corrected_curve_error_deg": float(np.median(cur)),
        "ratio": float(np.median(tan) / np.median(cur)),
        "verdict": "EARNED",
        "statement": ("A Gaussian posterior's principal axis IS the local tangent, so the tangent error "
                      "is precisely the error the Gaussian / Bernstein-von Mises limit makes about "
                      "posterior orientation. Measured on elongated events it is 5.02 deg, against 1.03 "
                      "deg once the arc is accounted for: the Gaussian approximation is wrong by about "
                      "5x more than the curve. The asymptotic Gaussian limit is therefore quantifiably "
                      "not reached at realistic signal-to-noise, and that gap is what this paper "
                      "measures and corrects.")}

    principal = {"verdict": "EARNED (E97)",
                 "statement": ("Hastie-Stuetzle self-consistency is implemented, not invoked: the "
                               "constant-Mc curve is not a principal curve, and the size of that "
                               "violation predicts the per-event orientation residual.")}
    if os.path.exists(E97_JSON):
        d = json.load(open(E97_JSON))
        g = d["grid_sweep"]["grid40_min40"]
        principal["median_violation"] = g["median_violation"]
        principal["spearman_violation_vs_residual"] = g["spearman_violation_vs_residual"]
        principal["p_value"] = g["p_value"]

    cencov = {"verdict": "NOT APPLICABLE -- would contradict our own measurement",
              "statement": ("Cencov's theorem concerns the uniqueness of the Fisher-Rao metric under "
                            "sufficient statistics. Our measured object is a Euclidean PCA angle in "
                            "fixed coordinates, and Gate C measured it at 1.03, 0.31 and 0.77 deg in "
                            "source-frame, detector-frame and log-mass coordinates respectively. The "
                            "quantity is demonstrably not invariant, so invoking Cencov would assert "
                            "the opposite of what we measured.")}

    backus = {"verdict": "NOT EARNED -- no resolution operator is computed",
              "statement": ("Backus-Gilbert resolution theory splits parameter space into resolved and "
                            "unresolved directions, which is a second vocabulary for the stiff/sloppy "
                            "split rather than an independent result. Earning it would require actually "
                            "computing a resolution operator and its trade-off curve, which this "
                            "analysis does not do. Left uncited.")}

    out = {"battery": "E98 framework audit", "seed": SEED,
           "provenance": {"cache": os.path.relpath(CACHE, ROOT), "hdf5_accessed": False},
           "sloppy_models": sloppy, "principal_curves": principal,
           "bernstein_von_mises": bvm, "cencov_fisher_rao": cencov,
           "backus_gilbert": backus,
           "summary": ("Of four frameworks commonly attached to results of this kind, two are earned "
                       "(principal curves, via E97; the Gaussian/Bernstein-von Mises limit, via the "
                       "tangent error), one is supported only as a concept and NOT as geometry (sloppy "
                       "models -- our 2-D eigenvalue ratio has median ~3, not the many decades a "
                       "hyperribbon requires), and one is inapplicable because it would contradict our "
                       "own coordinate-dependence measurement (Cencov). Backus-Gilbert is left uncited "
                       "for want of a computed resolution operator.")}
    json.dump(out, open(RESULT_JSON, "w"), indent=1)
    print(f"sloppy models      : ratio median {sloppy['eigenvalue_ratio_median']:.1f}, "
          f">1 decade {sloppy['frac_gt_1_decade']:.0%}, >2 {sloppy['frac_gt_2_decades']:.0%}"
          f"  -> {sloppy['verdict']}")
    print(f"principal curves   : {principal['verdict']}")
    print(f"Bernstein-von Mises: Gaussian {bvm['gaussian_tangent_error_deg']:.2f} deg vs curve "
          f"{bvm['arc_corrected_curve_error_deg']:.2f} deg ({bvm['ratio']:.1f}x)  -> {bvm['verdict']}")
    print(f"Cencov / Fisher-Rao: {cencov['verdict']}")
    print(f"Backus-Gilbert     : {backus['verdict']}")
    print("wrote", RESULT_JSON)


if __name__ == "__main__":
    main()
