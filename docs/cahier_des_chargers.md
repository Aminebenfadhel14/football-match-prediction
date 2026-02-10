# Cahier des charges — Prédiction du vainqueur d’un match de football

## 1. Objectif
Créer un modèle de Data Science capable de prédire le résultat d’un match de football à partir des données historiques.
Le modèle devra prédire :
- soit le résultat en 3 classes : Domicile (1) / Nul (X) / Extérieur (2)
- soit une version binaire : victoire domicile vs non-victoire domicile (optionnel)

## 2. Données
### Sources prévues
- Dataset “match-level” (historique des matchs : équipes, date, score, éventuellement stats)
- Option d’amélioration : StatsBomb Open Data (lineups + événements) pour intégrer l’impact des joueurs.

### Données utilisées (minimum)
- Date du match
- Équipe domicile / extérieur
- Buts domicile / extérieur (pour créer la variable cible)
- Ligue / saison (si disponible)

### Données dérivées (features)
- Forme récente (sur les 5 derniers matchs) : points, buts marqués/encaissés
- Avantage domicile
- Jours de repos depuis le dernier match
- Classement de force type Elo (calculé à partir des résultats)
- (Amélioration) Indicateurs joueurs : absences des joueurs clés, stabilité du XI

## 3. Périmètre du projet
### Inclus
- Collecte/chargement des données
- Nettoyage et préparation (valeurs manquantes, doublons, types)
- Analyse exploratoire (EDA) + visualisations
- Construction des features (rolling stats, Elo)
- Entraînement de plusieurs modèles (baseline + modèles avancés)
- Évaluation avec métriques adaptées
- Interprétation : importance des variables, analyse d’erreurs
- Rapport final + README + instructions d’exécution

### Non inclus (pour rester faisable)
- Prédiction “en temps réel” sur matchs du jour
- Scraping de sites interdits ou bloquants
- Modèles deep learning lourds (sauf bonus)

## 4. Méthodologie
- Découpage temporel : entraînement sur saisons anciennes, test sur saisons récentes (éviter fuite de données)
- Baseline : règle simple (ex : Elo seul / forme seule)
- Modèles ML : Logistic Regression, RandomForest / XGBoost (si autorisé), CatBoost (optionnel)

## 5. Métriques
- 3 classes : Accuracy, F1-macro, matrice de confusion
- Binaire : ROC-AUC + PR-AUC si déséquilibre
- Comparaison baseline vs modèle final

## 6. Livrables
- Repo Git structuré
- Notebook(s) EDA et Modélisation
- Code réutilisable dans `src/`
- Rapport synthèse (PDF ou Markdown)
- README complet (installation + exécution)

## 7. Répartition du travail
- Dev A : ingestion données + EDA + baseline
- Dev B : feature engineering + modèles + évaluation
- Travail commun : rédaction rapport + README


