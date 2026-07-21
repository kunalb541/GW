#!/usr/bin/env python3
"""Generate paper/numbers.tex -- every result number in the manuscript, as a LaTeX macro.

Figure captions were already emitted from their sidecars so text and figure could not drift. The body
prose was not: it carried ~130 numeric literals typed by hand. Two of them were already wrong when this
script was written (the elongation-band degradation and the paired frame p-value, both traceable to a
markdown note that had drifted from the artifacts), and one was stale (the abstract still quoted an
earlier cross-waveform number after the body had been corrected). Hand-typed numbers drift; this closes
the hole.

Each row of SPEC is (macro, artifact, json path, format). The macro is the ONLY way the number may
appear in the manuscript, so a changed artifact changes the paper on the next build and a number with
no artifact behind it cannot be written at all.

Formats:
  f1 f2 f3   fixed decimals            pct0     percent, no decimals
  int        integer                   sci      LaTeX $a\\times10^{b}$
  p          p-value: <0.001 / 3 s.f., whichever is honest

Run after any battery re-runs:  python3 src/build_paper_numbers.py
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "paper/numbers.tex")
# Machine-readable macro -> value -> source map, alongside the .tex comments. Borrowed from the
# sibling cosmo repo's paper/make_macros.py, which emits outputs/data/macro_sources.json: a greppable,
# diffable provenance record is far more useful to a referee than comments inside a .tex file.
MAP = os.path.join(ROOT, "results/paper_macro_sources.json")

E67 = "e67_gwtc4_curved_law"
E71 = "e71_gwtc5_curved_law"
E72 = "e72_gw_geometry_outlier_atlas"
E73 = "e73_information_anatomy"
E74 = "e74_gw250114_deepdive"
E78 = "e78_geometric_gr_exponent"
E79 = "e79_exponent_cross_catalog"
E92 = "e92_curve_uncertainty"
E95 = "e95_gate_regeneration"
E96 = "e96_curve_thickness_mechanism"
E97 = "e97_principal_curve_selfconsistency"
E98 = "e98_framework_audit"
E100 = "e100_frames_and_bands"
E99 = "e99_cache_stability_audit"


E65 = "e65_pn_fisher_rotation"

SPEC = [
    # --- training catalog (GWTC-3), from the derivation battery ---
    ("TrainTangentAll",  E65, "posthoc_curved_law.median_err_tangent_all", "f2"),
    ("TrainCurveElong",  E65, "posthoc_curved_law.median_err_curve_elong", "f2"),
    ("TrainN",           E65, "posthoc_curved_law.n", "int"),
    ("TrainSpearmanAxr", E65, "posthoc_curved_law.spearman_absres_axr", "f2"),
    # No LOCKED chirp-vs-total win fraction exists for the training catalog, so this one cell of
    # Table 1 is cache-derived and the caption says so. Table 1 previously printed 81% here with
    # nothing behind it.
    ("TrainWinFrac",     E100, "chirp_vs_total_win.GWTC-3.win_fraction", "pct0"),

    # --- locked out-of-sample scores (FULL released samples, not the cache) ---
    ("LockedOaCurveElong",   E67, "D1.median_err_curve_elong", "f2"),
    ("LockedObCurveElong",   E71, "D1.median_err_curve_elong", "f2"),
    ("LockedOaCurveAll",     E67, "D2.median_err_curve_all", "f2"),
    ("LockedObCurveAll",     E71, "D2.median_err_curve_all", "f2"),
    ("LockedOaTangentAll",   E67, "D2.median_err_tangent_all", "f2"),
    ("LockedObTangentAll",   E71, "D2.median_err_tangent_all", "f2"),
    ("LockedOaN",            E67, "n_scored", "int"),
    ("LockedObN",            E71, "n_scored", "int"),
    ("LockedOaNElong",       E67, "D1.n_elong", "int"),
    ("LockedObNElong",       E71, "D1.n_elong", "int"),
    ("LockedOaWinFrac",      E67, "@winfrac", "pct0"),
    ("LockedObWinFrac",      E71, "@winfrac", "pct0"),
    ("LockedOaSpearmanAxr",  E67, "D3.spearman_err_axr", "f2"),
    ("LockedObSpearmanAxr",  E71, "D3.spearman_err_axr", "f2"),

    # --- cache-backed reconstruction and its baselines (Gate A) ---
    ("CacheTrCurve",  E95, "gate_A.GWTC-3.own_q", "f2"),
    ("CacheOaCurve",  E95, "gate_A.O4a.own_q", "f2"),
    ("CacheObCurve",  E95, "gate_A.O4b.own_q", "f2"),
    ("CacheTrTangent", E95, "gate_A.GWTC-3.tangent", "f2"),
    ("CacheOaTangent", E95, "gate_A.O4a.tangent", "f2"),
    ("CacheObTangent", E95, "gate_A.O4b.tangent", "f2"),
    ("CacheTrPooled", E95, "gate_A.GWTC-3.pooled_q", "f2"),
    ("CacheOaPooled", E95, "gate_A.O4a.pooled_q", "f2"),
    ("CacheObPooled", E95, "gate_A.O4b.pooled_q", "f2"),
    ("PermN",         E95, "gate_A.O4a.perm_null.n", "int"),
    ("PermOaMin",     E95, "gate_A.O4a.perm_null.min", "f2"),
    ("PermOaMax",     E95, "@permmax:O4a", "f2"),
    ("DegradeMin",    E95, "@degrade_min", "f1"),
    ("DegradeMax",    E95, "@degrade_max", "f1"),

    # --- cross-waveform transfer ---
    ("XfamN",        E95, "gate_A_cross_family.n_elong", "int"),
    ("XfamAtoB",     E95, "gate_A_cross_family.A_to_B", "f2"),
    ("XfamBtoA",     E95, "gate_A_cross_family.B_to_A", "f2"),
    ("XfamDisagree", E95, "gate_A_cross_family.family_axis_disagreement", "f2"),
    ("XfamTanAtoB",  E95, "gate_A_cross_family.tangent_A_to_B", "f2"),
    ("XfamTanBtoA",  E95, "gate_A_cross_family.tangent_B_to_A", "f2"),

    # --- residual: Monte Carlo resolution and signed component ---
    ("ResidNElong",   E92, "n_elongated", "int"),
    ("ResidMedian",   E92, "monte_carlo_resolution.median_abs_err_deg", "f2"),
    ("ResidSigma",    E92, "monte_carlo_resolution.median_bootstrap_sigma_deg", "f2"),
    ("ResidRatio",    E92, "monte_carlo_resolution.median_ratio_err_over_sigma", "f1"),
    ("SignedMedian",  E92, "@signedmag", "f2"),
    ("SignedPTrain",  E92, "signed_residual.GWTC-3.sign_test_p", "p"),
    ("SignedPOa",     E92, "signed_residual.O4a.sign_test_p", "p"),
    ("SignedPOb",     E92, "signed_residual.O4b.sign_test_p", "p"),

    # --- sloppy-model framework audit ---
    ("EigRatioMedian", E98, "sloppy_models.eigenvalue_ratio_median", "f1"),
    ("EigFracDecade",  E98, "sloppy_models.frac_gt_1_decade", "pct0"),
    ("EigFracTwoDec",  E98, "sloppy_models.frac_gt_2_decades", "pct0"),
    ("GaussTangentErr", E98, "bernstein_von_mises.gaussian_tangent_error_deg", "f2"),
    ("GaussCurveErr",   E98, "bernstein_von_mises.arc_corrected_curve_error_deg", "f2"),
    ("GaussRatio",      E98, "bernstein_von_mises.ratio", "f1"),

    # --- principal-curve self-consistency ---
    ("SelfViolation",  E97, "grid_sweep.grid40_min40.median_violation", "pct1"),
    ("SelfRho",        E97, "grid_sweep.grid40_min40.spearman_violation_vs_residual", "f2"),
    ("SelfP",          E97, "grid_sweep.grid40_min40.p_value", "sci"),
    ("SelfRhoMin",     E97, "@rho_min", "f2"),
    ("SelfRhoMax",     E97, "@rho_max", "f2"),
    ("SelfIterMin",    E97, "@iter_min", "f2"),
    ("SelfIterMax",    E97, "@iter_max", "f2"),
    ("SelfXfamAPure",  E97, "cross_family.AtoB.pure_curve_deg", "f2"),
    ("SelfXfamACorr",  E97, "cross_family.AtoB.self_consistency_corrected_deg", "f2"),
    ("SelfXfamAP",     E97, "cross_family.AtoB.wilcoxon_p", "f3"),
    ("SelfXfamBPure",  E97, "cross_family.BtoA.pure_curve_deg", "f2"),
    ("SelfXfamBCorr",  E97, "cross_family.BtoA.self_consistency_corrected_deg", "f2"),
    ("SelfXfamBP",     E97, "cross_family.BtoA.wilcoxon_p", "f3"),

    # --- finite thickness ---
    ("ThickRelative", E96, "in_sample.median_relative_thickness", "f2"),
    ("ThickAPure",    E96, "cross_family.AtoB.pure_curve", "f2"),
    ("ThickAMeas",    E96, "cross_family.AtoB.measured", "f2"),
    ("ThickAP",       E96, "cross_family.AtoB.measured_vs_pure_wilcoxon_p", "f3"),
    ("ThickBPure",    E96, "cross_family.BtoA.pure_curve", "f2"),
    ("ThickBMeas",    E96, "cross_family.BtoA.measured", "f2"),
    ("ThickBP",       E96, "cross_family.BtoA.measured_vs_pure_wilcoxon_p", "f3"),

    # --- frames, coordinates, elongation gate (E100) ---
    ("FrameSourceErr",  E100, "frames.source_m1_m2.median_err_deg", "f2"),
    ("FrameDetErr",     E100, "frames.detector_m1_m2.median_err_deg", "f2"),
    ("FrameLogErr",     E100, "frames.log_source_m1_m2.median_err_deg", "f2"),
    ("FrameNPaired",    E100, "frames.detector_vs_source_paired.n_paired", "int"),
    ("FramePairedP",    E100, "frames.detector_vs_source_paired.wilcoxon_p", "sci"),
    ("FrameAxrSource",  E100, "frames.detector_vs_source_paired.median_axr_source", "f1"),
    ("FrameAxrDet",     E100, "frames.detector_vs_source_paired.median_axr_detector", "f1"),
    ("MatchedLowSource", E100, "matched_axis_ratio.3-5.median_source_deg", "f2"),
    ("MatchedLowDet",    E100, "matched_axis_ratio.3-5.median_detector_deg", "f2"),
    ("BandRound",   E100, "axr_bands.1-1.5.median_err_deg", "f1"),
    ("BandTwo",     E100, "axr_bands.1.5-2.median_err_deg", "f1"),
    ("BandThree",   E100, "axr_bands.2-3.median_err_deg", "f1"),
    ("BandFour",    E100, "axr_bands.3-5.median_err_deg", "f1"),
    ("BandFive",    E100, "axr_bands.5+.median_err_deg", "f1"),
    ("RandomBaseline", E100, "random_baseline_deg", "int"),
    # cache stability (E99): is the bootstrap-resampled cache representative of the full posteriors?
    ("CacheBias",      E99, "@maxbias", "f2"),
    ("CacheSpread",    E99, "verdict.max_seed_spread_deg", "f2"),
    ("CacheNSeeds",    E99, "@nseeds", "int"),
    ("FullOaCurve",    E99, "summary.O4a.full_sample", "f2"),
    ("FullObCurve",    E99, "summary.O4b.full_sample", "f2"),
    ("FullTrCurve",    E99, "summary.GWTC-3.full_sample", "f2"),
    ("ArcTr", E100, "arc_length_vs_tangent_error.GWTC-3.spearman_arc_vs_tangent_err", "f2"),
    ("ArcOa", E100, "arc_length_vs_tangent_error.O4a.spearman_arc_vs_tangent_err", "f2"),
    ("ArcOb", E100, "arc_length_vs_tangent_error.O4b.spearman_arc_vs_tangent_err", "f2"),

    # --- exponent diagnostic (exploratory) ---
    ("ExpOb",        E78, "p_hat", "f3"),
    ("ExpObErr",     E78, "stat_err_bootstrap", "f3"),
    ("ExpComb",      E79, "combined_exponent", "f3"),
    ("ExpCombErr",   E79, "combined_err", "f3"),
    ("ExpSpread",    E79, "systematic_followup.catalog_spread", "f3"),
    ("ExpOffset",    E79, "@expoffset", "f3"),
    ("ExpSyst",      E79, "systematic_followup.syst_floor", "f3"),
    ("ExpSigma",     E79, "systematic_followup.honest_sigma_from_GR", "f1"),
    ("ExpSpearman",  E79, "systematic_followup.spearman_pstar_axr", "f2"),
    ("ExpCleanHalf", E79, "systematic_followup.p_hat_most_elongated_half", "f3"),
    ("ExpNaiveSigma", E79, "@naivesigma", "f1"),

    # --- context sections ---
    ("AnatomyN",       E73, "n_events", "int"),
    ("AnatomySpearman", E73, "spearman_richness_vs_Mtot", "f2"),
    ("LoudMf",     E74, "characterization.Mf_source.0", "f1"),
    ("LoudChif",   E74, "characterization.final_spin_af.0", "f2"),
    ("LoudSNR",    E74, "characterization.network_snr.0", "int"),
    ("LoudFtwoTwoZero", E74, "kerr_qnm_prediction.f_220_Hz.0", "f1"),
    ("LoudTauTwoTwoZero", E74, "kerr_qnm_prediction.tau_220_ms.0", "f2"),
    ("LoudFtwoTwoOne", E74, "kerr_qnm_prediction.f_221_Hz.0", "f1"),
    ("LoudTauTwoTwoOne", E74, "kerr_qnm_prediction.tau_221_ms.0", "f2"),

    # --- outlier atlas ---
    ("AtlasN",       E72, "n", "int"),
    ("AtlasWfRho",   E72, "D1_correlations.waveform_disagreement.rho", "f2"),
    ("AtlasWfQ",     E72, "D1_correlations.waveform_disagreement.q_bh", "sci"),
]


def dig(d, path):
    """Dotted path lookup. Some artifact keys contain dots themselves (the axis-ratio band "1-1.5"),
    so at each level take the LONGEST prefix of the remaining segments that is an actual key."""
    seg = path.split(".")
    while seg:
        if isinstance(d, list):
            d = d[int(seg[0])]
            seg = seg[1:]
            continue
        for n in range(len(seg), 0, -1):
            k = ".".join(seg[:n])
            if k in d:
                d, seg = d[k], seg[n:]
                break
        else:
            raise KeyError(f"{seg[0]!r} in path {path!r}")
    return d


def derived(tag, d):
    """Quantities that are a stated function of artifact fields rather than a stored field."""
    if tag == "winfrac":
        return dig(d, "D3.chirp_wins") / dig(d, "D3.n")
    if tag.startswith("permmax:"):
        return max(dig(d, f"gate_A.{tag.split(':')[1]}.perm_null.draws"))
    if tag in ("degrade_min", "degrade_max"):
        # how far the best alternative q marginal degrades the score, per catalog
        r = [max(dig(d, f"gate_A.{c}.pooled_q"), 1e-9) / dig(d, f"gate_A.{c}.own_q")
             for c in ("GWTC-3", "O4a", "O4b")]
        return min(r) if tag == "degrade_min" else max(r)
    if tag == "signedmag":
        return abs(dig(d, "signed_residual.ALL.median_deg"))
    if tag in ("rho_min", "rho_max"):
        r = [v["spearman_violation_vs_residual"] for v in d["grid_sweep"].values()]
        return min(r) if tag == "rho_min" else max(r)
    if tag in ("iter_min", "iter_max"):
        r = [v["median_residual_after_one_iteration_deg"] for v in d["grid_sweep"].values()]
        return min(r) if tag == "iter_min" else max(r)
    if tag == "maxbias":
        return max(abs(v["abs_bias_vs_full"]) for v in d["summary"].values())
    if tag == "nseeds":
        return len(d["by_seed"])
    if tag == "naivesigma":
        return (dig(d, "combined_exponent") - dig(d, "gr_value")) / dig(d, "combined_err")
    if tag == "expoffset":
        return dig(d, "combined_exponent") - dig(d, "gr_value")
    raise KeyError(tag)


def fmt(v, how):
    if how == "int":
        return f"{int(round(v))}"
    if how.startswith("f"):
        return f"{v:.{int(how[1])}f}"
    if how == "pct0":
        return f"{100 * v:.0f}\\%"
    if how == "pct1":
        return f"{100 * v:.1f}\\%"
    if how == "p":
        return "<0.001" if v < 1e-3 else f"{v:.3f}"
    if how == "sci":
        e = 0
        m = float(v)
        while m and abs(m) < 1:
            m *= 10
            e -= 1
        while abs(m) >= 10:
            m /= 10
            e += 1
        return f"{m:.0f}\\times10^{{{e}}}"
    raise ValueError(how)


def main():
    cache, lines, prov = {}, [], []
    for macro, art, path, how in SPEC:
        if art not in cache:
            with open(os.path.join(ROOT, f"results/{art}_results.json")) as fh:
                cache[art] = json.load(fh)
        d = cache[art]
        v = derived(path[1:], d) if path.startswith("@") else dig(d, path)
        lines.append(f"\\newcommand{{\\{macro}}}{{{fmt(v, how)}}}")
        prov.append(f"% {macro:<22} {art}_results.json :: {path}")

    with open(OUT, "w") as fh:
        fh.write("% AUTO-GENERATED by src/build_paper_numbers.py -- DO NOT EDIT BY HAND.\n"
                 "% Every result number in the manuscript body is a macro defined here and read from a\n"
                 "% committed artifact. A number that cannot be sourced this way must not appear in the paper.\n"
                 "% Provenance for each macro (artifact :: json path):\n")
        fh.write("\n".join(prov) + "\n\n" + "\n".join(lines) + "\n")
    rows = [{"macro": m, "value": fmt(derived(pa[1:], cache[a]) if pa.startswith("@") else dig(cache[a], pa), h),
              "artifact": f"results/{a}_results.json", "path": pa, "format": h}
             for m, a, pa, h in SPEC]
    with open(MAP, "w") as fh:
        json.dump({"generator": "src/build_paper_numbers.py",
                   "note": ("Provenance for every number in paper/manuscript.tex. Each macro is the only "
                            "way its value may appear in the paper; see tests/test_paper_numbers.py."),
                   "n_macros": len(rows), "macros": rows}, fh, indent=1)
    print(f"wrote {os.path.relpath(OUT, ROOT)}: {len(lines)} macros from {len(cache)} artifacts")
    print(f"wrote {os.path.relpath(MAP, ROOT)}")


if __name__ == "__main__":
    main()
