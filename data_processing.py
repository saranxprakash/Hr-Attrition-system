import re
from io import BytesIO

import pandas as pd


CSV_COLUMNS = [
    ("employee_name", "Employee name", "Text", "Required", "Ayesha Khan"),
    ("department", "Department or team", "Text", "Required", "Sales"),
    ("satisfaction_score", "Satisfaction score", "Number from 1 to 5", "Required", "4"),
    ("engagement_score", "Engagement score", "Number from 0 to 100", "Required", "76"),
    ("feedback", "Employee feedback", "Text", "Required", "I have good support but workload is high."),
    ("tenure_years", "Tenure", "Number of years", "Optional", "2.5"),
    ("job_role", "Job role", "Text", "Optional", "Sales executive"),
]

ALIASES = {
    "employee_name": ["employee_name", "employee", "name", "employee_id"],
    "department": ["department", "team", "division"],
    "satisfaction_score": ["satisfaction_score", "satisfaction", "rating", "score"],
    "engagement_score": ["engagement_score", "engagement", "engagement_rating"],
    "feedback": ["feedback", "comments", "comment", "employee_feedback", "response"],
    "tenure_years": ["tenure_years", "tenure", "years_at_company"],
    "job_role": ["job_role", "role", "position"],
}


def normalise_columns(frame):
    copy = frame.copy()
    copy.columns = [re.sub(r"[^a-z0-9]+", "_", column.strip().lower()).strip("_") for column in copy.columns]
    return copy


def find_column(frame, canonical_name):
    return next((column for column in ALIASES[canonical_name] if column in frame.columns), None)


def validate_feedback_csv(frame):
    normalised = normalise_columns(frame)
    missing = [name for name, _, _, requirement, _ in CSV_COLUMNS if requirement == "Required" and find_column(normalised, name) is None]
    invalid = []
    satisfaction = find_column(normalised, "satisfaction_score")
    engagement = find_column(normalised, "engagement_score")
    if satisfaction:
        scores = pd.to_numeric(normalised[satisfaction], errors="coerce")
        if scores.isna().any() or ((scores < 1) | (scores > 5)).any():
            invalid.append("satisfaction_score must contain values from 1 to 5.")
    if engagement:
        scores = pd.to_numeric(normalised[engagement], errors="coerce")
        if scores.isna().any() or ((scores < 0) | (scores > 100)).any():
            invalid.append("engagement_score must contain values from 0 to 100.")
    for canonical_name in ("employee_name", "department", "feedback"):
        column = find_column(normalised, canonical_name)
        if column and normalised[column].fillna("").astype(str).str.strip().eq("").any():
            invalid.append(f"{canonical_name} cannot contain blank values.")
    return missing, invalid


def read_feedback_csv(uploaded_file):
    """Read common CSV encodings and return a dataframe with the original headers."""
    contents = uploaded_file.getvalue()
    if not contents:
        raise ValueError("The uploaded file is empty.")

    errors = []
    for encoding in ("utf-8-sig", "utf-8", "latin-1"):
        try:
            return pd.read_csv(BytesIO(contents), encoding=encoding)
        except (UnicodeDecodeError, pd.errors.ParserError) as exc:
            errors.append(str(exc))
    raise ValueError("The file could not be read as a comma-separated CSV.")


def sample_feedback():
    return pd.DataFrame(
        [
            ["Priya Shah", "Sales", 3, 35, "Very high workload and limited growth opportunities.", 1.2, "Account executive"],
            ["Arjun Mehta", "Sales", 2, 49, "Compensation is below market and targets feel unrealistic.", 2.0, "Sales executive"],
            ["Neha Rao", "Product", 3, 58, "I need better manager support and clearer priorities.", 3.1, "Product analyst"],
            ["Ravi Kumar", "Engineering", 5, 89, "Strong team culture and learning opportunities.", 4.5, "Software engineer"],
            ["Sara Ali", "HR", 4, 76, "Flexible work policy has improved my experience.", 2.7, "HR specialist"],
            ["Kiran Patel", "Engineering", 2, 42, "Frequent overtime is causing burnout.", 0.8, "Software engineer"],
            ["Maya Singh", "Marketing", 4, 81, "Good collaboration and recognition from leadership.", 5.2, "Marketing manager"],
            ["Dev Nair", "Sales", 2, 45, "Commission structure is unclear and workload is high.", 1.6, "Sales executive"],
        ],
        columns=[column[0] for column in CSV_COLUMNS],
    )


def analyze_feedback(frame):
    frame = normalise_columns(frame)
    employee = find_column(frame, "employee_name")
    department = find_column(frame, "department")
    satisfaction = find_column(frame, "satisfaction_score")
    engagement = find_column(frame, "engagement_score")
    feedback = find_column(frame, "feedback")
    tenure = find_column(frame, "tenure_years")
    role = find_column(frame, "job_role")

    result = pd.DataFrame(index=frame.index)
    result["Employee"] = frame[employee].astype(str)
    result["Department"] = frame[department].fillna("Unassigned").astype(str)
    result["Satisfaction"] = pd.to_numeric(frame[satisfaction], errors="coerce").clip(1, 5)
    result["Engagement"] = pd.to_numeric(frame[engagement], errors="coerce").clip(0, 100)
    result["Feedback"] = frame[feedback].fillna("").astype(str)
    result["Tenure (years)"] = pd.to_numeric(frame[tenure], errors="coerce") if tenure else pd.NA
    result["Job role"] = frame[role].fillna("Not provided").astype(str) if role else "Not provided"

    keywords = {
        "Burnout / workload": ["burnout", "overtime", "workload", "overworked", "stress"],
        "Compensation": ["pay", "salary", "compensation", "commission", "bonus"],
        "Management": ["manager", "leadership", "support", "management"],
        "Career growth": ["growth", "promotion", "career", "learning"],
    }
    result["Primary reason"] = [", ".join([label for label, terms in keywords.items() if any(term in text.lower() for term in terms)][:2]) or "Low engagement indicators" for text in result["Feedback"]]
    text_penalty = result["Feedback"].str.lower().str.contains("burnout|overtime|workload|salary|compensation|manager|leave").astype(int) * 12
    early_tenure_penalty = (result["Tenure (years)"].fillna(99) < 1).astype(int) * 5
    result["Risk score"] = ((5 - result["Satisfaction"]) * 13 + (100 - result["Engagement"]) * 0.45 + text_penalty + early_tenure_penalty).clip(5, 98).round().astype(int)
    result["Risk level"] = pd.cut(result["Risk score"], [0, 39, 64, 100], labels=["Low", "Medium", "High"], include_lowest=True)
    return result
