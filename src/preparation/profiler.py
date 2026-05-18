import pandas as pd


def profile_dataset(df: pd.DataFrame) -> dict:

    return {
        "rows": len(df),

        "columns": len(df.columns),

        "missing_total": int(
            df.isna().sum().sum()
        ),

        "missing_by_column": {
            column: int(count)
            for column, count
            in df.isna().sum().items()
        },

        "duplicated_rows": int(
            df.duplicated().sum()
        ),
    }