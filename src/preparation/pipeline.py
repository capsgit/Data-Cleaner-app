import pandas as pd

from src.preparation.profiler import profile_dataset
from src.preparation.audit import AuditLogger
from src.preparation.entities import (
    PreparationResult,
    PreparationSummary,
)

from src.preparation.transformations import (
    remove_fully_empty_rows,
)


class PreparationPipeline:

    def run(self, df: pd.DataFrame) -> PreparationResult:

        rows_before, cols_before = df.shape

        audit = AuditLogger()

        profile_before = profile_dataset(df)

        prepared_df = remove_fully_empty_rows(
            df=df,
            column="age",
            audit=audit,
        )

        profile_after = profile_dataset(prepared_df)

        rows_after, cols_after = prepared_df.shape

        summary = PreparationSummary(
            rows_before=rows_before,
            rows_after=rows_after,
            columns_before=cols_before,
            columns_after=cols_after,
            total_changes=audit.count(),
        )

        return PreparationResult(
            dataframe=prepared_df,
            summary=summary,
            profile_before=profile_before,
            profile_after=profile_after,
            audit_log=audit.get_changes(),
        )