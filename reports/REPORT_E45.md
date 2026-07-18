# E45 lab notebook - strong-gravity IMR-consistency test in the value/shape framework

Prereg: preregs/E45_imr_consistency_gr_prereg.md. Data: LVK GWTC-3 Tests-of-GR release (Zenodo
17461225, IMR-consistency imrct posteriors), 18 events. Each event provides a 2D posterior of the
fractional deviations (dMf/Mf-bar, daf/af-bar) between inspiral- and post-inspiral-inferred final
mass/spin; GR predicts (0,0).

## Result: GR upheld, but a coherent sub-threshold deviation direction surfaced

| test (locked) | outcome |
|---|---|
| D1 population combined GR consistency | CONSISTENT: combined mean dev (-0.035, +0.002), GR credible level Q_comb = 0.671 (<0.90) |
| D2 per-event | 17/18 GR-consistent (Q<0.90); 1 discrepant: S190814bv (=GW190814) Q=0.992 |
| D3 directional coherence (Rayleigh on mean-dev directions) | COHERENT: R=0.59, mean dir 122 deg, p=0.001 (NOT isotropic) |

## Reading

- D1: the population is fully consistent with GR -- the combined deviation posterior sits on
  (0,0) (combined mean within 0.035 of zero, GR at the 67th percentile). No GR violation.
- D2: the lone individual outlier is GW190814 (S190814bv), whose extreme mass asymmetry (q~0.11)
  leaves an almost-absent post-inspiral signal, so its IMR-consistency test is known to be
  systematics-dominated and unreliable -- not new physics. 1/18 above Q>0.95 is also ~chance.
- D3 (the framework's added test): the per-event mean deviations are NOT isotropic about (0,0)
  (Rayleigh p=0.001). The coherence is driven by a mild preference for POSITIVE final-spin
  deviation: 13/18 events have daf/af-bar > 0 (vs 6/18 for dMf/Mf-bar). A binomial 13/18 is
  p~0.05 on sign alone; with magnitudes the Rayleigh p is 0.001.

## Value vs shape: is the coherence real or a shared degeneracy?

The value/shape distinction is the point here. The coherent direction COULD be (a) a genuine
shared VALUE pull (systematic or new physics), or (b) a SHAPE artifact -- means scattering along a
common measurement degeneracy (all events have rho ~ +0.2..+0.6, similar deviation-ellipse
orientation). Checking each event's mean-deviation direction phi against its own ellipse axis psi:
only 10/18 lie within 30 deg of their degeneracy axis -- so the coherence is PARTIALLY shape
(means do slide along the shared degeneracy) but not fully: a residual coherent pull toward
+daf/af remains beyond the degeneracy.

Most plausible cause: a shared WAVEFORM/analysis systematic in the inspiral-vs-post-inspiral final
-spin estimate (a known, small, waveform-model-dependent effect), NOT new physics -- D1 upholds GR.

## Contribution

The standard LVK per-event IMR test asks only "is each event GR-consistent?" (here: yes, 17/18).
The value/shape framework ADDS a population-directional test that surfaces a coherent, individually
sub-threshold deviation (a mild +final-spin-deviation pull across events, Rayleigh p=0.001) that
no single-event test sees. This is a systematics-flagging tool: GR is not in question, but the
framework localizes a shared residual direction worth attributing (waveform systematic being the
leading candidate).

## Caveats

- 18 events (the GWTC-3 IMR set with usable inspiral+post-inspiral); combined posterior assumes a
  shared grid (verified: all on [-2,2]^2, 401x401) and independence across events (standard).
- The Rayleigh coherence is partly the shared measurement degeneracy (10/18 along-axis); the
  residual +daf/af pull is mild and attributed to systematics, not claimed as physics.
- GW190814 excluded from any physics reading (post-inspiral absent).
- No waveform-systematics marginalization; establishing the systematic origin definitively would
  need multiple waveform models (available in the par/rin releases, not analysed here).

## Provenance

data/chains/tgr/IGWN-GWTC3-TGR-v1-imr.zip (Zenodo 17461225, 4.12 GB, size-verified, gitignored).
No RNG.
