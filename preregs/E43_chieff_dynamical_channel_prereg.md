# E43 preregistration — does the BBH population require negative chi_eff (dynamical channel)?

Status: LOCKED before computing per-event P(chi_eff<0). Date 2026-07-07. Follows E42 (36% of
events have median chi_eff<0; but medians scatter negative under measurement noise even for a
truly chi_eff>=0 population -- this battery uses the FULL posteriors).

## Hypothesis

The BBH population contains systems with genuinely negative effective spin chi_eff < 0. Isolated
field-binary formation predicts chi_eff >= 0 (spins preferentially aligned with orbital angular
momentum); a secure negative-chi_eff event requires misaligned/anti-aligned spins, the signature
of DYNAMICAL assembly. Null: all sources have chi_eff >= 0 and any apparent negativity is
measurement scatter / prior.

## Method

For each of the 76 cached LVK posteriors, read the chi_eff samples from the SAME preferred
waveform dataset E38 uses (find_posterior_dataset: C01:Mixed, else C01:IMRPhenomXPHM, else any).
Compute per event: median chi_eff, P(chi_eff<0) = fraction of samples below 0, and the 90% / 95%
credible intervals (q5/q95, q2.5/q97.5) from the samples.

Prior note: the chi_eff prior (induced from isotropic spin priors) is peaked and ~symmetric at 0,
so a zero-spin event has P(chi_eff<0) ~ 0.5. Under a strictly chi_eff>=0 population, essentially
NO event should reach P(chi_eff<0) >> 0.5. Events with high P(chi_eff<0) therefore have data
pulling them negative.

## Decision rules (LOCKED)

D1 (PRIMARY): at least 2 events have P(chi_eff<0) > 0.90.  -> population inconsistent with
   strictly chi_eff>=0; a negative/dynamical component is present.
D2 (STRONG, secure single event): at least 1 event has its 95% credible interval entirely below
   0 (equivalently P(chi_eff<0) > 0.975).  -> a securely negative-chi_eff source.
D3 (DISTRIBUTION, reported not gated): the count of events with P(chi_eff<0) > 0.9 vs the ~0
   expected under the strictly-positive null; and the most-negative ranked list (expect to
   recover known negative-chi_eff events, e.g. GW191109).

## Interpretation

D1 pass = the data require a negative-chi_eff (dynamical-formation) component -- a real
astrophysical population result, distinct from E42's median-level 36% (which over-counts due to
noise). Honest scope: this is a per-event significance count, NOT a full hierarchical population
inference with selection effects; it establishes existence of a negative component, not its rate.

## Provenance

data/chains/gw_posteriors/*.h5 (76 events, gitignored). No downloads, no RNG.
