"""The CQG submission build is the PRD source with only the documentclass line changed.

manuscript_cqg.tex is generated from manuscript.tex by swapping the documentclass options
(twocolumn -> preprint); regenerate it with:

    sed 's/^\\documentclass\[aps,prd,twocolumn,amsmath,amssymb,nofootinbib,superscriptaddress\]{revtex4-2}/\\documentclass[aps,preprint,amsmath,amssymb,nofootinbib,superscriptaddress]{revtex4-2}/' \
        paper/manuscript.tex > paper/manuscript_cqg.tex

This test fails if the two ever drift anywhere else, so there is exactly one manuscript of record.
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _lines(name):
    with open(os.path.join(ROOT, "paper", name)) as f:
        return f.read().splitlines()


def test_cqg_tex_differs_only_in_documentclass():
    a, b = _lines("manuscript.tex"), _lines("manuscript_cqg.tex")
    assert len(a) == len(b), "manuscript_cqg.tex has drifted structurally from manuscript.tex"
    diff = [(i, x, y) for i, (x, y) in enumerate(zip(a, b), 1) if x != y]
    assert len(diff) == 1, f"unexpected divergence beyond the class line: {diff[:5]}"
    i, x, y = diff[0]
    assert x.startswith(r"\documentclass") and y.startswith(r"\documentclass")
    assert "twocolumn" in x and "preprint" in y


def test_cqg_pdf_exists():
    assert os.path.exists(os.path.join(ROOT, "paper", "manuscript_cqg.pdf"))
