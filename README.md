# Sales-USA-ETL-Pipeline
Automated ETL Pipeline using Python (Pandas) &amp; PostgreSQL. Transformation of raw Sales CSV data into a Star Schema for BI optimization. Features: logging, data cleaning, and relational modeling.

Sales Intelligence USA - Pipeline ETL Automatisé 🚀
📌 Contexte du Projet
Ce projet est né d'un besoin métier concret : analyser les performances de vente d'une entreprise aux USA sur l'année 2019. Initialement, les données étaient dispersées dans 12 fichiers CSV distincts (un par mois), totalisant plus de 186 000 lignes.

L'objectif de cette première phase est de sortir du traitement manuel en automatisant l'extraction, la transformation et le stockage des données dans une base relationnelle performante.

🛠 Stack Technique
Langage : Python 3.x

Librairies : Pandas (Traitement de données), SQLAlchemy (Interface DB), Psycopg2

Base de données : PostgreSQL

Environnement : Jupyter Notebook (Exploration) & Scripts Python (Production)

🏗 Architecture & Méthodologie
1. Extraction & Nettoyage
Fusion automatisée des 12 fichiers mensuels.

Gestion des valeurs manquantes et suppression des lignes erronées.

Normalisation des types de données (Conversion des dates et des montants).

2. Modélisation (Star Schema)
Pour optimiser les futures analyses BI, j'ai décomposé le schéma plat en un Schéma en Étoile :

Table de Fait : Ventes (Quantités, Prix).

Tables de Dimensions : dim_produit, dim_commande, dim_date, dim_adresse.

Innovation : Création d'un ID_unique pour garantir l'intégrité référentielle malgré l'absence d'identifiant natif dans les sources.

3. Fiabilité & Maintenance (Logging)
J'ai implémenté un système de Logging robuste pour répondre aux exigences de production :

Traçabilité : Chaque étape (Lecture, Transformation, Chargement) est consignée.

Gestion des erreurs : Utilisation de blocs try...except pour capturer les anomalies sans interrompre le pipeline.

Audit : Un fichier .log est généré pour permettre au data manager de vérifier l'historique des exécutions.

🚀 Installation & Utilisation
Cloner le répertoire : git clone ...

Créer l'environnement virtuel : python -m venv env

Installer les dépendances : pip install -r requirements.txt

Lancer l'ETL : python main.py

📈 Prochaines étapes
[ ] Connexion de la base PostgreSQL à Power BI.

[ ] Création d'un dashboard interactif (KPIs de CA, Top Produits, Analyse Géographique).

[ ] Mise en place d'alertes automatiques sur les anomalies de données.
