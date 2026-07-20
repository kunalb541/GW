#!/usr/bin/env python3
"""Figure 1c - the reconstruction needs the EVENT'S OWN mass-ratio marginal, not just a curve.

Figure 1b shows the curve beats the median-point tangent. That alone is compatible with a dull
explanation: "a curve is simply a better model of a banana-shaped posterior." Figure 1c closes that
door. Substituting any other q marginal -- pooled across the catalog, or another event's, drawn 300
times -- destroys the reconstruction. Own-q lies below EVERY one of 300 catalog-stratified
permutations in all three catalogs.

ARTIFACT-BACKED. Reads only results/e95_gate_regeneration_results.json. No HDF5, no e94 cache, no raw
PE. Fails loudly with regeneration instructions if the artifact is absent.

WHAT THE INTERVAL IS. The grey band is a PERMUTATION NULL -- the spread of the catalog-median error
when each event is handed a different event's q marginal. It is NOT a confidence interval, NOT
coverage, and NOT measurement uncertainty on own-q. E95 stores the null's summary (n, mean, sd, min,
5th/95th percentile), not the 300 raw draws, so the band is drawn as p05-p95 with the MINIMUM marked
explicitly -- the minimum is the load-bearing mark, because own-q sits below even the single best
permutation of 300.

The old single-shuffle number is deliberately NOT plotted: one permutation is not a null, and
re-drawing it moved the O4a value from 3.04 to 8.62 deg. Only the distribution appears here.

Colour: the two validated hues from Figure 1b (blue = own-q, orange = tangent). pooled-q and the
permutation null are rendered as NEUTRAL baselines rather than a third hue -- conceptually correct
(pooled-q is a null-family baseline, not a competing method) and it avoids a CVD failure: blue/orange/
green fails adjacent CVD separation at dE 3.2 (protan). Marker shape carries identity redundantly.
"""
import json, os, sys
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

E95 = os.path.join(ROOT, "results/e95_gate_regeneration_results.json")
FIGDIR = os.path.join(ROOT, "figures")
STEM = "fig1c_nontriviality_q_baselines"
CATALOGS = ("GWTC-3", "O4a", "O4b")
OWN_C, TANGENT_C = "#2a78d6", "#eb6834"          # identical to Figure 1b
NULL_BAND, NULL_EDGE, POOLED_C = "#e4e3dd", "#a8a79e", "#5c5b55"
INK, MUTED, GRID = "#1a1a19", "#5c5b55", "#d8d7d0"


def require(path):
    if not os.path.exists(path):
        raise SystemExit(
            f"FATAL: required artifact missing: {os.path.relpath(path, ROOT)}\n"
            "  Figure 1c is artifact-backed and will not recompute from raw data.\n"
            "  Regenerate with:  python3 src/e94_build_posterior_cache.py  (needs data/, ~5 min)\n"
            "                    python3 src/e95_gate_regeneration.py")
    return path


def build():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D
    from matplotlib.patches import Patch

    e95 = json.load(open(require(E95)))
    gate = e95["gate_A"]
    for cat in CATALOGS:
        if cat not in gate:
            raise SystemExit(f"FATAL: catalog {cat} absent from {os.path.relpath(E95, ROOT)}")

    fig, ax = plt.subplots(figsize=(7.6, 4.6))
    side = {"figure": STEM, "source_artifacts": [os.path.relpath(E95, ROOT)],
            "axr_min": e95["axr_min"], "catalogs": {},
            "interval_meaning": ("grey band = permutation null p05-p95 (own-q replaced by another "
                                 "event's q marginal, 300 catalog-stratified draws). NOT a confidence "
                                 "interval, NOT coverage, NOT uncertainty on own-q.")}

    ys = {cat: len(CATALOGS) - 1 - i for i, cat in enumerate(CATALOGS)}
    for cat in CATALOGS:
        g = gate[cat]
        n = g["perm_null"]
        y = ys[cat]

        ax.barh(y, n["p95"] - n["p05"], left=n["p05"], height=0.42, color=NULL_BAND,
                edgecolor=NULL_EDGE, linewidth=0.8, zorder=1)
        ax.plot([n["mean"], n["mean"]], [y - 0.21, y + 0.21], color=NULL_EDGE, lw=1.6, zorder=2)
        ax.plot([n["min"], n["min"]], [y - 0.26, y + 0.26], color=MUTED, lw=2.0, zorder=3)
        ax.plot(g["pooled_q"], y, marker="D", ms=6.5, color=POOLED_C, mec="white", mew=0.8, zorder=4)
        ax.plot(g["tangent"], y, marker="s", ms=8.5, color=TANGENT_C, mec="white", mew=0.9, zorder=5)
        ax.plot(g["own_q"], y, marker="o", ms=12, color=OWN_C, mec="white", mew=1.4, zorder=7)

        ax.annotate(f"{g['own_q']:.2f}°", (g["own_q"], y), textcoords="offset points",
                    xytext=(0, 17), ha="center", fontsize=9.5, color=OWN_C, fontweight="bold")
        ax.annotate("below all 300", (g["own_q"], y), textcoords="offset points",
                    xytext=(0, -24), ha="center", fontsize=7.6, color=MUTED)
        ax.annotate("best of 300", (n["min"], y), textcoords="offset points",
                    xytext=(0, 16), ha="center", fontsize=7.4, color=MUTED)

        side["catalogs"][cat] = {
            "n_elongated": g["n_elong"], "own_q_deg": g["own_q"], "tangent_deg": g["tangent"],
            "pooled_q_deg": g["pooled_q"],
            "perm_null": {k: n[k] for k in ("n", "mean", "sd", "min", "p05", "p95",
                                            "own_percentile", "own_below_all")}}
        assert n["own_below_all"] and g["own_q"] < n["min"], (cat, g["own_q"], n["min"])

    ax.set_yticks([ys[c] for c in CATALOGS])
    ax.set_yticklabels([f"{c}   (n = {gate[c]['n_elong']})" for c in CATALOGS],
                       fontsize=9.5, color=INK)
    ax.set_xscale("log")
    ax.set_xlim(0.55, 26)
    ax.set_ylim(-0.75, len(CATALOGS) - 0.25)
    ax.set_xlabel("median orientation error over elongated events   |Δψ|   (degrees)",
                  fontsize=9.5, color=INK)
    ax.grid(axis="x", color=GRID, lw=0.6, alpha=0.6)
    ax.set_axisbelow(True)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(colors=MUTED, labelsize=8.5, length=3)
    ax.tick_params(axis="y", length=0)

    leg_handles = [
        Line2D([], [], marker="o", color=OWN_C, ls="none", ms=8, mec="white", mew=1.0,
               label="event's OWN $q$ marginal"),
        Line2D([], [], marker="s", color=TANGENT_C, ls="none", ms=7, mec="white", mew=0.8,
               label="median-point tangent"),
        Line2D([], [], marker="D", color=POOLED_C, ls="none", ms=6, mec="white", mew=0.8,
               label="pooled-catalog $q$"),
        Patch(facecolor=NULL_BAND, edgecolor=NULL_EDGE,
              label="permutation null, p05–p95 (300 draws)"),
        Line2D([], [], color=MUTED, lw=2.0, label="null minimum (best of 300)")]
    fig.legend(handles=leg_handles, loc="lower center", ncol=3, frameon=False, fontsize=8.5,
               bbox_to_anchor=(0.5, 0.005))

    fig.suptitle("Substituting any other event's $q$ marginal destroys the reconstruction",
                 fontsize=10.5, color=INK, y=0.97)
    fig.subplots_adjust(left=0.19, right=0.97, top=0.87, bottom=0.30)

    os.makedirs(FIGDIR, exist_ok=True)
    outs = []
    for ext in ("png", "pdf"):
        p = os.path.join(FIGDIR, f"{STEM}.{ext}")
        fig.savefig(p, dpi=300, bbox_inches="tight", facecolor="white")
        outs.append(os.path.relpath(p, ROOT))
    plt.close(fig)

    side["outputs"] = outs
    side["note"] = ("own-q lies below the MINIMUM of 300 catalog-stratified permutations in every "
                    "catalog, so the permutation p-value is < 1/300 in each. The single-shuffle "
                    "figure from earlier prose is deliberately not plotted: re-drawing it moved the "
                    "O4a value from 3.04 to 8.62 deg, i.e. one permutation is not a null.")
    sp = os.path.join(FIGDIR, f"{STEM}.json")
    json.dump(side, open(sp, "w"), indent=1)
    outs.append(os.path.relpath(sp, ROOT))

    for cat in CATALOGS:
        s = side["catalogs"][cat]
        n = s["perm_null"]
        print(f"  {cat:>7} n={s['n_elongated']:3d}  own {s['own_q_deg']:.2f}  tangent "
              f"{s['tangent_deg']:.2f}  pooled {s['pooled_q_deg']:.2f}  | null {n['mean']:.2f}"
              f"±{n['sd']:.2f} min {n['min']:.2f}  below_all={n['own_below_all']}")
    print("wrote " + ", ".join(outs))
    return side


if __name__ == "__main__":
    build()
