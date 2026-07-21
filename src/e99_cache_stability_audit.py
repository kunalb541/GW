#!/usr/bin/env python3
"""E99 - is the E94 cache representative of the full released posteriors?

Raised in external review: E94 draws n_samp indices with `rng.integers`, i.e. WITH REPLACEMENT. That
makes the cache a bootstrap resample of the released samples, not a subsample of them, and downstream
text that says "the released posterior samples" is therefore imprecise. A deterministic artifact is not
automatically a representative one.

This battery answers the question directly rather than arguing about it:

  1. FULL vs CACHE -- recompute the headline reconstruction score from the FULL released samples
     (the only place in the project that re-reads HDF5 after E94) and compare to the cache value.
  2. SEED STABILITY -- rebuild the cache draw under several seeds and report the spread of the
     headline score, so the resampling noise is quantified rather than assumed small.
  3. DRAW SIZE -- repeat at several n_samp to show where the score converges.

If the spread across seeds is small compared with the effect being claimed, the cache is fit for
purpose and the paper can say so with a number attached. If it is not, the cache must be enlarged or
replaced by an exhaustive pass. Either way the answer is measured.

Seed 99. Slow by design: it reads HDF5 once for the full-sample reference.
"""
import json, os, sys, glob
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from src.e94_build_posterior_cache import CATALOGS, event_name, SRC
from src.e95_gate_regeneration import PREFERRED, AXR_MIN
from src.e71_gwtc5_curved_law import pick_group, psi_axr_rho, curve_psi
from src.e65_pn_fisher_rotation import adiff

SEED = 99
SEEDS = (94, 1, 2, 3, 4)
SIZES = (2000, 4000, 8000)
RESULT_JSON = os.path.join(ROOT, "results/e99_cache_stability_audit_results.json")


def full_samples():
    """Read every preferred-group posterior at FULL length. The only post-E94 HDF5 pass."""
    import h5py
    out = {}
    for lab, d in CATALOGS:
        for fp in sorted(glob.glob(os.path.join(ROOT, d, "*.h5"))
                         + glob.glob(os.path.join(ROOT, d, "*.hdf5"))):
            ev = event_name(fp)
            try:
                with h5py.File(fp, "r") as h:
                    groups = [g for g in h.keys()
                              if isinstance(h[g], h5py.Group) and "posterior_samples" in h[g]]
                    if not groups:
                        continue
                    g = next((p for p in PREFERRED[lab] if p in groups),
                             max(groups, key=lambda x: len(h[x]["posterior_samples"])))
                    ds = h[g]["posterior_samples"]
                    if not all(k in ds.dtype.names for k in SRC):
                        continue
                    cols = {k: np.asarray(ds[k], float) for k in SRC}
            except Exception:
                continue
            ok = np.ones(len(cols["mass_1_source"]), bool)
            for k in SRC:
                ok &= np.isfinite(cols[k])
            ok &= (cols["mass_ratio"] > 0.02) & (cols["mass_ratio"] <= 1.0)
            if ok.sum() < 400:
                continue
            out[(lab, ev)] = (cols["mass_1_source"][ok], cols["mass_2_source"][ok],
                              cols["mass_ratio"][ok], cols["chirp_mass_source"][ok])
    return out


def score(events, draw=None, rng=None):
    """Median elongated |dpsi| per catalog. draw=None uses the FULL samples."""
    per = {}
    for (lab, ev), (m1, m2, q, mcs) in events.items():
        if draw is not None:
            i = rng.integers(0, len(m1), min(draw, len(m1)))   # same scheme E94 uses
            m1, m2, q, mcs = m1[i], m2[i], q[i], mcs[i]
        psi, axr, _ = psi_axr_rho(m1, m2)
        if axr < AXR_MIN:
            continue
        per.setdefault(lab, []).append(abs(adiff(curve_psi(float(np.median(mcs)), q), psi)))
    return {k: {"n": len(v), "median": float(np.median(v))} for k, v in per.items()}


def main():
    ev = full_samples()
    print(f"read {len(ev)} events at full length")
    full = score(ev)
    out = {"battery": "E99 cache stability audit", "seed": SEED,
           "issue": ("E94 draws indices with replacement, so the cache is a BOOTSTRAP RESAMPLE of the "
                     "released samples, not a subsample. This audit quantifies the consequence."),
           "full_sample_reference": full, "by_seed": {}, "by_draw_size": {}}

    for s in SEEDS:
        out["by_seed"][str(s)] = score(ev, 4000, np.random.default_rng(s))
    for n in SIZES:
        out["by_draw_size"][str(n)] = score(ev, n, np.random.default_rng(94))

    summary = {}
    for cat in ("GWTC-3", "O4a", "O4b"):
        if cat not in full:
            continue
        vals = [out["by_seed"][str(s)][cat]["median"] for s in SEEDS if cat in out["by_seed"][str(s)]]
        summary[cat] = {
            "full_sample": full[cat]["median"], "n_elong_full": full[cat]["n"],
            "cache_seed_mean": float(np.mean(vals)), "cache_seed_sd": float(np.std(vals, ddof=1)),
            "cache_seed_min": float(np.min(vals)), "cache_seed_max": float(np.max(vals)),
            "abs_bias_vs_full": float(np.mean(vals) - full[cat]["median"])}
    out["summary"] = summary
    worst = max(abs(v["abs_bias_vs_full"]) for v in summary.values())
    spread = max(v["cache_seed_max"] - v["cache_seed_min"] for v in summary.values())
    out["verdict"] = {
        "max_abs_bias_deg": worst, "max_seed_spread_deg": spread,
        "fit_for_purpose": bool(worst < 0.35 and spread < 0.5),
        "statement": ("The cache is a bootstrap resample. Its headline score differs from the "
                      f"full-sample value by up to {worst:.2f} deg and moves by up to {spread:.2f} deg "
                      "across seeds. Any number quoted from the cache must be labelled as such, and the "
                      "LOCKED out-of-sample scores must continue to be quoted from the full-sample "
                      "E67/E71 artifacts, not from the cache.")}
    json.dump(out, open(RESULT_JSON, "w"), indent=1)

    print(f"\n{'catalog':>8} {'full':>7} {'cache mean':>11} {'sd':>6} {'range':>14} {'bias':>7}")
    for cat, v in summary.items():
        print(f"{cat:>8} {v['full_sample']:7.2f} {v['cache_seed_mean']:11.2f} {v['cache_seed_sd']:6.3f} "
              f"[{v['cache_seed_min']:.2f},{v['cache_seed_max']:.2f}] {v['abs_bias_vs_full']:+7.2f}")
    print("\nby draw size (seed 94):")
    for n, d in out["by_draw_size"].items():
        print(f"  n={n:>5}: " + "  ".join(f"{k} {d[k]['median']:.2f}" for k in sorted(d)))
    print(f"\nmax |bias| {worst:.2f} deg, max seed spread {spread:.2f} deg -> "
          f"fit for purpose: {out['verdict']['fit_for_purpose']}")
    print("wrote", RESULT_JSON)


if __name__ == "__main__":
    main()
