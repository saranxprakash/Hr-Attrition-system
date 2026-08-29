from datetime import date

import pandas as pd
import streamlit as st

from data_processing import CSV_COLUMNS, read_feedback_csv, sample_feedback, validate_feedback_csv
from storage import archive_csv, delete_archive, list_archives, load_archive


def render_upload_page():
    if st.session_state.user is None:
        st.session_state.page = "home"
        st.rerun()
    st.html('<div class="auth-header"><div class="brand"><span class="brand-mark">⌁</span> PeopleLens AI</div><div class="auth-kicker">Step 1 of 2 · Import workforce feedback</div></div>')
    upload_column, history_column = st.columns([1.25, .75], gap="large")
    with upload_column.container(key="upload-card", border=True):
        st.subheader(f"Welcome, {st.session_state.user['name']}")
        st.write("Upload an employee-feedback CSV to create a detailed, private workforce analysis.")
        st.download_button(
            "Download CSV template",
            sample_feedback().to_csv(index=False).encode("utf-8"),
            "hr_insight_feedback_template.csv",
            "text/csv",
            width="stretch",
        )
        if st.button("Explore with sample data", width="stretch", key="load_sample_data"):
            st.session_state.feedback_data = sample_feedback()
            st.session_state.archive_record = {"reporting_month_display": "Sample report"}
            st.session_state.chat_history = []
            st.session_state.page = "dashboard"
            st.rerun()
        with st.expander("CSV format instructions", expanded=True):
            st.write("Save the file as a UTF-8 comma-separated `.csv` file. Each row must represent one employee feedback response.")
            st.dataframe(
                pd.DataFrame(CSV_COLUMNS, columns=["Column", "Meaning", "Format", "Status", "Example"]),
                hide_index=True,
                width="stretch",
            )
            st.caption("Use exactly the recommended names where possible. Common alternatives such as `name`, `team`, `rating`, `engagement`, and `comments` are also recognised.")
        reporting_month = st.date_input(
            "Reporting month",
            value=date.today().replace(day=1),
            help="Choose the month represented by this employee-feedback report.",
        )
        st.caption(f"This upload will be saved as: {reporting_month.strftime('%B %Y')}")
        uploaded = st.file_uploader(
            "Employee feedback CSV",
            type="csv",
            key="feedback_upload",
            help="Upload a CSV with employee feedback and scores.",
        )
        if uploaded is not None:
            try:
                frame = read_feedback_csv(uploaded)
                if frame.empty:
                    st.error("This CSV has no data rows. Upload a file with employee feedback.")
                else:
                    missing, invalid = validate_feedback_csv(frame)
                    if missing or invalid:
                        if missing:
                            st.error("Missing required columns: " + ", ".join(f"`{name}`" for name in missing))
                        for message in invalid:
                            st.error(message)
                        st.info("Download the template above, copy your data into it, then upload the completed file.")
                    else:
                        st.success(f"{len(frame):,} feedback records passed validation and are ready for analysis.")
                    if not missing and not invalid and st.button("Generate detailed analysis", type="primary", width="stretch"):
                        st.session_state.feedback_data = frame
                        st.session_state.archive_record = archive_csv(
                            uploaded, frame, st.session_state.user["email"], reporting_month
                        )
                        st.session_state.chat_history = []
                        st.session_state.page = "dashboard"
                        st.rerun()
            except ValueError as exc:
                st.error(f"We could not read this CSV: {exc}")
            except Exception as exc:
                st.error(f"We could not process this CSV: {exc}")
        if st.button("Sign out", width="stretch"):
            st.session_state.user = None
            st.session_state.feedback_data = None
            st.session_state.page = "home"
            st.rerun()
    with history_column.container(key="archive-panel", border=True):
        st.subheader("Your CSV archive")
        st.caption("Past uploads are stored locally on this computer for your workspace.")
        archives = list_archives(st.session_state.user["email"])
        if not archives:
            st.info("No previous CSV uploads yet.")
        else:
            choices = {f"{item['original_name']} · {item['uploaded_at']}": item for item in archives}
            selected_label = st.selectbox("Past uploads", choices.keys())
            selected = choices[selected_label]
            st.caption(f"{selected['rows']:,} rows · Saved {selected['uploaded_at']}")
            if st.button("Load this dataset", width="stretch"):
                frame, record = load_archive(selected["id"], st.session_state.user["email"])
                if frame is not None:
                    st.session_state.feedback_data = frame
                    st.session_state.archive_record = record
                    st.session_state.chat_history = []
                    st.session_state.page = "dashboard"
                    st.rerun()
            if st.button("Delete this dataset", width="stretch"):
                delete_archive(selected["id"], st.session_state.user["email"])
                st.rerun()
