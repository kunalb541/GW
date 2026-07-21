# EXTERNAL READER PACKET

**Repo** <https://github.com/kunalb541/GW> · **state handed off at commit `c167e27`** (this packet is
committed immediately after; it changes no analysis) · **PDF** [`paper/manuscript.pdf`](../paper/manuscript.pdf),
13 pp · 165 contract tests, all passing.

Contact: Kunal Bhatia, ORCID [0009-0007-4447-6325](https://orcid.org/0009-0007-4447-6325).

---

## The thesis, in one paragraph

<!-- BEGIN GENERATED: thesis-packet -->
The orientation of a compact-binary $(m_1,m_2)$ posterior can be **reconstructed** from a single
one-dimensional marginal of that same posterior — its mass-ratio marginal — via the shape of the
constant-chirp-mass curve, with no coefficient calibrated on the validation catalogs, to a median
$1.19–1.26^\circ$ on elongated events (axis ratio $\ge 3$) in the two later, disjoint event
catalogs (O4a $1.26^\circ$, O4b $1.19^\circ$).
The median-point tangent approximation, which underlies rapid parameter-estimation tools, gets
$4.20–6.67^\circ$ on the same events. This is not merely "a curve beats a line": substituting any
other event's mass-ratio marginal degrades the result $3$–$11\times$ and the achieved error falls below the
**minimum** of 300 catalog-stratified permutations, while the reconstruction transfers between
separately inferred waveform-family posteriors of the same event. The residual $\sim1^\circ$ is a
genuine systematic, about $17\times$ the Monte Carlo resolution of the released samples, and its
per-event size is predicted by the curve's failure of Hastie–Stuetzle self-consistency
($\rho = +0.68$, $p = 7e-12$).
<!-- END GENERATED: thesis-packet -->

## What to read first

1. **This packet**, then [`REFEREE_READINESS.md`](REFEREE_READINESS.md) — the honest summary, including
   what is *not* claimed.
2. **The manuscript, §1–5.** That is the hardened core: definition, non-triviality, residual, frames.
3. **Figures 1–3** and their sidecar JSONs in `figures/` — every plotted number is machine-readable.
4. Skip to [`CITATION_VERIFICATION.md`](CITATION_VERIFICATION.md) if you want the literature audit
   (two claims narrowed, two citations removed as unsupported).

§6 is a diagnostics section with explicitly stated limits. §7–9 are labelled **exploratory** or
**Context** and are not evidence for the main claim.

## Strongest claims (attack these last)

<!-- BEGIN GENERATED: strongest-claims -->
| claim | number | why it holds up |
|---|---|---|
| out-of-sample reconstruction | $1.26^\circ$ (O4a), $1.19^\circ$ (O4b) | locked before data on O4b; two disjoint catalogs |
| non-triviality vs permutations | below the **minimum** of 300 draws in all three catalogs | $p < 1/300$ each; not a single shuffle |
| cross-waveform transfer | $2.08^\circ$ / $2.78^\circ$ vs a $1.99^\circ$ reference scale | answers the same-posterior circularity objection |
| residual is real, not sampling noise | $1.07^\circ$ vs $0.07^\circ$ resolution ($17\times$) | joint bootstrap on the full samples; correlated MC errors cancel |
| residual has a mechanism | $\rho = +0.68$, $p = 7e-12$, robust across a grid sweep | a correlation between measured quantities, not a fit |
<!-- END GENERATED: strongest-claims -->

## Weakest claims (attack these first)

1. **O4a's preregistration is not publicly timestamped.** Its prereg and results entered the public repo
   in the *same commit*; only O4b's lock (17 h gap, explicit commit message) is verifiable from the public
   record. Treat the two out-of-sample scores as *unequal* evidence.
<!-- BEGIN GENERATED: signed-o4b -->
2. **The signed residual is not significant in O4b** ($p = 0.110$) — the newest and largest catalog — though it is in GWTC-3 ($p < 0.001$) and O4a ($p = 0.019$). The paper reports it per catalog for this reason; if you think the signed effect is a training-set artifact, that is a live position.
<!-- END GENERATED: signed-o4b -->
3. **Gate E (the precision law) is NOT PASSED.** The pooled fit rejects the $5/3$ mass exponent
   ($z = -3.5$); agreement appears only in a light-mass band whose edges were chosen *after* seeing that
   rejection. `src/e93_precision_law.py` hard-codes `gate_E_status = "NOT PASSED - exploratory"` and a
   test fails if that changes.
<!-- BEGIN GENERATED: weakest-o4b -->
4. **O4b is the weakest panel of Figure 2**: pooled-$q$ ($3.77^\circ$) and tangent ($4.20^\circ$) are closest together there, and its null minimum ($2.23^\circ$) sits nearest own-$q$ ($1.19^\circ$).
<!-- END GENERATED: weakest-o4b -->
5. **Arc length correlates NEGATIVELY with the tangent error** ($\rho = -0.51 / -0.57 / -0.49$),
   where an earlier draft reported it weakly positive. It may simply be re-measuring elongation. An earlier draft claimed the
   tangent residual *grows* with elongation; the measured correlation is **negative** ($-0.42$ to $-0.69$)
   and the table caption now records that erratum.
6. **The self-consistency correction does not clear the out-of-sample bar** — it improves in both transfer
   directions but reaches $p<0.05$ in only one ($0.024$ / $0.064$).
7. **Arc-varying thickness is not established** — a *constant* taper does as well in one direction.
8. **§8's information anatomy is model-computed, not measured**; its perfect Spearman $-1.00$ is
   determinism of the forward model, not an empirical result.

## Reproduction

**Data are not distributed.** All sources are public and pinned in
[`DATA_AVAILABILITY.md`](DATA_AVAILABILITY.md).

> ⚠️ **Local-path warning.** In the author's working copy `data/chains/gw_posteriors` is a **symlink** to a
> sibling private repository. A fresh clone will have a **dangling link**, and GWTC-3 will silently drop out
> of every analysis (you will get 190 events instead of 266, and the GWTC-3 rows will vanish). Replace it
> with a real directory containing the GWTC-2.1/3 PE files before running anything.

```
data/chains/gw_posteriors/   GWTC-2.1/3 PE      ~6.3 GB    (replace the symlink!)
data/chains/gwtc4/           GWTC-4.0 / O4a     ~11 GB
data/chains/gwtc5/           GWTC-5.0 / O4b     ~41 GB
```

<!-- BEGIN GENERATED: cache-cmd -->
```bash
# one-time cache: the ONLY routine HDF5 pass in the project (~104 s measured; I/O-bound)
python3 src/e94_build_posterior_cache.py          # writes results/e94_posterior_cache.npz
                                                  # (~572 MB, no subsampling, gitignored)
```
<!-- END GENERATED: cache-cmd -->

**Time/resource budget:** ~58 GB download (hours, network-bound); ~5 min cache build; everything
downstream is seconds. The 165 tests need no data and run in ~1 min.

## Checklist for an external reader

- [ ] **Check the paper against its own artifacts in one command.** `python3 src/build_paper_numbers.py`
      rewrites `paper/numbers.tex`; if `git diff` is non-empty, the PDF disagrees with the committed
      results. Every result number in the manuscript is a macro from that file, so there is nothing to
      proofread by hand. `tests/test_paper_numbers.py` enforces this, plus a guard that no generated
      value is *also* typed as a literal.
- [ ] **Verify Figures 1b and 1c from the artifacts.** Every plotted number is in
      `figures/fig1b_*.json` and `figures/fig1c_*.json`; cross-check against
      `results/e95_gate_regeneration_results.json` and `results/e92_curve_uncertainty_results.json`.
      The figure scripts assert this equality at build time — confirm independently.
- [ ] **Check O4b separately.** It is the newest, largest and weakest catalog. Its signed residual is not
      significant, and its baselines are closest together. Does the claim survive on O4b alone?
- [ ] **Inspect Gate E's status.** Open `results/e93_precision_law_results.json` and confirm
      `gate_E_status` reads `NOT PASSED - exploratory` and that every mass band is keyed `*_POSTHOC`.
- [ ] **Inspect the O4a preregistration caveat.** Run
      `git log --format='%ad %h %s' --date=iso -- preregs/E67_gwtc4_curved_law_prereg.md results/e67_gwtc4_curved_law_results.json`
      and confirm they share a commit — i.e. the lock is *not* publicly timestamped, unlike E71's.
- [ ] **Hunt for remaining overclaims.** Search the PDF for `predict`, `independent`,
      `test of general relativity`, `coverage`, `invariant`. Each surviving instance should be either a
      denial or narrowly scoped — as of `c167e27` every `coverage` and `invariant` hit is a denial, and
      the three `test of general relativity` hits are the title-free disclaimers in §1 and §7. Report any
      that are not. (Use word boundaries: a naive search for `proves` matches *improves*, which is how
      this checklist item was first written and is a false positive, not a finding.)
- [ ] **Try to break the non-triviality result.** The obvious attack is that the $q$ marginal encodes the
      answer. The cross-waveform transfer is our reply — if you can construct a case where it fails, that
      is the most valuable thing you could find.

## Open questions we would most like challenged

1. Is the cross-waveform transfer a *sufficient* answer to the circularity objection, given that the two
   waveform families analyse the same strain with shared priors and calibration?
2. Is calling the $1.99^\circ$ family disagreement a "reference scale" rather than an error floor the right framing — could a
   reconstruction legitimately denoise below the families' mutual disagreement?
3. Does the reconstruction have practical value for low-latency PE, or is a $\sim1^\circ$ orientation
   correction below the noise of anything downstream?
4. Is the principal-curve self-consistency result the *explanation* of the residual, or a restatement of
   it in other coordinates?

## Corrections, and a correction to the corrections

Wiring the body prose to the artifacts surfaced six apparent errors. **Three of them were not errors.**
They were artifacts of a posterior cache that drew 4000 samples per row *with replacement* — and because
the draw was capped at the available sample count, it bootstrapped even when the cap exceeded that count,
so it never used the full sample at any setting, and its noise did not fall as the cap grew. The cache now
stores every sample exactly (23.1 M samples; 972 of 972 rows in full), and the regenerated values return
to the originals:

| item | original prose | "correction" | now, exact cache | verdict |
|---|---|---|---|---|
| cross-waveform transfer | 2.08 / 2.78 vs 1.99 | 2.25 / 2.93 vs 2.03 | **2.08 / 2.78 vs 1.99** | original was right |
| round-posterior band | 14.5° | 16.3° | **14.6°** | original was right |
| paired frame p | 4e-9 | 8e-8 | **6e-9** | original was right |
| arc-length rho | +0.26, +0.02, +0.12 | −0.51, −0.61, −0.42 | **−0.51, −0.57, −0.49** | **correction stands — the sign was wrong** |
| training win fraction | 81% | 76% | **78%** | both off; no locked artifact exists, so the cell is labelled cache-derived |
| GWTC-4.0 arXiv id | 2508.18080 | 2508.18082 | **2508.18082** | correction stands (unrelated to the cache) |

**The lesson is not subtle.** A generated-numbers pipeline is only as good as the artifacts beneath it.
Ours faithfully propagated a broken cache and, in doing so, "corrected" three numbers that had been right
— while every test passed, because the tests check that the paper matches the artifacts, not that the
artifacts are correct. What caught it was auditing the cache itself, not the paper.

A seventh finding is structural and is unaffected by any of this: psi_curve is **exactly invariant to
chirp mass** (rescaling Mc is a dilation, which preserves covariance eigenvectors). The reconstruction
takes **one** input, the q marginal, not two. No number changed; the thesis sentence did.

## Provenance note

The gate measurements were first written as prose and were **not reproducible**. That was corrected by
building E92–E98 so every number regenerates from committed code, after which the gate documents were
regenerated *from* those artifacts. Figure captions are emitted from the figure sidecars so text and figure
cannot drift. Two prior results were withdrawn during this work and are disclosed in the manuscript: an
apparent $3\sigma$ GR deviation (demoted to a systematic) and a Bayesian ringdown analysis (retracted for
prior domination).
