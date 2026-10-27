---
name: pecb-exam-blanc
description: Génère des examens blancs calibrés pour le QCM PECB ISO/IEC 27001 Lead Implementer (80 Q / 3 options / 70%) à partir du corpus local. Utiliser quand l'utilisateur demande un examen blanc, des questions d'entraînement supplémentaires, une recalibration de quiz, ou un entraînement type examen pour cette certification. Interdit toute question issue de dumps/annales.
---

# Générateur d'examens blancs — PECB 27001 LI

Produire un examen blanc = un blueprint + des questions vivantes + un corrigé séparé. Tout se joue contre DEUX impératifs : coller au format officiel (handbook v1.5) et ne jamais produire de question « morte » (réponse trouvable sans lire les options).

## 1. Blueprint officiel (source : Candidate Handbook v1.5, vérifié live le 26/10)

| Paramètre | Valeur |
|---|---|
| Nb questions | 80 (blanc partiels : 40 = demi-format) |
| Options par question | **exactement 3** (A/B/C) — jamais 4 |
| Durée | 3 h → **cible 135 s/Q** en conditions |
| Seuil de réussite | 70 % (56/80 ; diagnostic blanc 40 Q = 28/40) |
| Niveau « évaluation » | ≥ 46 % (mini-scénarios, verbes « le PLUS approprié / D'ABORD ») · ~37 % compréhension · ≤ 25 % mémorisation |

Poids par domaine (pour 80 Q → D1 15 · D2 12 · D3 18 · D4 14 · D5 10 · D6 6 · D7 5 ; pour 40 Q → 8/6/9/7/5/3/2) :
- D1 Fondamentaux & concept SMSI · D2 Initiation SMSI · D3 Planification · D4 Implémentation · D5 Surveillance/mesure/revue · D6 Maintien & amélioration · D7 Préparation audit de certification.

## 2. Sources de questions (dans l'ordre de légitimité)

1. **Corpus** : `/home/a8taleb/mypecb-extract/texte-jour-{1..4}-v3.md` — LA source de vérité. Chaque corrigé cite sa slide (`J2 s116`).
2. **Fiches** : `/home/a8taleb/mypecb-extract/notes-examen/0[0-5]-*.md` — pièges et confusions déjà cartographiés.
3. **Matériaux officiels du provider** (licenciés à l'utilisateur) : `/home/a8taleb/mypecb-extract/ressources-externes/quiz-formation-officiel-27001LI.md` (réformuler + produire le corrigé depuis le corpus), `etude-de-cas-escooter-officiel.md`, `exercices-formation-officiel-27001LI.md`.
4. **Banque existante comme référence de style** : `notes-examen/06-banque-quiz-{questions,corriges}.md` (110 Q v1.1 vérifiées). Réutilisation autorisée (spaced repetition assumée) mais reformuler ≥ 50 % des énoncés.
5. **Interdit** : toute question copiée d'un site d'annales/dump (ExamTopics, certempire, repos « Exam Questions », etc.) — contraire au Code of Ethics PECB, annulation de certification possible. S'inspirer des THÈMES seulement.

## 3. Règles de rédaction (ce qui différencie une question vivante d'une question morte)

- **Test du distracteur** : si la bonne réponse se déduit de l'énoncé seul, la question est morte → réécrire. Les 2 distracteurs doivent chacun correspondre à une ERREUR RÉELLE plausible.
- **Les 6 confusions à exploiter en priorité** : NC ≠ incident · RSI ≠ DSI · « l'une des premières informations documentées analysées » ≠ « le premier document » (J2 s116) · **10.1 amélioration vs 10.2 NC (2022 ! l'inverse en 2013)** · A.5 organisationnel vs A.8 technologique · normatif (« doit ») vs recommandation (« il convient »).
- **Annexe A en version 2022 UNIQUEMENT** : 93 contrôles, 4 thèmes (37/8/14/34), 5 attributs. Jamais 114/11 domaines (2013).
- **Scope LI, pas LA** : implémentation/leadership, jamais « comment conduire un audit » (sauf 1 piège assumé max par examen).
- Verbes « best answer » : 2 options défendables, une seule LA meilleure selon la logique PDCA/implémentation.
- Scénarios réalistes 2-5 lignes (s'inspirer du style Infralink/e-Scooter) : PME, société de conseil, industrie — jamais de prénoms type dump.
- Interdictions : question négative (« Lequel n'est PAS… ») > 1 fois sur 10 ; définitions verbatim habillées en « évaluation » ; indices dans le libellé des options (« volontairement », « toujours », « jamais » trahissent la réponse).

## 4. Équilibrage anti-triche (leçon du blanc v1 : 2 C sur 40)

Brasser les positions pour que chaque lettre ≈ ⅓ (jamais < 20 % ni > 40 % pour une position, en particulier dans un blanc diagnostique à seuil).

## 5. Sortie : 3 fichiers séparés (2 humains + 1 machine)

- `<dossier>/exam-blanc-N-questions.md` : titre + consignes temps + table répartition effective vs cible + Q numérotées `[ID · domaine · niveau]` + énoncé + A/B/C. Zéro indice de réponse.
- `<dossier>/exam-blanc-N-corriges.md` : notice « ouvrir APRÈS » + par Q : bonne réponse + pourquoi + pourquoi les 2 autres sont fausses + source + **chemin de récupération < 30 s**. Note d'impression : paysage ou saut de page.
- `<dossier>/exam-blanc-N.json` : **source de vérité machine** (schéma §5-bis) — le QCM interactif HTML se génère depuis ce JSON.

**Le chemin < 30 s** (dans le corrigé de CHAQUE question) : la route open-book concrète, 2 à 4 étapes, format tableau JSON `chemin_30s` (et colonne md « Retrouver en <30 s ») :
```json
"chemin_30s": [
  "Mot-clé de la question : « intervalle de revue de direction »",
  "→ 01-index §A, ligne 9.3 (détection clause)",
  "→ fiche 03 FICHE 9, bloc 9.3 (verbatim condensé)",
  "→ réponse : au moins 1×/an (27003, pas exigence 27001)"
]
```
Règles : partir du MOT-CLÉ de l'énoncé (pas de la réponse) → pointer le fichier/section qui déclenche la reconnaissance → dernière étape = le discriminateur. Si la source est une slide : indiquer la commande `grep -n "^## Slide N —" texte-jour-X-v3.md`.

## 5-bis. Schéma JSON + QCM interactif HTML

```json
{
  "titre": "Examen blanc #2 — PECB 27001 LI",
  "genere_le": "2026-11-05",
  "origine": "skill pecb-exam-blanc v2 · vérifié par critique",
  "seuil_reussite_pct": 70,
  "blocs": [
    {"nom": "Blanc complet (80 Q)", "ids": [1, 80], "duree_minutes": 180}
  ],
  "questions": [
    {
      "id": 1,
      "domaine": "D3",
      "niveau": "evaluation",
      "enonce": "…",
      "options": {"A": "…", "B": "…", "C": "…"},
      "bonne": "B",
      "pourquoi": "…",
      "fausses": {"A": "…", "C": "…"},
      "chemin_30s": ["…", "…"],
      "source": "J2 s115 · fiche 03 FICHE 6"
    }
  ]
}
```

Générer le QCM interactif (HTML autonome, offline, stdlib uniquement) :
```bash
python3 ~/.agents/skills/pecb-exam-blanc/scripts/build_qcm.py exam-blanc-N.json -o exam-blanc-N.html
```
Fonctions de l'HTML : choix du bloc (avec timer) · mode ENTRAÎNEMENT (correction immédiate) ou EXAMEN (correction au rendu) · feedback par Q = pourquoi + pourquoi-fausses + chemin <30 s + source · score final + décompte par domaine vs poids officiels · revue des ratées. Savegarde localStorage (refresh-safe).

Convertir la banque 06 existante (déjà fait une fois — rescript si la banque évolue) :
```bash
python3 ~/.agents/skills/pecb-exam-blanc/scripts/convert_banque06.py   # → notes-examen/qcm/banque-06.{json,html}
```

## 6. Contrôle qualité avant livraison (les 2 critiques du 26/10)

1. Balayage : 3 options partout, aucune fuite de corrigé, positions équilibrées, table de répartition honnête.
2. Tirage échantillon (10-15 Q) : chaque corrigé vérifié contre le corpus via `grep -n "^## Slide N —" texte-jour-X-v3.md` (les sources citent des slides sN).
3. Chronomètre 5 Q « évaluation » : ≤ 135 s/Q sinon scénario trop lourd.
4. Test du distracteur sur 10 Q : ≤ 1 morte tolérée.
5. `python3 -c "import json;json.load(open('exam-blanc-N.json'))"` sans erreur + build HTML réussi + nb de Q du JSON = nb de Q du md.

## 7. Contexte candidat (plan v4.3, examen 20/11 ou 13/11 si blancs verts)

Blanc #1 officiel = Q1-Q40 de la banque 06, sam 31/10, seuil 28/40 → ≥ 32/40 = avance au 13/11. Un examen blanc généré par ce skill est un ENTRAÎNEMENT, pas le diagnostic go/no-go (réservé à la banque vérifiée), sauf demande explicite.
