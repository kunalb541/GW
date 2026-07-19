#!/usr/bin/env python3
"""Fetch the GWTC-5.0 (O4b) per-event PE posterior HDF5 files into data/chains/gwtc5/.
Public LVK data: Zenodo 20276106 (Part 1) + 20348006 (Part 2).
Discipline (docs/WORKFLOW.md): <=6 parallel workers, verify every HDF5 with h5py, no `curl -C -`
resume (corrupts across Zenodo restarts), re-fetch stragglers. Skip-if-exists+valid.
Normalizes the IGWN-GWTC5p0-<hash>_25-<EVENT>-combined_PEDataRelease.hdf5 name down to
<EVENT>-combined_PEDataRelease.hdf5 so the E71 glob (GW*.hdf5) matches, mirroring E67's gwtc4 layout."""
import os, re, sys, json, subprocess, urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
import h5py

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEST = os.path.join(ROOT, "data/chains/gwtc5")
os.makedirs(DEST, exist_ok=True)
RECORDS = {"20276106": "part1", "20348006": "part2"}
IGWN_PREFIX = re.compile(r"^IGWN-GWTC5p0-[^-]+-")   # strip 'IGWN-GWTC5p0-<hash>_25-'

def gj(u):
    with urllib.request.urlopen(u, timeout=120) as r:
        return json.load(r)

def valid_h5(path):
    try:
        with h5py.File(path, "r") as h:
            found = []
            h.visititems(lambda n, o: found.append(n) if isinstance(o, h5py.Dataset)
                         and n.endswith("posterior_samples") else None)
            return bool(found)
    except Exception:
        return False

def dest_name(key, part):
    if "PESummaryTable" in key:
        return f"PESummaryTable_{part}.hdf5"      # keep both parts' summary tables, distinct
    return IGWN_PREFIX.sub("", key)               # -> GW<date>_<time>-combined_PEDataRelease.hdf5

# gather download jobs from both records
jobs = []   # (dest_filename, url, size)
for rid, part in RECORDS.items():
    rec = gj(f"https://zenodo.org/api/records/{rid}")
    print(f"record {rid} ({part}): {rec['metadata']['title']}", flush=True)
    for f in rec.get("files", []):
        key = f.get("key", "")
        if not key.endswith(".hdf5"):
            continue
        if not (key.endswith("combined_PEDataRelease.hdf5") or "PESummaryTable" in key):
            continue
        url = f["links"]["self"]
        jobs.append((dest_name(key, part), url, f.get("size", 0)))
n_event = sum(1 for d, _, _ in jobs if d.endswith("combined_PEDataRelease.hdf5"))
tot = sum(s for _, _, s in jobs)
print(f"{len(jobs)} files to consider ({n_event} event PE files), {tot/1e9:.1f} GB total", flush=True)

def already(dst):
    p = os.path.join(DEST, dst)
    return os.path.exists(p) and os.path.getsize(p) > 1_000_000 and valid_h5(p)

todo = [(d, u, s) for d, u, s in jobs if not already(d)]
print(f"already cached+valid: {len(jobs)-len(todo)} | to download: {len(todo)} "
      f"({sum(s for _,_,s in todo)/1e9:.1f} GB)", flush=True)

def dl(dst, url, size):
    p = os.path.join(DEST, dst); tmp = p + ".part"
    last = "?"
    for attempt in range(3):
        try:
            if os.path.exists(tmp): os.remove(tmp)
            subprocess.run(["curl", "-sL", "--retry", "8", "--retry-delay", "5",
                            "--speed-limit", "50000", "--speed-time", "45",
                            "-o", tmp, url], check=True, timeout=7200)
            if os.path.getsize(tmp) < 1_000_000:
                raise ValueError(f"too small ({os.path.getsize(tmp)}B)")
            if not valid_h5(tmp):
                raise ValueError("corrupt HDF5 (no posterior_samples)")
            os.replace(tmp, p)
            return (dst, os.path.getsize(p), None)
        except Exception as e:
            if os.path.exists(tmp): os.remove(tmp)
            last = str(e)[:90]
    return (dst, 0, last)

done = 0; failed = []
with ThreadPoolExecutor(max_workers=6) as ex:
    futs = {ex.submit(dl, d, u, s): d for d, u, s in todo}
    for fut in as_completed(futs):
        dst, sz, err = fut.result(); done += 1
        if err: failed.append((dst, err)); print(f"  [{done}/{len(todo)}] FAIL {dst}: {err}", flush=True)
        else:   print(f"  [{done}/{len(todo)}] ok {dst} ({sz/1e6:.0f}MB)", flush=True)

# sequential re-fetch of stragglers (Zenodo throttling class)
if failed:
    print(f"\nre-fetching {len(failed)} stragglers sequentially...", flush=True)
    still = []
    byname = {d: (u, s) for d, u, s in todo}
    for dst, _ in failed:
        u, s = byname[dst]
        d2, sz, err = dl(dst, u, s)
        if err: still.append((d2, err)); print(f"  STILL FAIL {d2}: {err}", flush=True)
        else:   print(f"  recovered {d2} ({sz/1e6:.0f}MB)", flush=True)
    failed = still

evs = [f for f in os.listdir(DEST) if f.endswith("combined_PEDataRelease.hdf5")]
total = sum(os.path.getsize(os.path.join(DEST, f)) for f in os.listdir(DEST) if f.endswith(".hdf5"))
print(f"\nDONE. {len(evs)} event PE files, {total/1e9:.2f} GB on disk. failures: {len(failed)}", flush=True)
for d, err in failed: print("  fail:", d, err)
