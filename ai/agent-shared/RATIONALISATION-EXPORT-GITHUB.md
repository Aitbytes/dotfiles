# Rationalisation de la couche IA + export GitHub

> Audit du 2026-10-27. Complète `PLAN-FIABILISATION-OUTILS.md` (qui couvre la couche
> OUTILS/recherche ; celui-ci couvre la couche CONFIG/répartition disque).

## 1. Inventaire de la couche IA

### 1.1 Hub central — `~/dotfiles/ai/` (suivi git, remote `Aitbytes/dotfiles`)
| Chemin | Contenu | État |
|---|---|---|
| `.agents/` (= `~/.agents`) | 18 définitions de subagents (`vague3.*`, `demolition.*`, `divergence.*`, `usines.*`, `furniture-analyzer`) | 16 fichiers **non committés** |
| `.agents/travel_planner/` | `preferences.json`, `trips.json` | ⚠️ données d'état mêlées à la config |
| `.agents/skills/` | 40 skills (recherche, e-commerce, sport, religion, rédaction…) | OK ; `.venv` gitignorés |
| `.agents/skills/.bak/` | vieilles versions de 3 skills | 🗑️ à supprimer |
| `agent-shared/` | `doctor.sh`, `drift_lint.py`, `budgets.md`, `user-preferences.md`, runbooks, `scripts/lbc_fetch.py`, PLAN-FIABILISATION | OK |
| `agent-shared/pi-skills-root-archive.tgz` | archive fantôme 2.6K | 🗑️ à supprimer |
| `.pi/agent/prompts/` | `deep_research.md`, `seed-context-from-obsidian.md` | OK, symlinké vers `~/.pi` ✓ |

### 1.2 Runtime pi — `~/.pi/` (883 Mo, dont 727 Mo sessions + 152 Mo node_modules)
| Chemin | Contenu | Problème |
|---|---|---|
| `~/.pi/prompts`, `~/.pi/agent/prompts` | symlinks → dotfiles | ✓ propre |
| `agent/settings.json` | skills path `~/skills/text-to-cad/skills`, packages npm (pi-subagents, pi-web, relays), provider zai/glm-5.3-flash | **pas dans git** |
| `agent/models.json` | provider custom `llama-rx480` (llama.cpp VM Proxmox 200, qwen3-8b) | **pas dans git** (aucun secret réel — `local-noauth`) |
| `agent/auth.json` | creds fournisseur (0600) | ❌ ne JAMAIS exporter |
| `agent/models-store.json` (483K), `run-history.jsonl` | caches régénérables | gitignore |
| `agent/bin/fd` | binaire vendou (déjà fourni par nix) | 🗑️ supprimable |
| `~/.pi/agents/` | **11 agents** (`comite*`, `critique-*`, `exam-*`, `web-researcher`) | ❌ HORS git — fragmentation |
| `~/.pi/agent/agents/` | **2 agents** (`infra.grumpy-reviewer`, `svg-visualizer`) | ❌ HORS git — 3e emplacement |

### 1.3 Binaires du PATH (couche IA uniquement)
`~/.local/bin` :
- Wrappers → scripts de skills : `maps`, `gmaps`, `mealie` (python3 sur `~/.agents/skills/...`), `cadgen` (source `~/scripts/cad-env.sh` puis cadgen réel)
- `tandem` (script Python 136K, CLI GTD) · `gws` (ELF Go 19 Mo, Google Workspace) · `linkedin-dm` (ELF Go 10 Mo)
- `autocomplete.sh` (45K, complétion bash LLM, vendu de ClosedLoop)
- ⚠️ non-IA mais volumineux au même endroit : `crc`, `oc`, `openshift-install` (≈740 Mo)

`~/.npm-global/bin` : `ghidra-agent-cli`, `@linkedapi/linkedin-cli` → `linkedin`, trio `pi-web*`

uv tools : `arxiv-mcp-server`, `browser-use` (5 entrypoints), `linkedin-cli` → `linkedin`, `playwright`, `yt-dlp`
pipx : `pypaperless-cli` (pngx), `yt-dlp` **v2026.3.17 obsolète en double**

### 1.4 CLIs IA concurrents (claude/codex/copilot/cursor/gemini/opencode)
- `~/.{claude,codex,copilot,cursor,gemini}/skills/browser-use/SKILL.md` : **5 copies manuelles datées du 1ᵉʳ août, divergées de la source dotfiles** (la source a évolué depuis).
- `~/.config/opencode/` + `~/dotfiles/opencode/` : agents opencode, skills (glm-ocr, browser-use), tools en double `.py` + `.ts` (fda_510k, patent_search, reddit, youtube, web_scraper…), cache `.reddit_data/` (gitignoré mais 14 fiches).
- `~/dotfiles/gemini/.gemini` : sessions de chat locales (gitignorées), `GEMINI.md` suivi.
- `~/dotfiles/mcphub/` : `servers.json`.
- `~/skills/text-to-cad` : repo externe 52 Mo (référencé par pi settings).
- `~/scripts/` : `vault-env` (bootstrap secrets via Vault AppRole + keyring — aboutissement du hardening 2026-10-13), `cad-env.sh` (fix libGL/zlib OCCT).

## 2. Problèmes identifiés

1. **Split-brain des agents** : 31 définitions réparties sur 3 emplacements, un seul suivi git → risque de perte (16 fichiers `??` dans git status).
2. **WIP non commité** : 8 fichiers modifiés (steel-browser, retail, gws, youtube…) + 4 skills entiers non suivis (business-coach, pecb-exam-blanc, video-montage).
3. **Doublons d'outillage** : `yt-dlp` (uv 2026.10 + pipx 2026.3 mort), `linkedin` (npm @linkedapi vs uv linkedin-cli), tools opencode en double `.py`/`.ts`.
4. **5 copies mortes** de browser-use dans les CLIs concurrents.
5. **État mêlé à la config** : `travel_planner/*.json` dans `.agents/` ; `models-store.json` ; archives `.tgz` ; `.bak` partout (`opencode.json.tui-migration.bak`, skills `.bak/`).
6. **Reproductibilité nulle des .venv de skills** (flights 38 Mo, steel 69 Mo) : pas de `requirements.txt` par skill → non reconstruisibles après clonage.
7. **Déchets** : `~/dotfiles/true<` (33 o, résidu de commande ratée), `~/~` (faux home), `pi-skills-root-archive.tgz`, `agent/bin/fd`.
8. **Binaires non sourcés** : `gws`, `linkedin-dm`, `autocomplete.sh` sans mention de version/origine → irreproductibles.
9. **Rien ne verrouille `settings.json`/`models.json` de pi** dans le repo.

## 3. Plan de rationalisation (5 phases) — ✅ EXÉCUTÉES le 2026-10-27

> Résultat : branch `ai-rationalisation` (8 commits), doctor 28 ok / 0 fail,
> export https://github.com/Aitbytes/agent-stack (privé, main = split subtree, CI branchée).
> Reste au user : merger la branche dans main dotfiles ; CI verte à vérifier au 1ᵉʳ push.

### Phase 0 — Filet de sécurité ✅
```bash
cd ~/dotfiles && git checkout -b ai-rationalisation
git add -A ai/ && git commit -m "wip: snapshot couche AI avant rationalisation"
tar -C ~ -czf ~/backups/pi-agents-untracked-$(date +%F).tgz .pi/agents .pi/agent/agents dotfiles/ai
```
Ne jamais toucher : `~/.pi/agent/auth.json`, keyring, `vault-env`.

### Phase 1 — Consolidation des agents (1 h)
1. Fusionner les 31 définitions vers `~/dotfiles/ai/agents/` (nouveau layout) :
   - déplacer les 18 de `.agents/*.md` (garder `.agents/skills/` en place — convention `~/.agents/skills` chargée par les skills)
   - rapatrier les 11 de `~/.pi/agents/` et 2 de `~/.pi/agent/agents/`
   - dédoublonner par `name:` frontmatter (aucun doublon détecté aujourd'hui)
2. Symlinker : `ln -s ~/dotfiles/ai/agents ~/.pi/agents` (idempotent, même modèle que `prompts`).
3. Vérifier que pi + pi-subagents voient les 31 agents (`pi agents` / doctor).

### Phase 2 — Dédoublement & nettoyage (2 h)
| Action | Commande cible |
|---|---|
| Supprimer pipx yt-dlp (garder uv) | `pipx uninstall yt-dlp` |
| Trancher `linkedin` : garder `linkedin-dm` (Go) + uv `linkedin-cli`, désinstaller `@linkedapi/linkedin-cli` si non utilisé | `npm -g uninstall @linkedapi/linkedin-cli` (vérifier 30 j d'usage d'abord) |
| Supprimer les 5 copies browser-use | `rm -r ~/.claude/skills ~/.codex/skills ~/.copilot/skills ~/.cursor/skills ~/.gemini/skills` puis symlink vers `~/dotfiles/ai/.agents/skills/browser-use` via le bootstrap (Phase 4) |
| opencode : garder 1 langage/tool, archiver l'autre ; `.reddit_data/` → données, déplacer hors git | décision à prendre (les `.ts` sont-ils encore appelés ?) |
| Déchets | `rm -r '~/dotfiles/true<' '~/' dotfiles/ai/agent-shared/pi-skills-root-archive.tgz ~/.pi/agent/bin/fd` |
| État travel_planner | déplacer vers `~/.local/state/travel-planner/` + skill mis à jour |
| `.bak` | `rm -r ~/dotfiles/ai/.agents/skills/.bak dotfiles/opencode/.opencode/*.bak` |

### Phase 3 — Reproductibilité (2 h)
1. `agent-shared/requirements/` : un `flights.txt`, `steel-browser.txt`, … (pip freeze des venv existants AVANT de les rendre re-créables par le bootstrap).
2. Commiter `dotfiles/ai/pi/settings.json` + `models.json` (sanitisés — vérifier absence de token ; `local-noauth` OK) ; gitignore `models-store.json`, `run-history.jsonl`, `sessions/`.
3. `bin/VENDORED.md` : provenance + version + sha256 de `gws`, `linkedin-dm`, `autocomplete.sh` ; idéal : scripts de build ou URLs de release.
4. Compléter le `doctor.sh` existant : check des symlinks (`~/.agents`, `~/.pi/agents`, `~/.pi/prompts`), présence des wrappers PATH, absence de doublons yt-dlp/linkedin.

### Phase 4 — Bootstrap idempotent (2 h)
`~/dotfiles/ai/bootstrap.sh` :
- crée les symlinks (agents, prompts, 5 CLIs concurrents → skill browser-use, wrappers `~/.local/bin` → `dotfiles/ai/bin/`)
- `uv tool install` la liste figée (arxiv-mcp-server, browser-use, linkedin-cli, playwright, yt-dlp)
- recrée les `.venv` de skills depuis `requirements/`
- vérifie `vault-env` fonctionnel (dry-run, sans exposer de secret)
Alternative NixOS propre : en faire un module `home-manager` — à garder en v2.

### Phase 5 — Export GitHub (1 h)
1. **Scan secrets sur l'historique** avant tout push : `gitleaks detect --source ~/dotfiles` (+ vérifier que `ai/.pi`, `auth.json`, `google_accounts.json` n'ont jamais été commités).
2. **Choix du shape** :
   - A (simple) : le repo `Aitbytes/dotfiles` actuel expose déjà `ai/` → il suffit de merger la branche.
   - B (partageable, recommandé si publication) : `git subtree split -P ai -b ai-export` → repo dédié `Aitbytes/agent-stack` avec historique préservé ; dans dotfiles, remplacer par un submodule ou garder les deux.
3. Hygiène du repo : README (architecture de la figure §1), LICENSE, `.gitignore` durci (`*.tgz`, `state/`, `models-store*`), suppression du dossier `true<` de l'index.
4. CI GitHub Actions : `drift_lint.py` + validation frontmatter des SKILL.md/agents + `shellcheck doctor.sh bootstrap.sh` + `gitleaks` en pré-push.
5. Push : `git push -u origin ai-rationalisation` → PR → merge main ; si option B : créer `agent-stack` et pusher la branche split.

### Ordre et effort
| Phase | Durée | Risque |
|---|---|---|
| 0 snapshot | 30 min | nul |
| 1 agents | 1 h | faible (symlinks vérifiables) |
| 2 dédoublonnage | 2 h | moyen (désinstallations — vérifier usages) |
| 3 reproductibilité | 2 h | faible |
| 4 bootstrap | 2 h | faible |
| 5 export | 1 h | nul si gitleaks propre |
| **Total** | **≈ 8 h 30** | |

## 4. Décisions (tranchées le 2026-10-27)
1. **linkedin** : garder uv `linkedin-cli` (+ `linkedin-dm` Go) → désinstaller `@linkedapi/linkedin-cli` npm. ✓
2. **opencode** : abandonné → décommissionner `~/.config/opencode` et `~/dotfiles/opencode` (les tools `.py` vivent déjà dans le skill `research-extended-tools`). ✓
3. **Export** : repo dédié `Aitbytes/agent-stack` via `git subtree split -P ai`. ✓
4. Agents `comite*/exam-*` : voir §5 — 3 options, recommandation = A.

## 5. Options agents PECB (`~/.pi/agents/`) — audit d'usage du 2026-10-27

Mécanique de découverte (pi-subagents) : user = `~/.pi/agent/agents/` (partout) ; projet =
`.pi/agents/` du cwd + ancêtres (stop au repo git). `~/mypecb-extract` n'étant PAS git, la
découverte remonte jusqu'à `$HOME` → c'est ainsi que `~/.pi/agents/` est vu depuis le projet PECB.

Usage réel (run-history + sessions) : tout est VIVANT (sessions du 26 oct, projet `mypecb-extract`) :
- `exam-redacteur` 22 · `critique-jourj` 16 · `critique-exactitude` 15 · `exam-planificateur` 4 · `comite*` 2-3 chacun · `web-researcher` 2
- user-scope : `grumpy-reviewer` 30 · `svg-visualizer` 22 (les plus utilisés de la machine)

### Option A — Scope projet propre ✅ EXÉCUTÉE le 2026-10-27
Réalisation effective :
- 9 agents PECB (`comite*`×5, `critique-*`×2, `exam-*`×2) → `~/mypecb-extract/.pi/agents/`
  (repo git initialisé, `.gitignore` excluant archive/, *.pdf, jour-*) ;
- `web-researcher`, `grumpy-reviewer`, `svg-visualizer` → `~/dotfiles/ai/agents/` (branch
  `ai-rationalisation`), exposés en user-scope par symlink de répertoire `~/.pi/agent/agents` ;
- `~/.pi/agents/` supprimé.
Vérifié par `/subagents-doctor` équivalent : depuis `~` projet 65→55 (−10, plus de pollution) ;
depuis `~/mypecb-extract` project 9 + user 61 (+web-researcher). Un symlink **fichier** dans le
user-scope n'est PAS suivi par la découverte — seuls les symlinks de répertoires le sont
(pareil pour `~/.agents`).
### Option B — Deux tiers dans agent-stack
Dans le repo dédié : `agents/` (permanents : 18 existants + web-researcher + grumpy-reviewer +
svg-visualizer, symlink user-scope `~/.pi/agent/agents` → repo) et `agents-projects/pecb/`
(jetables), exposés par symlink `~/.pi/agents` → `agents-projects/pecb/` le temps de la prépa.
Avantage : tout versionné au même endroit, historique préservé. Inconvénient : un symlink de
plus à penser à retirer après l'examen.
### Option C — Backup simple
Copier les 12 fichiers tels quels dans le repo (dossier `agents-legacy/`) sans toucher à la
découverte. Moins propre (split-brain conservé) mais zéro risque pendant la prépa.

> ⚠️ Quirk découvert à l'occasion (préexistant, Phase 1) : la découverte récursive du scope
> legacy `~/.agents/` parse aussi les `skills/*/SKILL.md` comme agents fantômes (duplicatas
> vus : playwright-browser ×2, research-assistant ×2, retail-research ×2). Fix Phase 1 :
> sortir les .md d'agents réels de `.agents/` vers `ai/agents/` (user-scope) et ne laisser
> dans `.agents/` que `skills/`.
