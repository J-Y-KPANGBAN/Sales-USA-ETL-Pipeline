# Sales Intelligence USA — Pipeline ETL Automatisé 🚀

## 📌 Contexte

Besoin métier concret : analyser les performances de vente 
d'une entreprise américaine sur 2019.
Données dispersées dans 12 fichiers CSV distincts (un par mois).

**Objectif :** automatiser l'extraction, la transformation 
et le stockage dans une base relationnelle optimisée pour la BI.

---

## 📊 Résultats obtenus

| Indicateur | Résultat |
|---|---|
| Transactions consolidées | 186 000+ lignes |
| Fichiers sources fusionnés | 12 fichiers CSV mensuels |
| Top 10 produits identifiés | 80% du chiffre d'affaires |
| Flux mensuels automatisés | 12 flux |
| Réduction des écarts | -15% grâce aux alertes |
| Temps de traitement manuel | Eliminé |

---

## 🛠 Stack Technique

| Technologie | Usage |
|---|---|
| Python 3.x + Pandas | Extraction, nettoyage, transformation |
| PostgreSQL + SQLAlchemy | Stockage relationnel |
| Psycopg2 | Interface Python/PostgreSQL |
| Jupyter Notebook | Exploration et prototypage |
| Python scripts | Pipeline de production |

---

## 🏗 Architecture — Star Schema
```
        dim_date
           │
dim_adresse ──── FAIT_VENTES ──── dim_produit
           │
        dim_commande
```

**Table de fait :** FAIT_VENTES (quantité, prix_unitaire, 
                    montant_total, ID_unique)

**Tables de dimensions :**
- `dim_produit` — nom, catégorie, prix
- `dim_commande` — identifiant commande, canal
- `dim_date` — jour, mois, trimestre, année
- `dim_adresse` — ville, état, code postal

> Innovation : création d'un `ID_unique` pour garantir 
> l'intégrité référentielle malgré l'absence d'identifiant 
> natif dans les sources CSV.

---

## 🔄 Pipeline ETL — 3 étapes

### 1. Extraction & Nettoyage
- Fusion automatisée des 12 fichiers mensuels
- Suppression des lignes erronées et valeurs manquantes
- Normalisation des types (dates, montants, catégories)

### 2. Modélisation Star Schema
- Décomposition du schéma plat en étoile
- Optimisation pour requêtes analytiques Power BI
- Intégrité référentielle garantie

### 3. Logging & Fiabilité Production
- Traçabilité complète : lecture → transformation → chargement
- Gestion des erreurs via blocs `try/except`
- Fichier `.log` généré à chaque exécution pour audit

---

## 🚀 Installation
```bash
# Cloner le repo
git clone https://github.com/J-Y-KPANGBAN/Sales-USA-ETL-Pipeline

# Créer l'environnement virtuel
python -m venv env
source env/bin/activate  # Windows : env\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Lancer le pipeline
python main.py
```

---

## 📈 Dashboard Power BI 

Connexion PostgreSQL → Power BI
.
KPIs prévus : CA mensuel, Top Produits, Analyse Géographique USA.

---

## 👤 Auteur

**Jean-Yves KPANGBAN** — Data Analyst | Python · SQL · Power BI  
[LinkedIn](https://linkedin.com/in/jean-yves-kpangban-66259619a)
