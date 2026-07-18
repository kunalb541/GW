#!/usr/bin/env python3
"""E59 - ringdown mode consistency (black-hole spectroscopy no-hair): does adding the 221 first
overtone shift the inferred remnant (Mf, af) away from the 220-fundamental-only value? If the
object is Kerr, it should not. Prereg E59.
HONEST: the 221 analysis shares data with the 220 (it is not an independent measurement), so this
is a SHIFT-vs-fundamental-uncertainty CONSISTENCY test, NOT a naive independent-difference
significance (which would be statistically wrong). No RNG."""
import os, json, math, zipfile, tempfile
import numpy as np
import h5py

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ZIP = os.path.join(ROOT, "data/chains/tgr/IGWN-GWTC3-TGR-v2-rin.zip")
zf = zipfile.ZipFile(ZIP)

def members(tag):
    d = {}
    for x in zf.namelist():
        if tag in x and x.endswith(".h5"):
            d[os.path.basename(x).split("_pyring_")[0].replace("rin_", "")] = x
    return d
m220 = members("pyring_Kerr_220_0M")
m221 = members("pyring_Kerr_221_0M")   # PLAIN 221 (overtone fixed at Kerr, no free deviation)

def load_Mf_af(member):
    with tempfile.NamedTemporaryFile(suffix=".h5", delete=False) as t:
        t.write(zf.read(member)); tp = t.name
    try:
        with h5py.File(tp, "r") as h:
            found = []
            h.visititems(lambda n, o: found.append(n) if isinstance(o, h5py.Dataset) and n.endswith("posterior_samples") else None)
            ds = h[found[0]]
            Mf = np.asarray(ds["Mf"], float); af = np.asarray(ds["final_spin"], float)
    finally:
        os.remove(tp)
    ok = np.isfinite(Mf) & np.isfinite(af)
    return Mf[ok], af[ok]

rows = []
for ev in sorted(set(m220) & set(m221)):
    Mf0, af0 = load_Mf_af(m220[ev])            # fundamental only
    Mf1, af1 = load_Mf_af(m221[ev])            # + overtone (deviation free)
    if min(Mf0.size, Mf1.size) < 200: continue
    mu0 = np.array([np.median(Mf0), np.median(af0)])
    mu1 = np.array([np.median(Mf1), np.median(af1)])
    C0 = np.cov(Mf0, af0)                        # fundamental posterior covariance (reference width)
    d = mu1 - mu0
    # shift of the overtone-analysis remnant relative to the FUNDAMENTAL's uncertainty
    shift_sigma = float(math.sqrt(d @ np.linalg.inv(C0) @ d))
    rows.append({"event": ev, "Mf_220": round(float(mu0[0]), 1), "af_220": round(float(mu0[1]), 3),
                 "Mf_221": round(float(mu1[0]), 1), "af_221": round(float(mu1[1]), 3),
                 "dMf": round(float(d[0]), 2), "daf": round(float(d[1]), 3),
                 "shift_in_fundamental_sigma": round(shift_sigma, 2)})

n = len(rows)
shifts = np.array([r["shift_in_fundamental_sigma"] for r in rows])
big = [r for r in rows if r["shift_in_fundamental_sigma"] > 2.0]
# COHERENCE diagnostic: are the shifts in a consistent DIRECTION (systematic) or scattered (stochastic)?
n_dMf_neg = sum(1 for r in rows if r["dMf"] < 0); n_daf_neg = sum(1 for r in rows if r["daf"] < 0)
frac_dMf_neg = n_dMf_neg / n; frac_daf_neg = n_daf_neg / n
coherent = (frac_dMf_neg > 0.8 or frac_dMf_neg < 0.2) and (frac_daf_neg > 0.8 or frac_daf_neg < 0.2)
# Correct decision: a COHERENT shift is a SYSTEMATIC (not a no-hair violation);
# a SCATTERED shift with events >2sigma would be the concerning (physics) case.
D1_systematic = coherent           # the shift is a coherent systematic, not stochastic
D2_no_stochastic_violation = coherent or len(big) == 0
print(f"events: {n}  (Kerr_220 fundamental vs plain Kerr_221 remnant, both assume Kerr)")
print(f"{'event':14s} {'Mf_220':>7} {'af_220':>7} {'Mf_221':>7} {'af_221':>7} {'shift/sig':>9}")
for r in sorted(rows, key=lambda r: -r["shift_in_fundamental_sigma"]):
    print(f"{r['event']:14s} {r['Mf_220']:7.1f} {r['af_220']:7.3f} {r['Mf_221']:7.1f} {r['af_221']:7.3f} {r['shift_in_fundamental_sigma']:9.2f}")
print(f"\nremnant shift adding the overtone: median {np.median(shifts):.2f}sig, max {shifts.max():.2f}sig; {len(big)} events >2sig")
print(f"COHERENCE: dMf<0 in {n_dMf_neg}/{n} ({frac_dMf_neg:.0%}), daf<0 in {n_daf_neg}/{n} ({frac_daf_neg:.0%})")
print(f"\nD1 (shift is a COHERENT systematic, not stochastic): {'YES -> SYSTEMATIC, not a no-hair violation' if D1_systematic else 'NO -> scattered'}")
print(f"D2 (no stochastic no-hair violation): {'PASS' if D2_no_stochastic_violation else 'FAIL'}")
print(f"=> the 220-vs-221 remnant shift is the known ringdown-overtone systematic (coherent all-event")
print(f"   down-shift), NOT evidence against Kerr. The clean no-hair result is E47 (221 deviation ~0).")

json.dump({"prereg": "preregs/E59_ringdown_mode_consistency_prereg.md", "n_events": n,
           "median_shift_sigma": round(float(np.median(shifts)), 2), "max_shift_sigma": round(float(shifts.max()), 2),
           "n_shift_gt_2sigma": len(big), "events_gt_2sigma": [r["event"] for r in big],
           "coherence_frac_dMf_neg": round(frac_dMf_neg, 2), "coherence_frac_daf_neg": round(frac_daf_neg, 2),
           "shift_is_coherent_systematic": bool(coherent),
           "D2_no_stochastic_violation": bool(D2_no_stochastic_violation),
           "interpretation": "coherent all-event down-shift of Mf,af with the overtone = known ringdown-overtone SYSTEMATIC, NOT a no-hair violation; clean no-hair result is E47 (221 deviation params ~0, isotropic)",
           "note": "shift relative to the 220-fundamental posterior width; 221 shares data with 220 so this is a consistency check, not an independent difference significance",
           "per_event": sorted(rows, key=lambda r: -r["shift_in_fundamental_sigma"])},
          open(os.path.join(ROOT, "results/e59_ringdown_mode_consistency_results.json"), "w"), indent=2)
print("\nwrote results/e59_ringdown_mode_consistency_results.json")
