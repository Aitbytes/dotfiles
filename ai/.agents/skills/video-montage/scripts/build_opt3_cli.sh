#!/usr/bin/env bash
# Build OPT3 — melt/MLT par CLI : producteurs coupés (in/out), filtres de fade
# attachés par -attach-cut avec numérotation relative à chaque coupe.
set -euo pipefail
# Dossier projet contenant raw/ et segs/ : cwd par défaut, ou passé en $1
B="${1:-$PWD}"
cd "$B"

gen() { # file in out finw foutw
  local f=$1 fin=$2 out=$3 finw=$4 foutw=$5
  printf ' "%s" in=%s out=%s' "$f" "$fin" "$out"
  local L=$((out-fin+1))
  if [ "$finw" -gt 0 ]; then
    printf ' -attach-cut brightness start=0 end=1 in=0 out=%d' $((finw-1))
    printf ' -attach-cut volume gain=0 end=1 in=0 out=%d' $((finw-1))
  fi
  if [ "$foutw" -gt 0 ]; then
    printf ' -attach-cut brightness start=1 end=0 in=%d out=%d' $((L-foutw)) $((L-1))
    printf ' -attach-cut volume gain=1 end=0 in=%d out=%d' $((L-foutw)) $((L-1))
  fi
}

ARGS=""
ARGS+="$(gen "$B/raw/c01_cold.webm"      150 593 15 8)"
ARGS+="$(gen "$B/segs/02_title.mp4"        0  89  0 0)"
ARGS+="$(gen "$B/raw/c03_musique.webm"   120 374  4 4)"
ARGS+="$(gen "$B/raw/c04_fun.mkv"          0 299  4 4)"
ARGS+="$(gen "$B/raw/c05_gag.webm"       135 359  4 4)"
ARGS+="$(gen "$B/raw/c06_cylindre.webm"   75 314  4 4)"
ARGS+="$(gen "$B/raw/test_twirl.mkv"      30 353  4 4)"
ARGS+="$(gen "$B/raw/c08_number.mkv"      60 224  4 4)"
ARGS+="$(gen "$B/raw/c09_bruno.mkv"       45 254  4 4)"
ARGS+="$(gen "$B/raw/c10_promesse.webm"   24 218  4 4)"
ARGS+="$(gen "$B/raw/c11_twist.mkv"      105 284  9 4)"
ARGS+="$(gen "$B/raw/c12_graziella.mkv"  120 314  4 4)"
ARGS+="$(gen "$B/raw/c13_chute3.webm"     78 212  4 5)"
ARGS+="$(gen "$B/segs/13b_flash.mp4"       0  20  0 0)"
ARGS+="$(gen "$B/raw/c13_chute3.webm"    436 516  4 18)"
ARGS+="$(gen "$B/segs/13d_black.mp4"       0  29  0 0)"
ARGS+="$(gen "$B/segs/14_endcard.mp4"      0 119  0 0)"

export HTTP_PROXY= HTTPS_PROXY=
# shellcheck disable=SC2086
nix-shell -p mlt --run "melt -profile atsc_720p_30 $ARGS \
  -consumer avformat:$B/night-game-trailer-opt3.mp4 vcodec=libx264 crf=20 preset=medium \
  pix_fmt=yuv420p acodec=aac ab=160k ar=48000 ac=2 movflags=+faststart progress=1" 2>&1 | tail -3

echo "=== OPT3 FINAL (attendu 3210 frames = 107.00 s) ==="
ffprobe -v error -select_streams v:0 -count_frames -show_entries stream=nb_read_frames -of csv=p=0 night-game-trailer-opt3.mp4
ffprobe -v error -show_entries format=duration,size -of default=noprint_wrappers=1 night-game-trailer-opt3.mp4
