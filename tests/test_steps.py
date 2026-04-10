import pandas as pd

from src.cleaning.steps import (
    cast_datetime,
    cast_numeric,
    drop_columns,
    drop_duplicates,
    drop_empty_rows,
    drop_na,
    remove_repeated_header_rows,
)


"""
Unit tests for individual cleaning steps.

Each function is tested in isolation using small, controlled DataFrames.
This ensures predictable behavior and simplifies debugging.
"""


def test_drop_empty_rows_removes_fully_empty_rows():
    """
    Ensure that rows where all values are NaN are removed.
    """
    df = pd.DataFrame({
        "A": [1, None, None],
        "B": [2, None, None],
    })

    result = drop_empty_rows(df)

    assert len(result) == 1


def test_remove_repeated_header_rows_removes_header_like_rows():
    """
    Ensure that rows containing repeated header values are removed.
    """
    df = pd.DataFrame({
        "Order ID": ["123", "Order ID", "456"],
        "Product": ["Cable", "Product", "Phone"],
    })

    result = remove_repeated_header_rows(
        df,
        column="Order ID",
        header_value="Order ID",
    )

    assert len(result) == 2
    assert "Order ID" not in result["Order ID"].values


def test_cast_numeric_converts_invalid_values_to_nan():
    """
    Ensure that non-numeric values are converted to NaN.
    """
    df = pd.DataFrame({
        "price": ["10", "20", "abc"]
    })

    result = cast_numeric(df, ["price"])

    assert result["price"].isna().sum() == 1


def test_cast_datetime_converts_invalid_values_to_nat():
    """
    Ensure that invalid datetime values are converted to NaT.
    """
    df = pd.DataFrame({
        "Order Date": ["04/19/19 08:46", "invalid"]
    })

    result = cast_datetime(
        df,
        column="Order Date",
        fmt="%m/%d/%y %H:%M",
    )

    assert result["Order Date"].isna().sum() == 1


def test_drop_na_removes_rows_with_missing_values():
    """
    Ensure that rows containing any NaN values are removed.
    """
    df = pd.DataFrame({
        "A": [1, None, 3]
    })

    result = drop_na(df)

    assert len(result) == 2


def test_drop_na_with_subset():
    """
    Ensure that drop_na only considers specified columns.
    """
    df = pd.DataFrame({
        "A": [1, None, 3],
        "B": [None, 2, 3],
    })

    result = drop_na(df, subset=["A"])

    assert len(result) == 2


def test_drop_duplicates_removes_duplicate_rows():
    """
    Ensure that duplicate rows are removed.
    """
    df = pd.DataFrame({
        "A": [1, 1, 2]
    })

    result = drop_duplicates(df)

    assert len(result) == 2


def test_drop_duplicates_with_subset():
    """
    Ensure that duplicates are removed based on a subset of columns.
    """
    df = pd.DataFrame({
        "id": [1, 1, 2],
        "value": ["A", "B", "C"],
    })

    result = drop_duplicates(df, subset=["id"])

    assert len(result) == 2


def test_drop_columns_removes_selected_columns():
    """
    Ensure that specified columns are removed from the DataFrame.
    """
    df = pd.DataFrame({
        "A": [1],
        "B": [2],
    })

    result = drop_columns(df, ["B"])

    assert "B" not in result.columns
    assert "A" in result.columns