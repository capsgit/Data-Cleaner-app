import io

import pandas as pd
import pytest
from fastapi import HTTPException, UploadFile

from backend.services.cleaning_service import (
    build_cleaning_options,
    parse_cleaning_request,
    read_csv_upload,
)


"""
Unit tests for backend cleaning service helpers.

These tests validate request parsing, option building,
and CSV upload reading behavior.
"""


def make_upload_file(filename: str, content: str) -> UploadFile:
    """
    Create an UploadFile instance for testing.
    """
    return UploadFile(
        filename=filename,
        file=io.BytesIO(content.encode("utf-8")),
    )


def test_parse_cleaning_request_returns_model():
    """
    Ensure that a valid JSON payload is parsed into a CleaningRequest model.
    """
    options_json = """
    {
        "drop_empty_rows": true,
        "cast_numeric": true,
        "numeric_columns": ["Price"]
    }
    """

    request_model = parse_cleaning_request(options_json)

    assert request_model.drop_empty_rows is True
    assert request_model.cast_numeric is True
    assert request_model.numeric_columns == ["Price"]


def test_parse_cleaning_request_raises_for_invalid_json():
    """
    Ensure that invalid JSON raises an exception.
    """
    invalid_json = "{invalid json}"

    with pytest.raises(Exception):
        parse_cleaning_request(invalid_json)


def test_build_cleaning_options_returns_domain_object():
    """
    Ensure that request model data is correctly converted into CleaningOptions.
    """
    options_json = """
    {
        "drop_empty_rows": true,
        "drop_duplicates": true,
        "duplicate_subset": ["Order ID"]
    }
    """

    request_model = parse_cleaning_request(options_json)
    options = build_cleaning_options(request_model)

    assert options.drop_empty_rows is True
    assert options.drop_duplicates is True
    assert options.duplicate_subset == ["Order ID"]


def test_read_csv_upload_reads_valid_csv():
    """
    Ensure that a valid CSV upload is correctly read into a DataFrame.
    """
    file = make_upload_file(
        filename="sample.csv",
        content="A,B\n1,2\n3,4\n",
    )

    df = read_csv_upload(file)

    assert isinstance(df, pd.DataFrame)
    assert df.shape == (2, 2)
    assert list(df.columns) == ["A", "B"]


def test_read_csv_upload_rejects_non_csv_extension():
    """
    Ensure that files without a .csv extension are rejected.
    """
    file = make_upload_file(
        filename="sample.txt",
        content="A,B\n1,2\n",
    )

    with pytest.raises(HTTPException) as exc_info:
        read_csv_upload(file)

    assert exc_info.value.status_code == 400
    assert "Only CSV files are supported" in exc_info.value.detail


def test_read_csv_upload_raises_for_invalid_csv_content():
    """
    Ensure that invalid CSV content raises an HTTPException.
    """
    file = UploadFile(
        filename="sample.csv",
        file=io.BytesIO(b"\x00\x01\x02\x03"),
    )

    with pytest.raises(HTTPException) as exc_info:
        read_csv_upload(file)

    assert exc_info.value.status_code == 400
    assert "Failed to read CSV file" in exc_info.value.detail