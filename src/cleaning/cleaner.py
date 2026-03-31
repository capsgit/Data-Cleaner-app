from dataclasses import dataclass, field

import pandas as pd

from src.cleaning.options import CleaningOptions
from src.cleaning.steps import (
    cast_datetime,
    cast_numeric,
    drop_columns,
    drop_duplicates,
    drop_empty_rows,
    drop_na,
    remove_repeated_header_rows,
)


@dataclass
class CleaningResult:
    """
    Cleaning process result.
    """
    cleaned_df: pd.DataFrame
    rows_before: int
    rows_after: int
    cols_before: int
    cols_after: int
    applied_steps: list[dict] = field(default_factory=list)


class DataCleaner:
    """
    Pipeline Orchestator.
    """

    def __init__(self, logger) -> None:
        self.logger = logger

    def clean_dataframe(
        self,
        df: pd.DataFrame,
        options: CleaningOptions,
    ) -> CleaningResult:
        """
        Aplay cleaning transformations following the options defined on Front-end.
        """
        working_df = df.copy()

        rows_before = len(working_df)
        cols_before = len(working_df.columns)
        applied_steps: list[dict] = []

        self.logger.info("Starting cleaning pipeline")
        self.logger.info("Initial shape: %s", working_df.shape)

        pipeline = [
            (
                "drop_empty_rows",
                options.drop_empty_rows,
                lambda current_df: drop_empty_rows(current_df),
            ),
            (
                "remove_repeated_header_rows",
                options.remove_repeated_header_rows,
                lambda current_df: remove_repeated_header_rows(
                    current_df,
                    column=options.repeated_header_column or "",
                    header_value=options.repeated_header_value or "",
                ),
            ),
            (
                "cast_numeric",
                options.cast_numeric,
                lambda current_df: cast_numeric(
                    current_df,
                    columns=options.numeric_columns,
                ),
            ),
            (
                "cast_datetime",
                options.cast_datetime,
                lambda current_df: cast_datetime(
                    current_df,
                    column=options.datetime_column or "",
                    fmt=options.datetime_format or None,
                ),
            ),
            (
                "drop_na",
                options.drop_na,
                lambda current_df: drop_na(
                    current_df,
                    subset=options.drop_na_subset,
                ),
            ),
            (
                "drop_duplicates",
                options.drop_duplicates,
                lambda current_df: drop_duplicates(
                    current_df,
                    subset=options.duplicate_subset,
                ),
            ),
            (
                "drop_columns",
                options.drop_columns,
                lambda current_df: drop_columns(
                    current_df,
                    columns=options.columns_to_drop,
                ),
            ),
        ]

        for step_name, enabled, step_func in pipeline:
            if not enabled:
                continue

            before_rows = len(working_df)
            before_cols = len(working_df.columns)

            working_df = step_func(working_df)

            after_rows = len(working_df)
            after_cols = len(working_df.columns)

            step_summary = {
                "step": step_name,
                "rows_before": before_rows,
                "rows_after": after_rows,
                "rows_removed": before_rows - after_rows,
                "cols_before": before_cols,
                "cols_after": after_cols,
                "cols_removed": before_cols - after_cols,
            }
            applied_steps.append(step_summary)

            self.logger.info(
                "%s | rows: %s -> %s | cols: %s -> %s",
                step_name,
                before_rows,
                after_rows,
                before_cols,
                after_cols,
            )

        result = CleaningResult(
            cleaned_df=working_df,
            rows_before=rows_before,
            rows_after=len(working_df),
            cols_before=cols_before,
            cols_after=len(working_df.columns),
            applied_steps=applied_steps,
        )

        self.logger.info("Cleaning finished. Final shape: %s", working_df.shape)
        return result