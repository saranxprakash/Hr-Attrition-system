import os
import textwrap

import pandas as pd
import streamlit as st

try:
    from google import genai
except ImportError:
    genai = None

MODEL = "gemini-3.6-flash"  # Current Gemini Flash model recommended by the API.

SYSTEM_PROMPT = textwrap.dedent(
    """
    You are the PeopleLens AI assistant, embedded in an internal workforce-analytics
    dashboard. You answer questions about ONE uploaded employee-feedback report,
    using only the data summary provided below. Ground every claim in that data.

    Rules:
    - Never invent numbers, employees, or departments that are not in the summary.
    - Never recommend or imply an automated employment decision (firing, promotion,
      discipline). This tool is a screening and awareness aid for HR professionals,
      not a decision system.
    - When discussing named individuals, remind the user that any outreach should
      be confidential and supportive, not punitive.
    - If the summary doesn't contain enough detail to answer, say so plainly and
      point to which dashboard view (Watchlist, Departments, Overview) has it.
    - Keep answers concise: 2-5 sentences, plain language, no markdown headers.
    """
).strip()


def _build_data_summary(analysis: pd.DataFrame) -> str:
    """Compress the feedback dataframe into a compact context block for the model."""
    total = len(analysis)
    risk_counts = analysis["Risk level"].value_counts().to_dict()

    dept_summary = (
        analysis.groupby("Department")
        .agg(
            employees=("Employee", "count"),
            avg_satisfaction=("Satisfaction", "mean"),
            avg_engagement=("Engagement", "mean"),
            high_risk=("Risk level", lambda s: (s == "High").sum()),
        )
        .round(1)
        .reset_index()
        .to_dict("records")
    )

    themes = (
        analysis["Primary reason"]
        .str.split(", ")
        .explode()
        .value_counts()
        .head(8)
        .to_dict()
    )

    watchlist_cols = ["Employee", "Department", "Risk level", "Risk score", "Primary reason"]
    watchlist = (
        analysis.sort_values("Risk score", ascending=False)
        .head(15)[watchlist_cols]
        .to_dict("records")
    )

    return textwrap.dedent(
        f"""
        Total employees in report: {total}
        Risk level counts: {risk_counts}

        Department summary:
        {dept_summary}

        Top feedback themes (mentions):
        {themes}

        Top 15 highest-risk employees (confidential HR follow-up only):
        {watchlist}
        """
    ).strip()


def _get_api_key() -> str | None:
    """Read the Gemini key without exposing it in the interface or source code."""
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if api_key:
        return api_key.strip()

    try:
        return str(st.secrets.get("GEMINI_API_KEY", "")).strip() or None
    except (FileNotFoundError, AttributeError):
        return None


def answer_question(prompt: str, analysis: pd.DataFrame) -> str:
    if genai is None:
        return (
            "The Gemini AI package is not installed. Run `python -m pip install -r "
            "requirements.txt` with the same Python environment used to start Streamlit, then restart the app."
        )

    api_key = _get_api_key()
    if not api_key:
        return (
            "The assistant isn't connected yet. Add your Gemini key as GEMINI_API_KEY in "
            "the environment or in `.streamlit/secrets.toml`, then restart the app."
        )

    data_summary = _build_data_summary(analysis)
    recent_history = st.session_state.get("chat_history", [])[-8:]
    conversation = "\n".join(f"{role.title()}: {message}" for role, message in recent_history)
    request = (
        f"{SYSTEM_PROMPT}\n\nCurrent report data:\n{data_summary}\n\n"
        f"Recent conversation:\n{conversation}\n\nUser: {prompt}"
    )

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(model=MODEL, contents=request)
        return response.text.strip() if response.text else "The model returned no answer. Please try a more specific question."
    except Exception as exc:  # keep the dashboard usable even if the API call fails
        return f"I couldn't reach the Gemini assistant just now ({exc}). Please check that the key has Gemini API access and try again."
