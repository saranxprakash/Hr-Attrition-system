import streamlit as st

from auth import render_auth_page
from dashboard import render_dashboard
from home import render_home
from styles import apply_styles
from upload import render_upload_page


st.set_page_config(
    page_title="PeopleLens AI",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)
apply_styles()

st.session_state.setdefault("page", "home")
st.session_state.setdefault("user", None)
st.session_state.setdefault("feedback_data", None)
st.session_state.setdefault("archive_record", None)
st.session_state.setdefault("chat_history", [])
st.session_state.setdefault("dashboard_view", "Overview")

requested_page = st.query_params.get("page")
if requested_page in {"login", "register"}:
    st.session_state.page = requested_page
    st.query_params.clear()

if st.session_state.page == "home":
    render_home()
elif st.session_state.page in {"login", "register"}:
    render_auth_page(st.session_state.page)
elif st.session_state.page == "upload":
    render_upload_page()
else:
    render_dashboard()
