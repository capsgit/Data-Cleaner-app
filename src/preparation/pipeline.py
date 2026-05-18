import pandas as pd

from src.preparation.profiler import profile_dataset
from src.preparation.audit import AuditLogger
from src.preparation.entities import (
    ImputationConfig,
    PreparationResult,
    PreparationSummary,
)

from src.preparation.imputers import apply_imputation
from src.preparation.transformations import (
    remove_fully_empty_rows,
)


class PreparationPipeline:

    def run(
            self,
            df: pd.DataFrame,
            imputation_config: ImputationConfig | None = None,
    ) -> PreparationResult:

        rows_before, cols_before = df.shape

        audit = AuditLogger()

        profile_before = profile_dataset(df)

        prepared_df = remove_fully_empty_rows(
            df=df,
            column="age",
            audit=audit,
        )

        if imputation_config is not None:
            prepared_df = apply_imputation(
                df=prepared_df,
                config=imputation_config,
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