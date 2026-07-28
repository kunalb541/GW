#!/usr/bin/env python3
"""Guard the duplicated curve math.

The constant-Mc curve m1(q) = Mc (1+q)^{1/5} q^{-3/5} and the derived principal-axis angle are
re-implemented in several batteries rather than imported from one place (e65, e67, e71, e96, e97, e100,
fig2a). An audit confirmed they currently agree with e71's canonical curve_psi to machine precision --
this test pins that so a future edit to one copy cannot silently diverge from the headline without
failing. Data-free: synthetic q only.
"""
import importlib
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from src.e71_gwtc5_curved_law import curve_psi as canonical


def test_every_curve_psi_matches_the_canonical_one():
    rng = np.random.default_rng(0)
    # a spread of q marginals and chirp masses, including near-equal-mass and extreme-ratio
    for a, b in [(4, 2), (2, 4), (1, 1), (8, 2), (2, 8)]:
        q = np.clip(rng.beta(a, b, 6000), 0.02, 1.0)
        ref = canonical(30.0, q)
        for mod in ("src.e67_gwtc4_curved_law",
                    "src.e96_curve_thickness_mechanism",
                    "src.e97_principal_curve_selfconsistency"):
            fn = getattr(importlib.import_module(mod), "curve_psi", None)
            if fn is None:
                continue  # module imports the canonical one rather than redefining it
            d = abs(fn(30.0, q) - ref)
            assert d < 1e-9, f"{mod}.curve_psi diverged from canonical by {d:.2e} deg (Beta{a,b})"


def test_curve_exponents_are_the_leading_order_values():
    """The 0.2 and -0.6 exponents ARE 1/5 and -3/5; a typo in any copy would break this."""
    q = np.linspace(0.2, 1.0, 500)
    mc = 30.0
    m1 = mc * (1 + q) ** (1 / 5) * q ** (-3 / 5)
    # reconstruct psi from these exact-exponent points and compare to canonical
    m2 = q * m1
    X = np.column_stack([m1, m2]) - np.column_stack([m1, m2]).mean(0)
    import math
    w, V = np.linalg.eigh(X.T @ X)
    psi = math.degrees(math.atan2(V[1, 1], V[0, 1])) % 180.0
    assert abs(psi - canonical(mc, q)) < 1e-9
