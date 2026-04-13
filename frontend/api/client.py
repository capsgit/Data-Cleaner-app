import json

import requests

from frontend.config import BACKEND_URL


def build_files(uploaded_file):
    return {
        "file": (uploaded_file.name, uploaded_file.getvalue(), "text/csv"),
    }


def build_data(payload: dict):
    return {
        "options_json": json.dumps(payload),
    }


def request_cleaning_preview(uploaded_file, payload: dict, timeout: int = 120):
    files = build_files(uploaded_file)
    data = build_data(payload)

    return requests.post(
        f"{BACKEND_URL}/cleaning/preview",
        files=files,
        data=data,
        timeout=timeout,
    )


def request_cleaned_csv(uploaded_file, payload: dict, timeout: int = 60):
    files = build_files(uploaded_file)
    data = build_data(payload)

    return requests.post(
        f"{BACKEND_URL}/cleaning/download-csv",
        files=files,
        data=data,
        timeout=timeout,
    )


def request_cleaning_report(uploaded_file, payload: dict, timeout: int = 60):
    files = build_files(uploaded_file)
    data = build_data(payload)

    return requests.post(
        f"{BACKEND_URL}/cleaning/download-report",
        files=files,
        data=data,
        timeout=timeout,
    )