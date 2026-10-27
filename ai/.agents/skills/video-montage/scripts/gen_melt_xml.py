#!/usr/bin/env python3
"""Génère timeline_opt3.xml : timeline MLT 1280x720@30fps, un seul rendu continu.
Coupes en frames de profil (30 fps), fades vidéo=brightness / audio=volume.

⚠️ RÉFÉRENCE SEULEMENT (retesté melt 7.28.0) : ce XML écrit à la main rend
0,04 s au lieu de 3 s (in/out cassés) → préférer melt CLI (build_opt3_cli.sh)
ou générer le XML via `melt … in=X out=Y -consumer xml` + absolutiser resource."""
from pathlib import Path

BASE = Path.home() / "Documents/research/text-game-agents/experiment/trailer_build"
RAW = BASE / "raw"
SEGS = BASE / "segs"  # cartons pré-rendus par build2.sh (pas de souci de sync : synthétiques)

# (id, resource, in_frame, out_frame_inclusif, fadein_frames, fadeout_frames)
CLIPS = [
    ("p01", RAW / "c01_cold.webm",      150, 593, 15, 8),   # cold open 5.0->19.8s
    ("p02", SEGS / "02_title.mp4",        0,  89,  0,  0),
    ("p03", RAW / "c03_musique.webm",   120, 374,  4,  4),   # 4.0s, 8.5s
    ("p04", RAW / "c04_fun.mkv",          0, 299,  4,  4),   # 0.0s, 10.0s
    ("p05", RAW / "c05_gag.webm",       135, 359,  4,  4),   # 4.5s, 7.5s
    ("p06", RAW / "c06_cylindre.webm",   75, 314,  4,  4),   # 2.5s, 8.0s
    ("p07", RAW / "test_twirl.mkv",      30, 353,  4,  4),   # 1.0s, 10.8s
    ("p08", RAW / "c08_number.mkv",      60, 224,  4,  4),   # 2.0s, 5.5s
    ("p09", RAW / "c09_bruno.mkv",       45, 254,  4,  4),   # 1.5s, 7.0s
    ("p10", RAW / "c10_promesse.webm",   24, 218,  4,  4),   # 0.8s, 6.5s
    ("p11", RAW / "c11_twist.mkv",      105, 284,  9,  4),   # 3.5s, 6.0s
    ("p12", RAW / "c12_graziella.mkv",  120, 314,  4,  4),   # 4.0s, 6.5s
    ("p13", RAW / "c13_chute3.webm",     78, 212,  4,  5),   # 2.6s, 4.5s (beat 1)
    ("p14", SEGS / "13b_flash.mp4",       0,  20,  0,  0),
    ("p15", RAW / "c13_chute3.webm",    436, 516,  4, 18),   # 14.533s, 2.7s (beat 2)
    ("p16", SEGS / "13d_black.mp4",       0,  29,  0,  0),
    ("p17", SEGS / "14_endcard.mp4",      0, 119,  0,  0),
]

producers, entries = [], []
total = 0
for pid, res, fin, fout, dfin, dfout in CLIPS:
    filt = []
    if dfin:
        filt.append(f'''    <filter id="{pid}_fin" in="{fin}" out="{fin+dfin-1}">
      <property name="mlt_service">brightness</property>
      <property name="start">0</property>
      <property name="end">1</property>
    </filter>
    <filter id="{pid}afin" in="{fin}" out="{fin+dfin-1}">
      <property name="mlt_service">volume</property>
      <property name="gain">0</property>
      <property name="end">1</property>
    </filter>''')
    if dfout:
        filt.append(f'''    <filter id="{pid}_fout" in="{fout-dfout+1}" out="{fout}">
      <property name="mlt_service">brightness</property>
      <property name="start">1</property>
      <property name="end">0</property>
    </filter>
    <filter id="{pid}afout" in="{fout-dfout+1}" out="{fout}">
      <property name="mlt_service">volume</property>
      <property name="gain">1</property>
      <property name="end">0</property>
    </filter>''')
    filters = "\n".join(filt)
    producers.append(f'''  <producer id="{pid}" in="{fin}" out="{fout}">
    <property name="resource">{res}</property>
    <property name="mlt_service">avformat</property>
    <property name="length">{fout - fin + 1}</property>
    <property name="in">{fin}</property>
    <property name="out">{fout}</property>
{filters}
  </producer>''')
    entries.append(f'    <entry producer="{pid}" in="{fin}" out="{fout}"/>')
    total += fout - fin + 1

xml = f'''<?xml version="1.0" standalone="no"?>
<mlt LC_NUMERIC="C" version="7.0" title="night game opt3" producer="tractor0">
  <profile description="nightgame 720p30" width="1280" height="720" progressive="1"
    sample_aspect_num="1" sample_aspect_den="1"
    display_aspect_num="16" display_aspect_den="9"
    frame_rate_num="30" frame_rate_den="1" colorspace="709"/>
{chr(10).join(producers)}
  <playlist id="pl0">
{chr(10).join(entries)}
  </playlist>
  <tractor id="tractor0" global_feed="1" in="0" out="{total-1}">
    <track producer="pl0"/>
  </tractor>
</mlt>
'''
(BASE / "timeline_opt3.xml").write_text(xml)
print(f"timeline_opt3.xml écrit : {len(CLIPS)} clips, {total} frames = {total/30:.2f} s")
