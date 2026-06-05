import streamlit as st
import os
import pandas as pd
from src.dashboard.prediction import show_prediction
from src.dashboard.analytics import show_analytics
from src.dashboard.explainability import show_explainability


# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="EduShield AI",
    page_icon="🎓",
    layout="wide"
)
# =======================
# AUTH SYSTEM (NEW)
# =======================
USERS_FILE = "users.csv"

if not os.path.exists(USERS_FILE):
    pd.DataFrame(columns=["username", "password"]).to_csv(USERS_FILE, index=False)

def load_users():
    return pd.read_csv(USERS_FILE)

def save_user(username, password):
    df = load_users()

    username = username.strip()
    password = password.strip()

    if username in df["username"].astype(str).str.strip().values:
        return False

    new_row = pd.DataFrame([[username, password]], columns=["username", "password"])
    df = pd.concat([df, new_row], ignore_index=True)

    df.to_csv(USERS_FILE, index=False)
    return True

def authenticate(username, password):
    df = load_users()

    username = username.strip()
    password = password.strip()

    df["username"] = df["username"].astype(str).str.strip()
    df["password"] = df["password"].astype(str).str.strip()

    user = df[
        (df["username"].str.lower() == username.lower()) &
        (df["password"] == password)
    ]

    return not user.empty

# session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user" not in st.session_state:
    st.session_state.user = None

# =======================
# LOGIN / SIGNUP UI
# =======================
if not st.session_state.logged_in:

    menu = st.radio("Choose Action", ["Signup","Login"])

    if menu == "Signup":
        st.subheader("Create Account")

        new_user = st.text_input("Username")
        new_pass = st.text_input("Password", type="password")

        if st.button("Signup"):
            if save_user(new_user, new_pass):
                st.success("Account created! Please login.")
            else:
                st.error("User already exists!")

    else:
        st.subheader("Login")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if authenticate(username, password):
                st.session_state.logged_in = True
                st.session_state.user = username
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid credentials")

    st.stop()   # 🚨 STOP APP until login

# =======================
# LOGOUT BUTTON
# =======================
st.sidebar.success(f"Logged in as: {st.session_state.user}")

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.user = None
    st.rerun()
# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title("🎓 EduShield AI")

page = st.sidebar.radio(

    "Navigation",

    [
        "Home",
        "Prediction",
        "Analytics",
        "Explainability"
    ]
)

# ==========================================
# HOME PAGE
# ==========================================

if page == "Home":

    st.title("🎓 EduShield AI")

    st.subheader(
        "Student Dropout Prediction & Early Warning System"
    )

    st.markdown(
        """
        ### Project Overview

        EduShield AI helps educational institutions
        identify students who are at risk of dropping out
        using Machine Learning and Explainable AI.

        ### Features

        ✅ Data Pipeline

        ✅ Feature Engineering

        ✅ Model Training

        ✅ Model Evaluation

        ✅ Explainable AI (SHAP)

        ✅ Prediction Dashboard

        ✅ Analytics Dashboard

        ### Objective

        Detect at-risk students early and support
        timely intervention by educators.
        
        📍Technology Stack: 
        Python | Machine Learning | Streamlit | SHAP
        """
    )

# ==========================================
# PREDICTION PAGE
# ==========================================

elif page == "Prediction":

    show_prediction()

# ==========================================
# ANALYTICS PAGE
# ==========================================

elif page == "Analytics":

    show_analytics()

# ==========================================
# EXPLAINABILITY PAGE
# ==========================================

elif page == "Explainability":

    show_explainability()