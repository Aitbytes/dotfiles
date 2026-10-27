# Symphony (YC, robotique agricole)

## Overview
Startup du batch YC visitée en immersion 24 h (chaîne productrice non renseignée dans les métadonnées) : Symphony équipe des modèles d'IA de bases mobiles robotiques pour travailler dans les champs — défi n°1 : cueillir des fraises sans les écraser. Sa thèse : la main-d'œuvre représente ~60 % des coûts agricoles, et elle se positionne comme la couche de déploiement physique de l'IA, en commençant par « le problème physique le plus dur des 3 prochaines années » comme preuve de plateforme. Limites du contenu : visite promotionnelle, aucun chiffre de revenus ni de coût unitaire par fraise cueillie.

## Frameworks & idées signature
- **Beachhead par le problème le plus dur** : attaquer la fraise (fruit délicat, environnement non structuré) crédibilise toute la plateforme de déploiement d'IA physique.
- **Itération hardware brutale** : en fin de batch YC, le modèle de cueillette performait mais le châssis mobile ne suivait pas — teardown complet et reconstruction (Asher V3), testée en conditions réelles (poussière, vent, pluie, vibrations).
- **Stack système** : modèles de fondation (notamment Generalist AI) + collecte de données par démonstrations répétées + « magic box » (cortex central) + GPU embarqués (réseau du champ trop lent) + streaming satellite à 450 Mbit/s testé sur place.
- **Data flywheel observable** : en un mois, le robot distingue fraises mûres/immatures ; en 2-3 mois, les fraises écrasées passent de « presque toutes » à rares — pendant le seul batch YC.
- **Vision mesurable** : « We are going to decrease the costs of food » — un résultat concret plutôt qu'une promesse d'abondance abstraite.

## Vidéos couvertes dans le corpus

### 24h Inside the YC Startup Going After Farming's 60% Labor Bill
- **Lien** : https://www.youtube.com/watch?v=ViQBOjQ4rLY · **Source** : Historique #426
- **Résumé** : Immersion d'une journée avec Symphony : la startup teste en conditions réelles son robot de cueillette de fraises, après un démontage complet de son hardware mobile en fin de batch YC. Elle se positionne comme la couche de déploiement physique de l'IA, avec un premier client (Genac, fermes de fraises en Californie du Sud) et l'ambition de faire baisser le coût de la nourriture. La vidéo montre aussi le déroulé réaliste d'une journée de test : circuit grillé, ~4 600 W tirés qui font tomber le générateur, échec du jour, succès le lendemain.
- **Idées clés** :
  - La main-d'œuvre = ~60 % des coûts agricoles ; les emplois dangereux coûtent cher et les robots peuvent les prendre tout en abaissant le prix payé par les consommateurs.
  - L'environnement comme contrainte produit : poussière, vent, précipitations, lumière, vibrations — un problème système et logistique, pas seulement de modèle.
  - Courbe d'apprentissage du robot observable en semaines pendant le batch.
  - « It was like watching an alien learn to walk » — l'itération publique comme preuve.
  - Le demo day comme deadline compressant toutes les décisions d'architecture.
- **Conseils actionnables** :
  - Choisissez comme premier client le problème le plus difficile de votre secteur : le résoudre crédibilise toute votre plateforme.
  - Entraînez sur ce que le client veut réellement, pas sur ce qu'il dit vouloir.
  - Assumez l'itération matérielle complète quand le hardware freine le logiciel — n'empilez pas de rustines.
  - Concevez pour les conditions réelles dès le prototype, pas après le demo day.
  - Formulez votre vision en résultat concret et mesurable plutôt qu'en promesse abstraite.
- **Citations** :
  - « We are going to decrease the costs of food. »
  - « It was like watching an alien learn to walk. »

## Quand consulter cette référence
Pour des leçons de deep tech et de physical AI : choix du beachhead par la difficulté, itération hardware en conditions réelles, et exécution sous deadline YC.
