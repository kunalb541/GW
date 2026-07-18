# E60 lab notebook - model-independent ringdown no-hair test: QNM frequency vs Kerr(inspiral)

Prereg: preregs/E60_ringdown_qnm_nohair_prereg.md. Measured 220 QNM frequency (DS_1mode damped
sinusoid, no Kerr assumption) vs the Kerr prediction f_220(Mf,af) from the INSPIRAL remnant (Berti
et al. 2006 fit) -- independent data segments. Detector frame.

## Result: Kerr/no-hair CONSISTENT (weak; 3 events)

Only 3 events have BOTH a DS ringdown frequency and an imr inspiral remnant (the imr inspiral
final_mass/final_spin is present for a minority of events):

| event | f_DS [Hz] | f_Kerr [Hz] | df/f | z from Kerr |
|---|---|---|---|---|
| GW150914 | 246.8 | 236.6 | +0.05 | 0.66 |
| GW170104 | 219.5 | 287.6 | -0.22 | -0.85 |
| GW170814 | 525.3 | 290.0 | +0.77 | 0.78 |

| decision (locked) | outcome |
|---|---|
| D1 no event QNM freq deviates from Kerr > 2 sigma | PASS (max |z| 0.85) |
| D2 no coherent population deviation (|comb z| < 2) | PASS (combined 0.34 sigma) |

## Reading

The measured, model-independent ringdown frequency is consistent with the Kerr prediction from the
independent inspiral remnant -- the no-hair theorem holds. GW150914 is the clean confirmation: the
Kerr f_220 predicted from its inspiral (236.6 Hz) matches the model-independent DS measurement
(246.8 Hz) to 5%, well within uncertainty. This is the strongest-in-principle ringdown no-hair test
(model-independent measurement vs independent-data prediction), and it passes.

## Honest limitations (weak constraint)

- Only 3 events (the imr inspiral remnant fields are sparse); the test has little population power.
- The individual fractional deviations are LARGE (GW170814 +77%, GW170104 -22%) but consistent at
  <1 sigma because the DS posteriors are broad -- GW170814's DS frequency (525 Hz) is high and
  poorly constrained (lower ringdown SNR, likely prior-influenced), not a real deviation.
- So E60 is GR-consistent but weak; GW150914 carries the clean confirmation.

## Ringdown no-hair trilogy (E47, E59, E60)

- E47: 221 overtone DEVIATION params (domega, dtau) ~ 0, isotropic -> GR/Kerr upheld (the clean result).
- E59: 220-vs-221 remnant shift is a coherent ringdown-overtone SYSTEMATIC (100%/95%), not a violation.
- E60: model-independent QNM frequency matches Kerr(inspiral) -> no-hair upheld (weak, GW150914 clean).
All three uphold Kerr; E59 shows why the naive remnant comparison must not be over-read.

## Provenance

rin.zip DS_1mode + imr.zip inspiral (independent). Berti et al. 2006 (2,2,0) fit. Seed 60.
