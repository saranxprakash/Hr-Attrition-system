import json
import re
from datetime import datetime
from pathlib import Path
from uuid import uuid4

import pandas as pd


ARCHIVE_DIRECTORY = Path(__file__).with_name("data") / "csv_archive"
ARCHIVE_INDEX = ARCHIVE_DIRECTORY / "index.json"


def _read_index():
    if not ARCHIVE_INDEX.exists():
        return []
    try:
        return json.loads(ARCHIVE_INDEX.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []


def _write_index(records):
    ARCHIVE_DIRECTORY.mkdir(parents=True, exist_ok=True)
    ARCHIVE_INDEX.write_text(json.dumps(records, indent=2), encoding="utf-8")


def archive_csv(uploaded_file, frame, owner_email, reporting_month):
    """Save an uploaded CSV locally and return its archive metadata."""
    ARCHIVE_DIRECTORY.mkdir(parents=True, exist_ok=True)
    safe_name = re.sub(r"[^A-Za-z0-9_.-]+", "_", uploaded_file.name)
    archive_id = uuid4().hex[:12]
    stored_name = f"{datetime.now():%Y%m%d_%H%M%S}_{archive_id}_{safe_name}"
    path = ARCHIVE_DIRECTORY / stored_name
    path.write_bytes(uploaded_file.getvalue())
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
    records = _read_index()
    records.insert(0, record)
    _write_index(records)
    return record


def list_archives(owner_email):
    return [record for record in _read_index() if record["owner"] == owner_email.lower()]


def load_archive(archive_id, owner_email):
    record = next((item for item in list_archives(owner_email) if item["id"] == archive_id), None)
    if record is None:
        return None, None
    path = ARCHIVE_DIRECTORY / record["stored_name"]
    if not path.exists():
        return None, None
    return pd.read_csv(path), record


def delete_archive(archive_id, owner_email):
    records = _read_index()
    target = next((item for item in records if item["id"] == archive_id and item["owner"] == owner_email.lower()), None)
    if target is None:
        return False
    path = ARCHIVE_DIRECTORY / target["stored_name"]
    if path.exists():
        path.unlink()
    _write_index([item for item in records if item["id"] != archive_id])
    return True
