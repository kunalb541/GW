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
    resid_ratio = (
        f"a real systematic, about {mc['median_ratio_err_over_sigma']:.0f} times the Monte Carlo "
        f"resolution of the released samples"
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

    return {"key-numbers": "\n".join(key), "strongest-claims": "\n".join(strongest),
            "weakest-o4b": weakest_o4b, "signed-o4b": signed_o4b, "residual-ratio": resid_ratio,
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
