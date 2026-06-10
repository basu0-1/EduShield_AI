import streamlit as st
import pandas as pd
import plotly.express as px


def show_risk_decomposition():

    st.header("🌳 Risk Decomposition Dashboard")

    if "latest_prediction" not in st.session_state:

        st.warning(
            "Please generate a prediction first."
        )

        return

    data = st.session_state["latest_prediction"]

    theme = st.session_state.get("theme", "Light")
    if theme == "Dark":
        font_color = "#e6eef8"
    else:
        font_color = "#0f172a"

    st.subheader(
        f"Current Risk: {data['Risk_Percent']}%"
    )

    st.markdown("---")

    # SAMPLE DECOMPOSITION VALUES
    decomposition_df = pd.DataFrame({

        "Category": [

            "Academic",
            "Academic",
            "Academic",

            "Psychological",
            "Psychological",

            "Financial",
            "Financial",

            "Lifestyle",
            "Lifestyle",
            "Lifestyle"
        ],

        "Feature": [

            "Attendance",
            "GPA",
            "Academic Risk",

            "Stress Index",
            "Stress Burden",

            "Income",
            "Scholarship",

            "Travel Time",
            "Internet Access",
            "Part-Time Job"
        ],

        "Impact": [

            35,
            20,
            15,

            12,
            8,

            4,
            2,

            2,
            1,
            1
        ]
    })

    # TREEMAP
    st.subheader("📊 Risk Contribution Treemap")

    fig_tree = px.treemap(

        decomposition_df,

        path=[
            "Category",
            "Feature"
        ],

        values="Impact",

        title="Dropout Risk Decomposition"
    )
    fig_tree.update_layout(
        margin=dict(l=10, r=10, t=50, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=font_color),
        title_font=dict(color=font_color),
    )
    fig_tree.data[0].textfont = dict(color=font_color)

    st.plotly_chart(
        fig_tree,
        use_container_width=True
    )

    st.markdown("---")

    # EXPANDABLE TREE
    st.subheader("🌲 Detailed Risk Breakdown")

    with st.expander("📚 Academic Factors"):

        st.write("Attendance")
        st.progress(35)

        st.write("GPA")
        st.progress(20)

        st.write("Academic Risk")
        st.progress(15)

    with st.expander("🧠 Psychological Factors"):

        st.write("Stress Index")
        st.progress(12)

        st.write("Stress Burden")
        st.progress(8)

    with st.expander("💰 Financial Factors"):

        st.write("Income")
        st.progress(4)

        st.write("Scholarship")
        st.progress(2)

    with st.expander("🏠 Lifestyle Factors"):

        st.write("Travel Time")
        st.progress(2)

        st.write("Internet Access")
        st.progress(1)

        st.write("Part-Time Job")
        st.progress(1)

    st.markdown("---")

    st.info(
        """
        This dashboard decomposes the overall
        dropout risk into major contributing
        categories and features, helping
        educators identify intervention points.
        """
    )
