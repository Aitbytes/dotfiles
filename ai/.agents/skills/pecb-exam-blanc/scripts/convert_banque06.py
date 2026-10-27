#!/usr/bin/env python3
"""convert_banque06.py — Convertit la banque 06 (md) en JSON + QCM HTML interactif.
Parse les fichiers vérifiés v1.1 : 06-banque-quiz-questions.md + 06-banque-quiz-corriges.md.
Sortie : notes-examen/qcm/banque-06.json + banque-06.html. Stdlib uniquement.
"""
import json, re, sys
from pathlib import Path

BASE = Path("/home/a8taleb/mypecb-extract/notes-examen")
QMD = BASE / "06-banque-quiz-questions.md"
CMD = BASE / "06-banque-quiz-corriges.md"
OUT_DIR = BASE / "qcm"
sys.path.insert(0, str(Path(__file__).parent))
from build_qcm import build  # noqa: E402

NIVEAU = {"évaluation": "evaluation", "compréhension": "comprehension",
          "memorisation": "memorisation", "mémorisation": "memorisation",
          "comprehension": "comprehension", "evaluation": "evaluation"}
DOM_NOM = {"D1": "D1 Fondamentaux", "D2": "D2 Initiation SMSI", "D3": "D3 Planification",
           "D4": "D4 Implémentation", "D5": "D5 Surveillance & mesure",
           "D6": "D6 Maintien & amélioration", "D7": "D7 Préparation audit"}

def clean(t):
    return re.sub(r"\*\*|`", "", t or "").strip()

def parse_questions():
    txt = QMD.read_text(encoding="utf-8")
    blocks = re.split(r"^\*\*Q(\d+) · \[(D\d) · ([^\]]+)\]\*\*\s*$", txt, flags=re.M)
    out = {}
    for i in range(1, len(blocks), 4):
        qid, dom, niveau = int(blocks[i]), blocks[i + 1], blocks[i + 2].strip().lower()
        body = blocks[i + 3]
        opts = dict(re.findall(r"^- ([ABC])\. (.*)$", body, flags=re.M))
        opts = {k: clean(v) for k, v in opts.items()}
        enonce_lines = []
        for line in body.splitlines():
            if re.match(r"^- [ABC]\. ", line):
                break
            if line.strip():
                enonce_lines.append(line.strip())
        if not opts or len(opts) != 3:
            print(f"⚠ Q{qid}: {len(opts)} option(s) trouvée(s) — ignorée", file=sys.stderr)
            continue
        out[qid] = {"id": qid, "domaine": dom, "niveau": NIVEAU.get(niveau, niveau),
                    "enonce": clean(" ".join(enonce_lines)), "options": opts}
    return out

def parse_corriges():
    txt = CMD.read_text(encoding="utf-8")
    out = {}
    for m in re.finditer(r"^\|\s*\*\*Q(\d+)\*\*\s*\|\s*\*\*([ABC])\*\*\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*$", txt, flags=re.M):
        qid, bonne, pourquoi, fausses, source = int(m[1]), m[2], clean(m[3]), m[4], clean(m[5])
        parts = re.split(r"\s+·\s+(?=[ABC]\s?:\s)", fausses)
        fmap = {}
        for p in parts:
            mm = re.match(r"^([ABC])\s?:\s*(.*)$", p.strip())
            if mm:
                fmap[mm[1]] = clean(mm[2])
        out[qid] = {"bonne": bonne, "pourquoi": pourquoi,
                    "fausses": {k: v for k, v in sorted(fmap.items())}, "source": source}
    return out

def chemin_30s(q, corr):
    steps, src = [], corr["source"]
    fiche = re.search(r"fiche 0(\d)", src) or re.search(r"fiches? 03.*?FICHE (\d+)", src)
    fnum = re.search(r"FICHE (\d+)", src)
    sec = re.search(r"§\s?([\w.\d]+)", src)
    slide = re.search(r"J(\d)\s*s(\d+)", src)
    if fnum or (fiche and fiche.group(1) == "3"):
        steps.append("Mot-clé de la question → ouvrir 03-fiches-clauses-4-10.md, FICHE "
                     + (fnum.group(1) if fnum else fiche.group(1)) + " (exigence verbatim condensée + qui + documents)")
    elif fiche:
        steps.append(f"Mot-clé → ouvrir la fiche 0{fiche.group(1)}"
                     + (f", section §{sec.group(1)}" if sec else ""))
    else:
        steps.append("Mot-clé → 01-index §A (table maîtresse : mot-clé → clause)")
    if slide:
        j, s = slide.group(1), slide.group(2)
        steps.append(f'Slide source {src.split("·")[0].strip()} → vérifier : grep -n "^## Slide {s} —" texte-jour-{j}-v3.md')
    if not steps:
        steps.append("Retrouver la clause par mot-clé via 01-index §A, puis fiche 03")
    steps.append(f"Bonne réponse : {corr['bonne']} — {corr['pourquoi'][:90]}{'…' if len(corr['pourquoi'])>90 else ''}")
    return steps

def main():
    qs, cs = parse_questions(), parse_corriges()
    missing = sorted(set(qs) - set(cs))
    extra = sorted(set(cs) - set(qs))
    if missing:
        print(f"⚠ {len(missing)} Q sans corrigé : {missing[:10]}{'…' if len(missing)>10 else ''}", file=sys.stderr)
    if extra:
        print(f"⚠ {len(extra)} corrigés orphelins : {extra[:10]}", file=sys.stderr)
    ids = sorted(set(qs) & set(cs))
    questions = []
    for qid in ids:
        q, c = qs[qid], cs[qid]
        q.update({"bonne": c["bonne"], "pourquoi": c["pourquoi"], "fausses": c["fausses"],
                  "source": c["source"], "chemin_30s": chemin_30s(q, c)})
        questions.append(q)
    data = {
        "titre": "Banque 06 — PECB 27001 LI (110 Q vérifiées)",
        "genere_le": "2026-10-26",
        "origine": "banque-06 v1.1 · vérifiée critique-exactitude + critique-jourj · convertie par skill pecb-exam-blanc",
        "seuil_reussite_pct": 70,
        "blocs": [
            {"nom": "Blanc #1 — Q1-Q40 (diagnostic 31/10, ≥32/40 = avance au 13/11)",
             "ids": [1, 40], "duree_minutes": 90},
            {"nom": "Pool interleaving — Q41-Q110 (5-10 Q par session, sans timer)",
             "ids": [41, 110], "duree_minutes": None},
        ],
        "questions": questions,
    }
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    jp = OUT_DIR / "banque-06.json"
    jp.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"JSON : {jp} ({len(questions)} Q)")
    build(jp, OUT_DIR / "banque-06.html")

if __name__ == "__main__":
    main()
