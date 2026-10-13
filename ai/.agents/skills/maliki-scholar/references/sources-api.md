# Sources & API Cookbook — Assistant malikite

Recettes concrètes pour vérifier textes et citations. Outils pi à utiliser : `fetch_content`, `web_search`, `bash` (curl), `code_search`.

---

## 1. Coran — API quran.com v4 (gratuite, sans clé)

Texte arabe (Hafs) + 100+ traductions. ID utiles : EN Saheeh International `131`, FR Hamidullah `166` (⚠ vérifier les IDs via l'endpoint resources), FR Peeters `500`.

```bash
# Verset exact (arabe + EN)
curl "https://api.quran.com/api/v4/verses/by_key/2:255?translations=131&fields=text_uthmani"

# Recherche par mot-clé
curl "https://api.quran.com/api/v4/search?q=patience&size=10&language=en"

# Chapitre complet
curl "https://api.quran.com/api/v4/chapters/1?language=fr"

# Lister les traductions disponibles (pour trouver l'ID français à jour)
curl "https://api.quran.com/api/v4/resources/translations?language=fr"
```

Fallback : `fetch_content` sur quran.com/{sourah}/{verset} ou quran.com API v4 doc : https://api.quran.com/api/v4/docs

## 2. Hadith — sunnah.com

**API officielle** (clé gratuite : https://sunnah.stoplight.io/docs/api/ — demander sur sunnah.com/developers) :

```bash
curl "https://api.sunnah.com/v1/hadiths/bukhari:1" -H "X-API-Key: VOTRE_CLE"
```

**Sans clé** — fetch des pages publiques :

```
https://sunnah.com/bukhari:1
https://sunnah.com/muslim:1a
https://sunnah.com/nasai:1
https://sunnah.com/abudawud:1
https://sunnah.com/tirmidhi:1
https://sunnah.com/ibnmajah:1
https://sunnah.com/malik:1   ← Muwatta Malik (essentiel pour le madhab)
```

**Corpus JSON brut** (GitHub `AhmedBaset/hadith-json`, les 9 livres, AR+EN) :

```bash
curl -L "https://raw.githubusercontent.com/AhmedBaset/hadith-json/main/db/by_book/the_9_books/malik.json" -o muwatta.json
# autres : bukhari.json, muslim.json, abudawud.json, tirmidhi.json, nasai.json, ibnmajah.json...
```

Vérification d'authenticité : dorar.net (grades des savants), `web_search` "hadith [extrait] authenticity grading".

## 3. Livres arabes classiques

- **Shamela** (al-Maktaba al-Shamela, la plus grande bibliothèque arabe) : fetch `https://shamela.ws/book/{id}/{page}` ; recherche : `web_search "site:shamela.ws [titre]"` ou `fetch_content` sur shamela.ws.
- **library.islamic.app** : interface moderne (Mukhtasar Khalil dispo).
- **Risala de Qayrawani en anglais** (trad. Daura + commentaire ath-Thamr ad-Dani) :
  https://www.iium.edu.my/deed/lawbase/risalah_maliki/index.html
- **Mukhtasar al-Akhdari** (EN, trad. Aisha Bewley) : pdf circulant via Diwan Press / scribd — chercher avant usage.
- **Islamic Lawbase** (lawbase.qfi.org) : matn malikites annotés.

## 4. Datasets HuggingFace (téléchargement en masse)

```bash
# Exemple : FiqhQA (rulings par madhab, AR/EN)
curl -L "https://huggingface.co/datasets/MBZUAI/FiqhQA/resolve/main/data/train-00000-of-00001.parquet" -o fiqhqa.parquet

# API de prévisualisation (sans télécharger)
curl "https://datasets-server.huggingface.co/rows?dataset=islamic-datasets%2Ffiqh-maliki-talqin&config=default&split=train&offset=0&length=10"
```

| Dataset | Contenu | Taille |
|---|---|---|
| `MBZUAI/FiqhQA` | Rulings LLM classés hanafi/maliki/shafi'i/hanbali, AR+EN | benchmark |
| `islamic-datasets/fiqh-maliki-talqin` | At-Talqin (Qadi 'Abd al-Wahhab) en QA | léger |
| `islamic-datasets/Masadir-Maliki-Dataset` | Bibliographie QA du fiqh malikite | léger |
| `islamic-datasets/Istilah_Maliki_Dataset` | Terminologie du madhab | léger |
| `ghazaliDev/Muwatta_Malik` | Muwatta en dataset | moyen |
| `Yehuda-Rubin/islam-canonical-corpus` | Quran + collections majeures sunni/shia, JSON | moyen |
| `AuthenticIlm/Shamela4_Full_DB` | Shamela complète : 8 589 livres, 7,6 M pages | ~19 GB |
| `Kandil7/Athar-Datasets` | Corpus RAG citation-grounded (Quran, hadith, fiqh, tafsir) | moyen |
| GitHub `arabic-digital-humanities/fiqh` | 49 M tokens de furû', sous-corpus malikite 9,2 M tokens | lourd |

## 5. Chaîne de vérification recommandée (pour chaque réponse)

1. Citation Coran → API quran.com (texte exact).
2. Citation hadith → sunnah.com (page ou API) ; noter le grade si disponible.
3. Ruling / position malikite → Risala/Talqin/Khalil via Shamela, Lawbase, ou dataset FiqhQA (colonne maliki).
4. Incertain → `web_search` avec domaines restreints (sunnah.com, shamela.ws, dorar.net, islamqa.org qui indexe par madhab) et citer la source trouvée.
5. Rien ne confirme → le dire explicitement, ne jamais improviser.

## 6. Sites de référence par madhab (fallback web)

- **islamqa.org** — archive de fatwas classées par madhab (notamment section malikite).
- **dorar.net** — encyclopédie hadith avec grades + encyclopédie fiqh malikite (arabe).
- **fiqh.islammessage.com / alukah.net** — articles de fuqaha malikites contemporains.
- **SeekersGuidance** — réponses savantes malikites en anglais (Sh. Faraz Rabbani et al.).
- **Lamppost Productions / Musa Furber** — fiqh pondéré en anglais.
