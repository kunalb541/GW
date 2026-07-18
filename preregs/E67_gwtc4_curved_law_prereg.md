# E67 preregistration — GWTC-4 out-of-sample test of the curved chirp-mass law (LOCKED 2026-07-17)

**LOCKED BEFORE ANY GWTC-4 FILE IS OPENED.** The prediction under test was placed on record in
REPORT_E65 (commit 8d09cbf, 2026-07-16), derived from GWTC-1/2.1/3 events only:

> "the curved law is the natural out-of-sample prediction for GWTC-4 (O4a events, disjoint):
>  median |psi_curve − psi_meas| < 2 deg for elongated events."

E40 (tangent law) and E65 (curved law, post-hoc on the 75 old events) are both scored here on a
fully disjoint catalog: GWTC-4.0 O4a parameter estimation release (Zenodo 16053484; 86 events,
per-event combined_PEDataRelease.hdf5, 14.6 GB).

## Method (locked, identical to E40/E65)
Per event, from the release's headline posterior samples (LOCKED preference order: the catalog's
combined/mixed-samples dataset if present, else the single available analysis; the dataset used is
recorded per event):
- source-frame (m1, m2) samples -> psi_meas = principal-axis angle of the sample covariance,
  axis_ratio; median source-frame chirp mass Mc; mass-ratio q samples.
- psi_tangent = constant-Mc tangent at the median (m1, m2)   [E40 law]
- psi_total   = constant-Mtot tangent (135 deg)              [E40 null]
- psi_curve   = principal axis of the constant-Mc curve m1(q) = Mc(1+q)^(1/5) q^(-3/5), m2 = q m1,
  evaluated at the median source Mc over the event's own q posterior   [E65 curved law]
Angles mod 180; errors are shortest-arc |dpsi|. No calibration constants anywhere; nothing is fit.

## Decision rules (LOCKED)
- **D1 (the on-record E65 prediction).** On O4a events with axis_ratio >= 3:
  median |psi_curve − psi_meas| < 2 deg. PASS/FAIL. This is the headline falsification test.
- **D2 (curved beats tangent).** On ALL O4a events with valid mass posteriors:
  median |psi_curve − psi_meas| < median |psi_tangent − psi_meas|. PASS/FAIL.
- **D3 (E40 tangent law replicates out-of-sample, descriptive).** Report median |psi_tangent −
  psi_meas|, chirp-vs-total win fraction, and Spearman(|dpsi_tangent|, axis_ratio) on O4a; compare
  against the GWTC-3 values (7.49 deg, 81%, −0.42). No pass/fail.

## Honesty commitments
- All 86 released events are processed; any event dropped (missing mass columns, unreadable file)
  is listed with the reason. No SNR or mass cuts beyond the release's own inclusion criteria.
- Mixed samples combine waveform families — that is the catalog's headline posterior and is used
  as-is; the per-event dataset name is recorded.
- Round posteriors have ill-defined orientation; that is what the pre-declared axis-ratio gates
  are for (same control logic as E40 D3 / E65).
- Transient errno-60 disk stalls handled by retry (E43/E65 failure class).
- Seed 67 (no RNG expected in the main path).
