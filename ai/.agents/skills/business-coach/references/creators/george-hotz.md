# George Hotz

## Overview
Hacker et entrepreneur américain, célèbre pour avoir débloqué l'iPhone puis fondé comma.ai et TinyCorp (tinygrad). Dans le corpus, il apparaît à travers un long stream mi-philosophique mi-technique où il joue les iconoclastes du milieu tech : charge contre le trading haute fréquence (« jeu à somme nulle »), contre une grande partie du B2B SaaS (« économie factice »), contre YC (« l'entrepreneuriat TM en boîte ») et contre les entreprises d'Elon Musk (« monarchies compétentes » sans gouvernance auto-perpétuante). Sa crédibilité vient de sa pratique de premier plan du hardware IA : il dissèque la carte Tenstorrent Blackhole et loue la Radeon 9070 XT sous tinygrad, dont il vante l'efficacité — il a investi 250 000 $ en AMD.

## Frameworks & idées signature
- **Revenus circulaires / B2B SaaS factice** : deux sociétés se facturent mutuellement des services et bookent la somme en revenu pour lever des fonds ; « ce qui est produit, c'est à peu près rien ».
- **Loi de Goodhart** : « quand une mesure devient une cible, elle cesse d'être une bonne mesure » — les ventes de devices mesurent la qualité du produit mais ne doivent pas être optimisées directement.
- **Somme nulle vs somme positive** : en HFT « tu ne peux jamais gagner » ; il ne gagne à grande échelle qu'en créant de la valeur qui n'existait pas.
- **Gouvernance des organisations** : « une bonne dictature est toujours plus efficace qu'une démocratie ; le problème, c'est qu'une mauvaise dictature est bien pire » — Linus Torvalds et les fondations open source comme institutions auto-perpétuantes face aux monarchies type Musk.
- **Stacks simples vs grandes organisations** : « les stacks logicielles complexes privilégient les grandes organisations ; les stacks simples privilégient les individus ».
- **Stratégie de challenger** : AMD clone CUDA et se contente de 5-10 % de part de marché en maintenant la pression sur le monopoleur Nvidia.

## Vidéos couvertes dans le corpus

### "I like the CCP". B2B SaaS IS A SCAM. Linus vs Elon. Jack Ma.
- **Lien** : https://www.youtube.com/watch?v=4ctr4cv-Jr8 · **Source** : Historique #408
- **Résumé** : Stream long s'ouvrant sur la mortalité et le refus du « goal-oriented behavior », avant une charge contre le HFT et le B2B SaaS. Thèse centrale : une grande partie du B2B SaaS est une économie factice de facturations croisées ; Google et Facebook ont épuisé le TAM il y a ~15 ans, donc la seule marge restante est d'extraire plus par utilisateur captif. Il attaque YC comme écosystème capturé et les entreprises de Musk comme monarchies sans héritiers. La seconde moitié est une revue technique de la carte Tenstorrent Blackhole et de sa stack logicielle éclatée, face au contre-exemple de la Radeon 9070 XT sous tinygrad (334 Go/s, 83 % du débit théorique).
- **Idées clés** :
  - Schéma de revenus circulaires : « Company A is paying company B for services. Company B is paying company A. Both book that as revenue. »
  - Silicon Valley : passage de « créer plus de valeur » à « extraire plus de chaque utilisateur captif ».
  - YC : « They've sold you entrepreneurship TM in a box… You work for a company with extra steps. »
  - Jack Ma puni pour avoir voulu IPO-iser Alibaba en Occident : « le capital entre en Chine, le capital n'en sort pas ».
  - Tenstorrent : 9 ans d'existence pour « à peu près un devkit » ; PyTorch ne marche que via torch.compile ; stack confuse (TT-Forge/TT-Torch/TTNN/TT-MLIR).
  - AMD 9070 XT : moitié prix, plus de bande passante, 334 Go/s sous tinygrad ; stratégie du challenger assumée (250 000 $ investis).
  - LLMs optimisés pour plaire (« helpful vs harmful ») au lieu d'être accordés sur « truth vs falsehood ».
- **Conseils actionnables** :
  - Vérifie d'où vient réellement le revenu d'une entreprise (client final vs facturations croisées) avant d'investir ou de t'y associer.
  - Refuse toute métrique comme objectif : définis le but (qualité réelle du produit) et n'utilise les métriques que pour mesurer.
  - Ne bâtis pas en somme nulle : crée de la valeur nouvelle au lieu d'essayer de prendre celle des autres.
  - Privilégie les stacks simples et les dépendances minimales ; ne construis jamais dans le seul but d'être racheté.
  - Chasse la vérité plutôt que l'agrément : cherche ceux qui prédisent ta prochaine évolution de pensée (méthode Jim Keller).
- **Citations** :
  - « When a measure becomes a target, it ceases to be a good measure. »
  - « You can never win a zero-sum game. » (sur le HFT)

## Quand consulter cette référence
Pour développer un esprit critique sur les modèles économiques artificiels (SaaS gonflé, HFT), la loi de Goodhart en management, et la stratégie de challenger face à un monopole.
