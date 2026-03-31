import pandas as pd


def drop_empty_rows(df: pd.DataFrame) -> pd.DataFrame:
    """
    Drop empty rows.
    """
    return df.dropna(how="all")


def remove_repeated_header_rows(
    df: pd.DataFrame,
    column: str,
    header_value: str,
) -> pd.DataFrame:
    """
    Drop repeated header rows.
    """
    if column not in df.columns:
        return df
    return df[df[column].astype(str) != str(header_value)]


def cast_numeric(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """
    Convert columns to numeric; invalide values get a NaN.
    """
    df = df.copy()
    for col in columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def cast_datetime(
    df: pd.DataFrame,
    column: str,
    fmt: str | None = None,
) -> pd.DataFrame:
    """
    Convert a column in datetime; invalide values get a NaT.
    """
    df = df.copy()
    if column in df.columns:
        if fmt:
            df[column] = pd.to_datetime(df[column], format=fmt, errors="coerce")
        else:
            df[column] = pd.to_datetime(df[column], errors="coerce")
    return df


def drop_na(
    df: pd.DataFrame,
    subset: list[str] | None = None,
) -> pd.DataFrame:
    """
    Drop row with null. If subset ist set in front-end, valid only that columns
    """
    if subset:
        valid_subset = [col for col in subset if col in df.columns]
        if valid_subset:
            return df.dropna(subset=valid_subset)
    return df.dropna()


def drop_duplicates(
    df: pd.DataFrame,
    subset: list[str] | None = None,
) -> pd.DataFrame:
    """
    Drop exact clones/duplicates or raws
    """
    if subset:
        valid_subset = [col for col in subset if col in df.columns]
        if valid_subset:
            return df.drop_duplicates(subset=valid_subset)
    return df.drop_duplicates()


def drop_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """
    Drop a whole column.
    """
    valid_columns = [col for col in columns if col in df.columns]
    return df.drop(columns=valid_columns, errors="ignore")