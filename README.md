# PeopleLens AI

A professional Streamlit dashboard with a matching PeopleLens AI home/login screen. The code is split into simple files: `app.py` (entry point), `home.py` (homepage and login), `dashboard.py` (analytics screen), `data_processing.py` (CSV analysis), and `styles.py` (design system).

## Run locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Open the local URL shown by Streamlit. The dashboard includes sample data until an employee-feedback CSV is uploaded.

## Gemini assistant setup

Install the dependencies with the same Python environment used to start Streamlit. Then copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` and add your Gemini API key as `GEMINI_API_KEY`. Keep this file private; it is excluded from Git.

If PowerShell blocks the activation script, run this once in the same terminal first:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

## Recommended feedback CSV fields

`employee_name`, `department`, `satisfaction_score` (1–5), `engagement_score` (0–100), and `feedback`.

The risk score is a screening signal based on satisfaction, engagement, and feedback themes. Use it to guide a private, supportive check-in; never use it as the sole basis for an employment decision.
