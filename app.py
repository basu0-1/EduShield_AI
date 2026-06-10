import streamlit as st
import os
import pandas as pd

from src.dashboard.prediction import show_prediction
from src.dashboard.analytics import show_analytics
from src.dashboard.explainability_page import show_explainability
from src.dashboard.risk_decomposition import show_risk_decomposition
import bcrypt

# PAGE CONFIG & CSS LOADING
st.set_page_config(
    page_title="EduShield AI",
    page_icon="🎓",
    layout="wide"
)

def load_css():
    css_path = "styles/style.css"
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# AUTH SYSTEM
USERS_FILE = "users.csv"
if not os.path.exists(USERS_FILE):
    pd.DataFrame(columns=["username", "password"]).to_csv(USERS_FILE, index=False)

def load_users():
    return pd.read_csv(USERS_FILE)

def save_user(username, password):
    df = load_users()
    username = username.strip()
    password = password.strip()
    
    if username.lower() in (df["username"].astype(str).str.strip().str.lower().values):
        return False

    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    new_row = pd.DataFrame([[username, hashed_password]], columns=["username", "password"])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(USERS_FILE, index=False)
    return True

def authenticate(username, password):
    df = load_users()
    username = username.strip()
    password = password.strip()
    
    user_row = df[df["username"].astype(str).str.strip().str.lower() == username.lower()]
    if user_row.empty:
        return False
        
    stored_hash = user_row.iloc[0]["password"]
    return bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8"))

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user" not in st.session_state:
    st.session_state.user = None
if "theme" not in st.session_state:
    st.session_state.theme = "Light"

# LOGIN / SIGNUP UI
if not st.session_state.logged_in:
    st.title("🎓 EduShield AI")
    menu = st.radio("Choose Action", ["Login", "Signup"], horizontal=True)

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
    st.stop()

# SIDEBAR NAVIGATION
st.sidebar.markdown(
    """
    <div style='padding: 24px 10px 18px;'>
        <h1 style='margin: 0; font-size: 28px; line-height: 1.1;'>🎓 EduShield AI</h1>
    </div>
    """,
    unsafe_allow_html=True,
)

page = st.sidebar.radio(
    "",
    [
        "📋 Dashboard",
        "🎯 Prediction",
        "📊 Analytics",
        "🔍 Explainability",
        "🌳 Risk Decomposition"
    ],
    index=0,
)

st.sidebar.markdown("<div class='sidebar-bottom-spacer'></div>", unsafe_allow_html=True)

with st.sidebar.expander("⚙️ Settings", expanded=False):
    st.session_state.theme = st.selectbox(
        "Theme",
        ["Light", "Dark"],
        index=0 if st.session_state.theme == "Light" else 1,
        key="theme_select",
    )

st.sidebar.markdown(
    f"""
    <div class='sidebar-user'>👤 <strong>{st.session_state.user}</strong></div>
    """,
    unsafe_allow_html=True,
)

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.user = None
    st.rerun()

# Apply theme overrides
if st.session_state.theme == "Dark":
    st.markdown(
        """
        <style>
            .main, .block-container {
                background-color: #081229 !important;
                color: #e2e8f0 !important;
            }
            .css-1d391kg, .css-1v3fvcr {
                background-color: #0f172a !important;
            }
            .stButton button {
                background-color: #2563eb !important;
                color: white !important;
            }
            .stTextInput input, .stSelectbox select {
                background-color: #0f172a !important;
                color: #e2e8f0 !important;
                border-color: #334155 !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

# HOME PAGE (THE IMAGE MATCHING DESIGN)
def show_dashboard_home():
    st.markdown(
        """
        <div class="hero-card">
            <p class="eyebrow">Intelligent student retention for modern institutions</p>
            <h1>EduShield AI</h1>
            <p class="hero-subtitle">
                Predict student dropout risk, translate insights into action,
                and support timely interventions with explainable machine learning.
            </p>
            <div class="hero-buttons">
                <span class="cta-pill">Predict Student Risk</span>
                <span class="cta-pill cta-pill-secondary">Explore Analytics</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="feature-grid">
        <div class="feature-card">
            <div class="feature-icon">🎯</div>
            <h4>Accurate Risk Prediction</h4>
            <p>Identify at-risk students early with a robust dropout model trained on education data.</p>
        </div>
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <h4>Interactive Analytics</h4>
            <p>Visualize attendance, grades, and engagement trends to inform data-driven decisions.</p>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🔍</div>
            <h4>Explainable AI Insights</h4>
            <p>Understand why the model predicts student risk with transparent feature explanations.</p>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🌱</div>
            <h4>Actionable Intervention</h4>
            <p>Break down risk contributors and focus support where it matters most.</p>
        </div>
    </div>
    """,
        unsafe_allow_html=True
    )

    st.markdown("---")
    st.markdown("## Trusted performance")

    c1, c2, c3 = st.columns(3)
    c1.metric("Model Accuracy", "91.4%")
    c2.metric("Total no. of data", "10,000")
    c3.metric("Key Features Used", "29")

    st.markdown("---")
    st.markdown(
        """
        <div class="feature-grid">
            <div class="step-card">
                <div class="step-number">1</div>
                <h4>Assess risk at scale</h4>
                <p>Use an intuitive prediction module to score student dropout risk in minutes.</p>
            </div>
            <div class="step-card">
                <div class="step-number">2</div>
                <h4>Review explainability</h4>
                <p>Inspect the most important factors driving each student's risk score.</p>
            </div>
            <div class="step-card">
                <div class="step-number">3</div>
                <h4>Enable early action</h4>
                <p>Translate AI insights into targeted interventions for academic success.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")
    st.markdown(
        """
        ### 🎯 Mission

        EduShield AI empowers educational institutions to identify at-risk students early and enable
        timely intervention through machine learning and explainable AI.
        """
    )

if page == "📋 Dashboard":
    show_dashboard_home()

# OTHER ROUTED PAGES
elif page == "🎯 Prediction":
    show_prediction()

elif page ==  "📊 Analytics":
    show_analytics()

elif page == "🔍 Explainability":
    show_explainability()
    
elif page == "🌳 Risk Decomposition":
    show_risk_decomposition()
