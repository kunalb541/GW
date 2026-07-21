#!/usr/bin/env python3
"""Contract tests for the generated-numbers pipeline.

The manuscript's result numbers are emitted from committed artifacts by src/build_paper_numbers.py and
inserted as LaTeX macros. These tests defend that property, because it decays silently: the failure mode
is not a crash, it is somebody typing "1.26" into the .tex during a revision and the paper quietly
disagreeing with its own artifacts six months later. That already happened four times before the
generator existed.

Data-free: reads only committed JSON and .tex files.
"""
import json
import os
import re
import subprocess
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NUMBERS = os.path.join(ROOT, "paper/numbers.tex")
MANUSCRIPT = os.path.join(ROOT, "paper/manuscript.tex")
sys.path.insert(0, ROOT)


def read(p):
    with open(p) as fh:
        return fh.read()


def strip_comments(tex):
    return "\n".join(l for l in tex.split("\n") if not l.lstrip().startswith("%"))


def macros():
    return dict(re.findall(r"\\newcommand\{\\([A-Za-z]+)\}\{(.*?)\}\s*$", read(NUMBERS), re.M))


def test_numbers_tex_regenerates_identically():
    """The committed numbers.tex must be exactly what the artifacts produce right now."""
    before = read(NUMBERS)
    subprocess.run([sys.executable, os.path.join(ROOT, "src/build_paper_numbers.py")],
                   check=True, capture_output=True)
    assert read(NUMBERS) == before, (
        "paper/numbers.tex is stale: regenerating it from the committed artifacts changed it. "
        "Re-run src/build_paper_numbers.py and rebuild the PDF.")


def test_every_macro_traces_to_a_committed_artifact():
    """Provenance comments must name a real artifact and a path that actually resolves in it."""
    from src.build_paper_numbers import SPEC, dig, derived

    for macro, art, path, _how in SPEC:
        fp = os.path.join(ROOT, f"results/{art}_results.json")
        assert os.path.exists(fp), f"{macro}: artifact {art} missing"
        with open(fp) as fh:
            d = json.load(fh)
        v = derived(path[1:], d) if path.startswith("@") else dig(d, path)
        assert v is not None, f"{macro}: {art}::{path} resolved to None"


def test_manuscript_uses_only_defined_macros():
    """Every custom macro the manuscript references must be defined by a generator, not assumed."""
    defined = set(macros())
    defined |= set(re.findall(r"\\newcommand\{\\([A-Za-z]+)\}",
                              read(os.path.join(ROOT, "paper/fig_captions.tex"))))
    used = set(re.findall(r"\\([A-Z][A-Za-z]{4,})\b", strip_comments(read(MANUSCRIPT))))
    builtin = {"LaTeX", "Huge", "Large", "Delta", "Sigma", "Omega", "Gamma", "Lambda",
               "Theta", "Phi", "Psi", "Upsilon", "Xi", "Pi", "Rightarrow", "Leftarrow"}
    unknown = {m for m in used - defined if m not in builtin}
    assert not unknown, f"manuscript references undefined macros: {sorted(unknown)}"


def test_no_generated_value_is_also_hardcoded():
    """The regression guard.

    If a value is generated, the manuscript must not ALSO contain it as a typed literal -- that is
    exactly the drift this pipeline exists to prevent. Restricted to decimal values (>=3 chars) so
    that ordinary integers like a threshold of 3, a PN order, or a year are not flagged, and to
    values of 4+ characters so that a one-decimal value that is also a legitimate structural constant
    (the axis-ratio band edge 1.5, say) does not collide with a generated one.
    """
    body = strip_comments(read(MANUSCRIPT))
    body = body.replace("\\input{numbers}", "")
    offenders = []
    for macro, val in macros().items():
        v = val.replace("\\%", "").strip()
        if "." not in v or len(v) < 4 or v.startswith("<"):
            continue
        if re.search(r"(?<![\d.])" + re.escape(v) + r"(?![\d])", body):
            offenders.append(f"{v} (should be \\{macro})")
    assert not offenders, (
        "hardcoded copies of generated numbers found in manuscript.tex: "
        + "; ".join(sorted(offenders)))


@pytest.mark.parametrize("wrong,why", [
    ("14.5", "round-posterior band; E100 measures 16.3"),
    ("4\\times10^{-9}", "paired frame p-value; E100 measures 8e-8"),
    ("+0.26,+0.02,+0.12", "arc-length correlation; E100 measures it negative"),
    ("2.1^\\circ, against a $2.0", "stale cross-waveform transfer in the abstract"),
    ("81\\%", "training win fraction that had no artifact behind it"),
])
def test_known_wrong_numbers_do_not_return(wrong, why):
    """Each of these was in the manuscript and was wrong. Regression-lock them out."""
    assert wrong not in strip_comments(read(MANUSCRIPT)), f"reintroduced {wrong!r}: {why}"


def test_data_citation_and_acknowledgment_present():
    """LVK/GWOSC data carries attribution obligations; a missing acknowledgment is a real defect."""
    m = read(MANUSCRIPT)
    for token in ["Gravitational Wave Open Science Center (gwosc.org)", "GWOSCthree",
                  "\\citep{GWTC3}", "\\citep{GWTC21}", "Acknowledgments",
                  "GWOSCfourA", "GWOSCfourB",   # O4a/O4b data papers -- we USE O4 data
                  "not a member of the", "bears no responsibility",
                  "Creative Commons", "numpy", "scipy", "matplotlib"]:
        assert token in m, f"data-citation/acknowledgment element missing: {token}"


def test_every_bibitem_is_cited_and_every_citation_defined():
    m = read(MANUSCRIPT)
    keys = set(re.findall(r"\\bibitem\[[^\]]*\]\{([^}]+)\}", m))
    cited = set()
    for grp in re.findall(r"\\cite[tp]?\{([^}]+)\}", m):
        cited |= {k.strip() for k in grp.split(",")}
    assert not cited - keys, f"cited but no bibitem: {sorted(cited - keys)}"
    assert not keys - cited, f"bibitem never cited (ornamental): {sorted(keys - cited)}"
