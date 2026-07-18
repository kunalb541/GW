#!/usr/bin/env python3
"""Fetch all confident GWTC PE posterior HDF5 files into data/chains/gw_posteriors/.
Skip-if-exists; saves as <commonName>_PE.h5 to match E38's glob. Public GWOSC/Zenodo data."""
import json, os, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEST = os.path.join(ROOT, "data/chains/gw_posteriors")
os.makedirs(DEST, exist_ok=True)
CATALOGS = ["GWTC-1-confident", "GWTC-2.1-confident", "GWTC-3-confident"]

def gj(u):
    with urllib.request.urlopen(u, timeout=90) as r:
        return json.load(r)

def pe_url(ev):
    """preferred PE combined data_url (.h5) for an event detail."""
    params = ev.get("parameters", {}) or {}
    cands = []
    for name, v in params.items():
        du = v.get("data_url")
        if not du or not du.endswith((".h5", ".h5/content")): continue
        # PE releases have mass params on the entry and/or pipeline_type 'pe'
        is_pe = (v.get("pipeline_type") == "pe") or ("mass_1_source" in v) or ("PEDataRelease" in du)
        if not is_pe: continue
        cands.append((bool(v.get("is_preferred")), int(v.get("date_added_ts", 0) or 0), du))
    if not cands: return None
    cands.sort(key=lambda t: (t[0], t[2]))   # preferred last; deterministic by url
    pref = [c for c in cands if c[0]]
    return (pref[-1] if pref else cands[-1])[2]

print("gathering PE URLs from confident catalogs...", flush=True)
jobs = {}
for c in CATALOGS:
    events = gj(f"https://gwosc.org/eventapi/json/{c}/")["events"]
    for k, meta in events.items():
        cn = meta.get("commonName")
        if cn and cn not in jobs: jobs[cn] = meta["jsonurl"]
print(f"{len(jobs)} unique events; resolving PE URLs in parallel...", flush=True)

def resolve(cn, jurl):
    try:
        det = gj(jurl)
        ev = det["events"][list(det["events"])[0]]
        return cn, pe_url(ev)
    except Exception as e:
        return cn, None

urls = {}
with ThreadPoolExecutor(max_workers=12) as ex:
    for cn, u in ex.map(lambda kv: resolve(*kv), jobs.items()):
        if u: urls[cn] = u
print(f"resolved {len(urls)} PE URLs", flush=True)

def existing(cn):
    # match E38 glob: any file starting with the common name and ending _PE.h5
    for f in os.listdir(DEST):
        if f.endswith("_PE.h5") and f.startswith(cn.split('_')[0]) and cn.split('GW')[-1][:6] in f:
            return f
    p = os.path.join(DEST, f"{cn}_PE.h5")
    return os.path.basename(p) if os.path.exists(p) else None

todo = {cn: u for cn, u in urls.items() if not existing(cn)}
print(f"already cached: {len(urls)-len(todo)} | to download: {len(todo)}")

import subprocess
import h5py
def valid_h5(path):
    try:
        with h5py.File(path, "r") as h:
            found = []
            h.visititems(lambda n, o: found.append(n) if isinstance(o, h5py.Dataset)
                         and n.endswith("posterior_samples") else None)
            return bool(found)
    except Exception:
        return False

def dl(cn, u):
    dest = os.path.join(DEST, f"{cn}_PE.h5")
    tmp = dest + ".part"
    for attempt in range(2):
        try:
            # FRESH download each time (no -C - resume: resuming across Zenodo restarts corrupts
            # the HDF5). --speed-limit drops stalled connections so --retry reconnects.
            if os.path.exists(tmp): os.remove(tmp)
            subprocess.run(["curl", "-sL", "--retry", "8", "--retry-delay", "5",
                            "--speed-limit", "50000", "--speed-time", "45",
                            "-o", tmp, u], check=True, timeout=3600)
            if os.path.getsize(tmp) < 1_000_000:
                raise ValueError(f"too small ({os.path.getsize(tmp)}B)")
            if not valid_h5(tmp):
                raise ValueError("corrupt HDF5")
            os.replace(tmp, dest)
            return (cn, os.path.getsize(dest), None)
        except Exception as e:
            if os.path.exists(tmp): os.remove(tmp)
            last = str(e)[:80]
    return (cn, 0, last)

done = 0; failed = []
with ThreadPoolExecutor(max_workers=6) as ex:
    futs = {ex.submit(dl, cn, u): cn for cn, u in todo.items()}
    for fut in as_completed(futs):
        cn, sz, err = fut.result()
        done += 1
        if err: failed.append((cn, err)); print(f"  [{done}/{len(todo)}] FAIL {cn}: {err}")
        else: print(f"  [{done}/{len(todo)}] ok {cn} ({sz/1e6:.0f}MB)")

total = sum(os.path.getsize(os.path.join(DEST, f)) for f in os.listdir(DEST) if f.endswith("_PE.h5"))
n = len([f for f in os.listdir(DEST) if f.endswith("_PE.h5")])
print(f"\nDONE. cache now {n} files, {total/1e9:.2f} GB. failures: {len(failed)}")
for cn, err in failed: print("  fail:", cn, err)
