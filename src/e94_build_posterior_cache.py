#!/usr/bin/env python3
"""E94 - one-time posterior cache, so every submission gate becomes reproducible in seconds.

WHY THIS EXISTS. The Gate A-E measurements were first run from throwaway scripts and committed as prose
only; a referee (and we) could not re-derive them. The reproducible package (E91-E93) then fell back to
re-serializing the committed E65/E67/E71 result JSONs, because a full HDF5 sweep is slow: a single pass
over all 266 events takes ~276 s wall (O4b alone ~205 s), and the multi-group / multi-frame sweeps the
gates need are several times that. HDF5 is NOT broken -- measured 266/266 opens with 0 failures -- it is
just too slow to sit inside an interactive analysis loop.

So: pay the cost ONCE. This extracts every quantity the gates need, for EVERY waveform group in every
file (not only the preferred group), in both source and detector frames, and writes a single .npz.
Downstream gates then run from the cache with no HDF5 access at all.

Cached per (catalog, event, group): subsampled aligned arrays m1/m2/q (source and detector frame),
median chirp masses, and network optimal SNR where available. Samples are ALIGNED sample-by-sample so
that bootstraps can resample the measured axis and the curve inputs jointly (the committed
`load_event` does not align q with the finite-mass mask -- that mismatch is a real trap).

Seed 94, but as of the no-subsampling change the seed is unused on the default path: the cache keeps
EVERY usable sample, so it is a deterministic, exact mirror of the released posteriors and carries no
resampling noise of its own.
"""
import os, sys, glob, json, time
import numpy as np
import h5py

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

CATALOGS = (("GWTC-3", "data/chains/gw_posteriors"),
            ("O4a", "data/chains/gwtc4"),
            ("O4b", "data/chains/gwtc5"))
CACHE = os.path.join(ROOT, "results/e94_posterior_cache.npz")
MANIFEST = os.path.join(ROOT, "results/e94_posterior_cache_manifest.json")
# N_SAMP = None means NO SUBSAMPLING: every usable sample is cached, so the cache is an exact mirror
# of the released posteriors and cache-backed numbers ARE full-sample numbers.
#
# It used to be 4000 drawn WITH REPLACEMENT, which was wrong twice over. (1) The median posterior has
# ~16.7k usable samples, so we discarded ~76% of the information. (2) Because the draw was
# `min(n_samp, len(idx))` indices sampled with replacement, even a cap ABOVE the sample count still
# bootstrapped -- the cache never used the full sample at any size, and the resampling noise therefore
# did not decay as the cap grew. E99 measured the consequence: unbiased to 0.06 deg but scattering up
# to 0.54 deg across seeds, and O4a reading 1.08 / 1.33 / 1.38 at caps of 2000 / 4000 / 8000, which is
# not a converging sequence. That instability sat underneath every downstream battery and figure.
#
# Storing everything costs ~650 MB (the sample-count distribution is bounded: 23.1M rows in total), which
# is barely more than a 100k cap would cost, so there is no reason to subsample at all. If a small cache
# is ever wanted, set N_SAMP to an int -- it now subsamples WITHOUT replacement, so a cap at or above an
# event's sample count keeps that event exactly.
N_SAMP = None
SEED = 94
SRC = ("mass_1_source", "mass_2_source", "mass_ratio", "chirp_mass_source")
DET = ("mass_1", "mass_2", "chirp_mass")


def event_name(fp):
    b = os.path.basename(fp)
    return (b.split("-")[0].replace("_PE.h5", "").replace(".h5", "").replace(".hdf5", "")
            .split("_PEDataRelease")[0])


def build(n_samp=N_SAMP, seed=SEED):
    rng = np.random.default_rng(seed)
    out, manifest = {}, {"n_events": 0, "n_group_rows": 0, "catalogs": {},
                         "n_samp": n_samp, "seed": seed, "skipped": {},
                         "subsampling": ("NONE -- every usable sample cached; cache-backed numbers are "
                                         "full-sample numbers" if n_samp is None else
                                         f"without replacement, cap {n_samp}"),
                         "rows_stored_exactly": 0, "samples_stored": 0}
    for lab, d in CATALOGS:
        files = sorted(glob.glob(os.path.join(ROOT, d, "*.h5"))
                       + glob.glob(os.path.join(ROOT, d, "*.hdf5")))
        t0, nrow, nev = time.time(), 0, 0
        for fp in files:
            ev = event_name(fp)
            got_any = False
            try:
                with h5py.File(fp, "r") as h:
                    for g in h.keys():
                        if not isinstance(h[g], h5py.Group) or "posterior_samples" not in h[g]:
                            continue
                        ds = h[g]["posterior_samples"]
                        nm = ds.dtype.names
                        if not all(k in nm for k in SRC):
                            continue
                        cols = {k: np.asarray(ds[k], float) for k in SRC}
                        has_det = all(k in nm for k in DET)
                        if has_det:
                            cols.update({k: np.asarray(ds[k], float) for k in DET})
                        snrc = [c for c in nm if c.endswith("_optimal_snr")]
                        snr = (np.sqrt(sum(np.asarray(ds[c], float) ** 2 for c in snrc))
                               if snrc else None)

                        ok = np.ones(len(cols["mass_1_source"]), bool)
                        for k in SRC:
                            ok &= np.isfinite(cols[k])
                        ok &= (cols["mass_ratio"] > 0.02) & (cols["mass_ratio"] <= 1.0)
                        if has_det:
                            for k in DET:
                                ok &= np.isfinite(cols[k])
                        if snr is not None:
                            ok &= np.isfinite(snr)
                        if ok.sum() < 400:
                            continue
                        idx = np.where(ok)[0]
                        if n_samp is None or len(idx) <= n_samp:
                            take = idx                      # exact: every usable sample
                        else:
                            take = np.sort(rng.choice(idx, n_samp, replace=False))
                        key = f"{lab}|{ev}|{g}"
                        out[key + "|m1s"] = cols["mass_1_source"][take].astype(np.float32)
                        out[key + "|m2s"] = cols["mass_2_source"][take].astype(np.float32)
                        out[key + "|q"] = cols["mass_ratio"][take].astype(np.float32)
                        out[key + "|mcs"] = cols["chirp_mass_source"][take].astype(np.float32)
                        if has_det:
                            out[key + "|m1d"] = cols["mass_1"][take].astype(np.float32)
                            out[key + "|m2d"] = cols["mass_2"][take].astype(np.float32)
                            out[key + "|mcd"] = cols["chirp_mass"][take].astype(np.float32)
                        if snr is not None:
                            out[key + "|snr"] = snr[take].astype(np.float32)
                        out[key + "|n_total"] = np.array([int(ok.sum())])
                        manifest["samples_stored"] += int(len(take))
                        manifest["rows_stored_exactly"] += int(len(take) == int(ok.sum()))
                        nrow += 1
                        got_any = True
            except Exception as e:
                manifest["skipped"].setdefault(lab, []).append(f"{ev}: {type(e).__name__}")
                continue
            if got_any:
                nev += 1
        manifest["catalogs"][lab] = {"files": len(files), "events_cached": nev,
                                     "group_rows": nrow, "seconds": round(time.time() - t0, 1)}
        manifest["n_events"] += nev
        manifest["n_group_rows"] += nrow
        print(f"  {lab}: {nev} events, {nrow} group rows, {time.time()-t0:.1f}s")
    np.savez_compressed(CACHE, **out)
    json.dump(manifest, open(MANIFEST, "w"), indent=1)
    print(f"\nwrote {CACHE} ({os.path.getsize(CACHE)/1e6:.1f} MB)")
    print(f"wrote {MANIFEST}")
    return manifest


def load(cache=CACHE):
    """Return {(catalog, event, group): dict of arrays}. No HDF5 access."""
    z = np.load(cache)
    rec = {}
    for k in z.files:
        cat, ev, grp, field = k.split("|")
        rec.setdefault((cat, ev, grp), {})[field] = z[k]
    return rec


if __name__ == "__main__":
    build()
