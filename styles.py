import streamlit as st


def apply_styles():
    st.html(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;600;700&family=Google+Sans+Display:wght@400;500;600;700&family=Roboto+Mono:wght@400;500;600&family=Inter:wght@400;500;600;700&display=swap');

        :root {
            /* Google-aligned palette */
            --ink:         #202124;
            --ink-soft:    #5F6368;
            --ink-muted:   #9AA0A6;
            --surface:     #FFFFFF;
            --surface-alt: #F8F9FA;
            --surface-hover: #F1F3F4;
            --line:        #E8EAED;
            --line-soft:   #F1F3F4;

            /* Google Blue system */
            --blue:        #1A73E8;
            --blue-dark:   #1557B0;
            --blue-soft:   #E8F0FE;
            --blue-mid:    #C5D8F6;

            /* Semantic accent colours (muted, professional) */
            --green:       #137333;
            --green-soft:  #E6F4EA;
            --red:         #C5221F;
            --red-soft:    #FCE8E6;
            --amber:       #B06000;
            --amber-soft:  #FEF7E0;

            /* Typography */
            --sans:  'Google Sans', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            --mono:  'Roboto Mono', 'IBM Plex Mono', ui-monospace, monospace;

            /* Elevation */
            --shadow-1: 0 1px 2px rgba(60,64,67,.3), 0 1px 3px 1px rgba(60,64,67,.15);
            --shadow-2: 0 1px 2px rgba(60,64,67,.3), 0 2px 6px 2px rgba(60,64,67,.15);
        }

        /* ── Base reset ─────────────────────────────────── */
        html, body, .stApp, [class*="css"] {
            font-family: var(--sans);
            color: var(--ink);
        }
        .stApp { background: var(--surface-alt); }
        #MainMenu, header, footer { visibility: hidden; }
        .block-container { max-width: none; padding: 0; }
        h1, h2, h3, h4 { font-family: var(--sans); font-weight: 500; letter-spacing: -.01em; }

        /* ── Sidebar ────────────────────────────────────── */
        [data-testid="stSidebar"] {
            background: var(--surface);
            border-right: 1px solid var(--line);
            box-shadow: none;
        }
        [data-testid="stSidebar"] > div:first-child { background: var(--surface); }

        /* Sidebar brand */
        .sidebar-brand {
            display: flex;
            align-items: center;
            gap: 10px;
            color: var(--ink);
            font-family: var(--sans);
            font-weight: 600;
            font-size: 17px;
            margin: 4px 0 28px;
        }
        .sidebar-brand span {
            display: grid;
            place-items: center;
            width: 32px;
            height: 32px;
            border-radius: 8px;
            background: var(--blue);
            color: #fff;
            font-size: 15px;
        }

        /* Sidebar section captions */
        .stSidebar [data-testid="stCaptionContainer"] p {
            color: var(--ink-muted) !important;
            font-size: 11px;
            letter-spacing: .07em;
            font-weight: 600;
            text-transform: uppercase;
        }
        .stSidebar label,
        .stSidebar [data-testid="stWidgetLabel"] { color: var(--ink) !important; }

        /* Sidebar nav items */
        .stSidebar [data-testid="stRadio"] { padding: 2px 0; }
        .stSidebar [data-testid="stRadio"] label {
            padding: 8px 10px;
            border-radius: 8px;
            transition: background .12s ease;
            width: 100%;
        }
        .stSidebar [data-testid="stRadio"] label:hover {
            background: var(--surface-hover);
        }
        .stSidebar [data-testid="stRadio"] label p,
        .stSidebar [data-testid="stRadio"] label div,
        .stSidebar [data-testid="stRadio"] label span {
            color: var(--ink) !important;
            font-size: 14px !important;
            font-weight: 500 !important;
        }
        .stSidebar [data-testid="stRadio"] label[data-checked="true"] {
            background: var(--blue-soft);
        }
        .stSidebar [data-testid="stRadio"] label[data-checked="true"] p,
        .stSidebar [data-testid="stRadio"] label[data-checked="true"] span {
            color: var(--blue) !important;
            font-weight: 600 !important;
        }
        .stSidebar [data-testid="stRadio"] label [data-baseweb="radio"] > div:first-child {
            border-color: var(--line) !important;
        }

        /* Sidebar buttons */
        .stSidebar button {
            background: transparent !important;
            border: 1px solid var(--line) !important;
            border-radius: 8px !important;
            color: var(--ink) !important;
        }
        .stSidebar button p, .stSidebar button div { color: var(--ink) !important; }
        .stSidebar button:hover {
            background: var(--surface-hover) !important;
            border-color: var(--ink-soft) !important;
        }
        .stSidebar hr { border-color: var(--line); margin: 16px 0; }

        /* ── Metrics / KPI cards ────────────────────────── */
        [data-testid="stMetric"] {
            background: var(--surface);
            border: 1px solid var(--line);
            border-radius: 12px;
            padding: 18px 20px;
            transition: box-shadow .15s ease;
        }
        [data-testid="stMetric"]:hover { box-shadow: var(--shadow-1); }
        [data-testid="stMetricLabel"] p {
            color: var(--ink-soft) !important;
            font-size: 12px !important;
            font-weight: 600 !important;
            text-transform: uppercase;
            letter-spacing: .06em;
        }
        [data-testid="stMetricValue"] {
            font-family: var(--sans);
            color: var(--ink) !important;
            font-weight: 600 !important;
            font-size: 28px !important;
        }
        [data-testid="stMetricDelta"] {
            font-size: 12px !important;
            font-weight: 500 !important;
        }

        /* ── Bordered containers ────────────────────────── */
        [data-testid="stVerticalBlockBorderWrapper"] {
            border: 1px solid var(--line) !important;
            border-radius: 12px !important;
            background: var(--surface);
        }

        /* ── Buttons ────────────────────────────────────── */
        .stApp button[kind="primary"] {
            background: var(--blue) !important;
            border-color: var(--blue) !important;
            border-radius: 6px !important;
            font-weight: 500 !important;
            letter-spacing: .01em;
        }
        .stApp button[kind="primary"]:hover {
            background: var(--blue-dark) !important;
            border-color: var(--blue-dark) !important;
            box-shadow: var(--shadow-1);
        }
        .stApp button[kind="secondary"] {
            border: 1px solid var(--line) !important;
            border-radius: 6px !important;
            color: var(--blue) !important;
            background: var(--surface) !important;
            font-weight: 500 !important;
        }
        .stApp button[kind="secondary"]:hover {
            background: var(--blue-soft) !important;
            border-color: var(--blue-mid) !important;
        }

        /* Plain-text dashboard navigation: no radio circles or button outlines. */
        .stApp div[class*="st-key-left-nav-"] button {
            justify-content: flex-start !important;
            background: transparent !important;
            border: 0 !important;
            box-shadow: none !important;
            border-radius: 6px !important;
            color: var(--ink-soft) !important;
            padding: 8px 10px !important;
        }
        .stApp div[class*="st-key-left-nav-"] button p {
            color: inherit !important;
            font-weight: 500 !important;
        }
        .stApp div[class*="st-key-left-nav-"] button:hover {
            background: var(--surface-hover) !important;
        }
        .stApp div[class*="st-key-left-nav-"] button[kind="primary"] {
            background: var(--blue-soft) !important;
            color: var(--blue) !important;
        }
        .stApp div[class*="st-key-left-nav-"] button[kind="primary"] p {
            font-weight: 600 !important;
        }

        /* ── Inputs & selects ───────────────────────────── */
        .stApp input, .stApp textarea, .stApp select {
            border-radius: 6px !important;
            border-color: var(--line) !important;
            font-size: 14px !important;
        }
        .stApp input:focus, .stApp textarea:focus {
            border-color: var(--blue) !important;
            box-shadow: 0 0 0 2px var(--blue-soft) !important;
        }
        .stApp label, .stApp [data-testid="stWidgetLabel"] p {
            font-size: 13px !important;
            font-weight: 500 !important;
            color: var(--ink-soft) !important;
        }

        /* ── DataFrames ─────────────────────────────────── */
        .stApp [data-testid="stDataFrame"] {
            border: 1px solid var(--line);
            border-radius: 10px;
            overflow: hidden;
        }

        /* ── Headings inside content ────────────────────── */
        .stApp h3 { font-size: 17px; font-weight: 600; color: var(--ink); }
        .stApp h2 { font-size: 22px; font-weight: 600; color: var(--ink); }

        /* ── Dashboard-level layout ─────────────────────── */
        .block-container > div > div { padding-top: 0 !important; }

        /* Dashboard top bar (page header) */
        .dashboard-topbar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 16px 28px 14px;
            background: var(--surface);
            border-bottom: 1px solid var(--line);
            position: sticky;
            top: 0;
            z-index: 100;
        }
        .dashboard-topbar-title {
            font-size: 16px;
            font-weight: 600;
            color: var(--ink);
        }
        .dashboard-topbar-sub {
            font-size: 13px;
            color: var(--ink-soft);
            margin-top: 1px;
        }

        /* Page content padding */
        .st-key-page-content { padding: 24px 28px; }

        /* Summary / attention panel */
        .st-key-summary-panel {
            background: var(--surface);
            border: 1px solid var(--line) !important;
            border-radius: 12px !important;
            padding: 4px 8px;
        }
        .st-key-kpi-row { margin-bottom: 4px; }

        /* Chart containers */
        .st-key-chart-left, .st-key-chart-right {
            background: var(--surface);
            border: 1px solid var(--line);
            border-radius: 12px;
        }

        /* Assistant panel */
        .st-key-assistant-panel {
            background: var(--surface);
            border: 1px solid var(--line) !important;
            border-radius: 12px !important;
        }

        /* Archive panel */
        .st-key-archive-panel {
            background: var(--surface-alt);
            border: 1px solid var(--line) !important;
            border-radius: 12px !important;
        }

        /* ── Home / marketing page ──────────────────────── */
        .st-key-home-page { background: var(--surface); min-height: 100vh; }

        /* Top nav */
        .top-navigation {
            min-height: 64px;
            padding: 0 24px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: var(--surface);
            border-bottom: 1px solid var(--line);
            position: sticky;
            top: 0;
            z-index: 200;
        }
        .brand {
            display: flex;
            align-items: center;
            gap: 10px;
            color: var(--ink);
            font-size: 16px;
            font-weight: 600;
        }
        .brand-mark {
            display: grid;
            place-items: center;
            width: 32px;
            height: 32px;
            background: var(--blue);
            border-radius: 8px;
            color: #fff;
            font-size: 15px;
        }
        .nav-links { color: var(--ink-soft); font-size: 14px; display: flex; gap: 24px; }
        .nav-links a { color: var(--ink-soft); text-decoration: none; font-weight: 500; }
        .nav-links a:hover { color: var(--blue); }

        /* Hero */
        .hero {
            padding: 72px 24px 56px;
            text-align: center;
            background: var(--surface);
            border-bottom: 1px solid var(--line);
        }
        .hero-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 6px 14px;
            background: var(--blue-soft);
            color: var(--blue);
            border-radius: 999px;
            font-size: 12px;
            font-weight: 600;
            letter-spacing: .03em;
            margin-bottom: 22px;
        }
        .hero h1 {
            font-size: 42px;
            font-weight: 600;
            color: var(--ink);
            line-height: 1.2;
            letter-spacing: -.02em;
            max-width: 680px;
            margin: 0 auto 18px;
        }
        .hero p {
            max-width: 540px;
            margin: 0 auto 30px;
            color: var(--ink-soft);
            font-size: 16px;
            line-height: 1.7;
        }
        .hero-actions { display: flex; gap: 12px; justify-content: center; flex-wrap: wrap; }
        .hero-btn-primary {
            display: inline-block;
            padding: 10px 24px;
            background: var(--blue);
            color: #fff;
            border-radius: 6px;
            font-weight: 500;
            font-size: 14px;
            cursor: pointer;
            border: none;
            text-decoration: none;
        }
        .hero-btn-secondary {
            display: inline-block;
            padding: 10px 24px;
            background: var(--surface);
            color: var(--blue);
            border: 1px solid var(--blue-mid);
            border-radius: 6px;
            font-weight: 500;
            font-size: 14px;
            cursor: pointer;
            text-decoration: none;
        }

        /* Stat strip */
        .st-key-stat-one, .st-key-stat-two, .st-key-stat-three {
            background: var(--surface-alt);
            border-bottom: 1px solid var(--line);
            padding: 24px 12px;
            text-align: center;
        }
        .st-key-stat-one, .st-key-stat-two { border-right: 1px solid var(--line); }
        .stat-number {
            font-size: 26px;
            font-weight: 600;
            color: var(--blue);
            font-family: var(--sans);
        }
        .stat-caption {
            color: var(--ink-soft);
            font-size: 13px;
            margin-top: 4px;
            font-weight: 500;
        }

        /* Login + feature panels */
        .st-key-login-panel {
            padding: 32px;
            background: var(--surface);
            border-right: 1px solid var(--line);
        }
        .st-key-feature-panel { padding: 32px; background: var(--surface-alt); }
        .panel-title { color: var(--ink); font-size: 20px; font-weight: 600; margin-bottom: 4px; }
        .panel-subtitle { color: var(--ink-soft); font-size: 14px; margin-bottom: 20px; }

        /* Login form styling */
        .st-key-login-panel label { color: var(--ink-soft) !important; font-size: 13px !important; font-weight: 500 !important; }
        .st-key-login-panel input {
            border: 1px solid var(--line) !important;
            border-radius: 6px !important;
            font-size: 14px !important;
        }
        .st-key-login-panel div[data-testid="stFormSubmitButton"] button {
            width: 100%;
            background: var(--blue) !important;
            border-color: var(--blue) !important;
            border-radius: 6px !important;
            font-weight: 500 !important;
            font-size: 14px !important;
        }
        .st-key-login-panel div[data-testid="stFormSubmitButton"] button:hover {
            background: var(--blue-dark) !important;
        }
        .forgot-password { color: var(--blue); font-size: 13px; text-align: right; margin: 2px 0 10px; font-weight: 500; }
        .sign-up { text-align: center; color: var(--ink-soft); font-size: 13px; margin-top: 16px; }
        .sign-up span { color: var(--blue); font-weight: 600; cursor: pointer; }

        /* Feature items */
        .feature { display: flex; gap: 14px; margin-bottom: 20px; align-items: flex-start; }
        .feature-icon {
            display: grid;
            place-items: center;
            width: 36px;
            height: 36px;
            min-width: 36px;
            border-radius: 8px;
            font-size: 16px;
            background: var(--blue-soft);
        }
        .feature-title { color: var(--ink); font-size: 14px; font-weight: 600; margin-bottom: 3px; }
        .feature-copy { color: var(--ink-soft); font-size: 13px; line-height: 1.5; }

        /* Preview strip */
        .preview-shell {
            border-top: 1px solid var(--line);
            background: var(--surface);
            padding: 24px 28px 20px;
        }
        .preview-label {
            color: var(--ink-muted);
            font-size: 11px;
            font-weight: 600;
            letter-spacing: .08em;
            text-transform: uppercase;
            margin-bottom: 12px;
        }
        .st-key-preview-one, .st-key-preview-two, .st-key-preview-three, .st-key-preview-four {
            min-height: 88px;
            padding: 14px 16px;
            border: 1px solid var(--line);
            border-radius: 10px;
            background: var(--surface);
            transition: box-shadow .12s ease;
        }
        .st-key-preview-one:hover, .st-key-preview-two:hover,
        .st-key-preview-three:hover, .st-key-preview-four:hover {
            box-shadow: var(--shadow-1);
        }
        .preview-value { font-size: 22px; font-weight: 600; color: var(--ink); }
        .preview-name { color: var(--ink-soft); font-size: 12px; margin-top: 4px; font-weight: 500; }
        .preview-note { font-size: 12px; margin-top: 6px; }

        /* Auth / upload cards */
        .st-key-auth-card, .st-key-upload-card {
            background: var(--surface);
            border: 1px solid var(--line) !important;
            border-radius: 12px;
            padding: 10px 14px;
            box-shadow: var(--shadow-1);
        }
        .auth-header {
            max-width: 720px;
            margin: 16px auto 28px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .auth-kicker { color: var(--ink-soft); font-size: 13px; }

        /* Explain / how it works section */
        .explain-heading { text-align: center; max-width: 600px; margin: 0 auto 28px; }
        .eyebrow {
            color: var(--blue);
            font-size: 11px;
            font-weight: 700;
            letter-spacing: .1em;
            text-transform: uppercase;
            font-family: var(--mono);
        }
        .explain-heading h2 { font-size: 28px; font-weight: 600; margin: 10px 0 8px; }
        .explain-heading p { color: var(--ink-soft); font-size: 14px; line-height: 1.6; }

        .st-key-step-1, .st-key-step-2, .st-key-step-3 {
            padding: 8px;
            background: var(--surface);
            border: 1px solid var(--line) !important;
            border-radius: 10px !important;
            min-height: 175px;
            transition: box-shadow .12s;
        }
        .st-key-step-1:hover, .st-key-step-2:hover, .st-key-step-3:hover {
            box-shadow: var(--shadow-1);
        }
        .step-number { color: var(--blue); font-family: var(--mono); font-size: 12px; font-weight: 700; margin-bottom: 12px; }
        .step-title { font-size: 15px; font-weight: 600; margin-bottom: 6px; }
        .step-copy { color: var(--ink-soft); font-size: 13px; line-height: 1.55; }

        /* System capability cards */
        .st-key-system-employee-satisfaction,
        .st-key-system-attrition-risk,
        .st-key-system-feedback-themes,
        .st-key-system-early-alerts {
            padding: 8px;
            background: var(--surface);
            border: 1px solid var(--line) !important;
            border-radius: 10px !important;
            min-height: 170px;
            transition: box-shadow .12s;
        }
        .st-key-system-employee-satisfaction:hover,
        .st-key-system-attrition-risk:hover,
        .st-key-system-feedback-themes:hover,
        .st-key-system-early-alerts:hover {
            box-shadow: var(--shadow-1);
        }
        .system-title { font-size: 15px; font-weight: 600; margin: 8px 0 6px; }
        .system-copy { color: var(--ink-soft); font-size: 13px; line-height: 1.5; }

        /* Hero copy variant (left-aligned) */
        .hero-copy {
            text-align: left;
            padding: 60px 24px 32px 48px;
            border-bottom: none;
        }
        .hero-copy h1 { font-size: 40px; line-height: 1.18; letter-spacing: -.02em; margin-bottom: 16px; }
        .hero-copy p { max-width: 520px; font-size: 15.5px; line-height: 1.7; color: var(--ink-soft); }
        .hero-trust { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 22px; }
        .hero-trust span {
            border: 1px solid var(--line);
            background: var(--surface-alt);
            color: var(--ink-soft);
            border-radius: 999px;
            padding: 5px 13px;
            font-size: 12px;
            font-weight: 500;
        }

        /* Reference shell */
        .reference-shell {
            background: var(--surface);
            border: 1px solid var(--line);
            border-radius: 12px;
            overflow: hidden;
        }

        /* Final callout */
        .final-callout { padding: 40px 0 52px; }
        .final-callout h2 { font-size: 30px; font-weight: 600; margin: 10px 0; }
        .final-callout p { color: var(--ink-soft); max-width: 600px; font-size: 15px; line-height: 1.65; }

        /* Report eyebrow label */
        .report-eyebrow {
            color: var(--blue);
            font-family: var(--mono);
            font-size: 11px;
            font-weight: 700;
            letter-spacing: .1em;
            text-transform: uppercase;
            margin-bottom: 6px;
        }

        /* ── Expanders ──────────────────────────────────── */
        .stApp [data-testid="stExpander"] {
            border: 1px solid var(--line) !important;
            border-radius: 10px !important;
        }
        .stApp [data-testid="stExpander"] summary { font-weight: 500; }

        /* ── Chat messages ───────────────────────────────── */
        .stApp [data-testid="stChatMessage"] {
            background: var(--surface);
            border: 1px solid var(--line);
            border-radius: 10px;
        }

        /* ── Download button ────────────────────────────── */
        .stApp [data-testid="stDownloadButton"] button {
            border-radius: 6px !important;
            font-weight: 500 !important;
        }

        /* ── Tabs ───────────────────────────────────────── */
        .stApp [data-baseweb="tab"] {
            font-size: 14px;
            font-weight: 500;
        }
        .stApp [data-baseweb="tab"][aria-selected="true"] {
            color: var(--blue) !important;
            border-bottom-color: var(--blue) !important;
        }

        /* ── Responsive ─────────────────────────────────── */
        @media (max-width: 768px) {
            .hero h1 { font-size: 28px; }
            .hero-copy { padding: 36px 18px 22px; }
            .hero-copy h1 { font-size: 30px; }
            .nav-links { display: none; }
            .top-navigation { padding: 0 16px; }
        }
        </style>
        """
    )
