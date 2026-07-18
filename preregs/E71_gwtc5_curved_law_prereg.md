# E71 preregistration — GWTC-5 (O4b) out-of-sample repeat of the curved chirp-mass law

**STATUS: DRAFT — to be LOCKED (committed + pushed) BEFORE ANY GWTC-5 FILE IS OPENED.**

This is the second, fully independent out-of-sample repeat of the E65 curved chirp-mass law. The
law was derived from GWTC-1/2.1/3 events only (E40 tangent form; E65 curved form), and was already
confirmed out-of-sample on the disjoint GWTC-4.0/O4a catalog (E67: D1 = 1.26°, prereg locked before
any O4a file was opened). E71 scores a **third, disjoint catalog** — the GWTC-5.0/O4b parameter
estimation release — with **zero tuning**: identical method, identical decision rules, identical
thresholds. The only permitted change is a purely structural file/group adapter (below), which does
not touch the law, the angle definitions, or any threshold.

## The prediction on record (locked here, before data)
Derived from GWTC-1/2.1/3 (E65) and independently reconfirmed on GWTC-4/O4a (E67):

> On elongated O4b events (axis_ratio ≥ 3): **median |ψ_curve − ψ_meas| < 2°.**
> The (m1, m2) posterior geometry is the constant-chirp-mass curve at the event's own measured
> source-frame M_c, with extent set by the event's own mass-ratio marginal. No free parameters.

## Data of record (LOCKED, disjoint from all prior batteries)
GWTC-5.0 Parameter Estimation Data Release, O4b events only, one `combined_PEDataRelease.hdf5` per
event (same file idiom as the GWTC-4.0 release used by E67):
- Part 1 of 2 — Zenodo **20276106** (≈44.2 GB).
- Part 2 of 2 — Zenodo **20348006** (≈9.0 GB).

O4b ran 2024-04-10 → 2025-01-28 (UTC). These events are disjoint from:
- the GWTC-1/2.1/3 training set of E40/E65 (through O3), and
- the GWTC-4.0/O4a events of E67 (Zenodo 16053484; O4a ended 2024-01-16).
Event names are date-coded (GWYYMMDD_HHMMSS); the O4a/O4b date ranges do not overlap, so
disjointness is checkable per event name and will be asserted in the results JSON.

## Method (locked, identical to E40/E65/E67)
Per event, from the release's headline posterior samples (LOCKED preference order: the catalog's
combined / "Mixed" samples dataset if present, else the single largest available analysis; the
dataset used is recorded per event):
- source-frame (m1, m2) samples → ψ_meas = principal-axis angle of the sample covariance,
  axis_ratio; median source-frame chirp mass M_c; mass-ratio q samples.
- ψ_tangent = constant-M_c tangent at the median (m1, m2)   [E40 law]
- ψ_total   = constant-M_tot tangent (135°)                 [E40 null]
- ψ_curve   = principal axis of the constant-M_c curve m1(q) = M_c (1+q)^(1/5) q^(-3/5), m2 = q·m1,
  evaluated at the median source M_c over the event's own q posterior   [E65 curved law]
Angles mod 180; errors are shortest-arc |dψ|. No calibration constants anywhere; nothing is fit.

## Structural adapter (declared in advance; NOT tuning)
GWTC-5.0 PE is produced by Bilby/RIFT via PESummary, so the HDF5 group naming may differ from
GWTC-4.0's `C00:...` convention, and the file names begin `IGWN-GWTC5p0-...` rather than `GW...`.
The ONLY code changes permitted relative to `src/e67_gwtc4_curved_law.py` are:
1. the data directory and file-glob (to match the GWTC-5 file naming), and event-name parsing from
   the IGWN filename;
2. the group-selection logic, IF and only if GWTC-5's combined/"Mixed" posterior group is named
   differently — adapted solely to locate (a) the combined/headline posterior group and (b) the
   four source-frame columns. The group actually selected is recorded per event in the results JSON.
The law, the angle definitions (ψ_meas, ψ_tangent, ψ_total, ψ_curve), the axis-ratio gate, and every
decision threshold are **byte-identical** to E67. If GWTC-5's combined group cannot be located by
generalizing the "Mixed"/largest-analysis rule, that is reported, not worked around by re-tuning.

## Decision rules (LOCKED — identical to E67)
- **D1 (the on-record E65/E67 prediction).** On O4b events with axis_ratio ≥ 3:
  median |ψ_curve − ψ_meas| < 2°. PASS/FAIL. This is the headline falsification test.
- **D2 (curved beats tangent).** On ALL O4b events with valid mass posteriors:
  median |ψ_curve − ψ_meas| < median |ψ_tangent − ψ_meas|. PASS/FAIL.
- **D3 (E40 tangent law replicates out-of-sample, descriptive).** Report median |ψ_tangent −
  ψ_meas|, chirp-vs-total win fraction, and Spearman(|dψ_tangent|, axis_ratio) on O4b; compare
  against BOTH prior catalogs: GWTC-3 (7.49°, 81%, −0.42) and GWTC-4/O4a (9.36°, 86%, −0.40).
  No pass/fail.

## Honesty commitments (identical to E67)
- All released O4b PE events are processed; any event dropped (missing mass columns, unreadable
  file, no combined posterior group) is listed with the reason. No SNR or mass cuts beyond the
  release's own inclusion criteria.
- Mixed/combined samples combine waveform families — that is the catalog's headline posterior and is
  used as-is; the per-event dataset name is recorded.
- Round posteriors have ill-defined orientation; that is what the pre-declared axis-ratio gate is
  for (same control logic as E40 D3 / E65 / E67).
- Transient errno-60 disk stalls handled by retry (E43/E65/E67 failure class).
- Seed 71 (no RNG expected in the main path).

## Verification plan (identical discipline to E67)
Headline numbers (D1, D2) re-derived from the results JSON through an independent aggregation path;
one elongated event recomputed end-to-end by hand from its raw HDF5 (ψ_meas, ψ_curve) as a spot
check; E65's machinery contract tests (angle conventions, kappa limits, chord-arc mechanism) rerun
green. Disjointness from O4a asserted programmatically from event dates.
