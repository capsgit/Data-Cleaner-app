import pandas as pd

from src.cleaning.cleaner import DataCleaner
from src.cleaning.options import CleaningOptions
from src.utils.logger import build_logger


def get_cleaner():
    logger = build_logger("test_logger")
    return DataCleaner(logger=logger)


# ---------------------------------------------------------
# TEST 1: basic pipeline
# ---------------------------------------------------------
def test_cleaner_removes_empty_rows():
    cleaner = get_cleaner()

    df = pd.DataFrame({
        "A": [1, None],
        "B": [2, None],
    })

    options = CleaningOptions(
        drop_empty_rows=True
    )

    result = cleaner.clean_dataframe(df, options)

    assert result.rows_after == 1


# ---------------------------------------------------------
# TEST 2: without activated options
# ---------------------------------------------------------
def test_cleaner_without_steps_returns_same_dataframe():
    cleaner = get_cleaner()

    df = pd.DataFrame({
        "A": [1, 2]
    })

    options = CleaningOptions()

    result = cleaner.clean_dataframe(df, options)

    assert result.rows_before == result.rows_after


# ---------------------------------------------------------
# TEST 3: cast_numeric into the pipeline
# ---------------------------------------------------------
def test_cleaner_cast_numeric_step():
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


# ---------------------------------------------------------
# TEST 4: applied_steps fully
# ---------------------------------------------------------
def test_cleaner_applied_steps_is_not_empty():
    cleaner = get_cleaner()

    df = pd.DataFrame({
        "A": [1, None],
        "B": [2, None],
    })

    options = CleaningOptions(
        drop_empty_rows=True
    )

    result = cleaner.clean_dataframe(df, options)

    assert len(result.applied_steps) > 0