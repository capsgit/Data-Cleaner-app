import pandas as pd

from src.preparation.audit import AuditLogger
from src.preparation.entities import CellChange


def remove_fully_empty_rows(
    df: pd.DataFrame,
    column: str,
    audit: AuditLogger,
) -> pd.DataFrame:

    empty_rows = df[df.isna().all(axis=1)]

    for row_idx in empty_rows.index:

        audit.log(
            CellChange(
                row_id=int(row_idx),
                column=None,
                old_value="FULL_ROW",
                new_value=None,
                action="DROP_ROW",
                method="remove_fully_empty_rows",
                status="deleted",
                reason="Row contains only missing values",
            )
        )

    cleaned_df = df.dropna(how="all")

    return cleaned_df