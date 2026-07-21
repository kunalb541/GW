#!/usr/bin/env python3
"""Regenerate the headline-number tables inside the public docs, from committed artifacts.

The manuscript's numbers have been generated since src/build_paper_numbers.py landed, and they no longer
drift. The DOCS were still hand-typed, and they drifted for exactly the same reason the paper used to:
three separate review rounds found stale values in REFEREE_READINESS.md and EXTERNAL_READER_PACKET.md
(0.83/1.32/1.00 after the cache rebuild, "six times" after the resolution improved to 17x, a p=0.377 that
had become 0.110). Proofreading caught them each time; proofreading is not a system.

So the same discipline applies here. Each managed table lives between sentinel comments:

    <!-- BEGIN GENERATED: key-numbers -->
    ...anything here is overwritten...
    <!-- END GENERATED: key-numbers -->

and is rewritten from results/*.json and figures/*.json on every run. Prose around the blocks is left
alone -- this script owns the numbers, not the argument.

Run after any battery re-runs, alongside build_paper_numbers.py. A test fails if a block is stale.
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# The cache is gitignored, so on a fresh clone there is no file to measure. Recorded here as the single
# source of truth and cross-checked against the real file whenever it happens to be present.
CACHE_MB = 572


def cache_mb():
    fp = os.path.join(ROOT, "results/e94_posterior_cache.npz")
    if os.path.exists(fp):
        actual = round(os.path.getsize(fp) / 1e6)
        assert abs(actual - CACHE_MB) <= 5, (
            f"CACHE_MB={CACHE_MB} but the cache is {actual} MB; update the constant")
    return CACHE_MB


def pdf_pages():
    """Page count of the built manuscript, or 0 if it cannot be determined.

    The PDF uses compressed object streams, so scanning for /Count finds nothing; pdfinfo is the
    reliable route and the raw scan is only a fallback for machines without poppler.
    """
    fp = os.path.join(ROOT, "paper/manuscript.pdf")
    if not os.path.exists(fp):
        return 0
    try:
        import subprocess
        out = subprocess.run(["pdfinfo", fp], capture_output=True, text=True, timeout=30).stdout
        m = re.search(r"Pages:\s+(\d+)", out)
        if m:
            return int(m.group(1))
    except Exception:
        pass
    with open(fp, "rb") as fh:
        counts = re.findall(rb"/Count\s+(\d+)", fh.read())
    return max((int(c) for c in counts), default=0)


def art(name):
    with open(os.path.join(ROOT, name)) as fh:
        return json.load(fh)


def blocks():
    """Return {sentinel_name: markdown} for every managed block."""
    e95 = art("results/e95_gate_regeneration_results.json")
    e92 = art("results/e92_curve_uncertainty_results.json")
    e97 = art("results/e97_principal_curve_selfconsistency_results.json")
    e98 = art("results/e98_framework_audit_results.json")
    e94m = art("results/e94_posterior_cache_manifest.json")
    f1c = art("figures/fig1c_nontriviality_q_baselines.json")["catalogs"]

    A, X = e95["gate_A"], e95["gate_A_cross_family"]
    mc = e92["monte_carlo_resolution"]
    g = e97["grid_sweep"]["grid40_min40"]
    b = e98["bernstein_von_mises"]
    CATS = ("GWTC-3", "O4a", "O4b")
    tri = lambda fn: " / ".join(f"{fn(c):.2f}°" for c in CATS)

    key = [
        "| claim | value | artifact |",
        "|---|---|---|",
        f"| out-of-sample reconstruction (elongated) | {tri(lambda c: A[c]['own_q'])} "
        "| `e95_gate_regeneration_results.json` |",
        f"| median-point tangent, same events | {tri(lambda c: A[c]['tangent'])} | same |",
        f"| pooled-$q$ baseline, same events | {tri(lambda c: A[c]['pooled_q'])} | same |",
        f"| permutation null ({A['O4a']['perm_null']['n']} draws), own-$q$ below **minimum** | "
        f"min {tri(lambda c: A[c]['perm_null']['min'])} | same |",
        f"| cross-waveform transfer A→B, B→A | {X['A_to_B']:.2f}°, {X['B_to_A']:.2f}° "
        f"(reference scale {X['family_axis_disagreement']:.2f}°) | same |",
        f"| residual vs Monte Carlo resolution | {mc['median_abs_err_deg']:.2f}° vs "
        f"{mc['median_bootstrap_sigma_deg']:.3f}° ({mc['median_ratio_err_over_sigma']:.1f}×) "
        "| `e92_curve_uncertainty_results.json` |",
        "| signed residual, per catalog | "
        + ", ".join(f"{c} $p" + ("<0.001$" if e92['signed_residual'][c]['sign_test_p'] < 1e-3
                                  else f"={e92['signed_residual'][c]['sign_test_p']:.3f}$")
                    for c in CATS)
        + " | same |",
        f"| self-consistency violation predicts residual | ρ = {g['spearman_violation_vs_residual']:+.3f}, "
        f"p = {g['p_value']:.1e} | `e97_principal_curve_selfconsistency_results.json` |",
        f"| Gaussian (BvM) orientation error | {b['gaussian_tangent_error_deg']:.2f}° vs "
        f"{b['arc_corrected_curve_error_deg']:.2f}° ({b['ratio']:.1f}×) "
        "| `e98_framework_audit_results.json` |",
        f"| posterior cache | no subsampling; {e94m['rows_stored_exactly']}/{e94m['n_group_rows']} rows "
        f"in full, {e94m['samples_stored'] / 1e6:.1f} M samples "
        "| `e94_posterior_cache_manifest.json` |",
    ]

    strongest = [
        "| claim | number | why it holds up |",
        "|---|---|---|",
        f"| out-of-sample reconstruction | ${A['O4a']['own_q']:.2f}^\\circ$ (O4a), "
        f"${A['O4b']['own_q']:.2f}^\\circ$ (O4b) | locked before data on O4b; two disjoint catalogs |",
        f"| non-triviality vs permutations | below the **minimum** of {A['O4a']['perm_null']['n']} draws "
        f"in all three catalogs | $p < 1/{A['O4a']['perm_null']['n']}$ each; not a single shuffle |",
        f"| cross-waveform transfer | ${X['A_to_B']:.2f}^\\circ$ / ${X['B_to_A']:.2f}^\\circ$ vs a "
        f"${X['family_axis_disagreement']:.2f}^\\circ$ reference scale | answers the same-posterior "
        "circularity objection |",
        f"| residual is real, not sampling noise | ${mc['median_abs_err_deg']:.2f}^\\circ$ vs "
        f"${mc['median_bootstrap_sigma_deg']:.2f}^\\circ$ resolution "
        f"(${mc['median_ratio_err_over_sigma']:.0f}\\times$) | joint bootstrap on the full samples; "
        "correlated MC errors cancel |",
        f"| residual has a mechanism | $\\rho = {g['spearman_violation_vs_residual']:+.2f}$, "
        f"$p = {g['p_value']:.0e}$, robust across a grid sweep | a correlation between measured "
        "quantities, not a fit |",
    ]

    weakest_o4b = (
        f"4. **O4b is the weakest panel of Figure 2**: pooled-$q$ (${f1c['O4b']['pooled_q_deg']:.2f}^\\circ$) "
        f"and tangent (${f1c['O4b']['tangent_deg']:.2f}^\\circ$) are closest together there, and its null "
        f"minimum (${f1c['O4b']['perm_null']['min']:.2f}^\\circ$) sits nearest own-$q$ "
        f"(${f1c['O4b']['own_q_deg']:.2f}^\\circ$)."
    )
    signed_o4b = (
        f"2. **The signed residual is not significant in O4b** "
        f"($p = {e92['signed_residual']['O4b']['sign_test_p']:.3f}$) — the newest and largest catalog — "
        f"though it is in GWTC-3 ($p < 0.001$) and O4a "
        f"($p = {e92['signed_residual']['O4a']['sign_test_p']:.3f}$). The paper reports it per catalog for "
        "this reason; if you think the signed effect is a training-set artifact, that is a live position."
    )
    e100 = art("results/e100_frames_and_bands_results.json")["arc_length_vs_tangent_error"]
    arc = ", ".join(f"{v['spearman_arc_vs_tangent_err']:+.2f}" for v in e100.values())

    # REFEREE_READINESS numbers its weak claims differently from the packet, so emit its own variants
    signed_rr = (
        f"3. **The signed residual is not catalog-universal**: significant in GWTC-3 (p < 0.001) and O4a\n"
        f"   (p = {e92['signed_residual']['O4a']['sign_test_p']:.3f}), **not significant in O4b "
        f"(p = {e92['signed_residual']['O4b']['sign_test_p']:.3f})** — the newest and largest catalog.")
    weakest_rr = (
        f"4. **O4b is the weakest panel of Figure 2**: its pooled-q ({f1c['O4b']['pooled_q_deg']:.2f}°) and\n"
        f"   tangent ({f1c['O4b']['tangent_deg']:.2f}°) are closest together, and its null minimum\n"
        f"   ({f1c['O4b']['perm_null']['min']:.2f}°) is nearest own-q ({f1c['O4b']['own_q_deg']:.2f}°).")
    arc_rr = (
        f"5. **Arc length correlates negatively with the tangent error** (ρ = {arc} across catalogs), where\n"
        f"   an earlier draft reported it weakly positive and claimed residuals *grow* with elongation. Both\n"
        f"   were wrong; the manuscript does not rest on either.")

    ratio = f"{mc['median_ratio_err_over_sigma']:.0f}"
    # The thesis sentence claims "two later, disjoint event catalogs", which is O4a and O4b. GWTC-3 is
    # the TRAINING catalog, so including it in that range mixes in a number the sentence does not claim.
    OUT = ("O4a", "O4b")
    span = lambda fn, cats: f"{min(fn(c) for c in cats):.2f}"+"–"+f"{max(fn(c) for c in cats):.2f}"
    own_span = span(lambda c: A[c]["own_q"], OUT)
    tan_span = span(lambda c: A[c]["tangent"], OUT)
    degrade = [A[c]["pooled_q"] / A[c]["own_q"] for c in CATS]
    npm = A["O4a"]["perm_null"]["n"]

    thesis_rr = (
        "The orientation of a compact-binary $(m_1,m_2)$ posterior can be **reconstructed** from a single\n"
        "one-dimensional marginal of that same posterior — its mass-ratio marginal — using the\n"
        f"constant-chirp-mass curve, with no coefficient calibrated on the validation catalogs, to a median\n"
        f"{own_span}° on elongated events across the two later, disjoint event catalogs\n"
        f"(O4a {A['O4a']['own_q']:.2f}°, O4b {A['O4b']['own_q']:.2f}°). This is not the trivial\n"
        "statement that a curve beats a line: substituting any other event's mass-ratio marginal degrades it\n"
        f"{min(degrade):.0f}–{max(degrade):.0f}× and the achieved error lies below the minimum of {npm} "
        "permutations, while the\n"
        "reconstruction transfers between separately inferred waveform-family posteriors of the same event.\n"
        f"The residual ~1° is a real systematic, about {ratio}× the Monte Carlo resolution of the released\n"
        f"samples, whose size is predicted by the curve's failure of Hastie–Stuetzle self-consistency\n"
        f"(ρ = {g['spearman_violation_vs_residual']:+.2f}, p = {g['p_value']:.0e}).")

    thesis_packet = (
        "The orientation of a compact-binary $(m_1,m_2)$ posterior can be **reconstructed** from a single\n"
        "one-dimensional marginal of that same posterior — its mass-ratio marginal — via the shape of the\n"
        "constant-chirp-mass curve, with no coefficient calibrated on the validation catalogs, to a median\n"
        f"${own_span}^\\circ$ on elongated events (axis ratio $\\ge 3$) in the two later, disjoint event\n"
        f"catalogs (O4a ${A['O4a']['own_q']:.2f}^\\circ$, O4b ${A['O4b']['own_q']:.2f}^\\circ$).\n"
        "The median-point tangent approximation, which underlies rapid parameter-estimation tools, gets\n"
        f"${tan_span}^\\circ$ on the same events. This is not merely \"a curve beats a line\": substituting any\n"
        f"other event's mass-ratio marginal degrades the result ${min(degrade):.0f}$–${max(degrade):.0f}"
        "\\times$ and the achieved error falls below the\n"
        f"**minimum** of {npm} catalog-stratified permutations, while the reconstruction transfers between\n"
        "separately inferred waveform-family posteriors of the same event. The residual $\\sim1^\\circ$ is a\n"
        f"genuine systematic, about ${ratio}\\times$ the Monte Carlo resolution of the released samples, and its\n"
        "per-event size is predicted by the curve's failure of Hastie–Stuetzle self-consistency\n"
        f"($\\rho = {g['spearman_violation_vs_residual']:+.2f}$, "
        f"$p = {g['p_value']:.0e}$).")

    cache_cmd = (
        "```bash\n"
        "# one-time cache: the ONLY routine HDF5 pass in the project (~104 s measured; I/O-bound)\n"
        "python3 src/e94_build_posterior_cache.py          # writes results/e94_posterior_cache.npz\n"
        f"                                                  # (~{cache_mb()} MB, no subsampling, gitignored)\n"
        "```")

    return {"thesis-rr": thesis_rr, "thesis-packet": thesis_packet, "cache-cmd": cache_cmd,
            "key-numbers": "\n".join(key), "strongest-claims": "\n".join(strongest),
            "weakest-o4b": weakest_o4b, "signed-o4b": signed_o4b,
            "signed-rr": signed_rr, "weakest-rr": weakest_rr, "arc-rr": arc_rr}


def apply(path, made):
    with open(os.path.join(ROOT, path)) as fh:
        text = fh.read()
    n = 0
    for name, body in made.items():
        pat = re.compile(r"(<!-- BEGIN GENERATED: %s -->).*?(<!-- END GENERATED: %s -->)"
                         % (re.escape(name), re.escape(name)), re.S)
        text, k = pat.subn(lambda m: m.group(1) + "\n" + body + "\n" + m.group(2), text)
        n += k
    with open(os.path.join(ROOT, path), "w") as fh:
        fh.write(text)
    return n


def main():
    made = blocks()
    total = 0
    for p in ("docs/REFEREE_READINESS.md", "docs/EXTERNAL_READER_PACKET.md"):
        k = apply(p, made)
        total += k
        print(f"  {p}: {k} generated block(s)")
    print(f"rewrote {total} blocks from committed artifacts")


if __name__ == "__main__":
    main()
