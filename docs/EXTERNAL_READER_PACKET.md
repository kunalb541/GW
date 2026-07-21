# EXTERNAL READER PACKET

**Repo** <https://github.com/kunalb541/GW> · **state handed off at commit `73229a0`** (this packet is
committed immediately after; it changes no analysis) · **PDF** [`paper/manuscript.pdf`](../paper/manuscript.pdf),
12 pp · 157 contract tests, all passing.

Contact: Kunal Bhatia, ORCID [0009-0007-4447-6325](https://orcid.org/0009-0007-4447-6325).

---

## The thesis, in one paragraph

The orientation of a compact-binary $(m_1,m_2)$ posterior can be **reconstructed** from a single
one-dimensional marginal of that same posterior — its mass-ratio marginal —
via the shape of the constant-chirp-mass curve, with no coefficient calibrated on the validation catalogs, to a median
$1.0$–$1.3^\circ$ on elongated events (axis ratio $\ge 3$) in two later, disjoint event catalogs. The
median-point tangent approximation, which underlies rapid parameter-estimation tools, gets $3.9$–$6.6^\circ$
on the same events. This is not merely "a curve beats a line": substituting any other event's mass-ratio
marginal degrades the result $2.5$–$12\times$ and the achieved error falls below the **minimum** of 300
catalog-stratified permutations, while the reconstruction transfers between separately inferred
waveform-family posteriors of the same event. The residual $\sim1^\circ$ is a genuine systematic — about
six times the Monte Carlo resolution of the released samples — and its per-event size is predicted by the
curve's failure of Hastie–Stuetzle self-consistency ($\rho = +0.68$, $p = 5\times10^{-12}$).

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

| claim | number | why it holds up |
|---|---|---|
| out-of-sample reconstruction | $1.26^\circ$ (O4a), $1.22^\circ$ (O4b) | locked before data on O4b; two disjoint event catalogs |
| non-triviality vs permutations | below the **minimum** of 300 draws in all three catalogs | $p < 1/300$ each; not a single shuffle |
| cross-waveform transfer | $2.25^\circ$ / $2.93^\circ$ vs a $2.03^\circ$ reference scale | answers the same-posterior circularity objection |
| residual is real, not sampling noise | $1.03^\circ$ vs $0.19^\circ$ resolution ($6.3\times$) | joint bootstrap; correlated MC errors cancel |
| residual has a mechanism | $\rho = +0.68$, $p = 5\times10^{-12}$, robust across a grid sweep | a correlation between measured quantities, not a fit |

## Weakest claims (attack these first)

1. **O4a's preregistration is not publicly timestamped.** Its prereg and results entered the public repo
   in the *same commit*; only O4b's lock (17 h gap, explicit commit message) is verifiable from the public
   record. Treat the two out-of-sample scores as *unequal* evidence.
2. **The signed residual is not significant in O4b** ($p = 0.377$) — the newest and largest catalog —
   though it is in GWTC-3 ($p < 0.001$) and O4a ($p = 0.019$). The paper reports it per catalog for this
   reason. If you think the signed effect is a training-set artifact, that is a live position.
3. **Gate E (the precision law) is NOT PASSED.** The pooled fit rejects the $5/3$ mass exponent
   ($z = -3.5$); agreement appears only in a light-mass band whose edges were chosen *after* seeing that
   rejection. `src/e93_precision_law.py` hard-codes `gate_E_status = "NOT PASSED - exploratory"` and a
   test fails if that changes.
4. **O4b is the weakest panel of Figure 2**: pooled-$q$ ($3.73^\circ$) and tangent ($3.90^\circ$) are
   nearly indistinguishable there, and its null minimum ($2.30^\circ$) sits closest to own-$q$.
5. **The arc-length mechanism is weak**: $\rho = +0.26 / +0.02 / +0.12$. An earlier draft claimed the
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

```bash
# one-time cache: the ONLY HDF5 pass in the project (~5 min; GWTC-3 dominates at ~4 min)
python3 src/e94_build_posterior_cache.py          # writes results/e94_posterior_cache.npz (~96 MB, gitignored)

# analyses (seconds each, cache-backed, no HDF5)
python3 src/e95_gate_regeneration.py              # Gates A / C / D
python3 src/e92_curve_uncertainty.py              # Gate B
python3 src/e93_precision_law.py                  # Gate E -- writes NOT PASSED
python3 src/e96_curve_thickness_mechanism.py
python3 src/e97_principal_curve_selfconsistency.py
python3 src/e98_framework_audit.py
python3 src/e100_frames_and_bands.py              # frames, coordinates, elongation bands
python3 src/e99_cache_stability_audit.py          # SLOW (~45 min): the one post-E94 HDF5 pass

# figures + artifact-derived captions
python3 src/fig1b_tangent_vs_curve_residual.py
python3 src/fig1c_nontriviality_q_baselines.py
python3 src/fig2a_posterior_geometry_examples.py
python3 src/build_manuscript_figures.py
python3 src/build_paper_numbers.py                # every result number in the paper -> paper/numbers.tex

cd paper && pdflatex manuscript.tex && pdflatex manuscript.tex

python3 -m pytest tests/ -q                       # 157 tests, data-free, run anywhere
```

**Time/resource budget:** ~58 GB download (hours, network-bound); ~5 min cache build; everything
downstream is seconds. The 157 tests need no data and run in ~1 min.

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
      denial or narrowly scoped — as of `73229a0` every `coverage` and `invariant` hit is a denial, and
      the three `test of general relativity` hits are the title-free disclaimers in §1 and §7. Report any
      that are not. (Use word boundaries: a naive search for `proves` matches *improves*, which is how
      this checklist item was first written and is a false positive, not a finding.)
- [ ] **Try to break the non-triviality result.** The obvious attack is that the $q$ marginal encodes the
      answer. The cross-waveform transfer is our reply — if you can construct a case where it fails, that
      is the most valuable thing you could find.

## Open questions we would most like challenged

1. Is the cross-waveform transfer a *sufficient* answer to the circularity objection, given that the two
   waveform families analyse the same strain with shared priors and calibration?
2. Is calling $1.99^\circ$ a "reference scale" rather than an error floor the right framing — could a
   reconstruction legitimately denoise below the families' mutual disagreement?
3. Does the reconstruction have practical value for low-latency PE, or is a $\sim1^\circ$ orientation
   correction below the noise of anything downstream?
4. Is the principal-curve self-consistency result the *explanation* of the residual, or a restatement of
   it in other coordinates?

## Corrections found by generating the numbers

Wiring the body prose to the artifacts (previously only captions were generated) surfaced five errors
that had survived multiple read-throughs, four numerical and one structural:

| was | is | how it got there |
|---|---|---|
| abstract cross-waveform $2.1^\circ$ vs $2.0^\circ$ | $2.25^\circ$ / $2.93^\circ$ vs $2.03^\circ$ | body was corrected, abstract was not |
| round-posterior band $14.5^\circ$ | $16.3^\circ$ | transcribed from a markdown note that had drifted |
| paired frame $p=4\times10^{-9}$ | $8\times10^{-8}$ | same note |
| arc-length $\rho=+0.26,+0.02,+0.12$ | $-0.51,-0.61,-0.42$ | **sign was wrong**; matched no artifact |
| training win fraction $81\%$ | $76\%$, labelled cache-derived | no artifact existed; $0.81$ looks like a transcribed *degree* value |

A sixth, structural, came out of a unit test written on a wrong assumption: $\psi_{\rm curve}$ is
**exactly invariant to chirp mass** (rescaling $\mathcal{M}_c$ is a dilation, which preserves covariance
eigenvectors). The paper had described the reconstruction as taking two inputs; it takes one, the $q$
marginal. No number changed — the framing did.

## Provenance note

The gate measurements were first written as prose and were **not reproducible**. That was corrected by
building E92–E98 so every number regenerates from committed code, after which the gate documents were
regenerated *from* those artifacts. Figure captions are emitted from the figure sidecars so text and figure
cannot drift. Two prior results were withdrawn during this work and are disclosed in the manuscript: an
apparent $3\sigma$ GR deviation (demoted to a systematic) and a Bayesian ringdown analysis (retracted for
prior domination).
