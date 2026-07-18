#!/bin/bash
# Parallel byte-range download of the GWTC-3 TGR parameterized-deviation zip.
set -e
URL="https://zenodo.org/api/records/17461225/files/IGWN-GWTC3-TGR-v1-par.zip/content"
DEST="data/chains/tgr"; mkdir -p "$DEST"
OUT="$DEST/IGWN-GWTC3-TGR-v1-par.zip"
SIZE=2523809848
N=8; CHUNK=$(( (SIZE + N - 1) / N ))
echo "downloading $SIZE bytes in $N chunks..."
pids=()
for i in $(seq 0 $((N-1))); do
  start=$(( i * CHUNK )); end=$(( start + CHUNK - 1 )); [ $end -ge $SIZE ] && end=$(( SIZE - 1 ))
  curl -sL --retry 8 --retry-delay 5 --speed-limit 30000 --speed-time 60 \
       -r ${start}-${end} "$URL" -o "$DEST/ppart_$i" & pids+=($!)
done
for p in "${pids[@]}"; do wait "$p"; done
echo "concatenating..."; cat "$DEST"/ppart_* > "$OUT"; rm -f "$DEST"/ppart_*
GOT=$(stat -f%z "$OUT" 2>/dev/null || stat -c%s "$OUT")
echo "downloaded $GOT (expected $SIZE)"; [ "$GOT" = "$SIZE" ] && echo "SIZE OK" || echo "SIZE MISMATCH"
