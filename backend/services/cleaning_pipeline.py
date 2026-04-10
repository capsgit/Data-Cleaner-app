import io

import pandas as pd

from src.cleaning.cleaner import DataCleaner
from src.cleaning.options import CleaningOptions
from src.reporting.profiler import build_profile_html


class CleaningPipeline:
    def __init__(self, cleaner: DataCleaner):
        self.cleaner = cleaner

    def _clean(self, df: pd.DataFrame, options: CleaningOptions):
        return self.cleaner.clean_dataframe(df, options)

    def run_preview(self, df: pd.DataFrame, options: CleaningOptions) -> dict:
        result = self._clean(df, options)
        cleaned_df = result.cleaned_df

        preview_records = cleaned_df.head(10).fillna("").to_dict(orient="records")

        return {
            "rows_before": result.rows_before,
            "rows_after": result.rows_after,
            "cols_before": result.cols_before,
            "cols_after": result.cols_after,
            "rows_removed": result.rows_before - result.rows_after,
            "cols_removed": result.cols_before - result.cols_after,
            "applied_steps": result.applied_steps,
            "preview": preview_records,
        }

    def run_download_csv(self, df: pd.DataFrame, options: CleaningOptions) -> str:
        result = self._clean(df, options)
        cleaned_df = result.cleaned_df

        buffer = io.StringIO()
        cleaned_df.to_csv(buffer, index=False)
        return buffer.getvalue()

    def run_download_report(self, df: pd.DataFrame, options: CleaningOptions) -> str:
        result = self._clean(df, options)
        cleaned_df = result.cleaned_df

        html, _ = build_profile_html(cleaned_df)
        return html