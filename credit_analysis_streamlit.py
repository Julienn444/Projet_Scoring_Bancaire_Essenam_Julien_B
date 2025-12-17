# ============================
# credit_analysis_streamlit.py
# ============================

import streamlit as st
import pandas as pd
import plotly.express as px

# ============================
# CONFIG
# ============================

st.set_page_config(
    page_title="Analyse de Données Crédit",
    layout="wide"
)

st.title("📊 Analyse de Données Crédit")
st.info(
    "Explorez les facteurs qui influencent le risque de défaut "
    "à travers des visualisations interactives."
)

# ============================
# LOAD DATA
# ============================

@st.cache_data
def load_credit_data():
    return pd.read_csv("application_train.csv")

df = load_credit_data()

# ============================
# SIDEBAR – FILTRES
# ============================

st.sidebar.subheader("🔎 Filtres d’analyse")

analysis_type = st.sidebar.radio(
    "Thématique",
    [
        "Ancienneté d'emploi",
        "Montant de crédit",
        "Revenu",
        "Famille & enfants"
    ]
)

min_credit, max_credit = st.sidebar.slider(
    "Montant de crédit (€)",
    int(df["AMT_CREDIT"].min()),
    int(df["AMT_CREDIT"].max()),
    (
        int(df["AMT_CREDIT"].quantile(0.05)),
        int(df["AMT_CREDIT"].quantile(0.95))
    )
)

min_income = st.sidebar.slider(
    "Revenu annuel minimum (€)",
    int(df["AMT_INCOME_TOTAL"].min()),
    int(df["AMT_INCOME_TOTAL"].max()),
    int(df["AMT_INCOME_TOTAL"].quantile(0.05))
)

run_analysis = st.sidebar.button("📈 Générer l’analyse")

# ============================
# CORE FUNCTIONS
# ============================

def load_credit_analysis_data(analysis_type, min_credit, max_credit, min_income):
    filtered = df[
        (df["AMT_CREDIT"] >= min_credit) &
        (df["AMT_CREDIT"] <= max_credit) &
        (df["AMT_INCOME_TOTAL"] >= min_income)
    ]

    if analysis_type == "Ancienneté d'emploi":
        filtered = filtered.copy()
        filtered["YEARS_EMPLOYED"] = filtered["DAYS_EMPLOYED"].apply(
            lambda x: 0 if x == 365243 else -x / 365.25
        )
        filtered["EMPLOYMENT_GROUP"] = pd.cut(
            filtered["YEARS_EMPLOYED"],
            bins=[-1, 1, 3, 5, 10, 100],
            labels=["< 1 an", "1-3 ans", "3-5 ans", "5-10 ans", "> 10 ans"]
        )

        result = filtered.groupby("EMPLOYMENT_GROUP").agg(
            DEFAULT_RATE=("TARGET", "mean"),
            CLIENT_COUNT=("TARGET", "count")
        ).reset_index()

        result["DEFAULT_RATE"] *= 100
        return result, "EMPLOYMENT_GROUP", "DEFAULT_RATE"

    if analysis_type == "Montant de crédit":
        filtered = filtered.copy()
        filtered["CREDIT_BUCKET"] = pd.qcut(
            filtered["AMT_CREDIT"], 5
        ).astype(str)   # ✅ FIX ICI

        result = filtered.groupby("CREDIT_BUCKET").agg(
            DEFAULT_RATE=("TARGET", "mean"),
            CLIENT_COUNT=("TARGET", "count")
        ).reset_index()

        result["DEFAULT_RATE"] *= 100
        return result, "CREDIT_BUCKET", "DEFAULT_RATE"

    if analysis_type == "Revenu":
        filtered = filtered.copy()
        filtered["INCOME_BUCKET"] = pd.qcut(
            filtered["AMT_INCOME_TOTAL"], 5
        ).astype(str)

        result = filtered.groupby("INCOME_BUCKET").agg(
            DEFAULT_RATE=("TARGET", "mean"),
            CLIENT_COUNT=("TARGET", "count")
        ).reset_index()

        result["DEFAULT_RATE"] *= 100
        return result, "INCOME_BUCKET", "DEFAULT_RATE"

    if analysis_type == "Famille & enfants":
        result = filtered.groupby("CNT_CHILDREN").agg(
            DEFAULT_RATE=("TARGET", "mean"),
            CLIENT_COUNT=("TARGET", "count")
        ).reset_index()

        result["DEFAULT_RATE"] *= 100
        return result, "CNT_CHILDREN", "DEFAULT_RATE"

def display_plotly_chart(df_plot, x_col, y_col, title):
    fig = px.bar(
        df_plot,
        x=x_col,
        y=y_col,
        color="CLIENT_COUNT",
        color_continuous_scale="Viridis",
        title=title,
        labels={y_col: "Taux de défaut (%)"}
    )
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)

def display_key_metrics(filtered_df):
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Clients analysés", f"{len(filtered_df):,}")
    col2.metric("Taux défaut moyen", f"{filtered_df['TARGET'].mean() * 100:.1f}%")
    col3.metric(
        "Ratio crédit / revenu",
        f"{(filtered_df['AMT_CREDIT'] / filtered_df['AMT_INCOME_TOTAL']).mean():.2f}"
    )
    col4.metric(
        "Crédit moyen",
        f"{filtered_df['AMT_CREDIT'].mean() / 1000:.0f} K€"
    )

def display_recommendations(analysis_type):
    st.subheader("📌 Recommandations")

    col1, col2 = st.columns(2)

    with col1:
        st.success(
            f"""
            **Optimisation du risque**
            - Ajuster les seuils selon **{analysis_type.lower()}**
            - Renforcer le contrôle des segments à risque
            """
        )

    with col2:
        st.info(
            """
            **Actions métiers**
            - Réviser les politiques d’octroi
            - Mettre en place un suivi renforcé
            """
        )

def display_active_filters(min_credit, max_credit, min_income):
    st.markdown(
        f"""
        🧮 **Filtres actifs**
        - Crédit : {min_credit:,} € → {max_credit:,} €
        - Revenu min : {min_income:,} €
        """
    )

# ============================
# PAGE RENDER
# ============================

if run_analysis:

    filtered_df = df[
        (df["AMT_CREDIT"] >= min_credit) &
        (df["AMT_CREDIT"] <= max_credit) &
        (df["AMT_INCOME_TOTAL"] >= min_income)
    ]

    display_active_filters(min_credit, max_credit, min_income)
    display_key_metrics(filtered_df)

    plot_df, x_col, y_col = load_credit_analysis_data(
        analysis_type,
        min_credit,
        max_credit,
        min_income
    )

    st.subheader(f"📈 {analysis_type}")
    display_plotly_chart(plot_df, x_col, y_col, analysis_type)

    display_recommendations(analysis_type)
