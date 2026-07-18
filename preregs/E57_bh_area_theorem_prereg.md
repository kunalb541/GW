# E57 preregistration — black-hole area theorem (Hawking's 2nd law) from GWTC-3 mergers

Status: LOCKED. Date 2026-07-07. Explores gravity via black holes: Hawking's area theorem says a
black hole's horizon area cannot decrease, so for a merger A_final >= A_initial (sum of the two
progenitor areas). This is a genuine test of classical BH gravity / the 2nd law of BH mechanics.

## Method (Isi et al. 2021 setup)

Kerr horizon area A = 8*pi*M^2*(1 + sqrt(1 - a^2)) (G=c=1), a = dimensionless spin. From the LVK
GWTC-3 IMR-consistency posteriors (imr.zip), the INSPIRAL segment measures the two progenitor
masses/spins -> A_initial = A(m1,a1) + A(m2,a2); the POSTINSPIRAL (ringdown) segment independently
measures the remnant -> A_final = A(Mf, af). The two segments are DISJOINT data, so A_initial and
A_final are independent; delta_A = A_final - A_initial by random pairing of posterior samples.
Detector-frame masses (mass_1, mass_2, final_mass) used (the directly-measured quantities; the
common (1+z)^2 scaling does not flip the inequality).

## Quantities (per event)

- P(delta_A > 0) = fraction of paired samples with A_final > A_initial (area theorem holds).
- median fractional area increase delta_A / A_initial.

## Decision rules (LOCKED)

D1 (AREA THEOREM HELD): no event has P(delta_A > 0) < 0.05 (i.e. no >2-sigma VIOLATION). Expected
   under GR: none violate; loud events give P near 1.
D2 (STRONG CONFIRMATION): at least one event has P(delta_A > 0) > 0.90 (a clean single-event
   confirmation, as GW150914 gave ~0.97 in Isi 2021).
D3 (POPULATION): the combined confidence that the area theorem holds -- events are independent, so
   combine the per-event evidence; report the joint/stacked significance. Reported.

## Interpretation

Expected under classical GR/BH thermodynamics: D1 and D2 pass -- the area theorem is confirmed and
no merger violates it. A confident P(delta_A>0) < 0.05 for any well-measured event would be an
area-theorem violation (treated with extreme skepticism -- systematics/measurement first). Reported
as-is. This is a black-hole-gravity test distinct from the E45-E47 GR tests: it probes the horizon
area / 2nd law, not the waveform deviation parameters.

## Provenance

data/chains/tgr/IGWN-GWTC3-TGR-v1-imr.zip inspiral + postinspiral posteriors. Random pairing seed 57.
