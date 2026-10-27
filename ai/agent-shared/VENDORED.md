# Binaires vendus (hors gestionnaires de paquets)

Tout binaire/script posé manuellement dans le PATH doit être listé ici avec
provenance, version et sha256. Vérification : `sha256sum ~/.local/bin/<nom>`.

| Binaire | Type | Version | Provenance | sha256 (16) |
|---|---|---|---|---|
| `gws` | ELF Go (~19 Mo) | 0.22.5 | Google Workspace CLI — release GitHub du projet amont | `ab59c4bab4e78487…` |
| `linkedin-dm` | ELF Go (~10 Mo) | n/a (pas de flag version) | CLI interne GraphQL LinkedIn — rebuild depuis source privée | `8b4b2168d52f1ea2…` |
| `autocomplete.sh` | script bash (45 K) | ACSH 0.5.0 | ClosedLoop Technologies (MIT) — https://github.com/seankruzel/autocomplete.sh | `bf505cc3ebc14db0…` |

Règles :
1. Un binaire sans provenance documentée = candidat à la suppression.
2. Préférer uv tool / npm -g / nix pour tout ce qui est packagable.
3. Mettre à jour ce fichier à chaque upgrade manuel.
