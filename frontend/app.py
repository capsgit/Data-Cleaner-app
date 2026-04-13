import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

import pandas as pd
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


# =========================================================
# SESSION STATE
# =========================================================
# We keep results and generated files in session state so
# the UI remains stable across reruns.
# =========================================================
if "preview_result" not in st.session_state:
    st.session_state["preview_result"] = None

if "csv_download_bytes" not in st.session_state:
    st.session_state["csv_download_bytes"] = None

if "html_download_bytes" not in st.session_state:
    st.session_state["html_download_bytes"] = None

if "last_input_signature" not in st.session_state:
    st.session_state["last_input_signature"] = None


def reset_processing_state() -> None:
    """
    Clear all processing-related state when the input file or
    cleaning configuration changes.
    """
    st.session_state["preview_result"] = None
    st.session_state["csv_download_bytes"] = None
    st.session_state["html_download_bytes"] = None


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
    # =====================================================
    # ORIGINAL DATA
    # =====================================================
    df = read_uploaded_csv(uploaded_file)
    columns = df.columns.tolist()

    # Sidebar inputs
    sidebar_values = render_cleaning_sidebar(columns)

    # Build payload from UI selections
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

    # =====================================================
    # INPUT SIGNATURE
    # =====================================================
    # If file or config changes, old results must be cleared.
    # =====================================================
    current_signature = {
        "filename": uploaded_file.name,
        "filesize": len(uploaded_file.getvalue()),
        "payload": payload,
    }

    if st.session_state["last_input_signature"] != current_signature:
        reset_processing_state()
        st.session_state["last_input_signature"] = current_signature

    # =====================================================
    # ORIGINAL DATA SECTION
    # =====================================================
    st.subheader("📄 Original Dataset")
    render_dataset_overview(df)

    # =====================================================
    # RUN CLEANING -> PREVIEW ONLY
    # =====================================================
    if sidebar_values["run_cleaning"]:
        try:
            with st.spinner("Sending file and configuration to backend..."):
                response = request_cleaning_preview(uploaded_file, payload)
        except Exception as exc:
            st.error(f"Could not connect to backend: {exc}")
            st.stop()

        if response.status_code != 200:
            st.error(f"Backend error: {response.text}")
            st.stop()

        st.session_state["preview_result"] = response.json()

    # =====================================================
    # RESULTS SECTION
    # =====================================================
    if st.session_state["preview_result"] is not None:
        st.subheader("📊 Results")
        st.caption(
            "These results reflect the current file and the current cleaning configuration."
        )

        render_preview_results(st.session_state["preview_result"])

        # =================================================
        # EXPORT SECTION
        # =================================================
        st.subheader("📦 Export Options")

        export_col1, export_col2 = st.columns(2)

        with export_col1:
            prepare_csv = st.button("Prepare Cleaned CSV")

        with export_col2:
            prepare_html = st.button("Prepare HTML Report")

        # -----------------------------------------------
        # CSV export request
        # -----------------------------------------------
        if prepare_csv:
            try:
                with st.spinner("Generating cleaned CSV..."):
                    csv_response = request_cleaned_csv(uploaded_file, payload)
            except Exception as exc:
                st.error(f"Could not generate CSV: {exc}")
                csv_response = None

            if csv_response is not None and csv_response.status_code == 200:
                st.session_state["csv_download_bytes"] = csv_response.content
            elif csv_response is not None:
                st.error(f"CSV generation failed: {csv_response.text}")

        # -----------------------------------------------
        # HTML export request
        # -----------------------------------------------
        if prepare_html:
            try:
                with st.spinner("Generating HTML profile report... this may take longer"):
                    html_response = request_cleaning_report(uploaded_file, payload)
            except Exception as exc:
                st.error(f"Could not generate HTML report: {exc}")
                html_response = None

            if html_response is not None and html_response.status_code == 200:
                st.session_state["html_download_bytes"] = html_response.content
            elif html_response is not None:
                st.error(f"HTML report generation failed: {html_response.text}")

        # -----------------------------------------------
        # Download buttons
        # -----------------------------------------------
        render_download_buttons(
            st.session_state["csv_download_bytes"],
            st.session_state["html_download_bytes"],
        )