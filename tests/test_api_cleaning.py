import json

from fastapi.testclient import TestClient

from backend.main import app


"""
API tests for cleaning endpoints.

These tests validate the FastAPI routes end-to-end using TestClient.
"""

client = TestClient(app)


def get_sample_csv_bytes() -> bytes:
    """
    Return a small sample CSV as bytes.
    """
    content = (
        "Order ID,Product,Quantity Ordered,Price Each,Order Date\n"
        "123,Cable,2,11.95,04/19/19 08:46\n"
        "Order ID,Product,Quantity Ordered,Price Each,Order Date\n"
        "456,Phone,1,600,04/20/19 10:30\n"
    )
    return content.encode("utf-8")


def get_sample_options_json() -> str:
    """
    Return a valid JSON string with cleaning options.
    """
    payload = {
        "drop_empty_rows": True,
        "remove_repeated_header_rows": True,
        "repeated_header_column": "Order ID",
        "repeated_header_value": "Order ID",
        "cast_numeric": True,
        "numeric_columns": ["Quantity Ordered", "Price Each"],
        "cast_datetime": True,
        "datetime_column": "Order Date",
        "datetime_format": "%m/%d/%y %H:%M",
        "drop_na": False,
        "drop_na_subset": [],
        "drop_duplicates": False,
        "duplicate_subset": [],
        "drop_columns": False,
        "columns_to_drop": [],
    }
    return json.dumps(payload)


def test_health_check_returns_ok():
    """
    Ensure that the health endpoint returns status ok.
    """
    response = client.get("/cleaning/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_preview_endpoint_returns_metrics_and_preview():
    """
    Ensure that preview endpoint returns metrics and preview data.
    """
    response = client.post(
        "/cleaning/preview",
        files={"file": ("sample.csv", get_sample_csv_bytes(), "text/csv")},
        data={"options_json": get_sample_options_json()},
    )

    assert response.status_code == 200

    body = response.json()

    assert "rows_before" in body
    assert "rows_after" in body
    assert "preview" in body
    assert isinstance(body["preview"], list)


def test_download_csv_returns_csv_file():
    """
    Ensure that CSV download endpoint returns CSV content.
    """
    response = client.post(
        "/cleaning/download-csv",
        files={"file": ("sample.csv", get_sample_csv_bytes(), "text/csv")},
        data={"options_json": get_sample_options_json()},
    )

    assert response.status_code == 200
    assert "text/csv" in response.headers["content-type"]
    assert "attachment; filename=cleaned_data.csv" in response.headers["content-disposition"]
    assert "Order ID" in response.text


def test_download_report_returns_html_file():
    """
    Ensure that HTML report download endpoint returns HTML content.
    """
    response = client.post(
        "/cleaning/download-report",
        files={"file": ("sample.csv", get_sample_csv_bytes(), "text/csv")},
        data={"options_json": get_sample_options_json()},
    )

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "attachment; filename=data_profile_report.html" in response.headers["content-disposition"]
    assert "<html" in response.text.lower() or "<!doctype html" in response.text.lower()