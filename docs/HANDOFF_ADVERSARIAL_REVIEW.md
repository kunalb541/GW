# HANDOFF — for adversarial review (round 3)

**Date:** 2026-07-21 · **Repo:** <https://github.com/kunalb541/GW> · **Branch:** `main` · **Head:** `3f0c9a3`
**Paper:** [`paper/manuscript.pdf`](../paper/manuscript.pdf), 13 pp · **Tests:** 158, all passing ·
**Generated macros:** 120 from 15 artifacts

This document exists to be attacked. The previous external review returned **Major Revision / Not Yet
Referee-Ready** with ten findings. All ten are closed. Closing them surfaced six further errors that the
review had not caught, one of which changed a claim in the abstract. That pattern — *the fix finds more
than the finding did* — is the reason for another hostile pass rather than a victory lap.

**Please do not treat "all findings closed" as a reason to go easy.** The base rate in this project is
that every audit finds something real. If this one doesn't, the most likely explanation is that it wasn't
hard enough.

---

## The one-command check that makes most proofreading unnecessary

```bash
python3 src/build_paper_numbers.py && python3 src/build_manuscript_figures.py && git diff --stat
```

Empty diff ⇒ every number in the PDF matches the committed artifacts. Non-empty ⇒ the paper disagrees
with its own results and that is a bug. This is the single highest-value thing to run first.

---

## What changed since the last review

### The ten review findings

| # | finding | what was done |
|---|---|---|
| F1 | abstract/Table 1 say `1.26/1.22`, figures say `1.32/1.00` — reads as internal contradiction | Table 1 caption now declares itself **locked full-sample**, names the cache values explicitly, and the difference is *measured* (E99), not asserted |
| F2 | stale cross-waveform numbers | now `2.25/2.93` vs `2.03`, from the artifact |
| F3 | cache subsampling undisclosed | disclosed — and corrected: it is **bootstrap with replacement**, not subsampling. Quantified by E99 |
| F4 | one transfer direction only; "below all 300" asserted not shown | E95 stores `tangent_B_to_A` (6.20 vs 3.50) and **all 300 raw permutation draws** |
| F5 | "mathematical explanation" overclaims | → "strongly tracked by a measurable geometric quantity", with an explicit *tracks ≠ explains* sentence |
| F6 | data availability incomplete | GWTC-2.1/3 listed; dangling-symlink trap documented |
| F7 | Figure 2a panel 3 unreadable | zoom inset **plus** a measurement that the failure is not a tail artifact — see below |
| F8 | permutation null not auditable | 300 raw draws committed |
| F9 | Hastie–Stuetzle citation now load-bearing | flagged as such in `CITATION_VERIFICATION.md` |
| F10 | README/citation docs stale | updated; a test now fails on uncited bibitems |

Bernstein–von Mises was invoked by content with nothing cited. Rather than add a reference for a theorem
the argument does not need, §3 now claims only the elementary fact it does need — the principal axis of a
Gaussian is its covariance eigenvector — and **explicitly disclaims** the asymptotic statement.

### The six errors the fixes found

Wiring the body prose to the artifacts (only captions were generated before; the body carried ~130
hand-typed literals) surfaced these:

| was | is | provenance of the error |
|---|---|---|
| abstract cross-waveform `2.1°` vs `2.0°` | `2.25°/2.93°` vs `2.03°` | body was corrected, abstract was not |
| round-posterior band `14.5°` | **`16.3°`** | transcribed from a markdown note that had drifted |
| paired frame `p = 4×10⁻⁹` | **`8×10⁻⁸`** | same note |
| arc-length `ρ = +0.26, +0.02, +0.12` | **`−0.51, −0.61, −0.42`** | **sign was wrong**; matched no artifact, and did not match its own source note either |
| training win fraction `81%` | `76%`, labelled cache-derived | no artifact ever existed; `0.81` appears to be a transcribed *degree* value |
| GWTC-4.0 cited as `arXiv:2508.18080` | **`2508.18082`** | `18080` is a different companion paper |

**The sixth is structural and is the most important thing in this document.** A unit test written on a
wrong assumption failed and revealed that `ψ_curve` is **exactly invariant to chirp mass** — rescaling
`Mc` is a dilation, which preserves covariance eigenvectors (verified to 10 decimals; locked by
`test_curve_angle_is_exactly_independent_of_chirp_mass`). The paper had described the reconstruction as
taking **two** inputs (median chirp mass + q marginal). **It takes one**: the q marginal. `Mc` still
positions the curve for the thickness/self-consistency/figure work, but contributes nothing to the
predicted orientation. No number changed; the thesis sentence, the definition, the cross-family
description and the discussion did.

*Attack this one hardest.* If the input count was wrong for this long, ask what else about the
construction is misdescribed.

### Data attribution (was entirely absent)

There was **no acknowledgments section, no data citation, and no licence statement**. Now:

- GWOSC's mandated sentence **verbatim**, plus the full funder list, verified at `gwosc.org/acknowledgement`.
- **Three** GWOSC data papers, one per observing run — we were citing only the O3 paper while running the
  two locked tests on O4a and O4b data. That was a real omission.
- Both catalog papers verified at their arXiv abstract pages: GWTC-4.0 `2508.18082`, GWTC-5.0 `2605.27225`.
- **Authorship checked, not assumed:** GWOSC imposes attribution and citation requirements and *no*
  authorship condition. The paper states explicitly that the author is not a collaboration member, that
  the LVK has not reviewed the analysis, and that it bears no responsibility for the conclusions.

### New batteries

- **E99** (`e99_cache_stability_audit`) — is the cache representative? Reads full-length posteriors once.
- **E100** (`e100_frames_and_bands`) — frames, coordinates, elongation bands, matched-axis-ratio control,
  win fractions, arc-length correlation. These had lived **only as prose** in a gate note.

---

## Where to attack — ranked by where I think it will break

### 1. The cache failed its own fitness criterion — and everything downstream rides on it

`results/e99_cache_stability_audit_results.json` → `verdict.fit_for_purpose: **false**`.

| catalog | full sample | cache mean (5 seeds) | seed range | bias |
|---|---|---|---|---|
| GWTC-3 | 0.80 | 0.78 ± 0.04 | [0.74, 0.84] | −0.02 |
| O4a | **1.26** | 1.23 ± 0.20 | [0.94, 1.48] | −0.02 |
| O4b | 1.19 | 1.13 ± 0.11 | [0.97, 1.24] | −0.06 |

The cache is **unbiased** (max 0.06°) but a single seed scatters by up to **0.54°**, against my own
threshold of 0.5°. Every downstream battery — E92, E95, E96, E97, E98, E100 and all three figures — runs
on **one draw** of that extract. Effects discussed at the ~1° level sit inside that noise.

The paper discloses this and quotes locked full-sample numbers for anything headline. **I still think
this is the strongest available attack.** Reasonable positions a referee could take:

- the cross-family improvements (`1.14→0.96`, `p=0.005`) are within resampling noise and not established;
- the E97 correlation `ρ=0.68` should be reported with a seed-to-seed error bar it does not have;
- the whole downstream layer should be re-run at larger `N_SAMP` or averaged over seeds before submission.

The fix is cheap (rebuild the cache, re-run downstream). **It has not been done.** If you think it must
be, say so plainly and it will be.

Note also the non-monotonicity in `by_draw_size`: O4a reads 1.08 / 1.33 / 1.38 at n = 2000 / 4000 / 8000.
That is not obviously converging, and I do not have a good explanation for it. Push on this.

### 2. §6 and §8–9 have never been claim-audited

`CITATION_VERIFICATION.md` states it outright: the coherence section and the two Context sections predate
all the gate work and were reviewed for **citation integrity only, never for claim strength**. §1–5 have
been through five audits; these three have been through none. They are labelled exploratory/Context, but
that labelling has not been tested against the prose. **This is unexamined territory — start here if §1–5
proves hard.**

### 3. The circularity objection may not be fully answered

The q marginal is taken from the very posterior being reconstructed. The reply is the cross-waveform
transfer. But the two waveform families analyse **the same strain with shared calibration and priors** —
the paper says so — so the test excludes reuse of one posterior's Monte Carlo noise, not correlated
modelling error common to both. Is that a *sufficient* answer? I am genuinely unsure. Now that the
reconstruction is known to use only the q marginal, the question sharpens: **how much of the orientation
is already determined by the q marginal for any plausible curve family?** The permutation null addresses
"any other event's q", not "any other curve".

### 4. Things that are known-weak and stated, but that you may think are stated too gently

- **Gate E (precision law) is NOT PASSED.** Hard-coded as such; a test fails if it changes.
- **O4a's preregistration is not publicly timestamped** — prereg and results entered the public repo in
  the same commit. Only O4b's lock is verifiable from the public record. The two out-of-sample scores are
  **not** equal evidence.
- **The signed residual is not significant in O4b** (`p = 0.377`), the newest and largest catalog.
- **O4b is the weakest panel** of Figure 2: pooled-q and tangent nearly coincide there.
- **The self-consistency correction does not clear the out-of-sample bar** (`p = 0.024 / 0.064`).
- **Arc-varying thickness is not established**; a constant taper does as well in one direction.
- **§8's Spearman `−1.00`** is determinism of the forward model, not an empirical result.
- **Waveform choice is the dominant per-event systematic.** Concretely, on the worst-case event the error
  spans **14.4° / 16.9° / 22.7°** across its three families (axis ratio 5.5 / 4.3 / 2.3). Measured while
  fixing F7; **noted here but deliberately not yet in the paper**, where limitation 8 still asserts "a few
  degrees" without a number. Tell me if that is a gap.

### 5. Figure 2a panel 3 (F7) — check the reasoning, not the cosmetics

The review asked for a rescale or a move to supplementary. Rescaling alone would have been cosmetic, so
instead: is the 16.9° worst case a real failure, or an outlier dragging the sample covariance? That
posterior has a median m₁ of 60 M⊙ and a tail to 613.

Trimming to the central 90% of samples leaves it at **16.4–18.6°**. Not a tail artifact. Recorded in the
sidecar, stated in the caption, locked by a test that fails if trimming ever drops it below 10°.

A zoom inset now shows the core: the measured axis tilts *up* while both predictions go *down*. Same three
lines, not a re-fit. **Check that I have not accidentally made a failure look like a success.**

---

## Specific things to try to break

1. **Run the regeneration check above.** Any diff is a bug.
2. **Attack the Mc-invariance claim.** If `ψ_curve` really is independent of chirp mass, is the
   "curved *chirp-mass* law" framing still honest? Is the permutation null testing the right thing now
   that we know only q enters? (I believe yes — it permutes q — but argue it.)
3. **Attack the cache.** Recompute any headline number under a different seed and see how much it moves.
   `E99_SEEDS` is the entry point; `src/e94_build_posterior_cache.py` has `N_SAMP = 4000`, `SEED = 94`.
4. **Attack the guard.** `tests/test_paper_numbers.py::test_no_generated_value_is_also_hardcoded` skips
   values shorter than 4 characters, so a hand-typed `1.5` or `3.3` could still slip in. Is that hole
   exploitable in practice? Find a number in the PDF that is *not* macro-backed.
5. **Attack E100.** It was written by the same process that produced the errors it corrects. The
   arc-length definition (curve length between the 5th and 95th percentiles of q, normalised by the
   posterior's own scale) is **my** choice and is not preregistered. Does the negative correlation survive
   a different normalisation? It may just be re-measuring elongation.
6. **Check the corrections are corrections.** For each of the six errors above, verify the *new* value
   against the artifact independently. A wrong fix is worse than the original error.
7. **Hunt for surviving overclaims.** Search the PDF for `predict`, `independent`, `explain`, `coverage`,
   `invariant`, `test of general relativity`. Each should be a denial or narrowly scoped. Use word
   boundaries — a naive search for `proves` matches *improves*.

---

## Reproduce

Data are **not** distributed; all sources are public and pinned in
[`DATA_AVAILABILITY.md`](DATA_AVAILABILITY.md).

> ⚠️ In the author's working copy `data/chains/gw_posteriors` is a **symlink** to a sibling private repo.
> A fresh clone gets a **dangling link** and GWTC-3 silently drops out of every analysis (190 events
> instead of 266) **without raising an error**. Replace it with a real directory first.

```bash
python3 src/e94_build_posterior_cache.py     # one-time, ~5 min, the ONLY routine HDF5 pass

python3 src/e95_gate_regeneration.py         # Gates A/C/D
python3 src/e92_curve_uncertainty.py         # Gate B
python3 src/e93_precision_law.py             # Gate E -- writes NOT PASSED
python3 src/e96_curve_thickness_mechanism.py
python3 src/e97_principal_curve_selfconsistency.py
python3 src/e98_framework_audit.py
python3 src/e100_frames_and_bands.py
python3 src/e99_cache_stability_audit.py     # SLOW (~45 min): full-length posteriors

python3 src/fig1b_tangent_vs_curve_residual.py
python3 src/fig1c_nontriviality_q_baselines.py
python3 src/fig2a_posterior_geometry_examples.py
python3 src/build_manuscript_figures.py      # captions from sidecars
python3 src/build_paper_numbers.py           # every number -> paper/numbers.tex

cd paper && pdflatex manuscript.tex && pdflatex manuscript.tex
python3 -m pytest tests/ -q                  # 158 tests, data-free
```

`results/paper_macro_sources.json` is the machine-readable macro → value → artifact → json-path map for
all 120 numbers. Use it to check any figure in the PDF against its source without reading LaTeX.

---

## Known-open, non-defect

- Both catalog papers are **preprints**; upgrade to journal refs if they publish before submission.
- Re-check the GWOSC acknowledgment boilerplate at submission — it changes as runs are released.
- Task #18 in the tracker (download GW250114 strain) is **stale**: superseded when the ringdown analysis
  was retracted for prior domination. Should be deleted.

## Ground rules for this review

Findings should name a **file and line**, state the **failure scenario concretely**, and — where the claim
is numerical — say **which artifact contradicts it**. "This feels overstated" is actionable only with the
sentence quoted and a proposed replacement. If a finding is that something is *missing*, say what
measurement would settle it.

Two prior results were **withdrawn** during this program and are disclosed in the paper: an apparent 3σ
GR deviation (demoted to a systematic) and a Bayesian ringdown analysis (retracted for prior domination).
Retraction is a normal outcome here. If something in this paper should be withdrawn, say so directly.
