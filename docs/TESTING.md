# TESTING — how to run and what a battery's tests must cover

## Run

```bash
cd ~/Desktop/Research/GW
python3 -m pytest tests/ -q          # full suite (currently 17 tests, all data-free)
python3 -m pytest tests/test_e65_fisher_rotation.py -q   # one battery
```

Requirements: python3 with numpy, scipy, h5py, pytest (getdist/anesthetic only needed to RUN
batteries, not tests). Tests are pure-function contract tests — they need **no downloaded data**
and finish in seconds; if a test wants data, it is wrong (put a validation gate inside the
battery script instead).

## Current inventory

| file | battery | guards |
|---|---|---|
| test_e63_ns_eos.py (5) | E63 | self-pair→no tension; pure value shift→value; orientation change→Δρ; C-Love sanity; ρ scale-invariance |
| test_e65_fisher_rotation.py (5) | E65/E67 | κ→0/∞ recovers chirp/total tangents; mod-180 conventions; Fisher-weight positivity + mass trend; chord-vs-tangent grows with arc |
| test_e68_pta.py (4) | E68 | self-pair null + Gaussian-faithful; degeneracy projection exact 1/0; ρ/ψ conventions; mean-shift→value-dominated |
| test_e69_dichotomy.py (3) | E69 | consensus arithmetic; precision weighting; tension symmetry/zero |

## What contract tests must cover for any NEW battery (the E64-D3 pattern)

1. **Null**: a probe/event against itself (or a synthetic twin) produces zero tension /
   zero effect — the machinery cannot manufacture a signal.
2. **Injection recovery**: a synthetic input with a KNOWN property (pure mean shift, pure
   orientation change, known slope) is classified/measured correctly.
3. **Invariance**: the claimed invariances actually hold (mod-180 angles, unit rescaling for ρ,
   inflation-immunity of fixed-metric value, limit cases of any model).
4. **Mechanism**: if the battery's story rests on a geometric mechanism (e.g. chord rotates with
   arc length), test the mechanism directly on synthetics.

Tests guard the MACHINERY, never the physics verdict — the verdict is what the locked prereg
decides on real data. Independent re-derivation of headline numbers (docs/WORKFLOW.md step 3)
is separate from and additional to these tests.

## Batteries without test files here

E38, E40–E47, E55, E57–E60 predate the contract-test convention (their guards live inline as
assertions + published-value validation gates, and their numbers were independently re-derived
in cosmo2). If any of them is RE-RUN or modified for the paper, write its test file first.
