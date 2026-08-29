import pandas as pd
import plotly.express as px
import streamlit as st

from assistant import answer_question

CHART_FONT = dict(family="Inter, sans-serif", color="#1C2127", size=13)
BLUE = "#2557C7"
BLUE_SOFT = "#D6E0F7"
TEAL = "#2E6F63"
AMBER = "#B0842C"
CLAY = "#B1502B"


def build_context(analysis):
    themes = analysis["Primary reason"].str.split(", ").explode()
    themes = themes[themes != "Low engagement indicators"].value_counts().reset_index(name="Mentions")
    high_risk = analysis[analysis["Risk level"] == "High"]
    medium_risk = analysis[analysis["Risk level"] == "Medium"]
    departments = analysis.groupby("Department", as_index=False).agg(
        Employees=("Employee", "count"),
        Average_satisfaction=("Satisfaction", "mean"),
        Average_engagement=("Engagement", "mean"),
        High_risk_employees=("Risk level", lambda series: (series == "High").sum()),
    ).sort_values("Average_engagement")
    return {
        "analysis": analysis,
        "themes": themes,
        "high_risk": high_risk,
        "medium_risk": medium_risk,
        "departments": departments,
        "positive_satisfaction": int((analysis["Satisfaction"] >= 4).mean() * 100),
        "average_engagement": round(analysis["Engagement"].mean()),
        "leading_theme": themes.iloc[0]["Primary reason"] if not themes.empty else "Low engagement indicators",
        "priority_department": departments.iloc[0],
    }


def render_overview(context):
    analysis = context["analysis"]
    with st.container(key="kpi-row"):
        kpis = st.columns(4, gap="small")
        metric_data = [
            ("Positive satisfaction", f"{context['positive_satisfaction']}%", f"{int((analysis['Satisfaction'] >= 4).sum())} of {len(analysis)} employees", "normal"),
            ("Average engagement", f"{context['average_engagement']}/100", "Across all uploaded teams", "normal"),
            ("High attrition risk", str(len(context["high_risk"])), f"{len(context['medium_risk'])} medium-risk employees", "inverse"),
            ("Leading concern", context["leading_theme"], "Most common written-feedback signal", "normal"),
        ]
        for column, (label, value, delta, color) in zip(kpis, metric_data):
            column.metric(label, value, delta, delta_color=color, border=True)

    with st.container(key="summary-panel", border=True):
        st.subheader("What needs attention", anchor=False)
        first, second, third = st.columns(3)
        priority = context["priority_department"]
        with first:
            st.markdown(f"**Priority team — {priority['Department']}**")
            st.caption(f"Average engagement: {priority['Average_engagement']:.0f}/100, the lowest in this report.")
        with second:
            st.markdown(f"**Leading concern — {context['leading_theme']}**")
            st.caption("Review the related feedback comments to understand the underlying cause.")
        with third:
            st.markdown(f"**Next action — {len(context['high_risk'])} supportive check-in(s)**")
            st.caption("Use the watchlist to prioritize human, confidential follow-up.")

    left, right = st.columns(2, gap="medium")
    with left:
        with st.container(border=True):
            st.subheader("Engagement by department", anchor=False)
            chart = px.bar(
                context["departments"], x="Average_engagement", y="Department", orientation="h", text_auto=".0f",
                color="Average_engagement", color_continuous_scale=[CLAY, AMBER, TEAL],
            )
            chart.update_layout(
                height=330, margin=dict(l=0, r=10, t=10, b=0), font=CHART_FONT,
                xaxis_title="Average engagement score", yaxis_title=None,
                coloraxis_showscale=False, paper_bgcolor="white", plot_bgcolor="white",
            )
            chart.update_traces(marker_line_width=0)
            st.plotly_chart(chart, width="stretch")
    with right:
        with st.container(border=True):
            st.subheader("Attrition risk distribution", anchor=False)
            risk_counts = analysis["Risk level"].value_counts().reindex(["Low", "Medium", "High"], fill_value=0).reset_index()
            risk_counts.columns = ["Risk level", "Employees"]
            chart = px.pie(
                risk_counts, values="Employees", names="Risk level", hole=.64, color="Risk level",
                color_discrete_map={"Low": TEAL, "Medium": AMBER, "High": CLAY},
            )
            chart.update_layout(
                height=330, margin=dict(l=0, r=0, t=10, b=0), font=CHART_FONT,
                paper_bgcolor="white", legend=dict(orientation="h", y=-.12),
            )
            chart.update_traces(marker=dict(line=dict(color="white", width=2)))
            st.plotly_chart(chart, width="stretch")


def render_watchlist(context):
    analysis = context["analysis"]
    st.subheader("Employee watchlist", anchor=False)
    st.caption("Employees are ranked by risk score. Use this to start confidential, supportive conversations — never to make an automated employment decision.")
    watchlist = analysis.sort_values("Risk score", ascending=False)[["Employee", "Department", "Job role", "Satisfaction", "Engagement", "Tenure (years)", "Risk score", "Risk level", "Primary reason"]]
    st.dataframe(
        watchlist,
        hide_index=True,
        width="stretch",
        column_config={
            "Risk score": st.column_config.ProgressColumn("Risk score", min_value=0, max_value=100, format="%d%%"),
            "Satisfaction": st.column_config.NumberColumn(format="%.1f / 5"),
            "Engagement": st.column_config.ProgressColumn(min_value=0, max_value=100, format="%d / 100"),
            "Tenure (years)": st.column_config.NumberColumn(format="%.1f"),
        },
    )
    st.download_button("Download detailed review list", watchlist.to_csv(index=False).encode(), "hr_insight_detailed_review.csv", "text/csv")
    with st.expander("How the risk score is used"):
        st.write("The score combines low satisfaction, low engagement, and recurring concern words in feedback. Short tenure is included only if `tenure_years` is provided. It is a screening signal for HR review, not a prediction or decision.")


def render_departments(context):
    st.subheader("Department insights", anchor=False)
    st.caption("Compare team-level satisfaction, engagement, and high-risk signals.")
    st.dataframe(
        context["departments"],
        hide_index=True,
        width="stretch",
        column_config={
            "Average_satisfaction": st.column_config.NumberColumn("Average satisfaction", format="%.1f / 5"),
            "Average_engagement": st.column_config.ProgressColumn("Average engagement", min_value=0, max_value=100, format="%d / 100"),
            "High_risk_employees": st.column_config.NumberColumn("High-risk employees"),
        },
    )
    themes = context["themes"]
    left, right = st.columns([1.1, .9], gap="medium")
    with left:
        with st.container(border=True):
            st.subheader("Feedback themes", anchor=False)
            if themes.empty:
                st.info("No specific feedback themes were detected in this report.")
            else:
                chart = px.bar(themes, x="Mentions", y="Primary reason", orientation="h", color="Mentions", color_continuous_scale=[BLUE_SOFT, BLUE])
                chart.update_layout(
                    height=310, margin=dict(l=0, r=10, t=10, b=0), font=CHART_FONT,
                    yaxis_title=None, coloraxis_showscale=False, paper_bgcolor="white", plot_bgcolor="white",
                )
                chart.update_traces(marker_line_width=0)
                st.plotly_chart(chart, width="stretch")
    with right:
        with st.container(border=True):
            st.subheader("Recommended team action", anchor=False)
            priority = context["priority_department"]
            st.markdown(f"**Start with {priority['Department']}.**")
            st.write(f"Its average engagement is {priority['Average_engagement']:.0f}/100, the lowest in this report.")
            st.markdown(f"**Then address {context['leading_theme'].lower()}.**")
            st.write("Use individual feedback themes to guide team-level policy, workload, or manager-support improvements.")


def render_assistant(context):
    st.subheader("PeopleLens AI assistant", anchor=False)
    st.caption("Ask questions about the active CSV. Answers are generated locally from this uploaded dataset.")
    with st.container(key="assistant-panel", border=True):
        if not st.session_state.chat_history:
            st.chat_message("assistant").write("Ask me about satisfaction, risk, feedback themes, or recommended next actions.")
        for role, message in st.session_state.chat_history:
            st.chat_message(role).write(message)
        prompt = st.chat_input("Ask about this workforce report")
        if prompt:
            st.session_state.chat_history.append(("user", prompt))
            st.session_state.chat_history.append(("assistant", answer_question(prompt, context["analysis"])))
            st.rerun()
