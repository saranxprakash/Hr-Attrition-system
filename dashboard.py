import streamlit as st

from dashboard_views import build_context, render_assistant, render_departments, render_overview, render_watchlist
from data_processing import analyze_feedback

ICON_B64 = "PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAzMiAzMiIgZmlsbD0ibm9uZSI+PHJlY3Qgd2lkdGg9IjMyIiBoZWlnaHQ9IjMyIiByeD0iOCIgZmlsbD0iIzFBNzNFOCIvPjxwYXRoIGQ9Ik03IDIyIEwxMSAyMiBMMTMgMTYgTDE2IDI2IEwxOSAxMiBMMjEgMjIgTDI1IDIyIiBzdHJva2U9IndoaXRlIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9yZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgZmlsbD0ibm9uZSIvPjwvc3ZnPg=="
ICON_URI = f"data:image/svg+xml;base64,{ICON_B64}"
NAVIGATION_OPTIONS = ["Overview", "Watchlist", "Departments", "AI assistant", "CSV archive"]


def _left_navigation(container):
    with container:
        st.html(
            f'''<style>
            .left-nav-brand {{ display:flex; align-items:center; gap:10px; color:#202124;
                font:600 16px 'Google Sans', Inter, sans-serif; margin:4px 0 28px; }}
            .left-nav-label {{ color:#5F6368; font-size:11px; font-weight:700;
                letter-spacing:.07em; margin:16px 0 12px; }}
            .left-nav-user {{ color:#202124; font-size:14px; font-weight:600; margin-bottom:18px; }}
            div[class*="st-key-left-nav-"] button {{
                justify-content: flex-start; border: 0 !important; box-shadow: none !important;
                padding: 8px 10px !important; color: #3C4043 !important;
                background: transparent !important; transition: background .18s ease, color .18s ease;
            }}
            div[class*="st-key-left-nav-"] button:hover {{ background: #F1F3F4 !important; }}
            div[class*="st-key-left-nav-"] button[kind="primary"] {{
                color: #1A73E8 !important; background: #E8F0FE !important; font-weight: 600 !important;
            }}
            </style>
            <div class="left-nav-brand">
              <img src="{ICON_URI}" width="30" height="30" style="border-radius:8px" alt="PeopleLens AI logo"/>
              PeopleLens AI
            </div>
            <div class="left-nav-label">WORKFORCE INTELLIGENCE</div>'''
        )
        selected = st.session_state.get("dashboard_view", "Overview")
        for option in NAVIGATION_OPTIONS:
            if st.button(
                option,
                key=f"left-nav-{option.lower().replace(' ', '-')}",
                type="primary" if option == selected else "secondary",
                width="stretch",
            ):
                selected = option
        st.divider()
        st.html(
            '<div class="left-nav-label">SIGNED IN AS</div>'
            f'<div class="left-nav-user">{st.session_state.user["name"]}</div>'
        )
        if st.button("Upload another CSV", width="stretch", key="left_upload"):
            st.session_state.page = "upload"
            st.rerun()
        if st.button("Log out", width="stretch", key="left_logout"):
            st.session_state.user = None
            st.session_state.feedback_data = None
            st.session_state.chat_history = []
            st.session_state.page = "home"
            st.rerun()
    return selected


def _render_content(selected):
    if selected == "CSV archive":
        st.session_state.page = "upload"
        st.rerun()

    archive = st.session_state.get("archive_record") or {}
    reporting_month = archive.get("reporting_month_display", "Current report")
    first_name = st.session_state.user["name"].split()[0]
    page_headings = {
        "Overview": f"Hello, {first_name}",
        "Watchlist": "Employee watchlist",
        "Departments": "Department insights",
        "AI assistant": "PeopleLens AI assistant",
    }
    st.html('<style>.block-container { padding: 30px 44px 64px !important; max-width: 1500px !important; margin: 0 auto; }</style>')
    st.html('<div class="report-eyebrow">WORKFORCE REPORT</div>')
    st.title(page_headings[selected])
    st.caption(f"{reporting_month} · Your employee-feedback insights are ready to review.")
    context = build_context(analyze_feedback(st.session_state.feedback_data))

    if selected == "Overview":
        render_overview(context)
    elif selected == "Watchlist":
        render_watchlist(context)
    elif selected == "Departments":
        render_departments(context)
    else:
        render_assistant(context)


def render_dashboard():
    if st.session_state.user is None or st.session_state.feedback_data is None:
        st.session_state.page = "upload" if st.session_state.user else "home"
        st.rerun()

    st.session_state.setdefault("dashboard_view", "Overview")
    st.session_state.setdefault("dashboard_menu_visible", False)

    if st.button(
        ":material/menu:",
        key="toggle_dashboard_menu",
        help="Show or hide dashboard navigation",
    ):
        st.session_state.dashboard_menu_visible = not st.session_state.dashboard_menu_visible
        st.rerun()

    if st.session_state.dashboard_menu_visible:
        navigation_column, content_column = st.columns([1.15, 5.85], gap="medium")
        selected = _left_navigation(navigation_column)
        st.session_state.dashboard_view = selected
    else:
        content_column = st.container()
        selected = st.session_state.dashboard_view

    with content_column:
        _render_content(selected)
