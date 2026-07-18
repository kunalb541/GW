# E59 lab notebook - ringdown mode consistency: the 220-vs-221 remnant shift is a SYSTEMATIC, not a no-hair violation

Prereg: preregs/E59_ringdown_mode_consistency_prereg.md. rin.zip Kerr_220_0M (fundamental) vs plain
Kerr_221_0M (fundamental+overtone, both Kerr), 22 events. Shift of the remnant (Mf, af) when the
overtone is added, in units of the 220-fundamental posterior width.

## Result: a naive test "fails", but the coherence diagnostic shows it is a SYSTEMATIC

- 7/22 events show a remnant shift > 2 sigma when the overtone is added (max 6.1 sigma, S191109d).
  A naive "any event > 2 sigma" reading would FALSELY flag a no-hair / mode-inconsistency violation.
- COHERENCE: the shift is in a consistent DIRECTION for essentially every event -- Mf DECREASES in
  22/22 (100%) and af DECREASES in 21/22 (95%) when the overtone is added. A stochastic no-hair
  inconsistency would scatter both ways; a uniform all-event down-shift is a SYSTEMATIC.

| decision (locked) | outcome |
|---|---|
| D1 shift is a coherent systematic (consistent direction) | YES (dMf<0 100%, daf<0 95%) -> SYSTEMATIC |
| D2 no STOCHASTIC no-hair violation | PASS (the shift is coherent, not scattered) |

## Reading

The 220-only and 221 (fundamental+overtone) analyses infer systematically different remnants: adding
the overtone at t=0M pulls Mf and af DOWN in every event. This is the well-documented ringdown-
overtone SYSTEMATIC -- overtone amplitude/phase degeneracies and start-time sensitivity bias the
remnant, and whether the GW150914 overtone is even robustly detected is an open controversy in the
literature (Isi et al. vs Cotesta et al.). The 100%/95% coherence is the definitive tell that this is
a modeling systematic, NOT evidence against the Kerr / no-hair nature of the remnants.

The value/shape coherence lens (the same tool that flagged E45's +final-spin and E46's +dchi0
systematics) once again separates a coherent systematic from a stochastic physics signal, and here it
PREVENTS a false no-hair-violation claim that a naive per-event significance test would have made.

The clean ringdown no-hair result remains E47: the 221 overtone DEVIATION parameters (domega_221,
dtau_221) are consistent with 0 and isotropic -- GR/Kerr upheld. E59 does not overturn that; it shows
that the raw 220-vs-221 remnant comparison is systematics-dominated and must not be read as a no-hair test.

## Caveats

- Shift is relative to the 220-fundamental posterior width; the 221 shares data with the 220 (not
  independent), so the >2 sigma numbers are shift-vs-fundamental-uncertainty, not clean significances.
- Both analyses start at t=0M (peak); overtone tests are notoriously start-time sensitive.

## Provenance

data/chains/tgr/IGWN-GWTC3-TGR-v2-rin.zip Kerr_220_0M + Kerr_221_0M posteriors. No RNG.
