
# 📊 Plateforme de Scoring Bancaire & Analyse de Risque Client

## 📌 Description du projet

Ce projet a pour objectif de développer une application de **scoring bancaire** permettant d’estimer le **risque de défaut de paiement** d’un client à partir de ses données financières et socio‑professionnelles.

L’application s’adresse à un **conseiller bancaire** qui peut :
- Rechercher un client par identifiant
- Visualiser ses informations personnelles
- Obtenir un score de risque en pourcentage
- Explorer des analyses statistiques sur les données crédit

Le projet s’inscrit dans un contexte pédagogique Big Data & Cloud (M2 DATA).

---

## 🎯 Objectifs

- Implémenter un modèle de Machine Learning pour le scoring crédit
- Mettre en place une API REST pour exposer les prédictions
- Développer une interface utilisateur interactive
- Proposer des visualisations explicables et orientées métier
- Concevoir une architecture évolutive vers le cloud

---

## 🧱 Architecture technique

**Frontend**
- Streamlit (interface utilisateur)

**Backend**
- Flask (API REST)

**Machine Learning**
- Scikit‑learn
- Modèle : Régression Logistique
- Sérialisation : Joblib

**Données**
- MongoDB : informations clients
- Fichiers CSV : données crédit (`application_train.csv`)

```
Streamlit
   |
   | HTTP Requests
   v
Flask API (app.py)
   |
   | Modèle ML (joblib)
   |
MongoDB + CSV
```

---

## 🐍 Scripts Python

- `train_model.py` : entraînement du modèle de Machine Learning
- `app.py` : API Flask (`/health`, `/predict_default`)
- `mongo_streamlit.py` : page Streamlit de prédiction client
- `credit_analysis_streamlit.py` : page Streamlit d’analyse des données crédit

---

## 📓 Notebooks

- `TP5_Streamlit.ipynb`
  - Exploration des données
  - Compréhension du problème métier
  - Analyses descriptives

---

## ⚙️ Installation et configuration

### Prérequis
- Python 3.10+
- pip

### Installation

```bash
git clone <url-du-repository>
cd scoring-bancaire
pip install -r requirements.txt
```

### Configuration

Créer un fichier `.env` à partir de `.env.example` et renseigner :
- URI MongoDB
- Variables d’environnement nécessaires

---

## ▶️ Utilisation de l’application

### 1️⃣ Lancer l’API Flask

```bash
python app.py
```

L’API est accessible sur :
```
http://localhost:5000
```

### 2️⃣ Lancer Streamlit

```bash
streamlit run mongo_streamlit.py
```

### 3️⃣ Parcours utilisateur

- Entrer un identifiant client
- Charger les informations personnelles (MongoDB)
- Calcul du score de risque via l’API Flask
- Visualisation du score, recommandations et graphiques
- Navigation vers la page d’analyse des données crédit

---

## 📈 Modèle de Machine Learning

- Modèle utilisé : **Régression Logistique**
- Type : Classification binaire
- Cible : Défaut de paiement (0 / 1)
- Sortie principale : **probabilité de défaut**

Le score affiché dans l’interface correspond à la probabilité fournie par la méthode `predict_proba()`.

### Avantages du modèle
- Rapide
- Interprétable
- Adapté au contexte bancaire

---

## 📊 Résultats et métriques

- Le modèle fournit un score de risque en pourcentage
- Une décision binaire est obtenue par application d’un seuil métier
- L’analyse statistique permet d’identifier les facteurs influençant le risque

Ce projet privilégie l’interprétabilité et la clarté plutôt que l’optimisation extrême des performances.

---

## 🚀 Perspectives d’amélioration

- Modèles avancés : XGBoost, Random Forest
- Explicabilité : SHAP pour interprétation client par client
- Historisation des décisions
- Déploiement cloud (Azure)
- Monitoring des performances du modèle

---

## 👥 Collaboration

Projet réalisé en binôme dans le cadre du Master 2 DATA.
