# E46 preregistration — parameterized PN-deviation tests in the value/shape framework

Status: LOCKED. Date 2026-07-07. Second strong-gravity battery (GWTC-3 TGR parameterized set).
Data: Zenodo 17461225, IGWN-GWTC3-TGR-v1-par.zip (SEOBNRv4 single-parameter analyses).

## Setup

The parameterized test varies ONE fractional PN inspiral-phase deviation coefficient at a time,
dchi_i (i in {-2,0,1,2,3,4,5l,6,6l,7}, i.e. -1PN..3.5PN), giving a 1D posterior per (event,
parameter). GR predicts dchi_i = 0. 9 events x 10 parameters = 90 posteriors. The value/shape
reading: per parameter, VALUE = displacement of the combined posterior from 0; the framework adds
a per-parameter cross-event SIGN-COHERENCE test (a coherent same-sign pull across events is a
systematic/new-physics VALUE signature that per-event bounds miss).

## Quantities

- Per (event, parameter): posterior median, std, sign, and GR quantile Q = 2*min(P(dchi<0),
  P(dchi>0)) style two-sided consistency (Q small => far from 0).
- Per parameter: combined posterior = product of the 9 event posteriors on a common grid;
  combined median, 90% CI, and whether 0 is inside.

## Decision rules (LOCKED)

D1 (COMBINED GR CONSISTENCY, per parameter): for each of the 10 parameters, 0 lies within the 90%
   credible interval of the combined (product) posterior. Report any parameter excluding 0 at 90%.
   Expected under GR: all 10 consistent.

D2 (PER-EVENT-PARAMETER): fraction of the 90 individual posteriors with 0 inside their 90% CI.
   Expect ~90% under GR (with ~10% excursions by chance).

D3 (SIGN COHERENCE, the framework's added test): for each parameter, binomial test on the number
   of the 9 events with dchi_i > 0 (null p=0.5). Flag any parameter with two-sided binomial
   p < 0.05. With 10 parameters, expect ~0-1 flags by chance -> apply a Bonferroni note (p <
   0.005 for a multiplicity-safe flag). A multiplicity-safe coherent parameter = a shared-sign
   systematic/new-physics direction across events.

## Interpretation

Expected under GR: D1 all consistent, D2 ~90%, D3 no multiplicity-safe coherent parameter. The
novel contribution over the standard per-parameter LVK bound is D3 (cross-event sign coherence).
A coherent parameter would be flagged as a systematic candidate (waveform/PN-truncation), NOT
claimed as new physics; a GR violation would be treated with extreme skepticism. Reported as-is.

## Provenance

data/chains/tgr/IGWN-GWTC3-TGR-v1-par.zip (Zenodo 17461225, 2.52 GB, size-verified, gitignored).
90 single-parameter posteriors. No RNG.
