# E73 lab notebook - the information anatomy of a detection (+ a dipole GR-sensitivity direction)

**CHARACTERIZATION, not a locked blind test.** The info-flow anatomy is a FORWARD Fisher computation from
the waveform model + PSD (measurement theory) - it is NOT extracted from each event's strain. So there is
no prereg (nothing new is blind-tested on data); the data-driven "did information arrive where GR predicts"
test needs frequency-sliced strain re-analysis and is the successor. Built on E65's analytic aLIGO PSD.

## What it computes
For each real O4a+O4b event (190 total), the frequency by which 50%/90% of the Fisher information about
each parameter is accumulated, using the leading-order TaylorF2 structure (scout-validated ordering):
chirp mass Mc at 0PN (~f^-5/3), symmetric mass ratio eta at 1PN (~f^-1), aligned spin chi at 1.5PN
(~f^-2/3). Plus a -1PN dipole term for the GR-test direction.

## Result: a clean, ordered, mass-dependent anatomy
- **Ordering Mc < eta < chi holds for ALL 190 events** - chirp mass is always learned first, spin last,
  exactly as GR's post-Newtonian structure dictates.
- **Chirp mass is always learned early**: Mc_f50 = 20-36 Hz across the catalog (mostly ~35 Hz).
- **Spin is learned later, and the separation widens for lighter binaries**: chi_f50 = 20-67 Hz; the
  anatomy "richness" (chi_f50 - Mc_f50) has **Spearman = -1.00 with total mass** - lighter / longer-inspiral
  events spread the anatomy across a wide band; heavy events (GW250114-like) compress Mc/eta/spin into a
  narrow low-frequency window because they merge almost immediately in band.

This is a genuine, per-event "measurement anatomy": when in the signal each property of the black hole was
determined - and it is a population-level structure, monotonic in mass.

## The GR-test direction (dipole)
A -1PN dipole term (dipole radiation - the classic scalar-tensor signature) injects information at even
lower frequency than the chirp mass. Which events best constrain it?
- **RANK (reliable): Spearman(sensitivity, total mass) = +1.00** - the lightest, longest-inspiral events are
  most sensitive. The best are the mass-gap / NSBH-like ones: **GW230529** (5.1 Msun, the mass-gap merger),
  **GW230518** (9.6 Msun). This matches the known result that dipole tests favour low-mass (especially NS)
  binaries.
- **MAGNITUDE (NOT reliable): the marginalized Fisher forecast sigma_beta is conditioning-limited** (the
  dipole f^-7/3 term is near-degenerate with chirp mass + timing; Fisher condition number ~1e12, and beta
  is in arbitrary units). Only the ordering is quoted; the absolute sensitivity and the comparison to the
  LVK -1PN bound need a numerically-stable, ppE-normalized forecast - the successor.

## Why this is interesting (and its honest ceiling)
- It turns "chirp mass is best-measured" into a *frequency-resolved* statement: not just what is measured,
  but WHEN in the signal - a measurement-theory anatomy of every detection.
- It is the information-geometry insight (Fisher information as the metric of distinguishability) applied to
  the internal frequency structure of GW signals.
- Ceiling: it is model-PREDICTED, not strain-MEASURED. It says what the measurement *can* do for a binary
  like this; it does not (yet) test whether information *actually* arrived where GR predicts. That data-driven
  test - re-analyse each loud event in frequency slices and compare the empirical information accumulation to
  this GR-Fisher prediction - is the real successor and needs strain + a PE pipeline (cf. E74's ringdown).

## Verification
- 5 contract tests (tests/test_e73_anatomy.py): anatomy ordering Mc<eta<chi; f ~ 1/M scaling; sigma_beta ~
  1/rho; lighter binary -> tighter dipole; sigma_beta positive-finite. Full suite 37/37.
- Conditioning explicitly checked (cond ~1e12) -> only the dipole RANK is reported, magnitude withheld.
- Independent re-derivation of the ordering (all 190) and the richness-vs-mass trend (Spearman -1.00).

## Successors (preregisterable)
1. Numerically-stable, ppE-normalized dipole Fisher -> absolute sigma_beta per event, compared to the LVK
   -1PN bound (does the geometric test have competitive teeth, or is it - like E78/E79 - an independent
   cross-check?).
2. Merger/ringdown contribution (E65's W_t weight) for the heavy events whose inspiral anatomy is compressed.
3. THE data-driven test: frequency-sliced re-analysis of the loudest events; compare empirical vs
   GR-predicted information accumulation. A coherent mismatch would be new physics (modified propagation /
   phasing); agreement is a novel consistency check.

Code: src/e73_information_anatomy.py. Numbers: results/e73_information_anatomy_results.json.
Tests: tests/test_e73_anatomy.py. PSD: E65 analytic aLIGO fit. No new data (uses E67+E71 event parameters).
