#!/usr/bin/env bash
# bootstrap.sh — reconstruit la couche IA depuis ce repo sur une machine neuve.
# Idempotent : relançable sans dommage. Aucun secret n'est stocké ici —
# les credentials passent par Vault (source ~/scripts/vault-env).
#
# Usage :  bash ~/dotfiles/ai/bootstrap.sh
set -euo pipefail
AI="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"   # .../dotfiles/ai
DOT="$(dirname "$AI")"
ok()   { printf '  \033[32mok\033[0m   %s\n' "$*"; }
skip() { printf '  \033[2mskip\033[0m %s\n' "$*"; }
act()  { printf '  \033[33mset\033[0m  %s\n' "$*"; }

link() { # link <chemin-lien> <cible>
  local p="$1" t="$2"
  if [ -L "$p" ] && [ "$(readlink -f "$p")" = "$(readlink -f "$t")" ]; then skip "$p"; return; fi
  mkdir -p "$(dirname "$p")"; [ -e "$p" ] && { mv "$p" "$p.pre-bootstrap.$(date +%s)"; act "$p sauvegardé"; }
  ln -s "$t" "$p"; act "$p -> $t"
}

echo "── 1. symlinks de découverte ──"
link "$HOME/.agents"             "$AI/.agents"
link "$HOME/.pi/agent/agents"    "$AI/agents"
link "$HOME/.pi/prompts"         "$AI/.pi/prompts"
link "$HOME/.pi/agent/prompts"   "$AI/.pi/agent/prompts"
for d in .claude .codex .copilot .cursor; do
  link "$HOME/$d/skills/browser-use" "$AI/.agents/skills/browser-use"
done
# .gemini est un symlink vers dotfiles/gemini/.gemini : 3 niveaux depuis l'emplacement physique
link "$HOME/.gemini/skills/browser-use" "../../../ai/.agents/skills/browser-use"

echo "── 2. outils uv (single source : uv, pas pipx) ──"
for t in arxiv-mcp-server browser-use linkedin-cli playwright yt-dlp; do
  if uv tool list 2>/dev/null | grep -q "^$t "; then skip "uv tool: $t"; else uv tool install "$t" && act "uv tool: $t"; fi
done

echo "── 3. venv des skills (reconstruits depuis agent-shared/requirements/) ──"
for req in "$AI"/agent-shared/requirements/*.txt; do
  name=$(basename "$req" .txt); venv="$AI/.agents/skills/$name/.venv"
  if [ -x "$venv/bin/python" ]; then skip "venv $name"; else
    python3 -m venv "$venv" && "$venv/bin/pip" install -q -r "$req" && act "venv $name reconstruit"
  fi
done

echo "── 4. config pi (si machine neuve uniquement) ──"
mkdir -p "$HOME/.pi/agent"
[ -f "$HOME/.pi/agent/settings.json" ] && skip "pi settings.json existe" || { cp "$AI/pi/settings.json" "$HOME/.pi/agent/settings.json"; act "pi settings.json installé (auth via 'pi' à refaire)"; }
[ -f "$HOME/.pi/agent/models.json" ]   && skip "pi models.json existe"   || { cp "$AI/pi/models.json"   "$HOME/.pi/agent/models.json";   act "pi models.json installé"; }

echo "── 5. binaires vendus (installation manuelle — voir agent-shared/VENDORED.md) ──"
for b in gws linkedin-dm autocomplete.sh; do
  command -v "$b" >/dev/null 2>&1 && skip "$b présent" || echo "  ⚠ $b absent — voir VENDORED.md"
done

echo "── 6. vérification finale ──"
bash "$AI/agent-shared/doctor.sh" || { echo "doctor a signalé des FAIL — corriger avant usage."; exit 1; }
echo "bootstrap terminé."
