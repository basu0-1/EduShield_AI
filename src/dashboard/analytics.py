import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def show_analytics():

    st.markdown(
        """
        <div class="page-heading">
            <h1>📊 Analytics Dashboard</h1>
            <p class="page-subtitle">
                Review the latest prediction results, compare student risk metrics, and explore historical trends with responsive insights.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if "latest_prediction" not in st.session_state:
        st.warning("Please generate a prediction first.")
        return
    
    
    data = st.session_state["latest_prediction"]

    st.markdown("<div class='analytics-card'>", unsafe_allow_html=True)
    st.markdown("<h2>📈 Current Student Snapshot</h2>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class='kpi-grid'>
            <div class='kpi-card'>
                <h4>Risk %</h4>
                <strong>{data['Risk_Percent']}%</strong>
            </div>
            <div class='kpi-card'>
                <h4>Attendance %</h4>
                <strong>{data['Attendance_Rate']}%</strong>
            </div>
            <div class='kpi-card'>
                <h4>GPA</h4>
                <strong>{data['GPA']:.2f}</strong>
            </div>
            <div class='kpi-card'>
                <h4>Stress Index</h4>
                <strong>{data['Stress_Index']:.1f}</strong>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    fig_gauge = go.Figure(
        go.Indicator(
            mode="gauge+number+delta",
            value=data["Risk_Percent"],
            delta={"reference": 50, "increasing": {"color": "#ef4444"}},
            title={"text": "Current Dropout Risk (%)"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#2563eb"},
                "steps": [
                    {"range": [0, 30], "color": "#22c55e"},
                    {"range": [30, 70], "color": "#f59e0b"},
                    {"range": [70, 100], "color": "#ef4444"},
                ],
                "threshold": {"line": {"color": "#0f172a", "width": 4}, "thickness": 0.75, "value": data["Risk_Percent"]},
            },
        )
    )
    fig_gauge.update_layout(
        margin=dict(l=10, r=10, t=50, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#0f172a"),
    )

    chart_df = pd.DataFrame(
        {
            "Metric": ["Attendance", "GPA x 25"],
            "Value": [data["Attendance_Rate"], data["GPA"] * 25],
        }
    )
    fig_bar = px.bar(
        chart_df,
        x="Metric",
        y="Value",
        text_auto=True,
        title="Attendance vs Equivalent GPA Scale",
        labels={"Value": "Scaled Value"},
    )
    fig_bar.update_traces(marker_color=["#2563eb", "#10b981"], hovertemplate="%{x}: %{y:.1f}<extra></extra>")
    fig_bar.update_layout(
        margin=dict(l=10, r=10, t=50, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#0f172a"),
    )

    st.markdown("<div class='analytics-row'>", unsafe_allow_html=True)
    st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
    st.plotly_chart(fig_gauge, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
    st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='analytics-card'>", unsafe_allow_html=True)
    st.markdown("<h2>📋 Student Summary</h2>", unsafe_allow_html=True)
    summary_df = pd.DataFrame(
        {
            "Attribute": [
                "Age",
                "Department",
                "Attendance",
                "Stress Index",
                "Risk Level",
                "Risk %",
            ],
            "Value": [
                data["Age"],
                data["Department"],
                f"{data['Attendance_Rate']}%",
                f"{data['Stress_Index']:.1f}",
                data["Risk_Level"],
                f"{data['Risk_Percent']}%",
            ],
        }
    )
    st.table(summary_df)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(
        """
        <div class='page-heading'>
            <h2>📈 Historical Analytics</h2>
            <p class='page-subtitle'>Track risk trends, department averages, and prediction history for better intervention planning.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    history_file = r"C:\Projects\EduShield_AI\data\predictions\predictions_history.csv"
    try:
        df = pd.read_csv(history_file)
        df["Timestamp"] = pd.to_datetime(df["Timestamp"])

        risk_counts = df["Risk_level"].str.title().value_counts()
        dept_risk = df.groupby("Department")["Risk_percent"].mean().reset_index()
        trend_df = df.sort_values("Timestamp")

        total_predictions = len(df)
        high_risk = len(df[df["Risk_level"].str.lower() == "high"])
        medium_risk = len(df[df["Risk_level"].str.lower() == "medium"])
        low_risk = len(df[df["Risk_level"].str.lower() == "low"])

        st.markdown("<div class='analytics-row'>", unsafe_allow_html=True)
        st.markdown("<div class='analytics-card'>", unsafe_allow_html=True)
        st.markdown("<h2>Prediction KPIs</h2>", unsafe_allow_html=True)
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Total Predictions", total_predictions)
        k2.metric("High Risk", high_risk)
        k3.metric("Medium Risk", medium_risk)
        k4.metric("Low Risk", low_risk)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
        fig_pie = px.pie(
            values=risk_counts.values,
            names=risk_counts.index,
            title="Risk Distribution",
            hole=0.45,
        )
        fig_pie.update_traces(textposition="inside", textinfo="percent+label")
        fig_pie.update_layout(
            margin=dict(l=10, r=10, t=50, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#0f172a"),
        )
        st.plotly_chart(fig_pie, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        fig_dept = px.bar(
            dept_risk,
            x="Department",
            y="Risk_percent",
            title="Average Risk by Department",
            text_auto=True,
            labels={"Risk_percent": "Risk (%)"},
        )
        fig_dept.update_traces(marker_color="#2563eb")
        fig_dept.update_layout(
            margin=dict(l=10, r=10, t=50, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#0f172a"),
        )

        fig_trend = px.line(
            trend_df,
            x="Timestamp",
            y="Risk_percent",
            markers=True,
            title="Risk Trend Over Time",
        )
        fig_trend.update_traces(line_color="#10b981", marker_color="#2563eb")
        fig_trend.update_layout(
            margin=dict(l=10, r=10, t=50, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#0f172a"),
        )

        st.markdown("<div class='analytics-row'>", unsafe_allow_html=True)
        st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
        st.plotly_chart(fig_dept, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
        st.plotly_chart(fig_trend, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='table-card'>", unsafe_allow_html=True)
        st.markdown("<h2>Recent Prediction History</h2>", unsafe_allow_html=True)
        st.dataframe(df.tail(20).reset_index(drop=True), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Unable to load history: {e}")
