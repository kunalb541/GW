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
        fp = os.path.join(ROOT, art if art.endswith(".json") else f"results/{art}_results.json")
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
    # Commands provided by LaTeX or by a loaded package are not "our" generated macros. Keep this
    # list explicit rather than pattern-matching, so a genuinely undefined macro still fails.
    builtin = {"LaTeX", "Huge", "Large", "Delta", "Sigma", "Omega", "Gamma", "Lambda",
               "Theta", "Phi", "Psi", "Upsilon", "Xi", "Pi", "Rightarrow", "Leftarrow",
               "FloatBarrier"}   # placeins
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
    # Layout lengths are not results: \includegraphics[width=0.92\textwidth] must not collide with a
    # macro that happens to equal 0.92. Strip optional-argument blocks of graphics/length commands.
    body = re.sub(r"\\includegraphics\[[^\]]*\]", "", body)
    body = re.sub(r"width\s*=\s*[\d.]+\\\w+", "", body)
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
                  "Creative Commons", "numpy", "scipy", "matplotlib",
                  # AI-use disclosure: required by most journals now, and easy to drop in a rewrite
                  "Use of AI assistants", "Opus 4.8", "OpenAI's Codex",
                  "solely responsible for the content", "not authors"]:
        assert token in m, f"data-citation/acknowledgment element missing: {token}"


def test_every_bibitem_is_cited_and_every_citation_defined():
    m = read(MANUSCRIPT)
    keys = set(re.findall(r"\\bibitem\[[^\]]*\]\{([^}]+)\}", m))
    cited = set()
    for grp in re.findall(r"\\cite[tp]?\{([^}]+)\}", m):
        cited |= {k.strip() for k in grp.split(",")}
    assert not cited - keys, f"cited but no bibitem: {sorted(cited - keys)}"
    assert not keys - cited, f"bibitem never cited (ornamental): {sorted(keys - cited)}"


def test_cache_stores_every_sample_and_never_bootstraps():
    """The cache must not resample.

    It used to draw N samples per row WITH replacement, capped at the available count -- so it
    bootstrapped even when the cap exceeded the sample count, never used the full sample at any setting,
    and its noise did not decay as the cap grew. Downstream numbers inherited that scatter, and three
    values in the paper were "corrected" to wrong ones as a result. Lock both halves of the fix.
    """
    import src.e94_build_posterior_cache as e94

    assert e94.N_SAMP is None, "cache must default to no subsampling"
    src = read(os.path.join(ROOT, "src/e94_build_posterior_cache.py"))
    assert "rng.integers(0, len(idx)" not in src, "with-replacement draw has returned"
    assert "replace=False" in src, "any optional cap must sample WITHOUT replacement"

    manifest = json.load(open(os.path.join(ROOT, "results/e94_posterior_cache_manifest.json")))
    assert manifest["n_samp"] is None
    assert manifest["rows_stored_exactly"] == manifest["n_group_rows"], (
        "every cached row must hold its full posterior")


def test_cache_reproduces_the_independent_full_sample_pass():
    """E99 read the HDF5 files directly, bypassing the cache. The rebuilt cache must agree with it."""
    e99 = json.load(open(os.path.join(ROOT, "results/e99_cache_stability_audit_results.json")))
    e95 = json.load(open(os.path.join(ROOT, "results/e95_gate_regeneration_results.json")))["gate_A"]
    for cat in ("O4a", "O4b"):
        full = e99["summary"][cat]["full_sample"]
        assert abs(e95[cat]["own_q"] - full) < 0.01, (
            f"{cat}: cache {e95[cat]['own_q']:.3f} vs independent full-sample pass {full:.3f}")


def test_generated_doc_blocks_are_current():
    """The public docs must agree with the artifacts too.

    Three review rounds each found stale numbers in REFEREE_READINESS.md and EXTERNAL_READER_PACKET.md
    (0.83/1.32/1.00 after the cache rebuild, "six times" after the resolution improved to 17x, a p=0.377
    that had become 0.110). Proofreading caught them every time, which is precisely why it is not a
    system. The headline tables now live in sentinel-delimited generated blocks.
    """
    import src.build_doc_numbers as bdn

    before = {p: read(os.path.join(ROOT, p))
              for p in ("docs/REFEREE_READINESS.md", "docs/EXTERNAL_READER_PACKET.md")}
    subprocess.run([sys.executable, os.path.join(ROOT, "src/build_doc_numbers.py")],
                   check=True, capture_output=True)
    for p, old in before.items():
        assert read(os.path.join(ROOT, p)) == old, (
            f"{p} has stale generated blocks: run src/build_doc_numbers.py")

    # every declared block must actually be anchored somewhere, or it silently stops being maintained
    joined = "".join(before.values())
    for name in bdn.blocks():
        assert f"<!-- BEGIN GENERATED: {name} -->" in joined, f"block {name!r} has no anchor in any doc"


def test_docs_do_not_contradict_the_cache_manifest():
    """A number a reader sees for the cache must match what the cache actually is."""
    m = json.load(open(os.path.join(ROOT, "results/e94_posterior_cache_manifest.json")))
    readme = read(os.path.join(ROOT, "README.md"))
    assert "~100 MB" not in readme, "README still quotes the pre-rebuild cache size"
    assert m["n_samp"] is None
    assert f"{m['rows_stored_exactly']}/{m['n_group_rows']}" in readme or "no subsampling" in readme


def _historical(line):
    """Lab notes are records: bannered lines and explicit supersession prose are exempt by design."""
    return any(k in line for k in ("BANNER", "SUPERSEDED", "superseded", "RETIRED", "retired",
                                   "previously", "earlier draft", "was right", "provisional"))


def _public_docs():
    """Every markdown file a reader can reach. Globbed, not listed.

    The previous version of this guard checked four files by name, and docs/TESTING.md ("17 tests") and
    docs/PAPER_PLAN.md ("100 MB / ~284 s") drifted straight through the gap. A hand-maintained scan list
    is the same class of bug as a hand-maintained number.
    """
    import glob
    return sorted(glob.glob(os.path.join(ROOT, "docs/*.md"))) + [os.path.join(ROOT, "README.md")]


def test_docs_state_the_real_test_and_page_counts():
    """Header metadata drifts silently and is the first thing a referee reads.

    Not generated: generating a test count from inside a test invites recursion, and the page count
    depends on a built PDF. Asserted instead -- a stale one fails the suite rather than reaching a reader.
    """
    import src.build_doc_numbers as bdn

    collected = subprocess.run([sys.executable, "-m", "pytest", os.path.join(ROOT, "tests"),
                                "--collect-only", "-q"], capture_output=True, text=True).stdout
    n_tests = int(re.search(r"(\d+) tests? collected", collected).group(1))
    pages = bdn.pdf_pages()

    for doc in _public_docs():
        rel = os.path.relpath(doc, ROOT)
        for ln, line in enumerate(read(doc).split("\n"), 1):
            if _historical(line):
                continue
            # Two orders occur in the docs and BOTH must be checked. "165 tests" was covered from the
            # start; "Tests: 164, all passing" was not, and a stale 164 sat in the adversarial-review
            # handoff through a full review round because of it -- found by reading, not by this guard.
            # The lookbehind must exclude digits as well as letters: with letters alone, "E71 tests"
            # still matches at the final "1" and reads as "1 tests".
            claims = re.findall(r"(?<![A-Za-z\d])(\d+)\s*(?:/\s*\d+\s*)?(?:contract |data-free )*tests?\b",
                                line)
            # colon is mandatory, or "locked out-of-sample test 1" reads as a claim of 1 test
            claims += re.findall(r"[Tt]ests?:\**\s*(\d+)", line)
            for claimed in claims:
                assert int(claimed) == n_tests, (
                    f"{rel}:{ln} claims {claimed} tests; {n_tests} are collected")
            # page counts only bind when the line is talking about the manuscript -- the 4 pp lab
            # notebook is a different document
            if pages and "manuscript" in line.lower():
                for claimed in re.findall(r"(?<![A-Za-z\d])(\d+)\s*pp\b", line):
                    assert int(claimed) == pages, f"{rel}:{ln} claims {claimed} pp; the PDF has {pages}"


def test_docs_describe_the_real_cache():
    """Cache size and runtime, wherever a doc mentions the cache by name.

    Scoped to lines naming e94, so the many legitimate dataset sizes in DATA_AVAILABILITY.md and
    HANDOFF.md are not swept up.
    """
    import src.build_doc_numbers as bdn

    for doc in _public_docs():
        rel = os.path.relpath(doc, ROOT)
        for ln, line in enumerate(read(doc).split("\n"), 1):
            if _historical(line) or "e94" not in line:
                continue
            for claimed in re.findall(r"(?<![\d.])(\d+)\s*MB", line):
                assert abs(int(claimed) - bdn.CACHE_MB) <= 5, (
                    f"{rel}:{ln} says the cache is {claimed} MB; it is {bdn.CACHE_MB} MB")
            for claimed in re.findall(r"~?\s*(\d+)\s*s\b", line):
                assert int(claimed) < 200, (
                    f"{rel}:{ln} quotes a {claimed} s cache build; the measured value is ~104 s")


def test_cache_size_constant_matches_reality():
    """The doc-facing cache size lives in one place and is checked against the file when present."""
    import src.build_doc_numbers as bdn

    assert bdn.cache_mb() == bdn.CACHE_MB          # asserts internally if the file disagrees
    assert "572" in read(os.path.join(ROOT, "docs/EXTERNAL_READER_PACKET.md"))
