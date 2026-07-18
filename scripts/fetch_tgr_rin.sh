#!/bin/bash
set -e
URL="https://zenodo.org/api/records/17461225/files/IGWN-GWTC3-TGR-v2-rin.zip/content"
DEST="data/chains/tgr"; mkdir -p "$DEST"
OUT="$DEST/IGWN-GWTC3-TGR-v2-rin.zip"
SIZE=2210047740
N=8; CHUNK=$(( (SIZE + N - 1) / N ))
echo "downloading $SIZE in $N chunks..."
pids=()
for i in $(seq 0 $((N-1))); do
  start=$(( i * CHUNK )); end=$(( start + CHUNK - 1 )); [ $end -ge $SIZE ] && end=$(( SIZE - 1 ))
  curl -sL --retry 8 --retry-delay 5 --speed-limit 30000 --speed-time 60 -r ${start}-${end} "$URL" -o "$DEST/rpart_$i" & pids+=($!)
done
for p in "${pids[@]}"; do wait "$p"; done
echo "concatenating..."; cat "$DEST"/rpart_* > "$OUT"; rm -f "$DEST"/rpart_*
GOT=$(stat -f%z "$OUT" 2>/dev/null || stat -c%s "$OUT")
echo "downloaded $GOT (expected $SIZE)"; [ "$GOT" = "$SIZE" ] && echo "SIZE OK" || echo "SIZE MISMATCH"
