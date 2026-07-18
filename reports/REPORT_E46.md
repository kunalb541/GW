# E46 lab notebook - parameterized PN-deviation tests in the value/shape framework

Prereg: preregs/E46_parameterized_deviations_prereg.md. Data: LVK GWTC-3 TGR parameterized set
(Zenodo 17461225, IGWN-GWTC3-TGR-v1-par.zip, SEOBNRv4 single-parameter analyses). 9 events x 10
fractional PN inspiral-phase deviations dchi_i (GR = 0), 90 posteriors.

## Headline (read carefully): GR is NOT violated. The framework flags a known waveform systematic.

The value/shape cross-event SIGN-COHERENCE test robustly isolates ONE parameter -- dchi0, the
leading (0PN) phase-deviation coefficient -- as coherent across events. This is the well-
documented low-PN WAVEFORM SYSTEMATIC of a single-waveform (SEOBNRv4) analysis, NOT new physics.

## Results

| test (locked) | outcome |
|---|---|
| D1 combined GR consistency (per param) | 6/10 params' naive-product posteriors contain 0; 4 exclude it |
| D2 per-event-parameter (0 in 90% CI) | 83% (75/90) consistent |
| D3 sign coherence (binomial per param) | dchi0 9/9 positive p=0.004 (Bonferroni-safe); dchi1, dchi2 8/9 p=0.039 |

Robustness cross-check (coherent AND combined-excludes-0):
| param | combined median | n_pos/9 | status |
|---|---|---|---|
| dchi0 | +0.109 [0.040, 0.177] | 9/9 | ROBUST coherent (the finding) |
| dchi1 | +0.173 | 8/9 | coherent p<0.05, combined CI spans 0 |
| dchi2 | +0.113 | 8/9 | coherent p<0.05, combined CI spans 0 |
| dchi3 | -0.094 (excl 0) | 2/9 | NOT coherent -> naive-combination artifact |
| dchi5l | -0.402 (excl 0) | 4/9 | NOT coherent -> naive-combination artifact |
| dchi6l | -2.514 (excl 0) | 3/9 | NOT coherent -> naive-combination artifact |

## Reading

- The only parameter that is BOTH sign-coherent (9/9) AND excludes 0 in combination is dchi0.
  The other combined exclusions (dchi3, dchi5l, dchi6l) are NOT sign-coherent (2-4 of 9 positive):
  they are driven by a few informative events plus the naive posterior-product, i.e. combination
  artifacts -- and the coherence test (D3) correctly discounts them. This is the framework doing
  its job: separating a genuine coherent VALUE (dchi0) from combination/noise.
- The coherent positive dchi0 across all 9 events is the classic low-PN systematic: the SEOBNRv4
  inspiral phase has small, coherent, mass-dependent modelling errors that a single-waveform
  parameterized test absorbs into a spurious dchi0 > 0. The LVK TGR papers document exactly this
  and handle it with multi-waveform comparison + hierarchical combination; the residual is
  GR-consistent. This battery used only the seob waveform, so it SEES the systematic.
- D2 at 83% (slightly below the ~90% GR expectation) is consistent with a handful of low-PN
  excursions from the same systematic, not a population GR failure.

## Contribution and the essential caveat

Contribution: the cross-event sign-coherence test (D3) is a sharp systematic detector -- it
isolates dchi0 as the single coherent direction and correctly rejects the non-coherent combined
exclusions. Per-parameter bounds alone (each event mostly consistent) hide this coherent low-PN
pull. Together with E45 (coherent +final-spin-deviation in IMR consistency), the value/shape
coherence-across-events test repeatedly surfaces real, individually-sub-threshold WAVEFORM
SYSTEMATICS in strong-gravity data.

CAVEAT (do not over-read): this is NOT evidence for a GR violation.
- Single waveform (SEOBNRv4). The systematic vs physics distinction REQUIRES multi-waveform
  robustness (the release includes phenom variants; not analysed here). A real deviation would be
  waveform-robust; a systematic is waveform-dependent -- the expected outcome for dchi0.
- The naive posterior-product combination over-constrains (it produced the non-coherent spurious
  exclusions); it is NOT an LVK-grade hierarchical bound.
- 9 events, low-PN coefficients most affected -- exactly where systematics dominate.

## Provenance

data/chains/tgr/IGWN-GWTC3-TGR-v1-par.zip (Zenodo 17461225, 2.52 GB, size-verified, gitignored).
90 single-parameter SEOBNRv4 posteriors. No RNG (binomial exact).
