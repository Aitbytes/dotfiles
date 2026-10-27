# Recherche d'un skill melt/MLT existant + sources

Date : 2026-10-27 · Budget : 7 requêtes HTTP (sous le budget de 10).

## Requêtes et résultats

| Requête | Résultat |
|---|---|
| GitHub API repos `q=mlt+melt+skill` | 0 résultat |
| GitHub API code `q=SKILL.md+melt+mlt` | null (code search API exige auth) |
| GitHub API repos `q=claude+skill+video+editing` | 297 résultats, tous Remotion/captions/vertical : haidrrrry/claude-remotion-skill (628★), zenstory-ai/video-recap-skills (590★), nateherkai/herk-edit-kit (2196★), nopefallacy/vertical-video-editing-skills (64★), 6missedcalls/video-editing-skill (47★) |
| skills.sh `q=melt` | `paulnsorensen/easy-cheese/melt` = résolution de conflits **git merge** (homonyme), MIT — hors sujet |
| skills.sh `q=video editing` | affaan-m/ecc/video-editing (14k installs, FFmpeg/Remotion/ElevenLabs/CapCut, metadata origin ECC), maxazure/video-editing-skill (XHS chinois, Remotion), ecliptic-ai/beat-sync (772) |
| raw affaan-m/ecc video-editing SKILL.md | Pipeline généraliste montage footage, aucun contenu melt/MLT, aucune doctrine anti-dérive A/V, pas de recette yt-dlp clients |
| tree maxazure/video-editing-skill | Prompts XHS/broadcast chinois — hors sujet |

## Verdict

**Aucun skill de qualité ne couvre melt/MLT ni la discipline anti-drift A/V** → création from scratch. Les skills trouvés sont orientés génération/captions/remotion, pas timeline NLE déterministe. Aucun import, donc pas de licence tierce à porter. Le SKILL.md cite la doc ffmpeg (filtre concat) et le man melt 7.42.0 (via la recherche de la session source, voir `~/Documents/research/text-game-agents/experiment/av-sync-tools-comparison.md`).

## Provenance du contenu

Tout le contenu opérationnel est miné de la session pi `2026-10-25T12-46-19-972Z` (`~/.pi/agent/sessions/--tmp--/`), projet `~/Documents/research/text-game-agents/experiment/trailer_build/` :
- `scripts/verify_sync.py`, `scripts/build_opt3_cli.sh`, `scripts/gen_melt_xml.py` : copiés tels quels depuis trailer_build (écrits et validés dans la session).
- Verdict A/V : melt une-passe = 0,00 s de dérive à tous les checkpoints whisper ; conform ffmpeg opt2 = dérive divisée par 2 mais non nulle (+0,56 s → +0,18 s max) ; concat v1 = +0,46/+0,56 s.
- Attributs XML `in=`/`out=` silencieusement ignorés : confirmé expérimentalement dans la session (deltas -1,00/-2,00 s = offsets des clips).
