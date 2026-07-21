#!/usr/bin/env python3
"""Figure 2a - EXAMPLES of the posterior geometry and its reconstruction. Explanatory, secondary.

This is NOT a main-claim panel and must not be captioned as proof of a mechanism. The main claims are
Figure 1b (the curve beats the median-point tangent) and Figure 1c (the event's OWN q marginal is
required). This figure only shows what the geometry looks like in three deterministically selected
events, so a reader can see what the numbers in Figures 1b/1c describe.

On the thickness mechanism: E96 found that FINITE thickness is supported out of sample but that ARC
VARIATION is NOT established -- a constant taper does as well as the measured profile in one
direction. The thickness-adjusted axis is therefore deliberately NOT drawn here: it would add a
fourth overlay of a quantity the artifact does not support as a mechanism.

Reads the E94 posterior cache ONLY (it needs actual samples to draw clouds). No HDF5, no
prose-derived numbers; every plotted angle is recomputed from the cached samples with the same
functions the gate batteries use.

DETERMINISTIC SELECTION RULES (no cherry-picking; recorded in the sidecar):
  panel 1  "clean success, high elongation" -> among elongated events with axr >= 8, the MINIMUM
                                               curve error
  panel 2  "typical"                        -> the event whose curve error is CLOSEST TO THE MEDIAN
                                               curve error over elongated events
  panel 3  "worst case"                     -> the MAXIMUM curve error over elongated events
Panel 3 is included so the figure is not a gallery of successes. Also recorded, though not plotted:
the tangent beats the curve in ~16% of elongated events overall and ~31% above axr 8 -- the
extreme-elongation regime where the curve's advantage shrinks (see Gate B2).

Axes use EQUAL ASPECT. Orientation angles are only visually truthful under equal aspect; any other
scaling silently distorts every angle in the figure.
"""
import json, math, os, sys
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from src.e94_build_posterior_cache import load, CACHE, MANIFEST
from src.e95_gate_regeneration import primary_rows, AXR_MIN
from src.e71_gwtc5_curved_law import curve_psi, tangent_angles, psi_axr_rho
from src.e65_pn_fisher_rotation import adiff

FIGDIR = os.path.join(ROOT, "figures")
STEM = "fig2a_posterior_geometry_examples"
CURVE_C, TANGENT_C = "#2a78d6", "#eb6834"          # identical to Figures 1b / 1c
MEAS_C, SAMPLE_C = "#1a1a19", "#9fbfe4"
INK, MUTED, GRID = "#1a1a19", "#5c5b55", "#d8d7d0"
HIGH_AXR = 8.0


def require_cache():
    if not os.path.exists(CACHE):
        raise SystemExit(
            f"FATAL: posterior cache missing: {os.path.relpath(CACHE, ROOT)}\n"
            "  Figure 2a needs actual posterior samples and will not read raw HDF5.\n"
            "  Build it with:  python3 src/e94_build_posterior_cache.py\n"
            "  (one HDF5 pass, ~5 minutes, requires the PE releases under data/ -- see README)")
    return CACHE


def collect(prim):
    rows = []
    for (cat, ev), v in sorted(prim.items()):
        if v["axr"] < AXR_MIN:
            continue
        ce = abs(adiff(curve_psi(v["mc"], v["q"]), v["psi"]))
        te = abs(adiff(tangent_angles(v["m1m"], v["m2m"])[0], v["psi"]))
        rows.append(dict(catalog=cat, event=ev, group=v["group"], axr=float(v["axr"]),
                         curve_err=float(ce), tangent_err=float(te), v=v))
    return rows


def select(rows):
    """The three deterministic rules. Returns [(label, rule_text, row), ...]."""
    med = float(np.median([r["curve_err"] for r in rows]))
    hi = [r for r in rows if r["axr"] >= HIGH_AXR]
    return [
        ("clean success (high elongation)",
         f"min curve error among elongated events with axr >= {HIGH_AXR}",
         min(hi, key=lambda r: r["curve_err"])),
        ("typical",
         f"curve error closest to the median over elongated events ({med:.3f} deg)",
         min(rows, key=lambda r: abs(r["curve_err"] - med))),
        ("worst case",
         "max curve error over elongated events",
         max(rows, key=lambda r: r["curve_err"])),
    ]


def build():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D

    require_cache()
    rec = load()
    prim, _ = primary_rows(rec)
    rows = collect(prim)
    picks = select(rows)

    fig, axes = plt.subplots(1, 3, figsize=(9.6, 3.9))
    side = {"figure": STEM, "role": "explanatory / secondary -- NOT a main-claim panel",
            "caption_guidance": ("Examples of the posterior geometry and its reconstruction. This "
                                 "panel illustrates; it does not establish a mechanism. E96 supports "
                                 "finite thickness out of sample but does NOT establish arc "
                                 "variation, so no thickness-adjusted axis is drawn."),
            "provenance": {"cache": os.path.relpath(CACHE, ROOT),
                           "manifest": os.path.relpath(MANIFEST, ROOT), "hdf5_accessed": False},
            "axr_min": AXR_MIN, "high_axr_threshold": HIGH_AXR,
            "n_elongated_considered": len(rows), "panels": []}

    for ax, (label, rule, r) in zip(axes, picks):
        v = r["v"]
        m1 = v["raw"]["m1s"].astype(float)
        m2 = v["raw"]["m2s"].astype(float)
        q = v["q"]
        mc = v["mc"]
        cx, cy = m1.mean(), m2.mean()

        ax.scatter(m1, m2, s=3, color=SAMPLE_C, alpha=0.30, linewidths=0, zorder=1, rasterized=True)

        # the constant-Mc model curve over the event's own q range
        qq = np.linspace(max(np.percentile(q, 1), 0.02), min(np.percentile(q, 99), 1.0), 400)
        c1 = mc * (1 + qq) ** 0.2 * qq ** -0.6
        ax.plot(c1, qq * c1, color=CURVE_C, lw=1.4, alpha=0.55, zorder=2)

        # direction lines, all the same length so they are comparable
        w, _, _ = psi_axr_rho(m1, m2)
        L = 2.1 * math.sqrt(max(np.linalg.eigvalsh(np.cov(np.vstack([m1, m2])))[-1], 1e-12))
        for ang, col, ls, lw, z in ((v["psi"], MEAS_C, "-", 2.4, 6),
                                    (tangent_angles(v["m1m"], v["m2m"])[0], TANGENT_C, "--", 2.0, 4),
                                    (curve_psi(mc, q), CURVE_C, "--", 2.0, 5)):
            dx, dy = math.cos(math.radians(ang)), math.sin(math.radians(ang))
            ax.plot([cx - L * dx, cx + L * dx], [cy - L * dy, cy + L * dy],
                    color=col, ls=ls, lw=lw, zorder=z, solid_capstyle="round")

        # Limits follow the DATA (1-99 percentile plus a margin), then are squared up so that
        # equal aspect does not distort angles. Centring a fixed +/-1.5L box on the mean instead
        # blows up for high-variance events -- it produced a +/-200 Msun panel showing NEGATIVE
        # masses and an invisible sample cloud. Lower bounds are clamped at 0: masses are positive.
        xlo, xhi = np.percentile(m1, [1, 99])
        ylo, yhi = np.percentile(m2, [1, 99])
        mx, my = 0.5 * (xlo + xhi), 0.5 * (ylo + yhi)
        half = 0.62 * max(xhi - xlo, yhi - ylo, 1e-6)
        x0, x1 = mx - half, mx + half
        y0, y1 = my - half, my + half
        if x0 < 0:
            x1, x0 = x1 - x0, 0.0
        if y0 < 0:
            y1, y0 = y1 - y0, 0.0
        ax.set_xlim(x0, x1)
        ax.set_ylim(y0, y1)
        ax.set_aspect("equal", adjustable="box")
        ax.set_title(f"{label}\n{r['event']}  ({r['catalog']})", fontsize=9, color=INK, pad=6)
        ax.set_xlabel("$m_1$  [$M_\\odot$]", fontsize=9, color=INK)
        ax.text(0.03, 0.97,
                f"axis ratio {r['axr']:.1f}\ncurve {r['curve_err']:.2f}°\ntangent {r['tangent_err']:.2f}°",
                transform=ax.transAxes, va="top", ha="left", fontsize=8.2, color=MUTED,
                linespacing=1.5)
        ax.grid(color=GRID, lw=0.5, alpha=0.5)
        ax.set_axisbelow(True)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        for s in ("left", "bottom"):
            ax.spines[s].set_color(GRID)
        ax.tick_params(colors=MUTED, labelsize=8, length=3)

        side["panels"].append({
            "panel": label, "selection_rule": rule, "event": r["event"], "catalog": r["catalog"],
            "waveform_group": r["group"], "axr": r["axr"], "curve_err_deg": r["curve_err"],
            "tangent_err_deg": r["tangent_err"], "n_samples_plotted": int(len(m1)),
            "thickness_adjusted_drawn": False})

    axes[0].set_ylabel("$m_2$  [$M_\\odot$]", fontsize=9, color=INK)
    fig.legend(handles=[
        Line2D([], [], color=MEAS_C, lw=2.4, label="measured principal axis"),
        Line2D([], [], color=CURVE_C, lw=2.0, ls="--", label="constant-$\\mathcal{M}_c$ curve prediction"),
        Line2D([], [], color=TANGENT_C, lw=2.0, ls="--", label="median-point tangent prediction"),
        Line2D([], [], color=CURVE_C, lw=1.4, alpha=0.55, label="constant-$\\mathcal{M}_c$ curve"),
        Line2D([], [], marker="o", color=SAMPLE_C, ls="none", ms=6, label="posterior samples")],
        loc="lower center", ncol=5, frameon=False, fontsize=8.3, bbox_to_anchor=(0.5, 0.0))
    # No suptitle: the LaTeX caption carries the description in the manuscript.
    fig.subplots_adjust(left=0.07, right=0.98, top=0.86, bottom=0.22, wspace=0.28)

    os.makedirs(FIGDIR, exist_ok=True)
    outs = []
    for ext in ("png", "pdf"):
        p = os.path.join(FIGDIR, f"{STEM}.{ext}")
        fig.savefig(p, dpi=300, facecolor="white")
        outs.append(os.path.relpath(p, ROOT))
    plt.close(fig)

    tw = [r for r in rows if r["tangent_err"] < r["curve_err"]]
    twh = [r for r in rows if r["axr"] >= HIGH_AXR and r["tangent_err"] < r["curve_err"]]
    nhi = sum(1 for r in rows if r["axr"] >= HIGH_AXR)
    side["recorded_but_not_plotted"] = {
        "tangent_beats_curve_fraction_all_elongated": round(len(tw) / len(rows), 3),
        "tangent_beats_curve_fraction_axr_ge_8": round(len(twh) / max(nhi, 1), 3),
        "note": ("at extreme elongation the tangent's disadvantage shrinks and it sometimes wins "
                 "(Gate B2). The two highest-axr events in the catalog are such cases. They are not "
                 "plotted here, but the fractions are recorded so the figure is not read as implying "
                 "the curve always wins.")}
    side["outputs"] = outs
    sp = os.path.join(FIGDIR, f"{STEM}.json")
    json.dump(side, open(sp, "w"), indent=1)
    outs.append(os.path.relpath(sp, ROOT))

    for p in side["panels"]:
        print(f"  {p['panel']:<32} {p['catalog']:>7} {p['event']:<22} axr={p['axr']:6.2f} "
              f"curve={p['curve_err_deg']:6.2f} tangent={p['tangent_err_deg']:6.2f}")
    print(f"  tangent beats curve: {side['recorded_but_not_plotted']['tangent_beats_curve_fraction_all_elongated']:.0%}"
          f" of elongated, {side['recorded_but_not_plotted']['tangent_beats_curve_fraction_axr_ge_8']:.0%} at axr>=8")
    print("wrote " + ", ".join(outs))
    return side


if __name__ == "__main__":
    build()
