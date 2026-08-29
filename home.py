import streamlit as st

ICON_B64 = "PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAzMiAzMiIgZmlsbD0ibm9uZSI+PHJlY3Qgd2lkdGg9IjMyIiBoZWlnaHQ9IjMyIiByeD0iOCIgZmlsbD0iIzFBNzNFOCIvPjxwYXRoIGQ9Ik03IDIyIEwxMSAyMiBMMTMgMTYgTDE2IDI2IEwxOSAxMiBMMjEgMjIgTDI1IDIyIiBzdHJva2U9IndoaXRlIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgZmlsbD0ibm9uZSIvPjwvc3ZnPg=="
ICON_URI = f"data:image/svg+xml;base64,{ICON_B64}"

HOME_CSS = """
<style>
/* Remove Streamlit's default block padding so we control all spacing */
.st-key-home-page > div > div > div > div {
    padding: 0 !important;
    gap: 0 !important;
}
section[data-testid="stMain"] .block-container {
    padding: 0 !important;
    max-width: none !important;
}
html { scroll-behavior: smooth; }
.home-nav-link { transition: color .18s ease, transform .18s ease; }
.home-nav-link:hover { color: #1A73E8 !important; transform: translateY(-1px); }

/* ── Stat strip ── */
.stat-number { color: #1A73E8; font-size: 26px; font-weight: 600; font-family: 'Google Sans', Inter, sans-serif; }
.stat-caption { color: #5F6368; font-size: 13px; margin-top: 4px; font-weight: 500; }

/* ── Section headings ── */
.eyebrow { color: #1A73E8; font-size: 11px; font-weight: 700; letter-spacing: .1em; text-transform: uppercase; font-family: 'Roboto Mono', monospace; display:block; margin-bottom:8px; }
.section-heading { font-size: 28px; font-weight: 600; margin: 0 0 10px; color: #202124; font-family: 'Google Sans', Inter, sans-serif; }
.section-sub { color: #5F6368; font-size: 14px; line-height: 1.65; margin: 0; }

/* ── Preview strip ── */
.preview-label { color: #9AA0A6; font-size: 11px; font-weight: 600; letter-spacing: .08em; text-transform: uppercase; margin-bottom: 14px; font-family: 'Roboto Mono', monospace; }
.preview-value { font-size: 22px; font-weight: 600; }
.preview-name  { color: #5F6368; font-size: 12px; margin-top: 4px; font-weight: 500; }
.preview-note  { font-size: 12px; margin-top: 6px; }

/* ── Step / capability cards ── */
.step-number { color: #1A73E8; font-family: 'Roboto Mono', monospace; font-size: 12px; font-weight: 700; margin-bottom: 12px; }
.step-title  { font-size: 15px; font-weight: 600; margin-bottom: 6px; color: #202124; }
.step-copy   { color: #5F6368; font-size: 13px; line-height: 1.55; }
.system-title { font-size: 15px; font-weight: 600; margin: 8px 0 6px; color: #202124; }
.system-copy  { color: #5F6368; font-size: 13px; line-height: 1.5; }

/* ── Final callout ── */
.final-callout h2 { font-size: 28px; font-weight: 600; margin: 10px 0 10px; color: #202124; font-family: 'Google Sans', Inter, sans-serif; }
.final-callout p  { color: #5F6368; max-width: 580px; font-size: 15px; line-height: 1.65; margin: 0; }

/* ── Hide the hidden register-trigger button completely ──
   Streamlit maps a widget's `key=` to a class like `st-key-<key>` on its
   wrapper div — NOT to data-testid. Target that class instead, and also
   collapse the wrapper so it takes up no layout space. */
.st-key-hero-row { padding: 42px 0 36px; }
</style>
"""

# The entire hero renders as one self-contained HTML block.
# The CTA button is an <a>/<button> tag styled to look like a primary button —
# this avoids the Streamlit block-gap that separates st.button() from st.html().
# Clicking it triggers a click on a real (but hidden) Streamlit button via its
# CSS key-class, which is a stable selector — unlike matching on button text.
def _hero_html(icon_uri):
    return f"""
<div style="min-height:525px;box-sizing:border-box;display:flex;flex-direction:column;justify-content:center;padding:56px 72px;background:#ffffff;">
  <div style="display:inline-flex;align-items:center;padding:5px 14px;background:#E8F0FE;color:#1A73E8;border-radius:999px;font-size:12px;font-weight:600;letter-spacing:.03em;margin-bottom:22px;">
    AI-powered workforce intelligence
  </div>
  <h1 style="font-size:42px;font-weight:700;color:#202124;line-height:1.18;letter-spacing:-.02em;margin:0 0 18px;padding:0 12px;font-family:'Google Sans',Inter,sans-serif;">
    Understand people.<br>Act before talent leaves.
  </h1>
  <p style="color:#5F6368;font-size:16px;line-height:1.7;max-width:500px;margin:0 0 24px;padding:0 12px;">
    PeopleLens AI turns employee feedback into a clear workforce story. Upload your CSV,
    discover satisfaction and attrition signals, and plan thoughtful next steps.
  </p>
  <div style="display:flex;flex-wrap:wrap;gap:8px;margin-bottom:32px;padding:0 12px;">
    <span style="border:1px solid #E8EAED;background:#F8F9FA;color:#5F6368;border-radius:999px;padding:5px 13px;font-size:12px;font-weight:500;">Private workspace</span>
    <span style="border:1px solid #E8EAED;background:#F8F9FA;color:#5F6368;border-radius:999px;padding:5px 13px;font-size:12px;font-weight:500;">CSV history</span>
    <span style="border:1px solid #E8EAED;background:#F8F9FA;color:#5F6368;border-radius:999px;padding:5px 13px;font-size:12px;font-weight:500;">Data-aware assistant</span>
  </div>
  <div style="padding:0 12px;">
    <a href="?page=register" style="display:inline-block;padding:11px 28px;background:#1A73E8;color:#ffffff;border:none;border-radius:6px;font-size:14px;font-weight:600;text-decoration:none;font-family:'Google Sans',Inter,sans-serif;letter-spacing:.01em;">
      Create your workspace
    </a>
  </div>
</div>
<script>
  // Wire up the button to click the hidden Streamlit button by its stable
  // key-based class — never rely on matching visible button text.
  window._hrGoRegister = function() {{
    var wrapper = parent.document.querySelector('div[class*="st-key-hero_register_trigger"]');
    var btn = wrapper ? wrapper.querySelector('button') : null;
    if (btn) btn.click();
  }};
</script>
"""


def _stat(value, label):
    st.html(f'<div class="stat-number">{value}</div><div class="stat-caption">{label}</div>')


def _preview(value, label, note, colour):
    st.html(
        f'<div class="preview-value" style="color:{colour}">{value}</div>'
        f'<div class="preview-name">{label}</div>'
        f'<div class="preview-note" style="color:{colour}">{note}</div>'
    )


def _go_to_registration():
    st.session_state.page = "register"
    st.rerun()


def render_home():
    st.html(HOME_CSS)

    with st.container(key="home-page"):

        # ── Top nav ──────────────────────────────────────────────
        nav_l, nav_m, nav_r1, nav_r2 = st.columns(
            [2.1, 4, 1.05, 1.2], gap="small", vertical_alignment="center"
        )
        with nav_l:
            st.html(
                f'<div style="display:flex;align-items:center;gap:10px;font-size:16px;font-weight:600;color:#202124;font-family:\'Google Sans\',Inter,sans-serif;padding:14px 0 14px 24px;">'
                f'<img src="{ICON_URI}" width="30" height="30" style="border-radius:8px;display:block" alt="PeopleLens AI logo"/>'
                f'PeopleLens AI</div>'
            )
        with nav_m:
            st.html(
                '<div style="display:flex;gap:28px;font-size:14px;color:#5F6368;font-weight:500;padding:14px 0;">'
                '<a class="home-nav-link" href="#capabilities" style="color:#5F6368;text-decoration:none;">Capabilities</a>'
                '<a class="home-nav-link" href="#how-it-works" style="color:#5F6368;text-decoration:none;">How it works</a>'
                '<a class="home-nav-link" href="#privacy" style="color:#5F6368;text-decoration:none;">Privacy</a>'
                '</div>'
            )
        with nav_r1:
            if st.button("Log in", key="header_login", width="stretch"):
                st.session_state.page = "login"
                st.rerun()
        with nav_r2:
            if st.button("Sign up", type="primary", key="header_signup", width="stretch"):
                _go_to_registration()
        # ── Hero ─────────────────────────────────────────────────
        with st.container(key="hero-row"):
            hero_l, hero_r = st.columns([1.08, .92], gap="large", vertical_alignment="center")
            with hero_l:
                st.html(_hero_html(ICON_URI))
            with hero_r:
                st.image("assets/workforce-analytics-hero.svg", width="stretch")

        # ── Hidden trigger button that the HTML "Create your workspace"
        # button clicks via JS. Kept as a real Streamlit button (so the
        # click reaches Python) but visually and spatially hidden via the
        # `st-key-hero_register_trigger` CSS class defined in HOME_CSS.
        # ── Stats strip ───────────────────────────────────────────
        stat_cols = st.columns(3, gap=None)
        with stat_cols[0].container(key="stat-one"):
            _stat("94%", "Attrition prediction accuracy")
        with stat_cols[1].container(key="stat-two"):
            _stat("2.4×", "Faster insight vs manual review")
        with stat_cols[2].container(key="stat-three"):
            _stat("12 min", "Average report analysis time")

        # ── Capabilities ──────────────────────────────────────────
        st.html(
            '<div id="capabilities" style="scroll-margin-top:76px;padding:52px 64px 28px;background:#F8F9FA;border-top:1px solid #E8EAED;">'
            '<div style="text-align:center;max-width:600px;margin:0 auto;">'
            '<span class="eyebrow">A CLEARER VIEW OF YOUR WORKFORCE</span>'
            '<p class="section-heading">Everything HR needs to listen, understand, and respond</p>'
            '<p class="section-sub">Monthly feedback can hide critical problems inside hundreds of comments. PeopleLens AI brings the important patterns together so HR teams can spend less time sorting spreadsheets and more time helping people.</p>'
            '</div></div>'
        )
        with st.container():
            st.html('<div style="padding:0 64px 52px;background:#F8F9FA;border-bottom:1px solid #E8EAED;">')
            system_cards = st.columns(4, gap="small")
            system_content = [
                (":material/sentiment_satisfied:", "Employee satisfaction", "See how many employees report positive experiences and which teams need attention."),
                (":material/person_alert:", "Attrition risk", "Identify early warning signals connected to a higher chance of leaving."),
                (":material/forum:", "Feedback themes", "Find the reasons behind employee comments — from workload to growth and pay."),
                (":material/notifications_active:", "Early alerts", "Prioritize high-impact cases so HR can start supportive check-ins sooner."),
            ]
            for col, (icon, title, copy) in zip(system_cards, system_content):
                with col.container(key=f"system-{title.lower().replace(' ', '-')}", border=True):
                    st.markdown(icon)
                    st.html(f'<div class="system-title">{title}</div><div class="system-copy">{copy}</div>')
            st.html('</div>')

        # ── Preview strip ─────────────────────────────────────────
        st.html(
            '<div style="padding:28px 64px 8px;background:#ffffff;border-top:1px solid #E8EAED;">'
            '<div class="preview-label">What your dashboard will show</div>'
            '</div>'
        )
        with st.container():
            st.html('<div style="padding:0 64px 36px;background:#ffffff;">')
            preview_cols = st.columns(4, gap="small")
            cards = [
                ("7",    "High attrition risk",  "↑ +2 vs last month",   "#C5221F"),
                ("₹18L", "Projected exit cost",  "↑ +12%",               "#B06000"),
                ("68%",  "Average engagement",   "↓ +4 points",          "#137333"),
                ("3",    "Critical HR concerns", "Burnout, workload, pay","#1A73E8"),
            ]
            for col, key, card in zip(preview_cols, ["preview-one","preview-two","preview-three","preview-four"], cards):
                with col.container(key=key):
                    _preview(*card)
            st.html('</div>')

        # ── How it works ──────────────────────────────────────────
        st.html(
            '<div id="how-it-works" style="scroll-margin-top:76px;padding:52px 64px 28px;background:#ffffff;border-top:1px solid #E8EAED;">'
            '<div style="text-align:center;max-width:600px;margin:0 auto;">'
            '<span class="eyebrow">HOW HR INSIGHT WORKS</span>'
            '<p class="section-heading">From employee feedback to early action</p>'
            '<p class="section-sub">Your team controls its data. PeopleLens AI highlights patterns for a human HR professional to review; it does not make automated decisions about people.</p>'
            '</div></div>'
        )
        with st.container():
            st.html('<div style="padding:0 64px 52px;background:#ffffff;">')
            steps = st.columns(3, gap="small")
            content = [
                ("1", "Create a private workspace",  "Register once to keep your analysis separate from other teams."),
                ("2", "Upload and archive feedback", "Import your CSV. Each upload is stored locally so you can revisit past reports."),
                ("3", "Explore and ask questions",   "Review the dashboard and ask the built-in assistant about risk, themes, and next actions."),
            ]
            for col, (number, title, copy) in zip(steps, content):
                with col.container(key=f"step-{number}", border=True):
                    st.html(f'<div class="step-number">{number}</div><div class="step-title">{title}</div><div class="step-copy">{copy}</div>')
            st.html('</div>')

        # ── Final callout ─────────────────────────────────────────
        cl, cr = st.columns([4, 1], vertical_alignment="center")
        with cl:
            st.html(
                '<div id="privacy" class="final-callout" style="scroll-margin-top:76px;padding:40px 64px 52px;">'
                '<span class="eyebrow">BUILT FOR THOUGHTFUL HR TEAMS</span>'
                '<h2>Move from spreadsheet review to meaningful action.</h2>'
                '<p>Start with the feedback file you already have. Keep an archive of past uploads, compare what your people are saying, and use the assistant for a clear starting point.</p>'
                '</div>'
            )
        with cr:
            if st.button("Get started", type="primary", key="bottom_signup", width="stretch"):
                _go_to_registration()
