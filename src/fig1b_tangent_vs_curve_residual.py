#!/usr/bin/env python3
"""Figure 1b - tangent vs curve residual on elongated events, across three disjoint event catalogs.

The manuscript's visual spine: the median-point TANGENT approximation leaves several degrees of
orientation error, and the constant-Mc CURVE reconstruction removes most of it, in every catalog.

ARTIFACT-BACKED. Reads only committed reproducible artifacts:
  results/e92_curve_uncertainty_results.json   per-event |dpsi| for curve and tangent
  results/e95_gate_regeneration_results.json   per-catalog medians (cross-check)
No HDF5, no cache, no recomputation from raw PE. The script FAILS LOUDLY if either file is missing
(they are produced by src/e92_curve_uncertainty.py and src/e95_gate_regeneration.py, both of which
require results/e94_posterior_cache.npz -- see README).

Form: a paired slopegraph. Each elongated event contributes ONE line from its tangent error to its
curve error, so the reader sees every event move rather than only a summary; catalogs are faceted
because they are disjoint event sets, not repeated measurements of the same thing. Log y because the
per-event errors span ~0.01-24 deg. Medians carry a bootstrap CI computed over events.

Colour: two categorical slots (blue = curve, orange = tangent), validated with the dataviz palette
checker (worst adjacent CVD dE 24.7 protan, normal-vision 33.6, all checks PASS). Identity is also
carried by marker shape and by direct labels, so the figure survives greyscale printing.
"""
import json, os, sys
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

E92 = os.path.join(ROOT, "results/e92_curve_uncertainty_results.json")
E95 = os.path.join(ROOT, "results/e95_gate_regeneration_results.json")
FIGDIR = os.path.join(ROOT, "figures")
STEM = "fig1b_tangent_vs_curve_residual"
CATALOGS = ("GWTC-3", "O4a", "O4b")
CURVE_C, TANGENT_C = "#2a78d6", "#eb6834"      # validated categorical slots 1 and 6
INK, MUTED, GRID = "#1a1a19", "#5c5b55", "#d8d7d0"
SEED = 1
N_BOOT = 5000


def require(path):
    if not os.path.exists(path):
        raise SystemExit(
            f"FATAL: required artifact missing: {os.path.relpath(path, ROOT)}\n"
            "  Figure 1b is artifact-backed and will not recompute from raw data.\n"
            "  Regenerate with:  python3 src/e94_build_posterior_cache.py  (needs data/, ~5 min)\n"
            "                    python3 src/e92_curve_uncertainty.py\n"
            "                    python3 src/e95_gate_regeneration.py")
    return path


def median_ci(x, rng, n_boot=N_BOOT):
    """Bootstrap CI on the MEDIAN over events (not the per-event Monte Carlo resolution)."""
    x = np.asarray(x, float)
    b = np.median(rng.choice(x, size=(n_boot, len(x)), replace=True), axis=1)
    return float(np.median(x)), float(np.percentile(b, 16)), float(np.percentile(b, 84))


def build():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    e92 = json.load(open(require(E92)))
    e95 = json.load(open(require(E95)))
    rng = np.random.default_rng(SEED)
    axr_min = e92["axr_min"]
    el = [r for r in e92["events"] if r["axr"] >= axr_min]

    fig, axes = plt.subplots(1, 3, figsize=(7.2, 3.5), sharey=True)
    side = {"figure": STEM, "source_artifacts": [os.path.relpath(E92, ROOT), os.path.relpath(E95, ROOT)],
            "axr_min": axr_min, "seed": SEED, "n_boot_median_ci": N_BOOT, "catalogs": {}}

    for ax, cat in zip(axes, CATALOGS):
        S = [r for r in el if r["catalog"] == cat]
        tan = np.array([r["tangent_err"] for r in S])
        cur = np.array([r["abs_err"] for r in S])

        for t, c in zip(tan, cur):                                   # one thin line per event
            ax.plot([0, 1], [t, c], color=GRID, lw=0.7, alpha=0.75, zorder=1,
                    solid_capstyle="round")
        ax.scatter(np.zeros_like(tan), tan, s=22, color=TANGENT_C, marker="s",
                   edgecolor="white", linewidth=0.5, alpha=0.7, zorder=3)
        ax.scatter(np.ones_like(cur), cur, s=22, color=CURVE_C, marker="o",
                   edgecolor="white", linewidth=0.5, alpha=0.7, zorder=3)

        stats = {}
        # medians are labelled in the empty TOP CORNERS (axes fraction): the point columns sit at
        # ~28% and ~72% of the axis width, so the corners never collide with data or the y-axis
        for xi, vals, col, key, ax_x, ha in ((0, tan, TANGENT_C, "tangent", 0.02, "left"),
                                             (1, cur, CURVE_C, "curve", 0.98, "right")):
            m, lo, hi = median_ci(vals, rng)
            stats[key] = {"median_deg": m, "ci16_deg": lo, "ci84_deg": hi, "n": len(vals)}
            ax.errorbar(xi, m, yerr=[[m - lo], [hi - m]], fmt="none", ecolor="white", elinewidth=5.0,
                        capsize=0, zorder=5)                      # white halo so the median reads
            ax.errorbar(xi, m, yerr=[[m - lo], [hi - m]], fmt="none", ecolor=col, elinewidth=2.4,
                        capsize=4, capthick=2.0, zorder=6)
            ax.plot([xi - 0.19, xi + 0.19], [m, m], color="white", lw=5.2, zorder=6,
                    solid_capstyle="round")
            ax.plot([xi - 0.19, xi + 0.19], [m, m], color=col, lw=2.8, zorder=7,
                    solid_capstyle="round")
            ax.text(ax_x, 0.965, f"{m:.2f}°", transform=ax.transAxes, ha=ha, va="top",
                    fontsize=9.5, color=col, fontweight="bold", zorder=8)

        # cross-check against the independently written e95 medians
        g = e95["gate_A"][cat]
        for key, ref in (("curve", g["own_q"]), ("tangent", g["tangent"])):
            assert abs(stats[key]["median_deg"] - ref) < 1e-6, (cat, key, stats[key], ref)
        stats["n_elongated"] = len(S)
        stats["e95_crosscheck"] = {"own_q": g["own_q"], "tangent": g["tangent"],
                                   "n_elong": g["n_elong"]}
        side["catalogs"][cat] = stats

        ax.set_xlim(-0.45, 1.45)
        ax.set_xticks([0, 1])
        ax.set_xticklabels(["tangent", "curve"], fontsize=9.5, color=INK)
        ax.set_yscale("log")
        ax.set_title(f"{cat}   (n = {len(S)})", fontsize=10, color=INK, pad=8)
        ax.grid(axis="y", color=GRID, lw=0.6, alpha=0.6)
        ax.set_axisbelow(True)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        for s in ("left", "bottom"):
            ax.spines[s].set_color(GRID)
        ax.tick_params(colors=MUTED, labelsize=8.5, length=3)

    axes[0].set_ylabel("orientation error  |Δψ|   (degrees)", fontsize=9.5, color=INK)
    axes[0].set_ylim(0.008, 40)

    from matplotlib.lines import Line2D
    fig.legend(handles=[
        Line2D([], [], marker="s", color=TANGENT_C, ls="none", ms=6.5, mec="white", mew=0.6,
               label="median-point tangent"),
        Line2D([], [], marker="o", color=CURVE_C, ls="none", ms=6.5, mec="white", mew=0.6,
               label="constant-$\\mathcal{M}_c$ curve reconstruction")],
        loc="lower center", ncol=2, frameon=False, fontsize=9, bbox_to_anchor=(0.5, -0.02))
    # No suptitle: in the manuscript the LaTeX caption carries the description, and an internal
    # title would duplicate it (and here would duplicate an interpretation as well).
    fig.tight_layout(rect=[0, 0.06, 1, 0.99])

    os.makedirs(FIGDIR, exist_ok=True)
    outs = []
    for ext in ("png", "pdf"):
        p = os.path.join(FIGDIR, f"{STEM}.{ext}")
        fig.savefig(p, dpi=300, bbox_inches="tight", facecolor="white")
        outs.append(os.path.relpath(p, ROOT))
    plt.close(fig)

    side["outputs"] = outs
    side["note"] = ("medians are over elongated events per catalog; the interval is a bootstrap CI on "
                    "the MEDIAN across events, not the per-event Monte Carlo resolution reported by "
                    "E92. Every median is asserted equal to the independently written E95 value.")
    sp = os.path.join(FIGDIR, f"{STEM}.json")
    json.dump(side, open(sp, "w"), indent=1)
    outs.append(os.path.relpath(sp, ROOT))

    for cat in CATALOGS:
        s = side["catalogs"][cat]
        print(f"  {cat:>7} n={s['n_elongated']:3d}  tangent {s['tangent']['median_deg']:.2f}"
              f" [{s['tangent']['ci16_deg']:.2f},{s['tangent']['ci84_deg']:.2f}]"
              f"   curve {s['curve']['median_deg']:.2f}"
              f" [{s['curve']['ci16_deg']:.2f},{s['curve']['ci84_deg']:.2f}]")
    print("wrote " + ", ".join(outs))
    return side


if __name__ == "__main__":
    build()
