# Olly Rosewell

## Overview
Développeur-entrepreneur issu de Response AI, désormais enseignant la monétisation d'API sur sa plateforme roseorld.dev. Son angle : transformer une simple table de données en API payante avec facturation à l'appel (ex. 10 000 appels/mois pour ~20 $), avec autant d'attention à la logique business (clé = accès payant, rate limiting = protection du modèle économique, documentation = onboarding) qu'à la sécurité (hachage SHA-256, edge function « videur », RLS). Sa conviction produit : « the first successful call is your activation moment » — le vrai moment de conversion est le premier appel réussi.

## Frameworks & idées signature
- **API-as-a-service à l'appel** : abonnement par volume (10 000 appels/mois pour 20 $ ; exemple réel cité : YouTube Transcript API, 10 appels/jour gratuits ou 10 000/mois à 9 $).
- **Zero-knowledge storage** : ne jamais stocker la clé brute — uniquement son hash SHA-256 + un préfixe lisible (style Stripe) ; la clé n'existe qu'une fois, dans le presse-papier du client.
- **3 portes d'entrée pour délivrer les clés** : manuelle (10 premiers clients), webhook Stripe à paiement (pas de login), dashboard connecté.
- **L'edge function comme videur** : seul point de contact du monde extérieur, isolation totale de la base, révocation instantanée par suppression de ligne.
- **Design API comme produit** : endpoints en noms pluriels, statuts explicites (200, 201, 401, 404, 429, 500), pagination/filtre/tri côté serveur, versioning /v1 dès le jour 1.
- **Doc = onboarding** : « one curl command » qui réussit du premier coup = moment d'activation payant.

## Vidéos couvertes dans le corpus

### Build a Profitable API Like a $10M Company (full guide / beginner friendly)
- **Lien** : https://www.youtube.com/watch?v=Un2F0VeN-pE · **Source** : Watch Later #109
- **Résumé** : Tutoriel complet et « beginner friendly » pour transformer une table de données en API payante avec facturation à l'appel. À partir d'une base Supabase de propriétés fictives hantées, il construit les trois pièces d'un système de clés API : table de hashes SHA-256, fonction Postgres de génération, edge function qui hache, vérifie et sert les données. Il traite aussi la gated architecture (RLS, service_role côté serveur, HTTPS, anti-injection, CORS strict) et la distribution : un curl copiable qui marche du premier coup est le vrai moment d'activation.
- **Idées clés** :
  - Supabase génère une REST API JWT qui expire (~1 h) : inadaptée à un développeur client qui a besoin d'un badge permanent.
  - Rate limiting : 100 req/min par clé → 429 ; et plafond au niveau utilisateur sur un compteur non éditable (sinon clés illimitées pour contourner).
  - Statuts explicites : jamais de 200 avec erreur cachée dans le body.
  - Ne jamais tout renvoyer d'un coup : pagination côté serveur = signe d'une API « produit » vs « script de week-end ».
  - Versionner dès le jour 1, sinon chaque amélioration devient un breaking change.
  - Dashboard front construit avec Cursor (prompt fourni) : la logique compte, le styling est trivial.
- **Conseils actionnables** :
  - Choisis un dataset que des professionnels paieraient et expose-le via une edge function fermée, jamais la base en direct.
  - Hache toutes les clés (SHA-256), stocke un préfixe, montre la clé complète exactement une fois.
  - Impose une limite d'appels par clé ET par utilisateur, sur une table non éditable, avec un 429 clair.
  - Versionne ton API dès la première URL et documente-la avec un curl copier-coller qui marche du premier coup.
  - Valide chaque entrée utilisateur et n'assemble jamais de requêtes SQL par concaténation de chaînes.
- **Citations** :
  - « You never store the actual key anywhere, ever. If you store real keys and your database leaks, you become the breach. »
  - « The best API is one a developer can use without reading the docs. »
  - « That first successful call is your activation moment. Treat your docs as onboarding, because that's what they are. »

## Quand consulter cette référence
Pour monétiser un dataset ou une API en produit payant : architecture des clés, sécurité minimale viable, rate limiting et onboarding développeur.
