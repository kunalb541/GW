#!/bin/bash
# Parallel byte-range download of the GWTC-3 TGR IMR-consistency zip (Zenodo throttles single
# connections; 8 ranged chunks beat it). Then concatenate + verify size.
set -e
URL="https://zenodo.org/api/records/17461225/files/IGWN-GWTC3-TGR-v1-imr.zip/content"
DEST="data/chains/tgr"
mkdir -p "$DEST"
OUT="$DEST/IGWN-GWTC3-TGR-v1-imr.zip"
SIZE=4120399443
N=8
CHUNK=$(( (SIZE + N - 1) / N ))
echo "downloading $SIZE bytes in $N chunks of ~$CHUNK ..."
pids=()
for i in $(seq 0 $((N-1))); do
  start=$(( i * CHUNK ))
  end=$(( start + CHUNK - 1 ))
  [ $end -ge $SIZE ] && end=$(( SIZE - 1 ))
  curl -sL --retry 8 --retry-delay 5 --speed-limit 30000 --speed-time 60 \
       -r ${start}-${end} "$URL" -o "$DEST/part_$i" &
  pids+=($!)
done
for p in "${pids[@]}"; do wait "$p"; done
echo "chunks done; concatenating..."
cat "$DEST"/part_* > "$OUT"
rm -f "$DEST"/part_*
GOT=$(stat -f%z "$OUT" 2>/dev/null || stat -c%s "$OUT")
echo "downloaded size: $GOT (expected $SIZE)"
if [ "$GOT" = "$SIZE" ]; then echo "SIZE OK"; else echo "SIZE MISMATCH"; fi
