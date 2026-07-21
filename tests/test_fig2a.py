"""Figure 2a contract tests - the explanatory geometry panel must stay cache-backed, must select its
events by a stated deterministic rule, and must not creep into being a mechanism claim."""
import ast
import json
import os

import numpy as np
import pytest

from src import fig2a_posterior_geometry_examples as F

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SIDE = os.path.join(ROOT, "figures", "fig2a_posterior_geometry_examples.json")
PNG = os.path.join(ROOT, "figures", "fig2a_posterior_geometry_examples.png")


def test_missing_cache_fails_with_build_instructions(monkeypatch):
    monkeypatch.setattr(F, "CACHE", os.path.join(ROOT, "results", "no_such_cache.npz"))
    with pytest.raises(SystemExit) as e:
        F.require_cache()
    msg = str(e.value)
    assert "FATAL" in msg and "cache missing" in msg
    assert "src/e94_build_posterior_cache.py" in msg      # tells the user exactly what to run
    assert "will not read raw HDF5" in msg


def test_no_raw_hdf5_use():
    """Samples come from the cache, never from the PE files directly."""
    path = os.path.join(ROOT, "src", "fig2a_posterior_geometry_examples.py")
    tree = ast.parse(open(path).read())
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(a.name.split(".")[0] for a in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module.split(".")[0])
    assert "h5py" not in imported
    src = open(path).read()
    assert "data/chains" not in src and "h5py.File" not in src


def test_selection_rules_are_deterministic_and_include_a_failure():
    """The three rules must be pure functions of the elongated-event table, and rule 3 must be the
    WORST case -- the figure is not allowed to become a gallery of successes."""
    rows = [dict(catalog="X", event=f"E{i}", group="g", axr=float(a), curve_err=float(c),
                 tangent_err=float(c) + 1.0, v=None)
            for i, (a, c) in enumerate([(3.5, 0.5), (9.0, 0.2), (12.0, 0.9), (4.0, 1.0), (5.0, 7.7)])]
    picks = F.select(rows)
    assert [p[0] for p in picks] == ["clean success (high elongation)", "typical", "worst case"]
    assert picks[0][2]["axr"] >= F.HIGH_AXR                       # high elongation
    assert picks[0][2]["event"] == "E1"                           # min curve err among axr>=8
    assert picks[2][2]["curve_err"] == max(r["curve_err"] for r in rows)   # the worst case
    assert F.select(rows)[1][2]["event"] == picks[1][2]["event"]  # deterministic on re-run


@pytest.mark.skipif(not os.path.exists(SIDE), reason="figure not built in this checkout")
def test_sidecar_events_satisfy_their_stated_rules():
    """Every plotted event must actually be the one its recorded rule selects."""
    side = json.load(open(SIDE))
    p = {x["panel"]: x for x in side["panels"]}
    assert set(p) == {"clean success (high elongation)", "typical", "worst case"}
    assert p["clean success (high elongation)"]["axr"] >= side["high_axr_threshold"]
    # worst case must have the largest curve error of the three, and be a genuine failure
    errs = {k: v["curve_err_deg"] for k, v in p.items()}
    assert errs["worst case"] == max(errs.values())
    assert errs["worst case"] > 5.0, "the 'worst case' panel is not showing a real failure"
    assert errs["clean success (high elongation)"] < 1.0
    for x in side["panels"]:
        assert x["selection_rule"], x["panel"]
        assert x["n_samples_plotted"] > 100
        assert x["catalog"] in ("GWTC-3", "O4a", "O4b")


@pytest.mark.skipif(not os.path.exists(SIDE), reason="figure not built in this checkout")
def test_panel_is_labelled_secondary_and_draws_no_thickness_axis():
    """E96 supports finite thickness but NOT arc variation, so no thickness-adjusted axis may be
    drawn here, and the sidecar must keep this figure marked explanatory."""
    side = json.load(open(SIDE))
    assert "secondary" in side["role"].lower() or "NOT a main-claim" in side["role"]
    assert "does not establish a mechanism" in side["caption_guidance"]
    assert "arc" in side["caption_guidance"].lower()
    for x in side["panels"]:
        assert x["thickness_adjusted_drawn"] is False


@pytest.mark.skipif(not os.path.exists(SIDE), reason="figure not built in this checkout")
def test_records_that_the_tangent_sometimes_wins():
    """Honesty guard: the figure shows three curve-favourable-to-neutral panels, so the sidecar
    must record how often the tangent actually beats the curve."""
    side = json.load(open(SIDE))
    r = side["recorded_but_not_plotted"]
    assert 0.0 < r["tangent_beats_curve_fraction_all_elongated"] < 0.5
    assert r["tangent_beats_curve_fraction_axr_ge_8"] > r["tangent_beats_curve_fraction_all_elongated"]


@pytest.mark.skipif(not os.path.exists(PNG), reason="figure not built in this checkout")
def test_rendered_image_is_non_empty_and_not_blank():
    assert os.path.getsize(PNG) > 20_000, "PNG suspiciously small"
    try:
        from PIL import Image
    except ImportError:
        return
    im = Image.open(PNG).convert("L")
    a = np.asarray(im)
    assert a.size > 0
    assert float(a.std()) > 5.0, "rendered image looks blank"
    assert float((a < 250).mean()) > 0.01, "almost no ink on the canvas"


def test_worst_case_carries_a_tail_sensitivity_check():
    """External review asked for the worst-case panel to be rescaled. Rescaling alone would have been
    cosmetic: the question it raises is whether the 16.9 deg failure is real or an outlier dragging the
    sample covariance. The figure must answer that, not just look better."""
    import json, os
    side = json.load(open(os.path.join(ROOT, "figures/fig2a_posterior_geometry_examples.json")))
    worst = next(p for p in side["panels"] if p["panel"].startswith("worst"))
    assert "inset" in worst, "worst-case panel must carry a zoom inset on the dense core"
    ts = worst["tail_sensitivity"]
    assert set(ts["percentile_trims"]) >= {"0-100", "1-99", "5-95", "10-90"}
    lo, hi = ts["curve_err_range_deg"]
    assert lo > 10.0, ("if trimming ever brings the worst case below ~10 deg it IS a tail artifact "
                       "and the caption's claim must be rewritten")
    assert "NOT a tail artifact" in ts["verdict"]
