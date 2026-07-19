#!/usr/bin/env python3
"""Fetch the GWTC-4.0 (O4a) per-event PE HDF5 files into data/chains/gwtc4/ (for E79 cross-catalog).
Public LVK data: Zenodo 16053484. Same discipline as fetch_gwtc5.py (<=6 workers, h5py-verify, no resume,
name normalized to <EVENT>-combined_PEDataRelease.hdf5 so the E71/E78 glob GW*.hdf5 matches)."""
import os, re, json, subprocess, urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
import h5py

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEST = os.path.join(ROOT, "data/chains/gwtc4"); os.makedirs(DEST, exist_ok=True)
RECORD = "16053484"
IGWN = re.compile(r"^IGWN-GWTC4p0-[^-]+-")

def gj(u):
    with urllib.request.urlopen(u, timeout=120) as r: return json.load(r)

def valid_h5(p):
    try:
        with h5py.File(p, "r") as h:
            f = []; h.visititems(lambda n, o: f.append(n) if isinstance(o, h5py.Dataset) and n.endswith("posterior_samples") else None)
            return bool(f)
    except Exception: return False

rec = gj(f"https://zenodo.org/api/records/{RECORD}")
print(f"record {RECORD}: {rec['metadata']['title']}", flush=True)
jobs = []
for f in rec.get("files", []):
    k = f.get("key", "")
    if k.endswith("combined_PEDataRelease.hdf5"):
        jobs.append((IGWN.sub("", k), f["links"]["self"]))
print(f"{len(jobs)} event PE files", flush=True)

def already(dst):
    p = os.path.join(DEST, dst); return os.path.exists(p) and os.path.getsize(p) > 1_000_000 and valid_h5(p)
todo = [(d, u) for d, u in jobs if not already(d)]
print(f"cached: {len(jobs)-len(todo)} | to download: {len(todo)}", flush=True)

def dl(dst, url):
    p = os.path.join(DEST, dst); tmp = p + ".part"; last = "?"
    for _ in range(3):
        try:
            if os.path.exists(tmp): os.remove(tmp)
            subprocess.run(["curl", "-sL", "--retry", "8", "--retry-delay", "5", "--speed-limit", "50000",
                            "--speed-time", "45", "-o", tmp, url], check=True, timeout=7200)
            if os.path.getsize(tmp) < 1_000_000: raise ValueError("too small")
            if not valid_h5(tmp): raise ValueError("corrupt HDF5")
            os.replace(tmp, p); return (dst, os.path.getsize(p), None)
        except Exception as e:
            if os.path.exists(tmp): os.remove(tmp)
            last = str(e)[:80]
    return (dst, 0, last)

done = 0; failed = []
with ThreadPoolExecutor(max_workers=6) as ex:
    futs = {ex.submit(dl, d, u): d for d, u in todo}
    for fut in as_completed(futs):
        d, sz, err = fut.result(); done += 1
        print(f"  [{done}/{len(todo)}] {'FAIL '+d+': '+err if err else 'ok '+d+f' ({sz/1e6:.0f}MB)'}", flush=True)
        if err: failed.append((d, u := None))
if failed:
    print(f"re-fetching {len(failed)} stragglers...", flush=True)
    byname = {d: u for d, u in todo}
    for d, _ in list(failed):
        d2, sz, err = dl(d, byname[d])
        print(f"  {'STILL FAIL '+d2+': '+err if err else 'recovered '+d2}", flush=True)
n = len([f for f in os.listdir(DEST) if f.endswith("combined_PEDataRelease.hdf5")])
tot = sum(os.path.getsize(os.path.join(DEST, f)) for f in os.listdir(DEST) if f.endswith(".hdf5"))
print(f"\nDONE. {n} event files, {tot/1e9:.2f} GB.", flush=True)
