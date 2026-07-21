# PLAN — turning the program into its papers

**For:** codex (execution and review) · **Date:** 2026-07-21 · **Repo head:** `422a563`
**Status:** proposal awaiting go/no-go per phase. Nothing here has been started.

## Why this document exists

The manuscript is 14 pp and reports one result. The repository holds **45 batteries with committed
results, 27 preregistrations and 36 reports**; **16 batteries** feed the paper. The author's reaction on
reading the PDF was that the paper looks thin relative to the work, and that reaction is correct for two
independent reasons — one of which is a defect and one of which is a scoping decision that was never
revisited.

**Defect.** Within the paper's own topic, measured sweeps are rendered as prose. The manuscript says
"robust across a sweep of grid resolutions" where four grids were measured and committed; it says the
error "falls monotonically across thresholds from 1.5 to 10" where nine thresholds were measured. A
referee wants to see the sweep, not be told it was done. This was over-correction: an external
readability review asked for compression, and evidence was compressed along with the defensive prose.

**Scoping.** A submission-gate audit narrowed the manuscript from four claims to one. The other three
were not withdrawn and were not shown to be weak — they were declared out of scope for *this* paper and
then left unpublished. 19 batteries sit in that category.

---

## Phase 1 — deepen the current paper (no new compute)

Every number below is already measured and committed. This phase adds no analysis; it promotes measured
material from prose into tables and figures. Expected effect: 14 pp → ~18–20 pp, and the sweeps become
inspectable rather than asserted.

**Hard rule: every new number must come through `src/build_paper_numbers.py`.** For a table of many rows,
add a generator that emits the whole table body as a macro (the pattern `src/build_doc_numbers.py`
already uses for markdown). Do not hand-type table cells — that is the failure mode this repo has spent
four rounds eliminating.

| # | new element | source artifact | json path | notes |
|---|---|---|---|---|
| T2 | Threshold sensitivity | `e92_curve_uncertainty_results.json` | `threshold_sensitivity` | 9 rows: axis-ratio cut, `n`, `curve_median_deg`, `tangent_median_deg`. Supports §5.2's "nothing distinguishes the threshold of 3". |
| T3 | Elongation bands + matched-frame control | `e100_frames_and_bands_results.json` | `axr_bands`, `matched_axis_ratio` | 5 bands and 3 matched bands. Currently one sentence each; the matched-band control is the discriminant for the detector-frame claim and deserves to be visible. |
| T4 | Per-waveform-family scores | `e95_gate_regeneration_results.json` | `gate_D_families` | 9 rows (catalog × waveform group, curve and tangent). This is the evidence for limitation (i), "waveform choice is the dominant per-event systematic", which the paper currently asserts with no number at all. |
| T5 | Mechanism controls | `e96_...json` `cross_family`, `e97_...json` `grid_sweep` | — | E96: measured/constant/linear/quadratic × both directions. E97: 4 grids × (violation, ρ, p, one-iteration residual). Both currently one sentence. |
| T6 | Outlier atlas | `e72_gw_geometry_outlier_atlas_results.json` | `D1_correlations` | 9 pre-declared axes × (ρ, p, partial-ρ, BH q, reject). §5.3 currently states the conclusion without the table; a null result is only credible if the reader sees what was tested. |
| F4 | Permutation null distributions | `e95_...json` | `gate_A.<cat>.perm_null.draws` | 300 raw draws per catalog. Histogram per catalog with own-q marked. The paper's strongest non-triviality claim is "below the minimum of 300 draws" and the distribution is committed but never shown. |
| F5 | Per-event residual vs axis ratio | `e92_...json` | `events` | 266 events, residual and bootstrap σ. Shows the elongation gate is a smooth physical effect rather than a cut, and exposes the tail the worst-case panel samples. |

**Sequencing.** F4 and T6 first — they carry the most argumentative weight per unit of effort. T4 next,
because it removes an unbacked qualitative claim. T2/T3/T5 are straightforward promotions.

**Watch for:** page count and float placement. Figure 3 already required a `\FloatBarrier` to stop it
drifting past the bibliography; adding two figures and five tables will need the float discipline
re-checked, and `tests/test_paper_numbers.py::test_docs_state_the_real_test_and_page_counts` will fail
until the doc page counts are updated.

---

## Phase 2 — companion paper: coherence as a systematics detector

**Batteries:** E45, E46, E47, E55, E57, E58, E59, E60. All eight have a prereg, a committed results JSON
and a report. This was claim #2 in the README before the narrowing audit.

**The claim, stated carefully.** Across a battery of GR consistency tests, apparent anomalies that are
*coherent across events* are method artifacts rather than physics. The current manuscript already
contains the honest caveat that must anchor this paper: coherence alone does not license the inference,
because a genuine physical effect would also be coherent across a catalog. The paper therefore cannot be
"coherent ⇒ systematic". It has to be about the *discriminants* — catalog-to-catalog disagreement
exceeding the quoted statistical error, and effects vanishing in a clean limit — with the geometric
exponent case (Appendix A of the current manuscript) as one worked example among several.

**Before writing anything:** re-verify each battery's numbers against its artifact, exactly as was done
for the current paper. These results predate the cache rebuild. Any that touched the posterior cache must
be re-run — the bootstrap-with-replacement defect corrupted every cache-derived number in the main paper
and there is no reason to assume these escaped. **Treat every number in E45–E60 as unverified until
regenerated.**

**Also required:** E58 has `naive_combined_m_g_eV_PRIOR_DEPENDENT` in its result keys. That name is a
warning left by the author. Whatever it is, it must be resolved or excluded before publication, not
carried forward.

---

## Phase 3 — the remaining independent results

Lower priority, and each is a separate paper rather than a section:

- **E68, PTA cross-experiment anatomy.** Four pulsar-timing arrays; inter-PTA offsets along the common
  A–γ degeneracy; a preregisterable successor prediction for IPTA DR3. Self-contained.
- **E66, spectral-siren obstruction.** What sirens can and cannot arbitrate; mass-scale as the dominant
  systematic lever.
- **E63, neutron-star equation of state.** Cross-messenger; uses the same geometric machinery.
- **E38–E44, early mass-plane geometry.** E40 is the direct ancestor of the current paper's result (the
  tangent law). Most likely absorbed as background rather than published separately.

---

## What must not happen

1. **No new numbers typed by hand.** Everything through the generators, including table bodies.
2. **No battery published without regenerating it against the current cache.** Three numbers in the main
   paper were "corrected" to wrong values because a broken cache was trusted; the same cache fed the
   earlier batteries.
3. **No preregistration written after the fact.** If a Phase 2 or 3 result needs a decision that was not
   preregistered, it is post-hoc and must be labelled so, as Gate E already is.
4. **Do not let Phase 1 restore the audit prose.** The readability review was right that the paper read
   defensively. The fix is to show the sweeps as tables, not to re-narrate every caveat in the text.

## Phase 0 — two things that outrank everything above

Raised by an external review of the built PDF, and both are cheap relative to their weight.

**0a. "Why does this matter" is asserted, not demonstrated.** The paper shows the arc beats the tangent
by a factor of $\GaussRatio$, then says the correction is essentially free for applications that use
posterior orientation. Nothing shows that an orientation error of this size changes a downstream
conclusion. Two routes: find one concrete consumer (a population/hierarchical pipeline or a low-latency
tool that uses a Gaussian approximation to the single-event posterior) and show the correction moves
something; or promote Sec 5.3, which is arguably the most novel result in the paper and is currently
undersold — across nine pre-declared physical axes the only surviving correlate of the residual is
waveform-model disagreement, which is a usable systematics diagnostic. The second is cheaper and uses
work already done. **This is the first thing a referee will ask and the paper currently has no answer.**

**0b. The O4a preregistration is not independently timestamped.** Limitation (iv) says so honestly, which
means half the out-of-sample claim rests on the author's word. A dated third-party deposit (Zenodo, OSF)
of the O4a prereg *as it stood*, with the existing private history as supporting evidence, would convert
this from an admission into a verifiable fact. This is the single item most likely to decide whether a
skeptical referee treats the central claim as established or asserted. It requires no analysis, only a
deposit — but it must be honest about the deposit date being later than the original lock.

## Open question for the author

Phase 1 is unambiguous — the material is measured, committed, and currently invisible. Phases 2 and 3 are
a decision about how much of the program to publish and in what order. My recommendation is Phase 1 now,
Phase 2 next as a genuinely separate manuscript, and Phase 3 only if the first two land.
