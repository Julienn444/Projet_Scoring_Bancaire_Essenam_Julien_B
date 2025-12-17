# ============================
# app.py
# ============================

from flask import Flask, request, jsonify
import joblib
import pandas as pd
from datetime import datetime

app = Flask(__name__)

# Charger le modèle ML
model = joblib.load("credit_model.pkl")

FEATURES = [
    "AMT_INCOME_TOTAL",
    "AMT_CREDIT",
    "AMT_ANNUITY"
]

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"}), 200

@app.route("/predict_default", methods=["GET"])
def predict_default():
    try:
        client_id = request.args.get("client_id")

        # Récupération des features envoyées par Streamlit
        income = float(request.args.get("income"))
        credit = float(request.args.get("credit"))
        annuity = float(request.args.get("annuity"))

        # Création du DataFrame pour le modèle
        X = pd.DataFrame([{
            "AMT_INCOME_TOTAL": income,
            "AMT_CREDIT": credit,
            "AMT_ANNUITY": annuity
        }])

        # Prédiction ML réelle
        risk_score = model.predict_proba(X)[0][1]

        return jsonify({
            "client_id": client_id,
            "prediction": {
                "risk_score": round(float(risk_score), 3),
                "predicted_default": int(risk_score >= 0.5)
            },
            "metadata": {
                "model": "LogisticRegression",
                "timestamp": datetime.now().isoformat()
            }
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
