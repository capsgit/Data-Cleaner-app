import pandas as pd

from src.cleaning.cleaner import DataCleaner
from src.cleaning.options import CleaningOptions
from src.utils.logger import build_logger


"""
Integration tests for the DataCleaner pipeline.

These tests validate that multiple cleaning steps are correctly
orchestrated and applied in sequence.
"""


def get_cleaner() -> DataCleaner:
    """
    Create a DataCleaner instance with a test logger.
    """
    logger = build_logger("test_logger")
    return DataCleaner(logger=logger)


def test_cleaner_removes_empty_rows():
    """
    Ensure that the pipeline removes fully empty rows when enabled.
    """
    cleaner = get_cleaner()

    df = pd.DataFrame({
        "A": [1, None],
        "B": [2, None],
    })

    options = CleaningOptions(drop_empty_rows=True)

    result = cleaner.clean_dataframe(df, options)

    assert result.rows_after == 1


def test_cleaner_without_steps_returns_same_dataframe():
    """
    Ensure that no changes occur when no cleaning options are enabled.
    """
    cleaner = get_cleaner()

    df = pd.DataFrame({"A": [1, 2]})

    options = CleaningOptions()

    result = cleaner.clean_dataframe(df, options)

    assert result.rows_before == result.rows_after
    assert result.cols_before == result.cols_after


def test_cleaner_cast_numeric_step():
    """
    Ensure that numeric casting is correctly applied within the pipeline.
    """
    cleaner = get_cleaner()

    df = pd.DataFrame({
        "price": ["10", "abc"]
    })

    options = CleaningOptions(
        cast_numeric=True,
        numeric_columns=["price"]
    )

    result = cleaner.clean_dataframe(df, options)

    assert result.cleaned_df["price"].isna().sum() == 1


def test_cleaner_applied_steps_is_not_empty():
    """
    Ensure that applied_steps is populated when transformations occur.
    """
    cleaner = get_cleaner()

    df = pd.DataFrame({
        "A": [1, None],
        "B": [2, None],
    })

    options = CleaningOptions(drop_empty_rows=True)

    result = cleaner.clean_dataframe(df, options)

    assert len(result.applied_steps) > 0


def test_cleaner_removes_repeated_header_rows():
    """
    Ensure that repeated header rows are removed correctly.
    """
    cleaner = get_cleaner()

    df = pd.DataFrame({
        "Order ID": ["123", "Order ID", "456"],
        "Product": ["Cable", "Product", "Phone"],
    })

    options = CleaningOptions(
        remove_repeated_header_rows=True,
        repeated_header_column="Order ID",
        repeated_header_value="Order ID",
    )

    result = cleaner.clean_dataframe(df, options)

    assert result.rows_after == 2
    assert "Order ID" not in result.cleaned_df["Order ID"].values


def test_cleaner_cast_datetime_step():
    """
    Ensure that datetime casting is correctly applied in the pipeline.
    """
    cleaner = get_cleaner()

    df = pd.DataFrame({
        "Order Date": ["04/19/19 08:46", "invalid"]
    })

    options = CleaningOptions(
        cast_datetime=True,
        datetime_column="Order Date",
        datetime_format="%m/%d/%y %H:%M",
    )

    result = cleaner.clean_dataframe(df, options)

    assert result.cleaned_df["Order Date"].isna().sum() == 1


def test_cleaner_drop_columns_step():
    """
    Ensure that column removal works correctly within the pipeline.
    """
    cleaner = get_cleaner()

    df = pd.DataFrame({
        "A": [1],
        "B": [2],
    })

    options = CleaningOptions(
        drop_columns=True,
        columns_to_drop=["B"],
    )

    result = cleaner.clean_dataframe(df, options)

    assert "B" not in result.cleaned_df.columns


def test_cleaner_drop_duplicates_with_subset():
    """
    Ensure that duplicates are removed based on a subset of columns.
    """
    cleaner = get_cleaner()

    df = pd.DataFrame({
        "id": [1, 1, 2],
        "value": ["A", "B", "C"],
    })

    options = CleaningOptions(
        drop_duplicates=True,
        duplicate_subset=["id"],
    )

    result = cleaner.clean_dataframe(df, options)

    assert result.rows_after == 2


def test_cleaner_multiple_steps_together():
    """
    Ensure that multiple cleaning steps are applied in sequence correctly.
    """
    cleaner = get_cleaner()

    df = pd.DataFrame({
        "Order ID": ["123", "Order ID", "123", None],
        "Price": ["10", "Price", "10", None],
    })

    options = CleaningOptions(
        drop_empty_rows=True,
        remove_repeated_header_rows=True,
        repeated_header_column="Order ID",
        repeated_header_value="Order ID",
        cast_numeric=True,
        numeric_columns=["Price"],
        drop_duplicates=True,
        duplicate_subset=["Order ID"],
    )

    result = cleaner.clean_dataframe(df, options)

    assert result.rows_after == 1