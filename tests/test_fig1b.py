"""Figure 1b contract tests - the figure must be artifact-backed and must not drift from the
committed numbers. Seed 1 (the figure's own seed)."""
import json
import os

import numpy as np
import pytest

from src import fig1b_tangent_vs_curve_residual as F

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_missing_artifact_fails_loudly():
    """The figure must refuse to render from a missing artifact rather than silently recomputing
    or emitting an empty plot."""
    with pytest.raises(SystemExit) as e:
        F.require(os.path.join(ROOT, "results", "definitely_not_a_real_artifact.json"))
    msg = str(e.value)
    assert "FATAL" in msg and "artifact missing" in msg
    assert "e94_build_posterior_cache" in msg      # tells the reader how to regenerate


def test_figure_reads_only_committed_artifacts():
    """No HDF5, no cache, no raw PE access from the figure layer. Checked on USAGE, not on
    mentions -- the cache filename legitimately appears in the regeneration help text."""
    import ast
    path = os.path.join(ROOT, "src", "fig1b_tangent_vs_curve_residual.py")
    tree = ast.parse(open(path).read())

    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(a.name.split(".")[0] for a in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module.split(".")[0])
            if node.module.startswith("src."):
                imported.add(node.module)
    assert "h5py" not in imported, "figure layer imports h5py"
    assert not any(m.startswith("src.e94") for m in imported), "figure layer imports the cache loader"

    # the only data files it may open are the two committed artifacts
    src = open(path).read()
    assert "np.load(" not in src, "figure layer loads a binary array (the cache?)"
    assert "data/chains" not in src
    assert "e92_curve_uncertainty_results.json" in src
    assert "e95_gate_regeneration_results.json" in src


@pytest.mark.skipif(not os.path.exists(os.path.join(ROOT, "figures",
                                                    "fig1b_tangent_vs_curve_residual.json")),
                    reason="figure not built in this checkout")
def test_sidecar_medians_match_the_artifacts():
    """THE guard: every number drawn on the figure must equal the committed artifact value.
    e92 supplies the per-event errors; e95 independently recorded the same medians, so both are
    checked -- a silent change in either would otherwise reach the manuscript through the figure."""
    side = json.load(open(os.path.join(ROOT, "figures", "fig1b_tangent_vs_curve_residual.json")))
    e92 = json.load(open(os.path.join(ROOT, "results", "e92_curve_uncertainty_results.json")))
    e95 = json.load(open(os.path.join(ROOT, "results", "e95_gate_regeneration_results.json")))
    el = [r for r in e92["events"] if r["axr"] >= e92["axr_min"]]

    for cat, s in side["catalogs"].items():
        S = [r for r in el if r["catalog"] == cat]
        assert s["n_elongated"] == len(S), cat
        # recomputed straight from e92's per-event rows
        assert abs(s["curve"]["median_deg"] - float(np.median([r["abs_err"] for r in S]))) < 1e-9
        assert abs(s["tangent"]["median_deg"] - float(np.median([r["tangent_err"] for r in S]))) < 1e-9
        # and equal to what e95 wrote independently
        g = e95["gate_A"][cat]
        assert abs(s["curve"]["median_deg"] - g["own_q"]) < 1e-6, (cat, s, g)
        assert abs(s["tangent"]["median_deg"] - g["tangent"]) < 1e-6, (cat, s, g)
        assert s["n_elongated"] == g["n_elong"], cat
        # the CI must bracket the median and be a real interval
        for k in ("curve", "tangent"):
            assert s[k]["ci16_deg"] <= s[k]["median_deg"] <= s[k]["ci84_deg"], (cat, k)


@pytest.mark.skipif(not os.path.exists(os.path.join(ROOT, "figures",
                                                    "fig1b_tangent_vs_curve_residual.json")),
                    reason="figure not built in this checkout")
def test_figure_shows_the_spine_in_every_catalog():
    """The claim the figure exists to make: curve ~1 deg, tangent several deg, in all three
    disjoint catalogs. If this ever fails the figure is no longer the manuscript's spine."""
    side = json.load(open(os.path.join(ROOT, "figures", "fig1b_tangent_vs_curve_residual.json")))
    assert set(side["catalogs"]) == {"GWTC-3", "O4a", "O4b"}
    for cat, s in side["catalogs"].items():
        assert s["curve"]["median_deg"] < 2.0, (cat, s["curve"])
        assert s["tangent"]["median_deg"] > 3.0, (cat, s["tangent"])
        assert s["tangent"]["median_deg"] > 2.5 * s["curve"]["median_deg"], cat


@pytest.mark.skipif(not os.path.exists(os.path.join(ROOT, "figures",
                                                    "fig1b_tangent_vs_curve_residual.png")),
                    reason="figure not built in this checkout")
def test_outputs_declared_in_sidecar_exist():
    side = json.load(open(os.path.join(ROOT, "figures", "fig1b_tangent_vs_curve_residual.json")))
    for rel in side["outputs"]:
        assert os.path.exists(os.path.join(ROOT, rel)), rel
    assert any(o.endswith(".png") for o in side["outputs"])
    assert any(o.endswith(".pdf") for o in side["outputs"])
