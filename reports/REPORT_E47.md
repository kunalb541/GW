# E47 lab notebook - ringdown 221-overtone no-hair test in the value/shape framework

Prereg: preregs/E47_ringdown_nohair_prereg.md. Data: LVK GWTC-3 TGR ringdown set (Zenodo
17461225, IGWN-GWTC3-TGR-v2-rin.zip, pyring Kerr_221_domega_dtau), 22 events. Joint 2D deviation
(domega_221, dtau_221) of the first overtone's frequency and damping time from the Kerr
prediction; GR/no-hair predicts (0,0).

## Result: GR/Kerr UPHELD -- clean, no coherent deviation

| test (locked) | outcome |
|---|---|
| D1 population combined no-hair (Gaussian product) | CONSISTENT: combined dev (-0.011, +0.079), 0.75-sigma from GR, Q_comb = 0.246 |
| D2 per-event | 22/22 GR-consistent (Q<0.90); 0 discrepant |
| D3 directional coherence (Rayleigh) | ISOTROPIC: R=0.105, p=0.789 (no preferred deviation direction) |

The 221 overtone frequency/damping matches the Kerr value inferred from the dominant mode: no-hair
holds, individually (22/22), combined (0.75-sigma), and with isotropic scatter about GR.

## Contrast with E45/E46 (informative)

The value/shape coherence test (D3) found COHERENT sub-threshold systematics in the two
inspiral/merger-based strong-gravity tests -- E45 IMR consistency (+final-spin-deviation pull,
p=0.001) and E46 PN deviations (+dchi0, p=0.004) -- but the ringdown no-hair test is ISOTROPIC
(p=0.789). The overtone deviations are broad and symmetric about GR with no shared direction. So
the coherent systematics seen in E45/E46 are specific to the inspiral phase modelling; the
ringdown/overtone test is clean at this sensitivity.

## Methodological catch (double-check caught a spurious "violation")

The first pass combined the 22 events by MULTIPLYING their 2D histogram densities (200x200 bins).
That reported a bogus combined "TENSION" (GR excluded at 99.9%) while D2 said 22/22 individually
consistent and D3 said isotropic -- a self-contradiction. The tell: an event flagged Q=0.987 yet
sat only 0.25-sigma (Mahalanobis) from GR. Cause: fine-binned 2D histogram density is noise-
dominated at any single cell, and the density at (0,0) landed in a low-count bin; multiplying 22
such noisy grids amplified the artifact into a fake exclusion. Fix: use the robust Gaussian
product (inverse-covariance-weighted mean/cov), with GR credible level Q = 1 - exp(-d^2/2) from
the Mahalanobis distance d. The corrected combined result is 0.75-sigma (consistent). This is why
the D1/D2/D3 cross-consistency and the Q-vs-sigma check matter -- reporting the raw D1 would have
been a spurious no-hair-violation claim.

## Caveats

- Single ringdown model (pyring Kerr_221); overtone tests are sensitive to ringdown start-time
  and overtone-modelling systematics (documented). The 221 overtone is weakly constrained in most
  events -> broad posteriors -> the test's power is modest; "consistent" here is a weak-constraint
  consistency, not a stringent no-hair bound.
- Gaussian-product combination assumes each event measures the same fractional deviation
  (standard for a universal no-hair deviation) and ~Gaussian posteriors.

## Strong-gravity trilogy (E45-E47) summary

Three GWTC-3 GR tests in the value/shape framework, all GR-consistent:
- E45 IMR consistency: consistent; coherent +final-spin systematic flagged (p=0.001).
- E46 PN deviations: consistent; coherent +dchi0 waveform systematic flagged (p=0.004).
- E47 ringdown no-hair: consistent; ISOTROPIC (no coherent systematic).
The framework's contribution: a cross-event coherence probe that flags inspiral-phase waveform
systematics (E45/E46) and confirms clean isotropy where none exists (E47) -- GR upheld throughout.

## Provenance

data/chains/tgr/IGWN-GWTC3-TGR-v2-rin.zip (Zenodo 17461225, 2.21 GB, size-verified, gitignored).
22 Kerr_221_domega_dtau posteriors. No RNG.
