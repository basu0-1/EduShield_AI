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

# PROFESSIONAL DASHBOARD HEADER
header_left, header_middle, header_right = st.columns([3, 5, 2])

with header_left:

    st.markdown(
        """
        <h1 style="
        margin-top:10px;
        font-size:36px;
        font-weight:700;
        ">
        🎓 EduShield AI
        </h1>
        """,
        unsafe_allow_html=True
    )

with header_middle:

    search = st.text_input(
        "",
        placeholder="🔍 Search Students..."
    )

with header_right:

    st.markdown(
        f"""
        <div style="
        text-align:right;
        font-size:18px;
        margin-top:15px;
        ">
        👤 <b>{st.session_state.user}</b>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("---")

# DASHBOARD NAVIGATION
page = st.selectbox(
    "",
    [
        "📋 Dashboard",
        "🎯 Prediction",
        "📊 Analytics",
        "🔍 Explainability",
        "🌳 Risk Decomposition"
    ]
)

logout_col1, logout_col2 = st.columns([8,1])

with logout_col2:

    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.rerun()

st.markdown("---")

# HOME PAGE (THE IMAGE MATCHING DESIGN)
if page == "📋 Dashboard":
    pass
    if page == "📋 Dashboard":
        st.markdown(
        """
        <div style="
        background: linear-gradient(135deg,#0b2b61,#2563eb);
        padding:60px;
        border-radius:20px;
        text-align:center;
        color:white;
        ">

        <h1 style="font-size:60px;">
        🎓 EduShield AI
        </h1>

        <h3>
        Student Dropout Prediction &
        Early Warning System
        </h3>

        <br>

        <p style="font-size:22px;">
        Predict • Explain • Prevent
        </p>

        </div>
        """,
        unsafe_allow_html=True
        )
        st.markdown("## Platform Modules")

        col1, col2, col3, col4 = st.columns(4)        

        with col1:
            st.info(
                """
                🎯 Prediction        

                Predict student dropout risk
                """
            )        

        with col2:
            st.info(
                """
                📊 Analytics        

                Analyze trends and performance
                """
            )        

        with col3:
            st.info(
                """
                🔍 Explainability        

                Understand AI decisions
                """
            )        

        with col4:
            st.info(
                """
                🌳 Risk Decomposition        

                Break down risk contributors
                """
            )
        st.markdown("---")

        st.subheader("Platform Statistics")
        
        c1, c2, c3 = st.columns(3)
        
        c1.metric("Model Accuracy", "91.4%")
        c2.metric("Total no. of Data", "10,000")
        c3.metric("Features", "29")
        
        st.markdown("---")

        st.markdown(
            """
            ### 🎯 Mission
        
            EduShield AI empowers educational institutions
            to identify at-risk students early and enable
            timely intervention through Machine Learning
            and Explainable AI.
            """
        )

# OTHER ROUTED PAGES
elif page == "🎯 Prediction":
    show_prediction()

elif page ==  "📊 Analytics":
    show_analytics()

elif page == "🔍 Explainability":
    show_explainability()
    
elif page == "🌳 Risk Decomposition":
    show_risk_decomposition()
