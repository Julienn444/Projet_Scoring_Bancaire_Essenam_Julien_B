# ============================
# train_model.py
# ============================

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
import joblib

# Charger les données
df = pd.read_csv("application_train.csv")

# Variables simples pour un premier modèle propre
FEATURES = [
    "AMT_INCOME_TOTAL",
    "AMT_CREDIT",
    "AMT_ANNUITY"
]

TARGET = "TARGET"

# Nettoyage minimal
df = df.dropna(subset=FEATURES + [TARGET])

X = df[FEATURES]
y = df[TARGET]

# Pipeline ML
pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("model", LogisticRegression(max_iter=1000))
])

# Entraînement
pipeline.fit(X, y)

# Sauvegarde du modèle
joblib.dump(pipeline, "credit_model.pkl")

print("✅ Modèle entraîné et sauvegardé : credit_model.pkl")
