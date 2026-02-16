# Football Match Winner Prediction ⚽️

Projet de Data Science : prédire le résultat d’un match de football (1 / X / 2) à partir des données historiques (forme, Elo, avantage domicile, etc.).
Option d’amélioration : intégrer des informations joueurs (lineups/absences) via StatsBomb Open Data.

## Objectifs
- Construire un pipeline complet : données → nettoyage → features → modèles → évaluation → interprétation.
- Comparer un **baseline** (Elo / forme) avec des modèles ML plus avancés.

## Données
### V1 (MVP) — Match-level dataset
Historique des matchs : date, équipes, score, (éventuellement stats comme tirs/cartons/corners).

### V2 (Amélioration) — StatsBomb Open Data
Ajout possible de :
- lineups (joueurs présents)
- événements (tirs, passes, etc. selon dispo)

> Note : on ne versionne pas les données brutes dans Git (voir `.gitignore`).

## Structure du projet
