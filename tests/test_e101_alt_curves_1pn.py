#!/usr/bin/env python3
"""Contract tests for E101 (alternative-curve null + 1PN Fisher residual).

The load-bearing check is the 1PN derivation: at 0PN the effective exponent MUST be exactly GR's 3/5,
and the 0PN Fisher long axis MUST equal the constant-Mc tangent. If either drifts, the "1PN explains the
offset" result is an artifact. The synthetic checks are data-free; the artifact checks skip if E101 has
not been run.
"""
import json
import os
import sys

import numpy as np
import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from src.e101_alternative_curves_and_1pn import (fisher_long_axis, p_eff_of_angle, curve_angle_p)
from src.e71_gwtc5_curved_law import tangent_angles
from src.e65_pn_fisher_rotation import adiff

RESULT = os.path.join(ROOT, "results/e101_alternative_curves_and_1pn_results.json")


@pytest.mark.parametrize("m1,m2", [(35.0, 30.0), (60.0, 12.0), (20.0, 18.0), (90.0, 25.0)])
def test_0PN_effective_exponent_is_exactly_three_fifths(m1, m2):
    """The whole 1PN result rests on this: with no 1PN term, the exponent is GR's 3/5."""
    a0 = fisher_long_axis(m1, m2, "0PN")
    assert abs(p_eff_of_angle(m1, m2, a0) - 0.6) < 1e-3, "0PN exponent drifted from 3/5"


@pytest.mark.parametrize("m1,m2", [(35.0, 30.0), (60.0, 12.0), (90.0, 25.0)])
def test_0PN_fisher_axis_equals_constant_mc_tangent(m1, m2):
    """The 0PN Fisher degenerate direction is, by construction, the constant-Mc contour tangent."""
    assert abs(adiff(fisher_long_axis(m1, m2, "0PN"), tangent_angles(m1, m2)[0])) < 0.05


@pytest.mark.parametrize("m1,m2", [(35.0, 30.0), (60.0, 12.0), (90.0, 25.0)])
def test_1PN_shifts_the_exponent_above_GR(m1, m2):
    """The 1PN eta-dependent term shifts the effective exponent above 3/5 -- the direction of the offset."""
    a1 = fisher_long_axis(m1, m2, "1PN")
    assert p_eff_of_angle(m1, m2, a1) > 0.6, "1PN did not raise the effective exponent above GR"


def test_curve_angle_p_reduces_to_canonical_at_three_fifths():
    from src.e71_gwtc5_curved_law import curve_psi
    q = np.random.default_rng(0).beta(3, 2, 5000)
    assert abs(curve_angle_p(q, 0.6) - curve_psi(30.0, q)) < 1e-9


@pytest.mark.skipif(not os.path.exists(RESULT), reason="E101 not run")
def test_artifact_D3_predicts_the_empirical_optimum():
    d = json.load(open(RESULT))["D3_1PN_fisher"]
    assert d["D3a_1PN_rotates_toward_measured"] is True
    assert d["D3b_p_eff_above_GR"] is True
    # the blind 1PN exponent must land near the empirical optimum p* (D1), ~0.62-0.63
    assert 0.615 < d["median_p_eff"] < 0.645, f"1PN p_eff {d['median_p_eff']} off the empirical optimum"


@pytest.mark.skipif(not os.path.exists(RESULT), reason="E101 not run")
def test_artifact_D1_exponents_carry_content_and_D2_ordering():
    d = json.load(open(RESULT))
    for c in ("GWTC-3", "O4a", "O4b"):
        assert d["D1_exponent_null"]["verdict"][c].startswith("PASS")
        assert d["D2_chord_baseline"][c]["ordering_holds"] is True  # tangent > chord > curve
