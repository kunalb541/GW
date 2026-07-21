# HANDOFF — for adversarial review (round 3)

**Date:** 2026-07-21 · **Repo:** <https://github.com/kunalb541/GW> · **Branch:** `main` · **Analysis state:** `c167e27` (the commit that produced the current artifacts;
later commits are documentation only)
**Paper:** [`paper/manuscript.pdf`](../paper/manuscript.pdf), 13 pp · **Tests:** 165, all passing ·
**Generated macros:** 120 from 16 artifacts

This document exists to be attacked. The previous external review returned **Major Revision / Not Yet
Referee-Ready** with ten findings. All ten are closed. Closing them surfaced six further errors that the
review had not caught, one of which changed a claim in the abstract. That pattern — *the fix finds more
than the finding did* — is the reason for another hostile pass rather than a victory lap.

**Please do not treat "all findings closed" as a reason to go easy.** The base rate in this project is
that every audit finds something real. If this one doesn't, the most likely explanation is that it wasn't
hard enough.

---

## What the automated checks do and do not prove

Read this before trusting a green suite. The 165 tests and the three generator scripts are **regression
tests for known failure modes**, not evidence of global consistency, and this project has now produced
four separate demonstrations of the difference:

- The generated-numbers pipeline propagated a broken posterior cache faithfully into every derived
  number, and "corrected" three values that had been right. Every test passed throughout, because the
  tests check that the paper matches the artifacts, not that the artifacts are correct.
- The stale-doc guard checked four documents **by name**, so `TESTING.md` and `PAPER_PLAN.md` drifted
  through the gap.
- Its test-count lookbehind excluded letters but not digits, so `E71 tests this on O4b` was read as a
  claim of "1 test".
- It matched `165 tests` but not `Tests: 164`, so a stale count sat in this file's own header through a
  full review round with the suite green.

Each guard was correct about the case that motivated it and blind to a neighbour. Treat a passing suite
as "the previously-found mistakes have not returned" and nothing more. Where you want assurance, check
the artifact, not the test.

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

### The corrections — and the three that turned out to be wrong

Wiring the body prose to the artifacts (only captions were generated before; the body carried ~130
hand-typed literals) surfaced six apparent errors. **Three of them were not errors.** They were artifacts
of the cache described in the next section, and the regenerated values return to the originals:

| item | original prose | "correction" | now, exact cache | verdict |
|---|---|---|---|---|
| cross-waveform transfer | 2.08 / 2.78 vs 1.99 | 2.25 / 2.93 vs 2.03 | **2.08 / 2.78 vs 1.99** | original was right |
| round-posterior band | 14.5° | 16.3° | **14.6°** | original was right |
| paired frame p | 4e-9 | 8e-8 | **6e-9** | original was right |
| arc-length rho | +0.26, +0.02, +0.12 | −0.51, −0.61, −0.42 | **−0.51, −0.57, −0.49** | **stands — the sign was wrong** |
| training win fraction | 81% | 76% | **78%** | both off; no locked artifact exists, cell labelled cache-derived |
| GWTC-4.0 arXiv id | 2508.18080 | 2508.18082 | **2508.18082** | stands (unrelated to the cache) |

**Attack this.** Every test passed while the paper carried three wrong "corrections", because the tests
check that the paper matches the artifacts — not that the artifacts are right. The generated-numbers
system faithfully propagated a broken cache. It is a guard against drift, not against being wrong, and
this document should not be read as claiming otherwise.

A seventh finding is structural and unaffected by the cache: `ψ_curve` is **exactly invariant to chirp
mass** — rescaling `Mc` is a dilation, which preserves covariance eigenvectors (verified to 10 decimals;
locked by `test_curve_angle_is_exactly_independent_of_chirp_mass`). The paper had described the
reconstruction as taking **two** inputs. **It takes one**: the q marginal. `Mc` still positions the curve
for the thickness/self-consistency/figure work, but contributes nothing to the predicted orientation.

*Attack this one hardest too.* If the input count was wrong for this long, ask what else about the
construction is misdescribed — and note that "chirp-mass law" is now partly branding, since the chirp
mass does not enter the orientation at all.

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

### 1. ~~The cache failed its own fitness criterion~~ — FIXED, but verify the fix

**This was the blocker in the previous round and it has been repaired at the root.** The cache used to
draw 4000 samples per row **with replacement**. Two things were wrong with that. It discarded ~76% of the
information (the median posterior has ~16.7k usable samples), and because the draw was
`min(n_samp, len(idx))` indices sampled with replacement, it bootstrapped **even when the cap exceeded the
sample count** — so it never used the full sample at any setting, and its noise did not decay as the cap
grew. That is why O4a read 1.08 / 1.33 / 1.38 at caps of 2000 / 4000 / 8000: not a converging sequence.

The cache now performs **no subsampling at all**: 23.1 M samples, **972 of 972 rows stored in full**,
572 MB. A cache-backed number is now a full-sample number and carries no resampling noise of its own.
Every downstream battery and all three figures were re-run.

**Verification** — the rebuilt cache reproduces an independent pass that re-reads the HDF5 files directly:

| catalog | independent full-sample pass | cache | locked |
|---|---|---|---|
| O4a | 1.26 | **1.26** | 1.26 |
| O4b | 1.19 | **1.19** | 1.22 |
| GWTC-3 | 0.80 | 0.88 | — |

O4a and O4b agree exactly, and O4a matches the locked preregistered score. The F1 "internal
contradiction" flagged in the last review has therefore **disappeared** rather than been explained away.
GWTC-3 differs by 0.08° on one extra event, from a preferred-waveform-group convention rather than
sampling — **that residual difference is worth checking; I have asserted the cause rather than proved it.**

Things that moved as a result, all of which deserve scrutiny:

- the Monte Carlo resolution fell from 0.19° to **0.07°**, so the residual is now **17×** the resolution
  rather than 6×. The "residual is real" claim got stronger — confirm it did so for the right reason
  (more samples ⇒ finer resolution) and not through a bug in the bootstrap;
- E97 cross-family A→B went to p = 0.002 and B→A to p = 0.107. The "improves in both directions but
  significant in only one" framing survives, but the directions swapped in strength;
- the elongated-event count went 81 → 80;
- `results/e99_cache_stability_audit_results.json` **describes the retired scheme.** Its
  `fit_for_purpose: false` verdict is a record of the old cache, not the current one. It is kept as
  provenance and its `full_sample_reference` block is the independent check used above. Do not read its
  verdict as current — and tell me if leaving it in the repo unrelabelled is too confusing.

### 2. §6 and §8–9 — now claim-audited once, which is not the same as clean

These sections predate all the gate work and had been reviewed for **citation integrity only**. A
claim-discipline pass has now been done (prose only, no new compute), which changed three things:

- §6's outlier-atlas null now states its own power limitation — a null on $n=32$ events bounds a large
  physical dependence rather than excluding one. It previously read as a clean "no physical axis survives".
- §6's `3σ` was a hand-typed literal in a paper where every other number is generated; it is now a macro,
  and the surviving correlate carries its ρ and FDR q.
- §8 claimed to map "what each detection measured". It is a forward-model computation, so it now says what
  the model *implies* each detection measured.

**One pass by the same author who wrote the prose is weak evidence.** §1–5 have been through six audits;
these have had one, by me, today. Treat them as the least-examined part of the paper and read them
adversarially — particularly §6's claim that coherence can diagnose systematics at all, which is argued
rather than demonstrated, and §8's status as Context that nonetheless occupies a full section.

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
- **The signed residual is not significant in O4b** (`p = 0.110`), the newest and largest catalog.
- **O4b is the weakest panel** of Figure 2: pooled-q and tangent nearly coincide there.
- **The self-consistency correction does not clear the out-of-sample bar** (`p = 0.002 / 0.107` —
  significant in one direction only; the directions swapped in strength after the cache rebuild).
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
3. **Attack the cache.** It no longer subsamples — `N_SAMP = None` in
   `src/e94_build_posterior_cache.py`, and the manifest reports 972 of 972 rows stored in full — so there
   is no seed to vary and no resampling noise left to find. The attack is therefore on the *claim of
   exactness*, not on stability: pick an event, read its posterior straight from the HDF5 file, and check
   the cached arrays are identical rather than merely close. `tests/test_paper_numbers.py` asserts the
   no-bootstrap property and agreement with the independent full-sample pass; try to find a row where
   that agreement is coincidental.
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
python3 -m pytest tests/ -q                  # 165 tests, data-free
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
