import hashlib
import hmac
import json
import secrets
from pathlib import Path

import streamlit as st

USER_FILE = Path(__file__).with_name("users.json")

ICON_B64 = "PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAzMiAzMiIgZmlsbD0ibm9uZSI+PHJlY3Qgd2lkdGg9IjMyIiBoZWlnaHQ9IjMyIiByeD0iOCIgZmlsbD0iIzFBNzNFOCIvPjxwYXRoIGQ9Ik03IDIyIEwxMSAyMiBMMTMgMTYgTDE2IDI2IEwxOSAxMiBMMjEgMjIgTDI1IDIyIiBzdHJva2U9IndoaXRlIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgZmlsbD0ibm9uZSIvPjwvc3ZnPg=="
ICON_URI = f"data:image/svg+xml;base64,{ICON_B64}"


def _load_users():
    if not USER_FILE.exists():
        return {}
    try:
        return json.loads(USER_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def _hash_password(password, salt=None):
    salt = salt or secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 310_000).hex()
    return salt, digest


def register_user(name, email, password):
    users = _load_users()
    email = email.strip().lower()
    if not name.strip() or "@" not in email or len(password) < 8:
        return False, "Enter your name, a valid email, and a password of at least 8 characters."
    if email in users:
        return False, "An account already exists for this email. Please sign in instead."
    salt, password_hash = _hash_password(password)
    users[email] = {"name": name.strip(), "salt": salt, "password_hash": password_hash}
    USER_FILE.write_text(json.dumps(users, indent=2), encoding="utf-8")
    return True, users[email]


def authenticate_user(email, password):
    user = _load_users().get(email.strip().lower())
    if not user:
        return None
    _, attempt = _hash_password(password, user["salt"])
    return user if hmac.compare_digest(attempt, user["password_hash"]) else None


def render_auth_page(mode):
    st.html(f"""
    <style>
    .auth-topbar {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        max-width: 720px;
        margin: 20px auto 32px;
        padding: 0 8px;
    }}
    .auth-brand {{
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 16px;
        font-weight: 600;
        color: #202124;
        font-family: 'Google Sans', Inter, sans-serif;
    }}
    .auth-kicker {{ color: #5F6368; font-size: 13px; font-weight: 500; }}
    </style>
    <div class="auth-topbar">
        <div class="auth-brand">
            <img src="{ICON_URI}" width="28" height="28"
                 style="border-radius:7px;display:block" alt="PeopleLens AI logo"/>
            PeopleLens AI
        </div>
        <div class="auth-kicker">Secure workforce intelligence</div>
    </div>
    """)

    _, center, _ = st.columns([1, 1.25, 1])
    with center.container(key="auth-card", border=True):
        is_registering = mode == "register"
        st.subheader("Create your workspace" if is_registering else "Welcome back")
        st.caption(
            "Create an account to upload feedback securely."
            if is_registering else
            "Sign in to continue to your workforce workspace."
        )
        with st.form("register_form" if is_registering else "sign_in_form", border=False):
            name = st.text_input("Full name", placeholder="Your name") if is_registering else ""
            email = st.text_input("Work email", placeholder="name@company.com")
            password = st.text_input(
                "Password", type="password",
                placeholder="At least 8 characters" if is_registering else "Your password"
            )
            submitted = st.form_submit_button(
                "Create account" if is_registering else "Sign in", width="stretch"
            )
        if submitted:
            if is_registering:
                success, result = register_user(name, email, password)
                if not success:
                    st.error(result)
                else:
                    st.session_state.user = {"email": email.strip().lower(), "name": result["name"]}
                    st.session_state.page = "upload"
                    st.rerun()
            else:
                user = authenticate_user(email, password)
                if user:
                    st.session_state.user = {"email": email.strip().lower(), "name": user["name"]}
                    st.session_state.page = "upload" if st.session_state.feedback_data is None else "dashboard"
                    st.rerun()
                else:
                    st.error("Incorrect email or password.")
        st.space("small")
        if st.button(
            "Already have an account? Sign in" if is_registering else "New here? Create an account",
            width="stretch"
        ):
            st.session_state.page = "login" if is_registering else "register"
            st.rerun()
        if st.button("← Back to home", width="stretch"):
            st.session_state.page = "home"
            st.rerun()
