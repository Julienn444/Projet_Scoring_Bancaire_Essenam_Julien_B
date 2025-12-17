# ============================
# mongo_streamlit.py
# ============================

import streamlit as st
from pymongo import MongoClient
import pandas as pd
import requests

# ============================
# CONFIG
# ============================

MONGO_URI = "mongodb+srv://sdv_user:SDV2025@cluster0.t2ptc.mongodb.net/?retryWrites=true&w=majority"
DB_NAME = "default_risk"
COLLECTION_NAME = "users_data"

FLASK_API_URL = "http://localhost:5000"

st.set_page_config(page_title="Risk Banking", layout="wide")
st.title("🔮 Prédiction de Défaut Client")

st.info(
    "📊 **SIMULATION DE RISQUE** — Cette page permet d’estimer la probabilité "
    "de défaut d’un client à partir de son identifiant."
)

# ============================
# FONCTIONS MÉTIER (SLIDE)
# ============================

@st.cache_resource
def get_mongo():
    return MongoClient(MONGO_URI)

@st.cache_data
def load_test_data():
    return pd.read_csv("test.csv")

def get_client_personal_data(client_id: int):
    """
    1️⃣ Récupération des données personnelles depuis MongoDB
    """
    mongo = get_mongo()
    collection = mongo[DB_NAME][COLLECTION_NAME]
    return collection.find_one({"SK_CURR_ID": client_id})

def predict_default_risk(client_id: int, income: float, credit: float, annuity: float):
    """
    2️⃣ Appel API Flask /predict_default
    ⚠️ LOGIQUE STRICTEMENT IDENTIQUE À app.py
    """
    response = requests.get(
        f"{FLASK_API_URL}/predict_default",
        params={
            "client_id": client_id,
            "income": income,
            "credit": credit,
            "annuity": annuity
        }
    )
    return response.json()

def risk_gauge(score: float):
    percent = round(score * 100, 1)
    st.markdown(
        f"""
        <style>
        .risk-bar {{
            height: 10px;
            border-radius: 5px;
            background: linear-gradient(
                to right,
                #2ecc71,
                #f1c40f,
                #e67e22,
                #e74c3c
            );
            position: relative;
        }}
        .risk-dot {{
            position: absolute;
            left: {percent}%;
            top: -6px;
            width: 14px;
            height: 14px;
            background: white;
            border: 3px solid #333;
            border-radius: 50%;
            transform: translateX(-50%);
        }}
        </style>

        <div class="risk-bar">
            <div class="risk-dot"></div>
        </div>
        <div style="display:flex; justify-content:space-between; font-size:12px;">
            <span>Faible</span><span>Élevé</span>
        </div>
        <div style="text-align:right; font-weight:bold;">{percent} %</div>
        """,
        unsafe_allow_html=True
    )

# ============================
# SIDEBAR (COMME LE SCREEN)
# ============================

st.sidebar.subheader("🔍 Rechercher un client")
client_id_input = st.sidebar.text_input("ID Client")
analyze = st.sidebar.button("🔴 Analyser le risque")

# ============================
# LOGIQUE PAGE
# ============================

if analyze and client_id_input:

    client_id = int(client_id_input)

    # 1️⃣ MongoDB — identité
    client = get_client_personal_data(client_id)
    if not client:
        st.error("Client non trouvé dans MongoDB")
        st.stop()

    # 2️⃣ CSV — données financières
    df_test = load_test_data()
    row = df_test[df_test["SK_ID_CURR"] == client_id]

    if row.empty:
        st.error("Client non trouvé dans test.csv")
        st.stop()

    row = row.iloc[0]

    income = float(row["AMT_INCOME_TOTAL"])
    credit = float(row["AMT_CREDIT"])
    annuity = float(row["AMT_ANNUITY"])

    # ============================
    # PROFIL CLIENT
    # ============================

    st.divider()
    col_img, col_name = st.columns([1, 4])

    with col_img:
        if client.get("PhotoURL"):
            st.image(client["PhotoURL"], width=120)

    with col_name:
        st.subheader(f"{client.get('FirstName')} {client.get('LastName')}")
        st.caption(f"ID Client : {client_id}")

    # ============================
    # APPEL API FLASK
    # ============================

    result = predict_default_risk(client_id, income, credit, annuity)

    if "prediction" not in result:
        st.error("Erreur lors de la prédiction")
        st.stop()

    risk_score = result["prediction"]["risk_score"]

    # ============================
    # RÉSULTAT ANALYSE
    # ============================

    st.divider()
    st.subheader("📊 Résultat de l’analyse de risque")
    risk_gauge(risk_score)

    st.markdown("### Recommandation")

    if risk_score >= 0.7:
        st.error("🔴 Refus recommandé – Risque élevé")
    elif risk_score >= 0.4:
        st.warning("🟠 Acceptation conditionnelle – Risque modéré")
    else:
        st.success("🟢 Acceptation recommandée – Risque faible")

    st.markdown(
        f"""
        **Montant demandé** : {credit:,.0f} €  
        **Ratio crédit / revenu** : {(credit / income):.2f}  
        **Date d’analyse** : aujourd’hui
        """
    )
