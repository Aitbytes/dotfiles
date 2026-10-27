# REA — Reverse Engineer Anything (Morluto)

## Overview
Outil du développeur Morluto (chaîne productrice non renseignée dans les métadonnées) : REA donne à un agent IA l'accès à une application pour analyser son fonctionnement, puis produit un rapport permettant à un agent de code (Codex, Claude Code, Cursor, Gemini CLI via serveurs MCP locaux) de construire une version équivalente. La vidéo du corpus en fait la démonstration sur Screen Studio (29 $/mois), étiquetée « piracy 2.0 » par l'auteur lui-même. Sa valeur pour le corpus : un cas limite qui montre où se déplace le moat du SaaS quand la fonction devient réversible — vers la distribution, la marque et l'itération continue.

## Frameworks & idées signature
- **Reverse engineering assisté par IA** : un rapport d'investigation automatisée alimente directement un agent de code via MCP — moins de tours d'essai-erreur, choix techniques mieux informés (frameworks Apple, event streams).
- **Comparaison A/B d'outils** : sans rapport, l'app générée fonctionne avec des défauts (feedback de clic raté, export 1080p) ; avec rapport, première version vérifiée en ~23 minutes et export 1440p.
- **Le polish comme moat résiduel** : la valeur de Screen Studio est le polish (zooms, suivi de curseur, cadrage, vidéo « partageable ») plus que la fonction d'enregistrement — la fonction seule n'est plus défendable.
- **Menace de substitution sur les abonnements** : la barrière technique d'un SaaS à 29 $/mois s'effondre ; le vrai fossé se déplace vers distribution, marque et maintenance continue.

## Vidéos couvertes dans le corpus

### I Reverse Engineered a $29/Month App in 23 Minutes
- **Lien** : https://www.youtube.com/watch?v=TbHiW-56q5Y · **Source** : Historique #300
- **Résumé** : Démonstration de REA sur Screen Studio : sans le rapport, l'app générée (Framecraft) fonctionne mais avec des défauts ; avec le rapport, FocusCut est vérifiée en ~23 minutes et exporte en 1440p, visuellement plus polie. L'agent explique que les findings Apple-framework ont guidé la capture et l'approche event-stream la gestion de projets. L'auteur pose le cadre « piracy 2.0 » et invite à choisir quelle app/feature reverse engineer en premier.
- **Idées clés** :
  - REA s'intègre aux agents de code existants via serveurs MCP locaux (Codex, Claude Code, Cursor, Gemini CLI).
  - Bénéfice mesurable : moins d'essai-erreur, polish supérieur dès la V1.
  - Implication marché : la fonction d'un SaaS petit ticket n'est plus un moat.
  - Tendance plus large du clonage assisté par IA.
  - Limite : ni la question légale du clonage ni les coûts cachés (maintenance, distribution) ne sont traités — le « 23 minutes » mesure le build, pas un business viable.
- **Conseils actionnables** :
  - Avant de payer un abonnement SaaS, évaluez ce qui est réellement défendable dans le produit : la fonction seule ne l'est plus.
  - Utilisez les rapports d'investigation automatisée pour réduire les cycles essai-erreur lors d'un build assisté par IA.
  - Testez en A/B la contribution d'un outil (avec/sans) pour mesurer sa valeur réelle.
  - Différenciez votre SaaS par la distribution et le polish continus plutôt que par des fonctionnalités réplicables.
- **Citations** :
  - « Some guy just created piracy 2.0! »
  - « The first working version was built and verified in about 23 minutes. »

## Quand consulter cette référence
Pour évaluer la défendabilité d'un SaaS à l'ère des agents de code : que reste-t-il quand la fonction devient clonable en une après-midi.
