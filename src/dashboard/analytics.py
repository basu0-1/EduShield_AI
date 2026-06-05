import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def show_analytics():

    st.header("📊 Analytics Dashboard")
    st.subheader("📈 Current Analytics")

    # Check prediction exists
    if "latest_prediction" not in st.session_state:

        st.warning(
            "Please generate a prediction first."
        )

        return

    data = st.session_state["latest_prediction"]
    st.markdown("---")

    # =====================================
    # KPI CARDS
    # =====================================

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Risk %",
        f"{data['Risk_Percent']}%"
    )

    col2.metric(
        "Attendance %",
        data["Attendance_Rate"]
    )

    col3.metric(
        "GPA",
        data["GPA"]
    )

    st.markdown("---")

    # =====================================
    # RISK GAUGE
    # =====================================

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=data["Risk_Percent"],
            title={
                "text": "Current Student Risk (%)"
            },
            gauge={
                "axis": {
                    "range": [0, 100]
                },
                "steps": [
                    {
                        "range": [0, 30],
                        "color": "lightgreen"
                    },
                    {
                        "range": [30, 70],
                        "color": "gold"
                    },
                    {
                        "range": [70, 100],
                        "color": "salmon"
                    }
                ]
            }
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.markdown("---")

    # =====================================
    # ATTENDANCE VS GPA
    # =====================================

    chart_df = pd.DataFrame({

        "Metric": [
            "Attendance",
            "GPA x 25"
        ],

        "Value": [
            data["Attendance_Rate"],
            data["GPA"] * 25
        ]
    })

    fig_bar = px.bar(

        chart_df,

        x="Metric",

        y="Value",

        title="Attendance vs GPA"
    )

    st.plotly_chart(
        fig_bar,
        use_container_width=True
    )

    st.markdown("---")

    # =====================================
    # STUDENT SUMMARY
    # =====================================

    st.subheader(
        "📋 Student Summary"
    )

    summary_df = pd.DataFrame({

        "Attribute": [

            "Age",
            "Department",
            "Attendance",
            "Stress Index",
            "Risk Level",
            "Risk %"
        ],

        "Value": [

            data["Age"],
            data["Department"],
            data["Attendance_Rate"],
            data["Stress_Index"],
            data["Risk_Level"],
            data["Risk_Percent"]
        ]
    })

    st.table(summary_df)
    
    st.markdown("---")

    st.subheader("📈 Historical Analytics")
    
    history_file = r"C:\Projects\EduShield_AI\data\predictions\predictions_history.csv"
    
    try:
    
        df = pd.read_csv(history_file)
        st.write("Columns in CSV:")
        st.write(df.columns.tolist())
        # =====================================
        # KPI CARDS
        # =====================================
    
        total_predictions = len(df)

        high_risk = len(
            df[df["Risk_level"].str.lower() == "high"]
        )
    
        medium_risk = len(
            df[df["Risk_level"].str.lower() == "medium"]
        )
    
        low_risk = len(
            df[df["Risk_level"].str.lower() == "low"]
        )
    
        col1, col2, col3, col4 = st.columns(4)
    
        col1.metric(
        "Total Predictions",
        total_predictions
        )
    
        col2.metric(
            "High Risk",
            high_risk
        )
    
        col3.metric(
            "Medium Risk",
            medium_risk
        )
    
        col4.metric(
            "Low Risk",
            low_risk
        )
    
        st.markdown("---")

    # =====================================
    # RISK DISTRIBUTION PIE CHART
    # =====================================

        risk_counts = df["Risk_level"].value_counts()
    
        fig_pie = px.pie(
            values=risk_counts.values,
            names=risk_counts.index,
            title="Risk Distribution"
        )
    
        st.plotly_chart(
            fig_pie,
            use_container_width=True
        )
    
        st.markdown("---")
    
        # =====================================
        # DEPARTMENT WISE RISK
        # =====================================
    
        dept_risk = df.groupby(
            "Department"
        )["Risk_percent"].mean().reset_index()
    
        fig_dept = px.bar(
            dept_risk,
            x="Department",
            y="Risk_percent",
            title="Average Risk by Department"
        )
    
        st.plotly_chart(
            fig_dept,
            use_container_width=True
        )
    
        st.markdown("---")
    
        # =====================================
        # HISTORY TABLE
        # =====================================
    
        st.subheader("📋 Prediction History")
    
        st.dataframe(
        df.tail(20),
        use_container_width=True
        )
        
        st.markdown("---")

        st.subheader("📈 Risk Trend Over Time")
        
        trend_df = df.copy()
        
        trend_df["Timestamp"] = pd.to_datetime(
            trend_df["Timestamp"]
        )
        
        fig_trend = px.line(
            trend_df,
            x="Timestamp",
            y="Risk_percent",
            markers=True,
            title="Student Risk Trend"
        )
        
        st.plotly_chart(
            fig_trend,
            use_container_width=True
        )
    except Exception as e:
    
        st.error(
            f"Unable to load history: {e}"
        )