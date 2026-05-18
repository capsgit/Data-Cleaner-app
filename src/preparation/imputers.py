import pandas as pd

from src.preparation.validators import validate_numeric_column
from src.preparation.audit import AuditLogger
from src.preparation.entities import (
    CellChange,
    ImputationConfig,
    ValidationIssue,
)


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


def fill_with_mode(
    df: pd.DataFrame,
    column: str,
    audit: AuditLogger,
) -> pd.DataFrame:

    mode_series = df[column].mode()

    if mode_series.empty:
        return df

    mode_value = mode_series[0]

    missing_mask = df[column].isna()

    for row_idx in df[missing_mask].index:

        audit.log(
            CellChange(
                row_id=int(row_idx),
                column=column,
                old_value=None,
                new_value=mode_value,
                action="IMPUTE_VALUE",
                method="mode",
                status="imputed",
                reason="Filled missing value using mode",
            )
        )

    df.loc[missing_mask, column] = mode_value

    return df


def fill_with_constant(
    df: pd.DataFrame,
    column: str,
    constant_value,
    audit: AuditLogger,
) -> pd.DataFrame:

    missing_mask = df[column].isna()

    for row_idx in df[missing_mask].index:

        audit.log(
            CellChange(
                row_id=int(row_idx),
                column=column,
                old_value=None,
                new_value=constant_value,
                action="IMPUTE_VALUE",
                method="constant",
                status="imputed",
                reason="Filled missing value using constant value",
            )
        )

    df.loc[missing_mask, column] = constant_value

    return df


def apply_imputation(
    df: pd.DataFrame,
    config: ImputationConfig,
    audit: AuditLogger,
    issues: list[ValidationIssue],
) -> pd.DataFrame:

    if not config.enabled:
        return df

    for column in config.columns:

        if column not in df.columns:
            continue

        if config.method == "median":
            print("11111", column, df[column].dtype, validate_numeric_column(df, column))

            if not validate_numeric_column(df, column):
                issues.append(
                    ValidationIssue(
                        row_id=None,
                        column=column,
                        issue_type="INVALID_IMPUTATION_METHOD",
                        severity="error",
                        message="Median imputation requires a numeric column",
                    )
                )
                continue

            df = fill_numeric_median(
                df=df,
                column=column,
                audit=audit,
            )
            print("1", column, df[column].dtype, validate_numeric_column(df, column))
        elif config.method == "mode":

            df = fill_with_mode(
                df=df,
                column=column,
                audit=audit,
            )

        elif config.method == "constant":

            df = fill_with_constant(
                df=df,
                column=column,
                constant_value=config.constant_value,
                audit=audit,
            )

    return df