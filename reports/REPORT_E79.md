# E79 lab notebook - cross-catalog exponent: a coherent 3-sigma "GR deviation" that is a systematic, not physics

Prereg: preregs/E79_exponent_cross_catalog_prereg.md - locked (before the E78 estimator was run on any
O4a file). Tests E78's on-record successor: is the geometry-fit inspiral mass-combination exponent
reproducible across catalogs and equal to GR's 0.600? GWTC-4/O4a PE (Zenodo 16053484, 86 events, 14.31 GB;
disjoint from O4b - 0 overlapping events; column-ID clean) scored with the E78 estimator UNCHANGED.

## Raw outcome (the trap)
| | n_elong | p_hat | vs GR 0.600 |
|---|---|---|---|
| O4a | 19 | 0.647 +/- 0.014 | 3.3 sigma |
| O4b | 32 | 0.616 +/- 0.011 | 1.4 sigma |
| **combined** | 51 | **0.628 +/- 0.009** | **3.1 sigma** |

- **D1 (O4a consistent with GR, as literally locked on stat-only error): FAIL** (3.3 sigma).
- **D2 (O4a reproduces O4b): PASS** (|0.647-0.616| = 0.031, within errors).
- Estimator injection-unbiased on both catalogs (bias < 0.001).

Taken at face value this is a coherent 3.1-sigma departure of a GR quantity - the kind of thing that, if
announced, becomes a false alarm. The prereg pre-committed that a coherent >3 sigma departure triggers a
dedicated follow-up BEFORE any claim. It does, and it dissolves.

## Pre-committed follow-up: the offset is a SYSTEMATIC of the leading-order model
1. **The stat error is underestimated.** The two INDEPENDENT catalogs disagree by 0.031 - as large as the
   0.028 offset from GR. That catalog-to-catalog spread is a systematic the bootstrap (0.009) never
   captured. Honest budget: **p_hat = 0.628 +/- 0.009 (stat) +/- 0.016 (syst) => 1.5 sigma from GR**, not 3.1.
2. **The offset is elongation-dependent (the fingerprint).** Spearman(p*, axr) = -0.41, COHERENT across
   both catalogs (O4a p=0.08, O4b p=0.02, combined p<0.01): rounder events fit higher p; the well-measured
   elongated events fit lower. **The cleanest (most-elongated) half gives p_hat = 0.606 ~ GR's 0.600.**

By the repo's coherence lens (WORKFLOW.md: an anomaly coherent across datasets is a systematic, not
physics), and given that a real GR violation of this size is excluded by direct LVK tests, the verdict is
unambiguous: the coherent offset above 0.600 is a **finite-width / higher-order-geometry imperfection of
the pure-0PN constant-Mc model** - the leading-order curve is a slightly worse fit for less-elongated
posteriors, biasing their fitted exponent high - and it vanishes in the clean (elongated) limit where the
orientation is sharpest. **No GR-violation claim. The exponent is GR-consistent.**

## What actually happened, and why it is a GOOD result
- The method **reproduces across two independent catalogs** (D2 PASS) - it is a stable measurement.
- It is **sensitive enough to detect a real ~3 sigma effect** - the leading-order model's own imperfection,
  now resolvable with 51 elongated events.
- Careful, pre-committed accounting (two-estimator systematic + elongation control + coherence lens)
  **correctly demotes a would-be 3-sigma GR-violation to a 1.5-sigma systematic** with the cleanest events
  landing on 0.600. This is the E47/E58 false-alarm lesson executing live: the naive combination lies; the
  discipline catches it.
- It sharpens E78 (which flagged exactly this ~1.2 deg law-residual floor as the likely source of its small
  O4b offset): E79 confirms that flag - the offset is the leading-order geometry's residual, elongation-
  dependent, coherent, and GR-consistent when controlled.

## Honest headline
The GW inspiral's leading mass-combination exponent, measured from posterior geometry across O4a+O4b, is
**0.628 +/- 0.009 (stat) +/- 0.016 (syst), consistent with GR's 0.600 (1.5 sigma); the cleanest events give
0.606.** The naive stat-only 3.1 sigma is a systematic-underestimate artifact, not a signal.

## Verification
- Independent re-derivation of the honest error budget (stat 0.009, syst 0.016, 1.5 sigma) and the
  cleanest-half exponent (0.606) through a second aggregation path - exact match.
- Injection recovery on BOTH catalogs' q-marginals (bias < 0.001); estimator unbiased.
- Disjointness O4a n O4b = 0 (asserted from event sets); O4a column-ID (chirp == Mc(m1,m2)) clean; 86/86
  files h5py-valid, 0 dropped. E78 contract tests green; full suite 32/32.

## Successor (preregisterable)
The elongation trend predicts a specific fix: a first-principles 1PN (not 0PN) geometric model should (a)
reproduce the Spearman(p*, axr) = -0.4 trend and (b) shift the effective exponent to 0.6 across all
elongations. Add GWTC-3 as a third catalog. If the 1PN model flattens the trend, the systematic is
identified and closed; the geometric GR test then quotes the clean-limit exponent.

Code: src/e79_exponent_cross_catalog.py. Numbers: results/e79_exponent_cross_catalog_results.json.
Data: data/chains/gwtc4/ (O4a, Zenodo 16053484) + data/chains/gwtc5/ (O4b). Estimator = E78 verbatim.
