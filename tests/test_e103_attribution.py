#!/usr/bin/env python3
"""Contract tests for E103 (exponent attribution: 1PN vs finite-width).

The manuscript now makes a two-mechanism claim: 1PN sets the population-level exponent offset; a distinct
elongation-dependent effect produces the variation across events. These tests pin the artifact structure
that claim quotes. Skip if E103 has not been run.
"""
import json
import os

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULT = os.path.join(ROOT, "results/e103_exponent_attribution_results.json")


@pytest.mark.skipif(not os.path.exists(RESULT), reason="E103 not run")
class TestArtifact:
    @staticmethod
    def load():
        return json.load(open(RESULT))

    def test_population_medians_match(self):
        d = self.load()["D1_median_match"]
        assert d["medians_consistent"] is True
        assert abs(d["median_p_star"] - d["median_p_pred_1PN"]) < 0.02

    def test_prediction_is_flat_in_elongation(self):
        """If this fails, the 1PN prediction DOES carry elongation dependence and the manuscript's
        two-mechanism sentence is wrong."""
        d = self.load()["D3_prediction_flat_in_axr"]
        assert d["flat"] is True and abs(d["rho"]) < 0.3

    def test_elongation_trend_survives_partialling(self):
        d = self.load()["D2_correlations"]["pstar_vs_axr_partial_ppred"]
        assert d["rho"] < 0 and d["p"] < 0.05, "the finite-width mechanism claim rests on this"

    def test_verdict_is_two_mechanisms(self):
        assert self.load()["verdict"]["two_mechanisms"] is True
