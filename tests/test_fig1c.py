"""Figure 1c contract tests - the non-triviality panel must stay artifact-backed and must not
soften its own claim. Seed-free (the figure draws no random numbers)."""
import ast
import json
import os

import pytest

from src import fig1c_nontriviality_q_baselines as F

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SIDE = os.path.join(ROOT, "figures", "fig1c_nontriviality_q_baselines.json")
E95 = os.path.join(ROOT, "results", "e95_gate_regeneration_results.json")


def test_missing_artifact_fails_loudly():
    with pytest.raises(SystemExit) as e:
        F.require(os.path.join(ROOT, "results", "not_a_real_artifact.json"))
    msg = str(e.value)
    assert "FATAL" in msg and "artifact missing" in msg
    assert "e95_gate_regeneration" in msg          # names how to regenerate


def test_no_raw_hdf5_or_cache_read():
    """The figure layer must read the artifact and nothing else. Checked on USAGE (imports and
    calls), not on string mentions -- the cache filename appears in the regeneration help text."""
    path = os.path.join(ROOT, "src", "fig1c_nontriviality_q_baselines.py")
    tree = ast.parse(open(path).read())
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(a.name.split(".")[0] for a in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module.split(".")[0])
            if node.module.startswith("src."):
                imported.add(node.module)
    assert "h5py" not in imported
    assert not any(m.startswith("src.e94") for m in imported)
    src = open(path).read()
    assert "np.load(" not in src and "data/chains" not in src
    assert "e95_gate_regeneration_results.json" in src


@pytest.mark.skipif(not os.path.exists(SIDE), reason="figure not built in this checkout")
def test_sidecar_matches_the_artifact():
    side = json.load(open(SIDE))
    gate = json.load(open(E95))["gate_A"]
    assert set(side["catalogs"]) == {"GWTC-3", "O4a", "O4b"}
    for cat, s in side["catalogs"].items():
        g = gate[cat]
        assert s["n_elongated"] == g["n_elong"], cat
        assert abs(s["own_q_deg"] - g["own_q"]) < 1e-9, cat
        assert abs(s["tangent_deg"] - g["tangent"]) < 1e-9, cat
        assert abs(s["pooled_q_deg"] - g["pooled_q"]) < 1e-9, cat
        for k in ("n", "mean", "sd", "min", "p05", "p95", "own_percentile", "own_below_all"):
            assert s["perm_null"][k] == g["perm_null"][k], (cat, k)


@pytest.mark.skipif(not os.path.exists(SIDE), reason="figure not built in this checkout")
def test_own_q_is_below_every_stored_permutation():
    """THE claim of the figure. own-q must beat not just the null's mean but its MINIMUM -- the
    single best of 300 permutations -- in all three catalogs, giving p < 1/300 each."""
    side = json.load(open(SIDE))
    for cat, s in side["catalogs"].items():
        n = s["perm_null"]
        assert n["n"] >= 300, (cat, n["n"])
        assert n["own_below_all"] is True, cat
        assert s["own_q_deg"] < n["min"], (cat, s["own_q_deg"], n["min"])
        assert n["own_percentile"] == 0.0, (cat, n["own_percentile"])
        # and it must beat every non-permutation baseline too
        assert s["own_q_deg"] < s["tangent_deg"], cat
        assert s["own_q_deg"] < s["pooled_q_deg"], cat


@pytest.mark.skipif(not os.path.exists(SIDE), reason="figure not built in this checkout")
def test_interval_is_labelled_as_a_permutation_null():
    """It is a null distribution, not coverage or uncertainty on own-q. The sidecar must say so, so
    the distinction survives into whatever prose quotes it."""
    side = json.load(open(SIDE))
    m = side["interval_meaning"].lower()
    assert "permutation null" in m
    assert "not a confidence interval" in m and "not coverage" in m
    assert "single-shuffle" in side["note"].lower()      # records why one draw is not plotted


@pytest.mark.skipif(not os.path.exists(SIDE), reason="figure not built in this checkout")
def test_declared_outputs_exist():
    side = json.load(open(SIDE))
    for rel in side["outputs"]:
        assert os.path.exists(os.path.join(ROOT, rel)), rel
    assert any(o.endswith(".png") for o in side["outputs"])
    assert any(o.endswith(".pdf") for o in side["outputs"])
