import streamlit as st
from PIL import Image


def show_explainability():

    st.header("🔍 Explainable AI Dashboard")

    st.markdown("---")

    st.subheader("SHAP Summary Plot")

    summary_img = Image.open(
        "reports/figures/shap_summary.png"
    )

    st.image(
        summary_img,
        use_container_width=True
    )

    st.markdown("---")

    st.subheader("Feature Importance")

    bar_img = Image.open(
        "reports/figures/shap_bar.png"
    )

    st.image(
        bar_img,
        use_container_width=True
    )

    st.markdown("---")

    st.subheader("SHAP Waterfall Plot")

    waterfall_img = Image.open(
        "reports/figures/shap_waterfall.png"
    )

    st.image(
        waterfall_img,
        use_container_width=True
    )