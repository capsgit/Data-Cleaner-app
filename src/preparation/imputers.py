import pandas as pd

from src.preparation.audit import AuditLogger
from src.preparation.entities import CellChange


def fill_numeric_median(
    df: pd.DataFrame,
    column: str,
    audit: AuditLogger,
) -> pd.DataFrame:

    median_value = df[column].median()

    missing_mask = df[column].isna()

    for row_idx in df[missing_mask].index:

        audit.log(
            CellChange(
                row_id=int(row_idx),
                column=column,
                old_value=None,
                new_value=median_value,
                action="IMPUTE_VALUE",
                method="median",
                status="imputed",
                reason="Filled missing numeric value using median",
            )
        )

    df.loc[missing_mask, column] = median_value

    return df