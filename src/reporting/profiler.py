import pandas as pd


def build_profile_html(df: pd.DataFrame) -> tuple[str, str]:
    """
    Generate an HTML report from DataFrame.

    Returns:
        (html_str, mode)
        mode = "ydata-profiling" | "simple-fallback"
    """

    try:
        from ydata_profiling import ProfileReport

        report = ProfileReport(
            df,
            title="Data Profile Report",
            explorative=True,
        )

        return report.to_html(), "ydata-profiling"

    except Exception:
        return _build_simple_html(df), "simple-fallback"


def _build_simple_html(df: pd.DataFrame) -> str:
    """
    Create a basic HTML with dataset information.
    """
    n_rows, n_cols = df.shape
    dtypes = df.dtypes.to_frame(name="dtype")
    missing = df.isna().sum().to_frame(name="missing_values")
    numeric_summary = df.describe().to_html()
    categorical_cols = df.select_dtypes(include="object").columns

    if len(categorical_cols) > 0:
        categorical_summary = df[categorical_cols].describe().to_html()
    else:
        categorical_summary = "<p>No categorical columns</p>"

    # construir HTML
    html = f"""
    <html>
        <head>
            <title>Simple Data Profile</title>
        </head>
        <body>
            <h1>Simple Data Profile</h1>

            <h2>Dataset Overview</h2>
            <p>Rows: {n_rows}</p>
            <p>Columns: {n_cols}</p>

            <h2>Data Types</h2>
            {dtypes.to_html()}

            <h2>Missing Values</h2>
            {missing.to_html()}

            <h2>Numeric Summary</h2>
            {numeric_summary}

            <h2>Categorical Summary</h2>
            {categorical_summary}

        </body>
    </html>
    """

    return html