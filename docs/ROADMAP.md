# ROADMAP — proposed next batteries (backlog)

Captured 2026-07-18. These are candidate experiments beyond the ported record (E38–E69).
Discipline: **one battery at a time**, full WORKFLOW.md cycle each, lean orchestration.
Numbering continues cosmo2's sequence; next free number was E71.

**Done this session: E71 (PASS 1.22°) + E72 (physical null).** E73–E77 below are proposed, not started.

| # | deliverable slug | one-line | reuses | new build | data | gate/dep | status |
|---|---|---|---|---|---|---|---|
| **E71** | `gwtc5_chirp_curve_stress_test` | Score GWTC-5/O4b with the locked zero-parameter chirp-curve law (D1<2°, D2 curve>tangent, D3 E40 replication) | E67/E65 scorer verbatim | data path + O4b disjointness assert only | GWTC-5 PE Zenodo 20276106 + 20348006 (~53 GB) | prereg locked (d19a7a8); layout validated | **in progress** |
| E72 | `gw_geometry_outlier_atlas` | Rank O4b events by chirp-curve residual; inspect the top outliers, not the median | E71 per-event residuals | correlation engine | E71 output + per-event precession/χ_eff/q/higher-mode/waveform-disagreement proxies | needs E71 done | **DONE `a35069e`: physical null — no physical axis (precession/spin/q/z/mass/NSBH) drives the residual; only waveform-disagreement (systematic) survives FDR; one weak marginal flag GW240507** |
| E73 | `frequency_resolved_information_geometry` | Go to strain for a few loud events: time-frequency tracks, inspiral-only vs merger-only geometry, where in frequency the chirp-curve law emerges; test the E65 rotation hypothesis on high-freq merger data | E65 geometry | strain/TF pipeline (GWOSC strain, not just posteriors) | loud-event strain (GWOSC) | new modality | proposed |
| E74 | `o4_ringdown_kerr_stress_test` | Loudest O4/O4b ringdowns → rerun no-hair/area (Kerr freq + damping consistency, overtone systematics) | E47/E59/E60 | loud-event selection | GWTC-5 (rides E71 download) + LVK TGR rin products | ringdown SNR still binding; manage expectations | proposed |
| E75 | `cross_band_gw_fundamental_physics` | PTA (nHz) + LVK (stellar-mass) in ONE framework: do both prefer GR tensor correlations/propagation? one modified-gravity parameter across bands? PTA curvature vs SMBHB/strings/phase-transition as a cross-band falsifier | E58 (propagation) + E68 (PTA) | cross-band linkage | LVK propagation posteriors + PTA chains | genuinely fundamental; medium-high build | proposed |
| E76 | `mass_peak_evolution_spectral_siren` | Model redshift drift of the BH mass peak: how much fake H0 shift; does O4/O4b help; can the data internally separate cosmology from mass evolution | E66 | z-dependent mass-function model | GWTC-5 population + E66 icarogw chains | deepest future-siren failure mode; attack early | proposed |
| E77 | `population_anomaly_geometry` | Geometry-based anomaly score for PBH/eccentric/dynamical-channel candidates (low spin, mass-gap occupancy, high z, unusual q, eccentricity-assumption breakdown) — NOT a PBH claim, a clean anomaly map | E38 atlas + E71/E72 | anomaly scorer | full PE atlas (GWTC-1→5) | after E71/E72 | proposed |

## Also captured — distinct threads from the earlier E71–E76 menu (folded into the above, kept explicit so none is lost)
- **Propagation battery** (attach to E75): extend E58 beyond massive-graviton / LIV to (a) **parity birefringence** — needs public parity-violation/birefringence posteriors or a strain-level method; (b) **amplitude damping / modified luminosity distance** (d_L^GW vs d_L^EM). Unifies the propagation tests into one comparison.
- **Non-tensor polarization geometry** (E73/E75): compare the *correlation-function geometry* of tensor-transverse vs **scalar-transverse vs vector** modes — a generalization of PTA Hellings–Downs; anchor on NANOGrav 15yr's GR-like quadrupolar evidence.
- **PTA spectral curvature** (E75 / PTA successor to E68): **broken vs single power law**; **SMBHB-only vs cosmic-strings / phase-transition** templates; test whether E68's γ-vs-span ordering **survives subset resampling**. Preregister now, run on IPTA DR3 / NANOGrav 20yr when public.

## Standing on-record predictions (from WORKFLOW.md — preregister when data lands)
- **Curved law**: elongated events in ANY future catalog follow the constant-M_c curve to <2° (E71 tests this on O4b).
- **PTA span-ordering**: longer-span subsets of the same array fit steeper γ (prereg the day IPTA DR3 / NANOGrav 20yr chains are public → the E76-adjacent PTA successor).
- **GWTC-4 TGR products**: re-run E45–E60 unchanged when the O4a/O4b TGR release lands (feeds E74).

## User's framing (this session)
"do E71 + E72 together" was the strongest recommendation, but the standing instruction is **do only one** —
so E71 runs now; E72 (turn E71's residuals into an outlier atlas) is the designated immediate successor.
E71's report will include a descriptive largest-residual ranking as the E72 seed (labelled post-hoc).
