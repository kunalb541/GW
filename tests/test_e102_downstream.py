#!/usr/bin/env python3
"""Contract tests for E102 (downstream demonstration).

The honest structure of the result must be preserved: coverage of the total 90% region is
orientation-insensitive (a NULL, reported as one), while the component-mass marginal width is
orientation-sensitive (the demonstrated effect). Synthetic checks are data-free; artifact checks skip if
E102 has not been run.
"""
import json
import os
import sys

import numpy as np
import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from src.e102_downstream_demonstration import gaussian_from, coverage, m2_width_err

RESULT = os.path.join(ROOT, "results/e102_downstream_demonstration_results.json")


def test_gaussian_from_has_the_requested_axis_and_eigenvalues():
    cov = gaussian_from(0.0, 0.0, 30.0, [1.0, 9.0])
    w, V = np.linalg.eigh(cov)
    assert np.allclose(sorted(w), [1.0, 9.0])
    import math
    ang = math.degrees(math.atan2(V[1, 1], V[0, 1])) % 180.0
    assert abs(ang - 30.0) < 1e-6


def test_coverage_of_a_gaussians_own_region_is_about_ninety_percent():
    rng = np.random.default_rng(0)
    cov = gaussian_from(0.0, 0.0, 20.0, [1.0, 16.0])
    X = rng.multivariate_normal([0, 0], cov, 40000)
    c = coverage(X[:, 0], X[:, 1], np.zeros(2), cov)
    assert 0.88 < c < 0.92, f"coverage {c} not ~0.90 for a Gaussian on its own region"


def test_coverage_is_insensitive_to_orientation_but_width_is_not():
    """The mechanism behind the split verdict: rotating a fixed-area ellipse barely changes total
    coverage, but it does change the projected marginal width."""
    rng = np.random.default_rng(1)
    truth = gaussian_from(0.0, 0.0, 20.0, [1.0, 9.0])        # 3:1 ellipse
    X = rng.multivariate_normal([0, 0], truth, 40000)
    right = gaussian_from(0.0, 0.0, 20.0, [1.0, 9.0])
    wrong = gaussian_from(0.0, 0.0, 25.0, [1.0, 9.0])        # a realistic 5 deg mis-orientation
    cov_gap = abs(coverage(X[:, 0], X[:, 1], np.zeros(2), right)
                  - coverage(X[:, 0], X[:, 1], np.zeros(2), wrong))
    w_gap = abs(m2_width_err(X[:, 0], X[:, 1], np.zeros(2), right)
                - m2_width_err(X[:, 0], X[:, 1], np.zeros(2), wrong))
    # the marginal width is many times more sensitive to orientation than total coverage -- the mechanism
    # behind the paper's split verdict
    assert w_gap > 5 * cov_gap, f"width gap {w_gap:.3f} not >> coverage gap {cov_gap:.3f}"


@pytest.mark.skipif(not os.path.exists(RESULT), reason="E102 not run")
def test_artifact_reports_coverage_null_and_width_effect_honestly():
    v = json.load(open(RESULT))["verdict"]
    # primary coverage is reported as a null (curve does not beat tangent by much)
    assert "NULL" in v["primary_coverage"]["outcome"]
    assert abs(v["primary_coverage"]["oracle"] - v["primary_coverage"]["tangent"]) < 0.02
    # secondary marginal width shows the effect: tangent clearly worse, curve near oracle
    w = v["secondary_m2_width_abs_err"]
    assert w["tangent"] > 2 * w["curve"], "the demonstrated effect (tangent >> curve) must hold"
    assert w["curve"] <= w["tangent"]
