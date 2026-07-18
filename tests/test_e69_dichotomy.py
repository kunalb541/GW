"""Contract tests for E69 (ruler-dichotomy arithmetic)."""
import math
from src.e69_ruler_dichotomy import consensus, tens


def test_consensus_equal_weights():
    mu, sig, chi2, dof = consensus({"a": (70.0, 2.0), "b": (72.0, 2.0)})
    assert abs(mu - 71.0) < 1e-12
    assert abs(sig - 2.0 / math.sqrt(2)) < 1e-12
    assert dof == 1


def test_consensus_weighting():
    # precise member dominates
    mu, _, _, _ = consensus({"tight": (70.0, 0.1), "loose": (80.0, 10.0)})
    assert abs(mu - 70.0) < 0.01


def test_tension_symmetric_and_zero():
    assert tens((70, 1), (70, 2)) == 0.0
    assert abs(tens((70, 1), (73, 1)) - 3 / math.sqrt(2)) < 1e-12
