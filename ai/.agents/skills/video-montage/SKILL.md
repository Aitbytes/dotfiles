---
name: video-montage
description: "USE WHEN montage vidéo, trailer, timelapse, extrait vidéo, couper/concaténer des clips, sync audio/vidéo, sous-titres ou habillage sur fichier vidéo. Priorité melt/MLT (rendu timeline une passe, zéro dérive A/V) sur ffmpeg concat. yt-dlp fiable pour télécharger les sources YouTube. NE PAS utiliser le filtre concat ffmpeg multi-segments (dérive A/V croissante)."
---

# Video Montage (ffmpeg / yt-dlp / MLT melt)

Recettes issues d'un build réel (trailer night-game 107 s, 17 clips, 8 sources YouTube) où la dérive A/V a été réduite de +0,56 s à **0,00 s** (vérifiée par whisper) en passant de ffmpeg concat à melt CLI une-passe.

## 1. Règle d'or anti-drift A/V

**JAMAIS de concat ffmpeg multi-segments** (filtre `-filter_complex concat` ni demuxer `-f concat`). Cause documentée : le filtre « works on segments of *synchronized* video and audio streams » — il ne resynchronise rien. Vidéo quantifiée 30 fps (33 ms), audio AAC par frames de 1024 samples (23 ms), `start_time` variables → 20-50 ms de dérive **par jonction**, qui s'accumule (inconfortable vers 0:43 sur 17 segments). Mesuré en parallèle : le conform ffmpeg « audio cadenassé sur frames vidéo exactes » réduit la dérive de moitié mais ne l'élimine pas.

**Pipeline gagnant :**
1. **Timeline rendue EN UNE PASSE avec melt CLI** (voir §4). Un seul rendu continu = l'écart A/V est structurellement impossible (moteur NLE de Shotcut/Kdenlive, synchro frame/sample par conception).
2. ⚠️ **Le XML MLT écrit à la main est piégeux** (retesté sur melt 7.28.0 : un XML style `gen_melt_xml.py` — double spec `in=`/`out=` en attributs ET en properties + `length` coupé + `<entry>` en absolu — rend **0,04 s au lieu de 3 s**). Le XML **généré par melt lui-même** (`… in=X out=Y -consumer xml`) round-trippe correctement (coupes respectées, vérifié par PSNR), MAIS ses chemins `resource` sont **relatifs au dossier du XML** → consommé depuis ailleurs = rendu **tout noir** (absolutiser les chemins). **Préférer le CLI melt avec `in=`/`out=` par producteur** : respecté (PSNR 37,8 dB vs source).
3. **Post-pass habillage APRÈS le rendu maître** : drawtext/lower-thirds + `loudnorm` en une seule passe ffmpeg sur le fichier continu (aucun risque de dérive, c'est une transco + filtres, pas un concat).

## 2. Téléchargement yt-dlp fiable (validé 2026-10, NixOS)

**Ce qui marche (client `visionos`, pas de PO token requis) :**
```bash
uv tool install yt-dlp --force   # version récente OBLIGATOIRE : c'est elle dont le client par défaut est visionos
export SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt   # sinon erreur de bundle CA (install uv)
export HTTP_PROXY= HTTPS_PROXY=
~/.local/bin/yt-dlp -q -f "bv*[height<=720]+ba/b" \
  --download-sections "*62-83" --force-keyframes-at-cuts \
  -o "raw/clip.%(ext)s" "https://www.youtube.com/watch?v=VIDEO_ID"
```
- `--download-sections` + `--force-keyframes-at-cuts` : ne télécharge que l'extrait, coupes sur keyframes.
- `SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt` est indispensable sur NixOS (le binaire uv/Python ne trouve pas le store CA sinon).
- **Cookies navigateur en fallback** si toujours 403 : `--cookies-from-browser firefox` (warning si cookies > 90 jours).

**Ce qui échoue (à ne pas refaire)** : clients `android_vr`, `web`, `ios`, `mweb`, `tv`, `web_embedded`, `tv_embedded` → 403 Forbidden ou PO token bloqué (système ancien comme récent). `default,ios` → « Requested format is not available ». Preuve que le client par défaut est bien visionos : l'URL googlevideo téléchargée contient `c=VISIONOS`.

**Piège concat demuxer** : `ffmpeg -f concat -i list.txt -c copy out.mp4` a **gobé silencieusement les 2 derniers segments** (hétérogénéité de codecs/durées non signalée). Toujours vérifier la durée finale par ffprobe contre la somme attendue.

## 3. Protocole QA token-économe (les images coûtent ~750 Ko chacune relues en base64)

1. **Valider par ffprobe/mesures AVANT toute lecture d'image** : durée (`format=duration`), nb frames (`-count_frames -show_entries stream=nb_read_frames`), `start_time` par flux, mean_volume (`volumedetect`) aux points de contrôle.
2. **Extraire les frames de contrôle SÉPARÉMENT** — jamais en multi-input :
   ```bash
   # FAUX : produit des PNG IDENTIQUES (le -ss du 2e -i est ignoré)
   ffmpeg -y -ss 6 -i in.mp4 -frames:v 1 a.png -ss 20 -i in.mp4 -frames:v 1 b.png
   # JUSTE : une commande par frame
   ffmpeg -y -ss 6 -i in.mp4 -frames:v 1 a.png
   ffmpeg -y -ss 20 -i in.mp4 -frames:v 1 b.png
   ```
3. **Lire l'image 1×/build max, à résolution réduite** : extraction avec `-vf scale=640:-1` pour le QA (les overlays restent visibles, le coût token est divisé par ~4). Ne jamais relire un PNG déjà validé après un rebuild non lié.

## 4. Recette melt CLI (commandes exactes de la session)

melt n'est **pas dans le PATH** → `nix-shell -p mlt`. Coupes en **frames du profil** (30 fps : `in=150` = 5,0 s). Fades : filtres `brightness` (vidéo) + `volume` (audio) attachés par `-attach-cut`, numérotation **relative à la coupe**.

```bash
# Test rapide : le in=/out= est-il respecté sur ce build ?
export HTTP_PROXY= HTTPS_PROXY=
nix-shell -p mlt --run "melt -profile atsc_720p_30 clip.webm in=150 out=593 -consumer xml" | sed -n '1,40p'

# Rendu maître une passe (extrait de scripts/build_opt3_cli.sh)
ARGS=' "raw/c01_cold.webm" in=150 out=593 -attach-cut brightness start=0 end=1 in=0 out=14 -attach-cut volume gain=0 end=1 in=0 out=14'
# ... un gén() par clip (voir script), fades video=start 0→1 / audio gain 0→1, et inverse en sortie
nix-shell -p mlt --run "melt -profile atsc_720p_30 $ARGS \
  -consumer avformat:$PWD/master.mp4 vcodec=libx264 crf=20 preset=medium \
  pix_fmt=yuv420p acodec=aac ab=160k ar=48000 ac=2 movflags=+faststart progress=1"

# Post-pass habillage sur le fichier continu (drawtext + loudnorm, zéro concat)
FONT=/nix/store/*/dejavu-fonts-*/share/fonts/truetype/DejaVuSansCondensed-Bold.ttf  # via fc-list
ffmpeg -y -i master.mp4 -vf "drawtext=fontfile=$FONT:text='TEXTE':fontsize=46:fontcolor=white:box=1:boxcolor=black@0.55:boxborderw=18:x=90:y=h-text_h-100:enable='between(t,1.3,3.1)'" \
  -af "loudnorm=I=-16:TP=-1.5:LRA=11" -c:v libx264 -crf 20 -pix_fmt yuv420p -c:a aac -movflags +faststart final.mp4

# Vérif frame-exacte du rendu
ffprobe -v error -select_streams v:0 -count_frames -show_entries stream=nb_read_frames -of csv=p=0 final.mp4
```
Fichiers annexes : `scripts/build_opt3_cli.sh` (générateur CLI complet, validé ; lancer depuis le dossier projet contenant `raw/` et `segs/`, ou `build_opt3_cli.sh <dossier_projet>`), `scripts/gen_melt_xml.py` (variante XML — référence SEULEMENT : rend 0,04 s sur melt 7.28.0, cf. piège §1 ; pour du XML valide, le générer via `melt … in=X out=Y -consumer xml` puis absolutiser les chemins `resource`).

## 5. verify_sync.py — validation de synchro par whisper

`scripts/verify_sync.py <fichier.mp4>` : extrait des fenêtres audio, transcrit avec faster-whisper (`word_timestamps=True`), compare la position mesurée de mots-marqueurs à leur position théorique dans la timeline, imprime le delta par checkpoint.

```bash
cd /tmp && HTTP_PROXY= HTTPS_PROXY= HF_HOME=/tmp/hf_cache \
  uv run --with faster-whisper --with "av<14" python3 ~/.agents/skills/video-montage/scripts/verify_sync.py final.mp4
```
(`av<14` : pin obligatoire, sinon `ModuleNotFoundError: No module named 'faster_whisper'` lié à l'API av.)

⚠️ **La liste `CK` est spécifique au projet night-game** : éditer les tuples `(motif, temps_attendu_s, début_fenêtre, durée_fenêtre, langue)` avec les mots-verbatim de VOTRE timeline avant usage.

**Si dérive détectée (> 0,20 s)** : (1) vérifier que les `in=`/`out=` sont bien respectés (test `-consumer xml` + grep, ou écouter si un clip démarre du début du fichier) ; (2) si le rendu vient d'un concat ffmpeg → rebasculer sur melt une passe §4 ; (3) ne JAMAIS "corriger" par un `-itsoffset` global — la dérive cumulée n'est pas uniforme.

## 6. Environnement

- **melt** : absent du PATH système → `nix-shell -p mlt --run "melt ..."` (melt 7.28.0 testé en réel 2026-10). Toujours `export HTTP_PROXY= HTTPS_PROXY=` avant (nix-shell + proxy = lenteurs).
- **ffmpeg / ffprobe** : dispo système (`/run/current-system/sw/bin/ffmpeg`).
- **yt-dlp** : `~/.local/bin/yt-dlp` via `uv tool install` (§2).
- Profils melt usuels : `atsc_720p_30` (1280x720@30). Coupes `in=`/`out=` en **frames**, jamais en secondes.

## Recherche d'un skill existant (2026-10-27)

Rien de réutilisable couvrant melt/MLT ou l'anti-drift : `skills.sh` "melt" → skill git-merge homonyme ; GitHub "claude skill video editing" → skills Remotion/CapCalc/captions/vertical (ecc, maxazure, herk-edit-kit) sans melt ni doctrine de synchro. Créé from scratch — voir `RECHERCHE.md`.
