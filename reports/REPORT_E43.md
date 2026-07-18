# E43 lab notebook - does the BBH population require negative chi_eff? (NULL, per-event)

Prereg: preregs/E43_chieff_dynamical_channel_prereg.md. Reads chi_eff samples from all 76 cached
LVK posteriors (75 usable) via E38's preferred dataset (C01:Mixed, else IMRPhenomXPHM), computes
per-event P(chi_eff<0) and credible intervals.

## Result: FAILS both gates (no per-event-secure negative-chi_eff source in this sample)

| decision (locked) | threshold | outcome |
|---|---|---|
| D1: >=2 events with P(chi_eff<0) > 0.90 | | FAIL (0) |
| D2: >=1 event with 95% CI entirely < 0 | | FAIL (0) |

Most-negative events (combined-waveform posteriors):

| event | median chi_eff | P(<0) | 90% CI |
|---|---|---|---|
| GW191109_010717 | -0.293 | 0.900 | [-0.602, +0.124] |
| GW200225_060421 | -0.116 | 0.846 | [-0.395, +0.056] |
| GW200115_042309 | -0.153 | 0.818 | [-0.568, +0.084] |
| GW200209_085452 | -0.117 | 0.777 | [-0.419, +0.128] |
| GW190421_213856 | -0.095 | 0.765 | [-0.370, +0.117] |

GW191109 is right at the P=0.900 boundary and is the only strong candidate, but even its 90%
credible interval includes 0 (and its negativity is known to be waveform/glitch-subtraction
dependent in the literature). No event reaches a 95% CI below 0.

## The key correction to E42

E42 reported 34-36% of events with MEDIAN chi_eff < 0 and read it as a dynamical-formation
signature. E43 shows that at the per-event level this is NOT backed by secure negatives: the
median statistic over-counts because measurement noise scatters near-zero true spins below 0.
The ~35% (0.347) median-negative fraction here does NOT establish individually-negative sources.

## Honest scope / what this does and does not show

- It does NOT refute a dynamical channel. The real LVK evidence for a negative-chi_eff component
  is HIERARCHICAL (a population fit that lets the chi_eff distribution extend below 0), not a
  per-event significance count. This battery only did the per-event count, which is under-powered:
  individual events rarely pin chi_eff below 0.
- What it DOES show: within this 75-event sample and these combined posteriors, there is no
  single securely-negative-chi_eff event at P>0.9 / 95%-CI, so E42's median-level negativity must
  not be over-interpreted as per-event dynamical detections.
- The proper follow-up (E44, DONE) is a hierarchical mixture model of the chi_eff
  distribution -- it also finds the negative component NOT required by this sample.

## Provenance

data/chains/gw_posteriors/*.h5 (75 usable of 76; a transient read-timeout dropped one file in the original run — corrected on re-derivation, conclusion unchanged). No downloads, no RNG.
