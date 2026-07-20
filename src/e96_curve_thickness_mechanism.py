#!/usr/bin/env python3
"""E96 - is arc-varying posterior thickness the mechanism behind the curved-law residual?

The last major claim still living in prose. Gate B observed a ~1 deg residual between the measured
(m1,m2) principal axis and the constant-Mc curve reconstruction, and proposed that the curve model's
ZERO THICKNESS is why: a real posterior has finite perpendicular width, and if that width varies along
the arc it rotates the PCA axis. An in-sample fit improved the residual, which proves little -- the
thickness was learned from the very posterior it was then asked to explain.

This battery makes the estimator explicit, reproduces the in-sample result, and adds the test that
matters: learn w(q) from waveform family A and predict family B's SEPARATELY INFERRED axis without ever
touching B's thickness. It is scored against the pure curve and against equal-complexity nuisance tapers
(constant / linear / quadratic fitted to the SAME family-A widths), so "any taper helps" is
distinguishable from "the measured taper helps".

Reads `results/e94_posterior_cache.npz` only. No HDF5 access. Seed 96.

THICKNESS ESTIMATOR (declared, not implied):
  curve point      m1_c(q) = Mc (1+q)^(1/5) q^(-3/5),  m2_c = q m1_c, at the event's MEDIAN Mc
  perpendicular    unit normal to the local curve tangent, from a finite difference dq = 1e-4
  offset           d_perp = (m1 - m1_c, m2 - m2_c) . n_hat, per sample
  binning          N_BINS equal-count (quantile) bins in q
  min bin count    MIN_PER_BIN samples, else the bin is dropped; >=MIN_GOOD_BINS bins required
  width statistic  standard deviation of d_perp within the bin
  smoothing        none; linear interpolation between bin centres, clamped at the ends
A constant-thickness synthetic control is run to confirm the estimator does not IMPOSE monotonicity.
"""
import json, math, os, sys
import numpy as np
from scipy.stats import spearmanr, wilcoxon

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from src.e94_build_posterior_cache import load, CACHE, MANIFEST
from src.e95_gate_regeneration import sdiff, primary_rows, AXR_MIN, FAMILY_PAIR
from src.e71_gwtc5_curved_law import psi_axr_rho, curve_psi
from src.e65_pn_fisher_rotation import ang_of, adiff

SEED = 96
N_BINS = 6
MIN_PER_BIN = 20
MIN_GOOD_BINS = 4
N_MODEL = 8000            # samples drawn when rebuilding a curve+thickness cloud
DQ = 1e-4
RESULT_JSON = os.path.join(ROOT, "results/e96_curve_thickness_mechanism_results.json")


# ---------------- geometry ----------------
def curve_pt(mc, q):
    m1 = mc * (1 + q) ** 0.2 * q ** -0.6
    return m1, q * m1


def normal_at(mc, q, dq=DQ):
    a1, a2 = curve_pt(mc, q)
    b1, b2 = curve_pt(mc, q + dq)
    tx, ty = b1 - a1, b2 - a2
    n = np.hypot(tx, ty)
    return -ty / n, tx / n


def thickness_profile(m1, m2, q, mc, n_bins=N_BINS, min_per_bin=MIN_PER_BIN):
    """Return (bin_centres_q, width_per_bin) using the declared estimator. NaN bins are dropped."""
    c1, c2 = curve_pt(mc, q)
    nx, ny = normal_at(mc, q)
    dperp = (m1 - c1) * nx + (m2 - c2) * ny
    edges = np.quantile(q, np.linspace(0, 1, n_bins + 1))
    mid, w = [], []
    for i in range(n_bins):
        s = (q >= edges[i]) & (q < edges[i + 1]) if i < n_bins - 1 else (q >= edges[i]) & (q <= edges[i + 1])
        if s.sum() >= min_per_bin:
            mid.append(0.5 * (edges[i] + edges[i + 1]))
            w.append(float(np.std(dperp[s])))
    return np.array(mid), np.array(w)


def taper_model(mid, w, kind):
    """Equal-complexity alternatives fitted to the SAME widths. 'measured' = interpolation."""
    if kind == "measured":
        return lambda qq: np.interp(qq, mid, w)
    if kind == "constant":
        c = float(np.mean(w))
        return lambda qq: np.full_like(qq, c)
    deg = {"linear": 1, "quadratic": 2}[kind]
    if len(mid) <= deg:
        c = float(np.mean(w))
        return lambda qq: np.full_like(qq, c)
    p = np.polyfit(mid, w, deg)
    return lambda qq: np.clip(np.polyval(p, qq), 0.0, None)


def psi_curve_with_thickness(mc, q_marginal, wfun, rng, n=N_MODEL):
    """PCA axis of a curve cloud given a thickness profile. Pure curve is wfun == 0."""
    qs = q_marginal[rng.integers(0, len(q_marginal), n)]
    c1, c2 = curve_pt(mc, qs)
    nx, ny = normal_at(mc, qs)
    off = rng.normal(0, 1, n) * np.asarray(wfun(qs), float)
    X = np.column_stack([c1 + nx * off, c2 + ny * off])
    X = X - X.mean(0)
    _, V = np.linalg.eigh(X.T @ X / len(X))
    return ang_of(V[:, 1])


# ---------------- controls ----------------
def constant_thickness_control(rng, cases=((25.0, 1.0), (25.0, 3.0), (10.0, 0.5), (60.0, 2.0)),
                               growing=((25.0, 1.0, 0.5), (25.0, 1.0, 1.5))):
    """The estimator must NOT manufacture monotonic w(q) when the true thickness is constant."""
    out = {"constant": [], "growing": []}
    for mc, w0 in cases:
        q = rng.uniform(0.25, 0.95, 60000)
        c1, c2 = curve_pt(mc, q); nx, ny = normal_at(mc, q)
        off = rng.normal(0, w0, len(q))
        mid, w = thickness_profile(c1 + nx * off, c2 + ny * off, q, mc)
        out["constant"].append({"mc": mc, "true_w": w0, "spearman_w_q": float(spearmanr(mid, w)[0]),
                                "w_first": float(w[0]), "w_last": float(w[-1])})
    for mc, w0, slope in growing:
        q = rng.uniform(0.25, 0.95, 60000)
        c1, c2 = curve_pt(mc, q); nx, ny = normal_at(mc, q)
        off = rng.normal(0, 1, len(q)) * (w0 * (1.0 + slope * (q - 0.25) / 0.7))
        mid, w = thickness_profile(c1 + nx * off, c2 + ny * off, q, mc)
        out["growing"].append({"mc": mc, "slope": slope, "spearman_w_q": float(spearmanr(mid, w)[0]),
                               "w_first": float(w[0]), "w_last": float(w[-1])})
    return out


# ---------------- main analyses ----------------
def in_sample(prim, rng):
    rows = []
    for (cat, ev), v in sorted(prim.items()):
        d = v["raw"]
        if v["axr"] < AXR_MIN:
            continue
        m1 = d["m1s"].astype(float); m2 = d["m2s"].astype(float); q = d["q"].astype(float)
        mc = v["mc"]
        mid, w = thickness_profile(m1, m2, q, mc)
        if len(mid) < MIN_GOOD_BINS:
            continue
        pure = sdiff(curve_psi(mc, q), v["psi"])
        thick = sdiff(psi_curve_with_thickness(mc, q, taper_model(mid, w, "measured"), rng), v["psi"])
        total = float(np.std(np.hypot(m1 - m1.mean(), m2 - m2.mean())))
        rows.append({"catalog": cat, "event": ev, "axr": float(v["axr"]),
                     "signed_pure": float(pure), "signed_thick": float(thick),
                     "abs_pure": abs(float(pure)), "abs_thick": abs(float(thick)),
                     "spearman_w_q": float(spearmanr(mid, w)[0]) if len(mid) > 2 else float("nan"),
                     "w_median_rel": float(np.median(w) / total) if total > 0 else float("nan"),
                     "n_bins": int(len(mid))})
    ap = np.array([r["abs_pure"] for r in rows]); at = np.array([r["abs_thick"] for r in rows])
    sp = np.array([r["spearman_w_q"] for r in rows])
    return rows, {
        "n": len(rows),
        "median_signed_pure": float(np.median([r["signed_pure"] for r in rows])),
        "median_signed_thick": float(np.median([r["signed_thick"] for r in rows])),
        "median_abs_pure": float(np.median(ap)), "median_abs_thick": float(np.median(at)),
        "frac_improved": float(np.mean(at < ap)),
        "wilcoxon_p": float(wilcoxon(ap, at).pvalue),
        "median_spearman_w_q": float(np.nanmedian(sp)),
        "frac_spearman_eq_1": float(np.mean(np.isclose(sp, 1.0))),
        "median_relative_thickness": float(np.nanmedian([r["w_median_rel"] for r in rows])),
        "caveat": ("IN-SAMPLE: w(q) is learned from the same posterior it then helps reconstruct, and "
                   "adds flexibility. Improvement here is not evidence of mechanism.")}


def cross_family(rec, byev, rng):
    """THE test: learn w(q) on family A, predict family B's axis, never touching B's thickness."""
    kinds = ("measured", "constant", "linear", "quadratic")
    per, rows = {f"{d}_{k}": [] for d in ("AtoB", "BtoA") for k in kinds}, []
    pure = {"AtoB": [], "BtoA": []}
    for (cat, ev), gs in sorted(byev.items()):
        A, B = FAMILY_PAIR[cat]
        if A not in gs or B not in gs:
            continue
        da, db = rec[(cat, ev, A)], rec[(cat, ev, B)]
        pa, aa, _ = psi_axr_rho(da["m1s"].astype(float), da["m2s"].astype(float))
        pb, ab, _ = psi_axr_rho(db["m1s"].astype(float), db["m2s"].astype(float))
        if aa < AXR_MIN or ab < AXR_MIN:
            continue
        rec_row = {"catalog": cat, "event": ev, "axr_A": float(aa), "axr_B": float(ab)}
        for src, tgt, tag in ((da, db, "AtoB"), (db, da, "BtoA")):
            mc_s = float(np.median(src["mcs"]))
            mid, w = thickness_profile(src["m1s"].astype(float), src["m2s"].astype(float),
                                       src["q"].astype(float), mc_s)
            if len(mid) < MIN_GOOD_BINS:
                continue
            mc_t = float(np.median(tgt["mcs"])); q_t = tgt["q"].astype(float)
            psi_t = pb if tag == "AtoB" else pa
            pure[tag].append(abs(adiff(curve_psi(mc_t, q_t), psi_t)))
            for k in kinds:
                e = abs(adiff(psi_curve_with_thickness(mc_t, q_t, taper_model(mid, w, k), rng), psi_t))
                per[f"{tag}_{k}"].append(e)
                rec_row[f"{tag}_{k}"] = float(e)
            rec_row[f"{tag}_pure"] = float(pure[tag][-1])
        rows.append(rec_row)
    summary = {}
    for tag in ("AtoB", "BtoA"):
        if not pure[tag]:
            continue
        summary[tag] = {"n": len(pure[tag]), "pure_curve": float(np.median(pure[tag]))}
        for k in kinds:
            v = per[f"{tag}_{k}"]
            summary[tag][k] = float(np.median(v))
            summary[tag][f"{k}_beats_pure_frac"] = float(np.mean(np.array(v) < np.array(pure[tag])))
            summary[tag][f"{k}_vs_pure_wilcoxon_p"] = float(wilcoxon(v, pure[tag]).pvalue)
    return rows, summary


def verdict(cross):
    """Declared rules, applied mechanically. TWO questions are separated:
       (1) does FINITE thickness beat the zero-thickness curve out of sample?
       (2) does the ARC-VARYING part matter, i.e. does the measured profile beat a CONSTANT one
           and hold up against equal-complexity linear/quadratic tapers?
    Passing (1) but failing (2) means the zero-thickness idealization is what is wrong -- not that
    the specific measured taper is the mechanism."""
    finite, varying = [], []
    for tag in ("AtoB", "BtoA"):
        s = cross.get(tag)
        if not s:
            return {"finite_thickness": "INCONCLUSIVE", "arc_variation": "INCONCLUSIVE",
                    "statement": "insufficient cross-family events"}
        finite.append(s["measured"] < s["pure_curve"] and s["measured_vs_pure_wilcoxon_p"] < 0.05)
        # the measured taper must beat a constant one AND not be beaten by a simpler parametric taper
        varying.append(s["measured"] < s["constant"] and s["measured"] <= min(s["linear"], s["quadratic"]))
    v = {"finite_thickness": "SUPPORTED OUT-OF-SAMPLE" if all(finite) else "NOT SUPPORTED",
         "arc_variation": "SUPPORTED" if all(varying) else "NOT ESTABLISHED"}
    if all(finite) and all(varying):
        v["statement"] = ("Arc-varying thickness supported out of sample. Still EXPLANATORY only: "
                          "thickness is two-dimensional information and is NOT part of the "
                          "two-summary compression claim.")
    elif all(finite):
        v["statement"] = ("FINITE thickness improves cross-family prediction in both directions, so the "
                          "zero-thickness idealization is genuinely part of the residual. But the "
                          "ARC-VARYING part is NOT established: a constant or simple linear taper does "
                          "as well as or better than the measured profile. Do not claim the measured "
                          "taper is the mechanism, and do not quote a fraction of the residual explained.")
    else:
        v["statement"] = ("IN-SAMPLE ONLY - cross-family thickness does not beat the pure curve; the "
                          "mechanism is not established and must not be described as explaining any "
                          "fraction of the residual.")
    return v


def main():
    rng = np.random.default_rng(SEED)
    rec = load()
    prim, byev = primary_rows(rec)
    manifest = json.load(open(MANIFEST)) if os.path.exists(MANIFEST) else {}
    ctrl = constant_thickness_control(rng)
    ev_rows, ins = in_sample(prim, rng)
    x_rows, cross = cross_family(rec, byev, rng)
    out = {
        "battery": "E96 curve thickness mechanism", "seed": SEED,
        "provenance": {"cache": os.path.relpath(CACHE, ROOT), "manifest": os.path.relpath(MANIFEST, ROOT),
                       "cache_manifest": manifest, "hdf5_accessed": False},
        "estimator": {"n_bins": N_BINS, "min_per_bin": MIN_PER_BIN, "min_good_bins": MIN_GOOD_BINS,
                      "width_statistic": "std of perpendicular offset within equal-count q bins",
                      "smoothing": "none; linear interpolation between bin centres, clamped",
                      "normal_finite_difference_dq": DQ, "n_model_samples": N_MODEL},
        "estimator_controls": ctrl,
        "in_sample": ins,
        "cross_family": cross,
        "verdict": verdict(cross),
        "events_in_sample": ev_rows,
        "events_cross_family": x_rows,
    }
    json.dump(out, open(RESULT_JSON, "w"), indent=1)
    print(f"in-sample n={ins['n']}: pure |err| {ins['median_abs_pure']:.3f} -> thick "
          f"{ins['median_abs_thick']:.3f}, improved {ins['frac_improved']:.0%}, "
          f"wilcoxon p={ins['wilcoxon_p']:.2e}")
    print(f"  median spearman(w,q)={ins['median_spearman_w_q']:.3f}, "
          f"frac exactly +1 = {ins['frac_spearman_eq_1']:.2f}, "
          f"relative thickness {ins['median_relative_thickness']:.3f}")
    print("  estimator control (CONSTANT true thickness) spearman(w,q):",
          [round(c["spearman_w_q"], 2) for c in ctrl["constant"]])
    print("  estimator control (GROWING true thickness)  spearman(w,q):",
          [round(c["spearman_w_q"], 2) for c in ctrl["growing"]])
    for tag, s in cross.items():
        print(f"  {tag} n={s['n']}: pure {s['pure_curve']:.2f} | measured {s['measured']:.2f} "
              f"(p={s['measured_vs_pure_wilcoxon_p']:.3f}) | const {s['constant']:.2f} "
              f"| lin {s['linear']:.2f} | quad {s['quadratic']:.2f}")
    print("VERDICT finite thickness:", out["verdict"]["finite_thickness"])
    print("VERDICT arc variation :", out["verdict"]["arc_variation"])
    print(" ", out["verdict"]["statement"])
    print("wrote", RESULT_JSON)


if __name__ == "__main__":
    main()
