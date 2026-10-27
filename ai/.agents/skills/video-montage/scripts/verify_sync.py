#!/usr/bin/env python3
"""Vérifie la synchro A/V d'un montage en mesurant la position réelle des mots
(whisper) vs leur position théorique dans la timeline. Usage: verify_sync.py <file>"""
import subprocess, sys, tempfile, os, re, json

FILE = sys.argv[1]
# (motif, temps attendu, début fenêtre, durée fenêtre, langue)
# opt2 et opt3 ont la même structure ; seul "answer" diffère de 0.02s -> tolérance large
CK = [
    ("aucun",      5.76,  3.5, 5.0, "fr"),   # cold open, « Aucun. » isolé (2e occurrence)
    ("marrer",    35.10, 32.0, 6.0, "fr"),   # fin du beat fun
    ("toro",      61.16, 58.5, 6.0, "en"),   # twirl (whisper: "toro")
    ("call",      66.84, 64.5, 5.0, "en"),   # « because I'm going to call you »
    ("tradition", 69.25, 67.5, 4.5, "en"),   # bruno
    ("answer",   101.46, 99.5, 4.0, "en"),   # chute 2 « take no for an answer »
]

from faster_whisper import WhisperModel
model = WhisperModel("small", device="cpu", compute_type="int8")

print(f"== {FILE} ==")
deltas = []
for pat, exp, wstart, wdur, lang in CK:
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tf:
        wav = tf.name
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                    "-ss", str(wstart), "-t", str(wdur), "-i", FILE,
                    "-vn", "-ac", "1", "-ar", "16000", wav], check=True)
    segs, info = model.transcribe(wav, language=lang, vad_filter=True, word_timestamps=True)
    hits = []
    for s in segs:
        for w in s.words:
            if re.search(rf"\b{pat}", w.word, re.I):
                hits.append(w.start + wstart)
    os.unlink(wav)
    if not hits:
        print(f"  {pat:10s} ATTENDU {exp:7.2f}  -> MOT INTROUVABLE")
        continue
    # l'occurrence la plus proche de l'attendu
    meas = min(hits, key=lambda h: abs(h - exp))
    delta = meas - exp
    deltas.append(delta)
    flag = "OK " if abs(delta) <= 0.20 else ">>> Dérive"
    print(f"  {pat:10s} attendu {exp:7.2f}  mesuré {meas:7.2f}  delta {delta:+5.2f}s  {flag}")
if deltas:
    print(f"  -> delta max |{max(map(abs, deltas)):.2f}|s sur {len(deltas)} checkpoints")
