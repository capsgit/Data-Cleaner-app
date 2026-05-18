import pandas as pd


def validate_numeric_column(
    df: pd.DataFrame,
    column: str,
) -> bool:
    return pd.api.types.is_numeric_dtype(df[column])