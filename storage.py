import re
from datetime import datetime
from uuid import uuid4

import pandas as pd
from io import StringIO
from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()  # this line must come BEFORE os.environ
from dotenv import load_dotenv
import os

load_dotenv()
SUPABASE_URL = "https://bprkzmyvfxyoljhjeyyr.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJwcmt6bXl2Znh5b2xqaGpleXlyIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc4ODAwNTgwMSwiZXhwIjoyMTAzNTgxODAxfQ.6JsHLIXAzaGAmJmP3D5CTXz-CxKwHFwTIMA6Jj2LUrQ"  # use service role for backend
BUCKET_NAME = "csv-archive"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def archive_csv(uploaded_file, frame, owner_email, reporting_month):
    """Upload CSV to Supabase Storage and save metadata to Postgres."""
    archive_id = uuid4().hex[:12]
    safe_name = re.sub(r"[^A-Za-z0-9_.-]+", "_", uploaded_file.name)
    stored_name = f"{datetime.now():%Y%m%d_%H%M%S}_{archive_id}_{safe_name}"

    # Upload file to Supabase Storage
    supabase.storage.from_(BUCKET_NAME).upload(
        path=stored_name,
        file=uploaded_file.getvalue(),
        file_options={"content-type": "text/csv"},
    )

    # Save metadata to Postgres
    record = {
        "id": archive_id,
        "owner": owner_email.lower(),
        "original_name": uploaded_file.name,
        "stored_name": stored_name,
        "rows": len(frame),
        "reporting_month": reporting_month.strftime("%Y-%m"),
        "reporting_month_display": reporting_month.strftime("%B %Y"),
        "uploaded_at": datetime.now().strftime("%d %b %Y, %I:%M %p"),
    }
    supabase.table("csv_archives").insert(record).execute()
    return record


def list_archives(owner_email):
    response = (
        supabase.table("csv_archives")
        .select("*")
        .eq("owner", owner_email.lower())
        .order("uploaded_at", desc=True)
        .execute()
    )
    return response.data


def load_archive(archive_id, owner_email):
    # Verify ownership
    response = (
        supabase.table("csv_archives")
        .select("*")
        .eq("id", archive_id)
        .eq("owner", owner_email.lower())
        .single()
        .execute()
    )
    record = response.data
    if not record:
        return None, None

    # Download CSV from Storage
    file_bytes = supabase.storage.from_(BUCKET_NAME).download(record["stored_name"])
    frame = pd.read_csv(StringIO(file_bytes.decode("utf-8")))
    return frame, record


def delete_archive(archive_id, owner_email):
    # Verify ownership and get stored_name
    response = (
        supabase.table("csv_archives")
        .select("stored_name")
        .eq("id", archive_id)
        .eq("owner", owner_email.lower())
        .single()
        .execute()
    )
    record = response.data
    if not record:
        return False

    # Delete from Storage and Postgres
    supabase.storage.from_(BUCKET_NAME).remove([record["stored_name"]])
    supabase.table("csv_archives").delete().eq("id", archive_id).execute()
    return True