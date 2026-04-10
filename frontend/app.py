import sys

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))


import streamlit as st

from frontend.api.client import (
    request_cleaned_csv,
    request_cleaning_preview,
    request_cleaning_report,
)
from frontend.config import APP_LAYOUT, APP_PAGE_ICON, APP_PAGE_TITLE, APP_TITLE
from frontend.ui.results import (
    render_dataset_overview,
    render_download_buttons,
    render_preview_results,
)
from frontend.ui.sidebar import render_cleaning_sidebar
from frontend.ui.uploads import read_uploaded_csv, render_file_uploader
from frontend.utils.payload import build_cleaning_payload


st.set_page_config(
    page_title=APP_PAGE_TITLE,
    page_icon=APP_PAGE_ICON,
    layout=APP_LAYOUT,
)

st.title(APP_TITLE)
st.write(
    "Upload a CSV file, configure the cleaning steps from the sidebar, "
    "and run the pipeline through the FastAPI backend."
)

uploaded_file = render_file_uploader()

if uploaded_file is not None:
    df = read_uploaded_csv(uploaded_file)
    columns = df.columns.tolist()

    sidebar_values = render_cleaning_sidebar(columns)

    render_dataset_overview(df)

    if sidebar_values["run_cleaning"]:
        payload = build_cleaning_payload(
            drop_empty_rows_option=sidebar_values["drop_empty_rows_option"],
            remove_repeated_header_rows_option=sidebar_values["remove_repeated_header_rows_option"],
            repeated_header_column=sidebar_values["repeated_header_column"],
            repeated_header_value=sidebar_values["repeated_header_value"],
            cast_numeric_option=sidebar_values["cast_numeric_option"],
            numeric_columns=sidebar_values["numeric_columns"],
            cast_datetime_option=sidebar_values["cast_datetime_option"],
            datetime_column=sidebar_values["datetime_column"],
            datetime_format=sidebar_values["datetime_format"],
            drop_na_option=sidebar_values["drop_na_option"],
            drop_na_subset=sidebar_values["drop_na_subset"],
            drop_duplicates_option=sidebar_values["drop_duplicates_option"],
            duplicate_subset=sidebar_values["duplicate_subset"],
            drop_columns_option=sidebar_values["drop_columns_option"],
            columns_to_drop=sidebar_values["columns_to_drop"],
        )

        try:
            with st.spinner("Processing..."):
                response = request_cleaning_preview(uploaded_file, payload)
        except Exception as exc:
            st.error(f"Could not connect to backend: {exc}")
            st.stop()

        if response.status_code != 200:
            st.error(f"Backend error: {response.text}")
            st.stop()

        result = response.json()
        render_preview_results(result)

        with st.spinner("Preparing CSV download..."):
            try:
                csv_response = request_cleaned_csv(uploaded_file, payload)
            except Exception as exc:
                st.error(f"Could not generate CSV: {exc}")
                csv_response = None

        with st.spinner("Preparing HTML report..."):
            try:
                html_response = request_cleaning_report(uploaded_file, payload)
            except Exception as exc:
                st.warning(f"HTML report error: {exc}")
                html_response = None

        render_download_buttons(csv_response, html_response)