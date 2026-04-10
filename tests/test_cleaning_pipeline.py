import pandas as pd

from backend.services.cleaning_pipeline import CleaningPipeline
from src.cleaning.cleaner import DataCleaner
from src.cleaning.options import CleaningOptions
from src.utils.logger import build_logger


"""
Integration tests for the backend cleaning pipeline.

These tests validate preview generation, CSV generation,
and HTML report generation on top of the core cleaning logic.
"""


def get_pipeline() -> CleaningPipeline:
    """
    Create a CleaningPipeline instance with a DataCleaner dependency.
    """
    logger = build_logger("test_pipeline_logger")
    cleaner = DataCleaner(logger=logger)
    return CleaningPipeline(cleaner=cleaner)


def test_run_preview_returns_expected_structure():
    """
    Ensure that preview output contains the expected keys and values.
    """
    pipeline = get_pipeline()

    df = pd.DataFrame({
        "A": [1, None],
        "B": [2, None],
    })

    options = CleaningOptions(drop_empty_rows=True)

    result = pipeline.run_preview(df, options)

    assert "rows_before" in result
    assert "rows_after" in result
    assert "cols_before" in result
    assert "cols_after" in result
    assert "rows_removed" in result
    assert "cols_removed" in result
    assert "applied_steps" in result
    assert "preview" in result

    assert result["rows_before"] == 2
    assert result["rows_after"] == 1
    assert isinstance(result["preview"], list)


def test_run_preview_contains_preview_records():
    """
    Ensure that preview output returns row records as dictionaries.
    """
    pipeline = get_pipeline()

    df = pd.DataFrame({
        "A": [1, 2],
        "B": [3, 4],
    })

    options = CleaningOptions()

    result = pipeline.run_preview(df, options)

    assert len(result["preview"]) == 2
    assert isinstance(result["preview"][0], dict)
    assert result["preview"][0]["A"] == 1


def test_run_download_csv_returns_csv_string():
    """
    Ensure that CSV export returns string content with column names and rows.
    """
    pipeline = get_pipeline()

    df = pd.DataFrame({
        "A": [1, 2],
        "B": [3, 4],
    })

    options = CleaningOptions()

    csv_content = pipeline.run_download_csv(df, options)

    assert isinstance(csv_content, str)
    assert "A,B" in csv_content
    assert "1,3" in csv_content
    assert "2,4" in csv_content


def test_run_download_report_returns_html_string():
    """
    Ensure that HTML report generation returns HTML content.
    """
    pipeline = get_pipeline()

    df = pd.DataFrame({
        "A": [1, 2, 3],
        "B": [4, 5, 6],
    })

    options = CleaningOptions()

    html_content = pipeline.run_download_report(df, options)

    assert isinstance(html_content, str)
    assert "<html" in html_content.lower() or "<!doctype html" in html_content.lower()