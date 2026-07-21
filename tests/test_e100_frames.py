#!/usr/bin/env python3
"""Contract tests for E100 (frames, coordinates, elongation bands).

E100 exists because these numbers previously lived only in a markdown note, which had drifted from the
artifacts by the time anyone checked. The tests below pin the geometry that makes the battery's central
claim -- that the measured angle is coordinate-DEPENDENT -- true by construction rather than by
assertion. Data-free: synthetic curves and the committed JSON only.
"""
import json
import os
import sys

import numpy as np
import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from src.e100_frames_and_bands import curve_psi_log, BANDS, MATCHED, THRESHOLDS
from src.e71_gwtc5_curved_law import curve_psi

RESULT = os.path.join(ROOT, "results/e100_frames_and_bands_results.json")


def test_log_and_linear_curve_angles_differ():
    """The whole point of the frames section: a PCA angle is not reparameterization-invariant.

    If this ever passed with the two equal, the log-coordinate row would be measuring nothing and the
    paper's coordinate-dependence claim would be vacuous.
    """
    q = np.linspace(0.2, 1.0, 500)
    lin, log = curve_psi(30.0, q), curve_psi_log(30.0, q)
    assert abs(lin - log) > 1.0, "log and linear angles agree; coordinate-dependence claim is vacuous"


def test_log_curve_angle_is_scale_free():
    """In log coordinates a change of chirp mass is a pure translation, so the angle cannot move."""
    q = np.linspace(0.2, 1.0, 500)
    a, b = curve_psi_log(10.0, q), curve_psi_log(80.0, q)
    assert abs(a - b) < 1e-6, f"log-coordinate angle moved with Mc: {a} vs {b}"


def test_curve_angle_is_exactly_independent_of_chirp_mass():
    """The reconstruction's predicted ANGLE uses only the q marginal; Mc is inert.

    m1(q) = Mc (1+q)^{1/5} q^{-3/5} and m2 = q m1, so changing Mc scales both coordinates by the same
    factor. That is a pure dilation about the origin, which leaves the sample covariance's eigenvectors
    -- and hence the principal-axis angle -- exactly unchanged. Mc still positions the curve in the
    plane, which E96/E97 and Figure 2a need, but it contributes nothing to the orientation.

    This was discovered by a test written on the WRONG assumption (that the angle moved with mass) and
    is recorded here so the paper's input count cannot silently revert.
    """
    q = np.linspace(0.2, 1.0, 500)
    ref = curve_psi(30.0, q)
    for mc in (1.0, 5.0, 80.0, 300.0):
        assert abs(curve_psi(mc, q) - ref) < 1e-9, f"angle moved with Mc={mc}"


def test_curve_angle_does_depend_on_the_q_marginal():
    """The complement: the q marginal is the ONLY input that moves the prediction."""
    q1 = np.random.default_rng(0).beta(4, 2, 4000)
    q2 = np.random.default_rng(0).beta(2, 4, 4000)
    assert abs(curve_psi(30.0, q1) - curve_psi(30.0, q2)) > 1.0


@pytest.mark.skipif(not os.path.exists(RESULT), reason="E100 not yet run")
class TestArtifact:
    @staticmethod
    def load():
        with open(RESULT) as fh:
            return json.load(fh)

    def test_source_frame_is_declared_primary(self):
        d = self.load()
        assert "LOCKED PRIMARY" in d["frames"]["source_m1_m2"]["role"]
        for k in ("detector_m1_m2", "log_source_m1_m2"):
            assert d["frames"][k]["role"] == "post-hoc", f"{k} must stay labelled post-hoc"

    def test_bands_degrade_monotonically_toward_round(self):
        """Round posteriors must score worse; that is what justifies the elongation gate."""
        d = self.load()
        keys = [f"{lo:g}-{hi:g}" if hi < 1e8 else f"{lo:g}+" for lo, hi in BANDS]
        vals = [d["axr_bands"][k]["median_err_deg"] for k in keys]
        assert vals == sorted(vals, reverse=True), f"bands not monotone: {dict(zip(keys, vals))}"
        assert vals[0] < d["random_baseline_deg"], "roundest band should not reach the random baseline"

    def test_threshold_sweep_is_smooth_and_monotone(self):
        """No special status for the locked threshold of 3."""
        d = self.load()
        assert d["threshold_monotone"] is True
        v = [d["threshold_sweep"][f"{t:g}"]["median_err_deg"] for t in THRESHOLDS]
        assert v == sorted(v, reverse=True)

    def test_matched_axis_ratio_control_is_reported_not_skipped(self):
        """The detector-frame gain must be checked against elongation, not asserted away."""
        d = self.load()
        for lo, hi in MATCHED:
            k = f"{lo:g}-{hi:g}" if hi < 1e8 else f"{lo:g}+"
            assert k in d["matched_axis_ratio"]
        low = d["matched_axis_ratio"]["3-5"]
        assert low["detector_better"] is False, (
            "the paper states the detector frame is worse in the 3-5 band; artifact disagrees")

    def test_detector_frame_is_more_elongated(self):
        """The stated mediation mechanism: removing redshift uncertainty elongates posteriors."""
        p = self.load()["frames"]["detector_vs_source_paired"]
        assert p["median_axr_detector"] > p["median_axr_source"]

    def test_arc_length_correlation_sign_is_recorded(self):
        """An earlier draft had this positive. It is negative in every catalog; lock the sign."""
        arc = self.load()["arc_length_vs_tangent_error"]
        assert set(arc) == {"GWTC-3", "O4a", "O4b"}
        for cat, v in arc.items():
            assert v["spearman_arc_vs_tangent_err"] < 0, f"{cat}: sign flipped to positive"
