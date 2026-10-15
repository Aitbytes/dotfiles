# Plan de fiabilisation OUTILS (audit sessions 01a13c77 + 01a13f93, 2026-10-15)

Postulat validé: la MÉTHODO tient (les 2 sessions ont complété, routing correct, pivots
intelligents: amazon quand fnac bloqué, startpage quand DDG meurt, brand-direct quand
marketplace bloque). Ce qui saigne = la couche OUTILS. Audit:

## Ce que les sessions ont prouvé

| Constat | Session | Preuve |
|---|---|---|
| fnac.com, darty.com, boulanger.com = mur total | B | steel blocked (01a13f93) + probes 2026-10-15: 403 partout pour fnac/darty; boulanger 400/soft-404 SPA sans données serveur. IRRÉCUPÉRABLE côté outil. |
| L'agent n'ose pas le proxy sans permission | B | "Tu peux utiliser le proxy" (12:56) — 15 min perdues |
| DDG casse (anomaly/traceback) ~1 fois/session | B | fallback startpage.com a marché (non documenté avant) |
| but.fr DataDome intermittent CONFIRMÉ live | B+précédente | 2 blocked puis 2 ok même session |
| boulanger absent de sites.json | B | 0 row → l'agent a dû tenter pour découvrir |
| web_scraper = cheval de bataille réel (22-27 appels/session, taux de succès élevé) | A+B | brand-direct (aarke.com, my-soda.com) et pages statiques passent sans impersonation |
| Session A (admin/URSSAF): quasi zéro friction | A | 7x IDF Mobilités ok, service-public.fr ok |

## Actions (fait, 2026-10-15)

1. sites.json: row boulanger.com AJOUTÉE (blocked, bot_hardening_spa, datée, preuves);
   fnac.com + darty.com DATÉES (datadome_tls, 403 both paths, fallbacks explicites). 42 sites.
2. retail + social: section "FR DataDome trio — DO NOT steel-fetch" (fallback ladder direct)
   + chaîne de fallback recherche (DDG → startpage → bing) + proxy par défaut.
3. deep_research Phase 1: `eval "$(env-guard proxy)"` au démarrage de session — plus jamais
   besoin de la permission utilisateur.
4. (déjà fait 2026-10-13/14) web_scraper wrapper doc, DDG pattern, anti-stall, venv-only steel.

## Reste à faire (proposé, non urgent)

- **fr_retail_fetch.py (v2, optionnel)**: curl_cffi chrome + FR proxy + extraction JSON-LD
  générique (schema.org Product) en un seul outil pour les sites steel-ok SANS extracteur
  (brand-direct, petits e-commerce). Utilité réelle: moyenne (web_scraper couvre déjà ces cas).
- **youtube.py anti-quota**: 1 err/7 appels en session B — acceptable, surveiller.
- **Re-sonder le trio DataDome tous les 90 j** (staleness law) — un changement de protection
  chez eux est possible; le doctor signale les rows >90j.
- **Playwright comme fallback but.fr**: jamais testé en live — à valider à la prochaine
  occasion réelle (pas en synthétique).
