# GW — The Geometry of Gravitational-Wave Inference

**Kunal Bhatia** — Independent researcher, Meerut, India ·
ORCID [0009-0007-4447-6325](https://orcid.org/0009-0007-4447-6325)

Paper project distilling the gravitational-wave program developed inside
[`cosmo2`](https://github.com/kunalb541/cosmo2) (experiments E38–E68) into a standalone
manuscript. The organizing thesis: the *uncertainty geometry* of GW measurements is lawful —
predictable from first principles, usable as a systematics detector, and transferable as a
diagnostic of cross-experiment consistency.

## What the paper now claims

**Note.** This section previously listed four results as the paper's spine. Following an internal
submission-gate audit the manuscript was narrowed to the component-mass reconstruction alone; the PTA
and spectral-siren results below remain in the repository as separate batteries but are **not** part of
the current manuscript. See [`docs/EXTERNAL_READER_PACKET.md`](docs/EXTERNAL_READER_PACKET.md).

### The paper's claim — this and nothing else

1. **The curved chirp-mass law** (E40 → E65 → E67 → E71). A **single** one-dimensional marginal of a
   compact-binary mass posterior — its mass-ratio marginal — **reconstructs** the orientation of the
   full two-dimensional posterior to ~1° on elongated events, with **zero coefficients calibrated on
   the validation catalogs**. Out-of-sample: 1.26° on O4a, 1.22° on O4b.
   *This is a posterior-compression law, not a prediction from source medians, and the residual ~1°
   is a genuine systematic — see the claim-status note below before citing it.*
   *The predicted orientation is **exactly invariant to chirp mass** (rescaling it is a dilation, which
   preserves covariance eigenvectors), so the reconstruction takes one input, not two. The chirp mass
   positions the curve in the plane but contributes nothing to its orientation.*

### In the repository, NOT in the paper

The submission-gate audit narrowed the manuscript to item 1 alone. The three results below are complete,
locked and reproducible batteries, but they are **not** claims of the paper and are not covered by its
verification. Do not cite them as such.

2. **Coherence as a systematics detector** (E45–E47, E55, E57–E60). Across the GR-test battery,
   apparent anomalies that are *coherent across events* are method artifacts, not physics —
   the lens that kept three naive-combination false alarms out of the record; GR passes every test.
3. **Cross-experiment anatomy of the PTA background** (E68). Four pulsar-timing arrays: universal
   constraint geometry, inter-PTA offsets 94.6–99.9% along the common A–γ degeneracy
   (degeneracy-sliding, not disagreement); γ = 13/3 excluded by NANOGrav alone; γ̂ strictly
   monotonic in observing span — a bending-spectrum signature, with a preregisterable successor
   prediction for IPTA DR3.
4. **What sirens can and cannot arbitrate** (E66). On the real LVK joint chains the mass-scale
   is the top systematic lever of spectral-siren H₀ but contributes ≲0.5 km/s/Mpc today;
   the lever goes live at ~1 km/s/Mpc precision (O5/XG era).

## Status

- [x] All underlying batteries locked-preregistered, run, independently re-derived (in cosmo2).
- [x] **Full port complete**: all 18 GW experiments (E38, E40–E47, E55, E57–E60, E65–E68) plus the
      GW-adjacent set (E63 NS-EOS via GW170817; E16/E52/E69 H0-anchor context; qinfo) live here
      self-contained — preregs/, src/, results/ (numbers of record), reports/, contract tests, fetch scripts.
      All files byte-identical copies; originals remain in cosmo2.
- [x] GW lab notebook: [`paper/gw_lab_notebook.pdf`](paper/gw_lab_notebook.pdf) (26 entries; new this cycle: E71, E72, E73, E74, E78, E79).
- [x] **New results (this cycle):** E71 curved law reconfirmed out-of-sample on GWTC-5/O4b (1.22°, 3rd
      catalog); E72 physics-blind null; E78/E79 geometric GR-exponent diagnostic (0.628±0.009±0.016,
      GR-consistent at 1.5σ; a naive 3σ false alarm, demoted). E92–E100: reproducible gate regeneration,
      thickness and self-consistency mechanisms, framework audit, frames/bands.
- [x] **Posterior cache rebuilt exactly (E94).** It previously drew 4000 samples per row *with
      replacement*, which never used the full sample at any cap and left up to 0.54° of scatter in every
      downstream number. It now stores all 23.1 M samples, 972/972 rows in full, and reproduces an
      independent HDF5 pass exactly for O4a and O4b.
- [x] **Adversarial-review handoff**: [`docs/HANDOFF_ADVERSARIAL_REVIEW.md`](docs/HANDOFF_ADVERSARIAL_REVIEW.md)
      — what changed, and a ranked list of where the paper is most likely to break. Start there.
- [x] **Manuscript draft**: [`paper/manuscript.pdf`](paper/manuscript.pdf) (13 pp; **every** number in the paper — abstract, text, table, captions — is a macro generated from a committed artifact by `src/build_paper_numbers.py`; none is typed by hand).
- [x] Figures: three artifact-backed panels in the manuscript, captions generated from their sidecars.
- [x] Claim-discipline pass on §6 and §8–9 (2026-07-21, prose only) — **one pass, by the author who wrote
      the prose**. §1–5 have been through six audits; these have had one. Still the least-examined sections
      and they need external review, not another self-review.
- [ ] Manuscript: journal formatting; upgrade the two GWTC catalog preprints to journal refs when published.

## Claim status (read before citing any number)

This repository contains a **submission-gate audit** of its own headline result. The gates narrowed
several claims; the current status lives in
[`docs/PAPER_PLAN.md`](docs/PAPER_PLAN.md) and the five gate notes in `docs/`:

| item | status |
|---|---|
| curved-law reconstruction (Gates A/C/D) | reproducible via `src/e94` + `src/e95` |
| uncertainty & threshold (Gate B) | reproducible via `src/e92`; the ~1° residual is a real systematic at ~17× Monte Carlo resolution, **not** sampling noise |
| precision law (Gate E) | **NOT PASSED — exploratory**; the mass-band split is post-hoc (`src/e93`) |
| thickness mechanism | finite thickness supported out-of-sample; **arc-variation NOT established** (`src/e96`) |
| E85 Bayesian ringdown | **RETRACTED** — superseded by E87; its posterior was prior-dominated |

Two provenance caveats stated plainly: E71's preregistration lock is publicly timestamped in this
repo's history (17 h before its result); **E67's is not** — its prereg and results entered in the same
port commit, so its out-of-sample status rests on a private history. And O4a/O4b are *disjoint event
catalogs*, not independent experiments.

## Data and reproducibility

**Raw parameter-estimation data are NOT included in this repository.**

- `data/` is gitignored (~68 GB of LVK PE releases). Fetch it separately — every source is pinned with
  record numbers and DOIs in [`docs/DATA_AVAILABILITY.md`](docs/DATA_AVAILABILITY.md), with helpers in
  `scripts/`.
- `results/e94_posterior_cache.npz` (**572 MB** — it stores every posterior sample, see below) is
  also **not** tracked. It is regenerable:
  ```
  python3 src/e94_build_posterior_cache.py
  ```
  This takes **~104 s** on the author's machine (one HDF5 pass, measured 2026-07-21; it was ~284 s
  before the O4a/O4b files were on local SSD, so expect this to be I/O-bound and machine-dependent) and
  **requires the downloaded
  PE files** to be present under `data/`.
- The cache is the single provenance source for the gate batteries: `src/e92`, `src/e93`, `src/e95`,
  `src/e96`, `src/e97`, `src/e98` and `src/e100` read it and perform **no HDF5 access of their own**.
  Without it they will not run. It performs **no subsampling** — every usable sample is stored (~572 MB,
  gitignored), so a cache-backed number is a full-sample number.
- Contract tests are data-free and run anywhere: `python3 -m pytest tests/ -q` (165 tests).

## Layout (cosmo2 conventions)

```
GW/
├── preregs/    locked pre-registrations for any NEW battery run for the paper
├── src/        self-contained analysis code (ported + frozen from cosmo2)
├── results/    numbers of record (JSON)
├── reports/    lab-notebook reports
├── docs/       WORKFLOW (battery discipline), TESTING, HANDOFF, SCOPE, DATA_AVAILABILITY
├── paper/      manuscript
├── scripts/    data fetchers
├── tests/      contract tests
└── data/       chains/posteriors (gitignored)
```

## Working in this repo

Start with [`docs/WORKFLOW.md`](docs/WORKFLOW.md) (the locked-prereg battery cycle + the
GW-specific rules learned the hard way), [`docs/TESTING.md`](docs/TESTING.md) (run: `python3 -m
pytest tests/ -q`; 165 data-free contract tests), [`docs/HANDOFF.md`](docs/HANDOFF.md) (current
state, data routes, next steps), and [`docs/DATA_AVAILABILITY.md`](docs/DATA_AVAILABILITY.md)
(every source pinned with record numbers). Next free experiment number: **E101**.

## License

MIT.
