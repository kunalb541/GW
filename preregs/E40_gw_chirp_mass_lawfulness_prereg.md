# E40 preregistration — GW mass-plane geometry is the chirp-mass degeneracy

Status: LOCKED. Date 2026-07-07. GW-domain analog of the cosmo psi(alpha) question.
Method was hand-validated on 3 events (GW190814/GW190425/GW190519) during design; the full
14-event scoring and the thresholds below are fixed before the automated run.

## Hypothesis

The (m1_source, m2_source) posterior degeneracy orientation of a compact-binary event is set,
from first principles, by the CONSTANT-CHIRP-MASS curve at the event's median masses -- because
chirp mass M_c = (m1 m2)^{3/5}/(m1+m2)^{1/5} is the best-measured mass combination. Predicted
orientation is the tangent to the constant-M_c curve; the physical NULL comparator is the
constant-TOTAL-mass curve (M=m1+m2, tangent fixed at psi=135 deg).

## Prediction (parameter-free)

For each event at median (m1,m2):
  g = ( (3/5)/m1 - (1/5)/(m1+m2), (3/5)/m2 - (1/5)/(m1+m2) )   [grad ln M_c]
  psi_chirp = atan2(g_x, -g_y) mapped to [0,180)                [tangent perp to g]
  psi_total = 135 deg (constant-total-mass tangent, direction (1,-1))
Delta = circular distance to measured psi on [0,180).

## Decision rules (LOCKED)

D1 (PRIMARY): median |Delta psi_chirp| over all 14 events < median |Delta psi_total|, AND the
   chirp model wins on >= 11/14 events. -> mass geometry follows chirp mass, not total mass.
D2 (STRENGTH, well-defined-orientation subset): on events with axis_ratio >= 3 (posterior
   genuinely elongated, so orientation is meaningful), median |Delta psi_chirp| < 12 deg.
D3 (round-posterior control, pre-declared): on axis_ratio < 1.5 events, |Delta psi| is expected
   to be LARGE for both models (orientation ill-defined); reported, not gated. If chirp still
   holds there it is a bonus.

## Reported diagnostics

Per-event table (psi_meas, psi_chirp, psi_total, both deltas, axis_ratio, rho); correlation of
|Delta psi_chirp| with axis_ratio (predict: smaller error for more elongated events).

## Interpretation contract

- Pass = a rare POSITIVE geometric-lawfulness result, contrasting the cosmo nulls (E34/E35):
  GW mass geometry is lawfully predictable because a genuine dominant physical combination
  (chirp mass) exists. Fail or chirp~total = degeneracy not specifically chirp-mass.

## Provenance

Measured psi + median masses from results/e38_gw_black_hole_geometry_results.json (14 events,
GWOSC *_PE.h5). No new downloads. No RNG.
