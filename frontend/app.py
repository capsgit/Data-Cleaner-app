import json

import pandas as pd
import requests
import streamlit as st

# =========================================================
# CONFIG
# =========================================================
BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Data Cleaner App",
    page_icon="🧹",
    layout="wide",
)

# =========================================================
# HEADER
# =========================================================
st.title("🧹 Data Cleaner App")
st.write(
    "Upload a CSV file, configure the cleaning steps from the sidebar, "
    "and run the pipeline through the FastAPI backend."
)

# =========================================================
# UPLOAD
# =========================================================
left_col, center_col, right_col = st.columns([3, 2, 3])

with center_col:
    uploaded_file = st.file_uploader(
        label="",
        type=["csv"],
    )

# =========================================================
# MAIN FLOW
# =========================================================
if uploaded_file is not None:
    # -----------------------------------------------------
    # Read CSV locally only to:
    # - preview original data
    # - know column names for the sidebar widgets
    # The actual cleaning happens in the backend.
    # -----------------------------------------------------
    try:
        df = pd.read_csv(uploaded_file)
    except Exception as exc:
        st.error(f"Error reading CSV: {exc}")
        st.stop()

    columns = df.columns.tolist()

    # =====================================================
    # SIDEBAR = INPUTS ONLY
    # =====================================================
    with st.sidebar:
        st.header("⚙️ Cleaning Configuration")

        drop_empty_rows_option = st.checkbox("Drop fully empty rows")

        remove_repeated_header_rows_option = st.checkbox(
            "Remove repeated header rows"
        )
        repeated_header_column = None
        repeated_header_value = None
        if remove_repeated_header_rows_option:
            repeated_header_column = st.selectbox(
                "Column used to detect repeated headers",
                options=columns,
            )
            repeated_header_value = st.text_input(
                "Header value to remove",
                value=repeated_header_column,
            )

        cast_numeric_option = st.checkbox("Cast columns to numeric")
        numeric_columns: list[str] = []
        if cast_numeric_option:
            numeric_columns = st.multiselect(
                "Numeric columns",
                options=columns,
            )

        cast_datetime_option = st.checkbox("Cast one column to datetime")
        datetime_column = None
        datetime_format = None
        if cast_datetime_option:
            datetime_column = st.selectbox(
                "Datetime column",
                options=columns,
            )
            datetime_format = st.text_input(
                "Datetime format (optional)",
                value="",
                placeholder="%m/%d/%y %H:%M",
            )

        st.divider()

        drop_na_option = st.checkbox("Drop rows with missing values")
        drop_na_subset: list[str] = []
        if drop_na_option:
            drop_na_subset = st.multiselect(
                "Columns considered for missing values",
                options=columns,
            )

        drop_duplicates_option = st.checkbox("Drop duplicate rows")
        duplicate_subset: list[str] = []
        if drop_duplicates_option:
            duplicate_subset = st.multiselect(
                "Columns used to identify duplicates (optional)",
                options=columns,
            )

        drop_columns_option = st.checkbox("Drop selected columns")
        columns_to_drop: list[str] = []
        if drop_columns_option:
            columns_to_drop = st.multiselect(
                "Columns to drop",
                options=columns,
            )

        st.divider()

        run_cleaning = st.button(
            "▶ Run Cleaning",
            use_container_width=True,
        )

        # Color only sidebar button
        st.markdown(
            """
            <style>
            section[data-testid="stSidebar"] button {
                background-color: #22C55E;
                color: white;
                font-weight: bold;
            }
            section[data-testid="stSidebar"] button:hover {
                background-color: #16A34A;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

    # =====================================================
    # BODY = ORIGINAL DATA INFO
    # =====================================================
    st.subheader("📊 Dataset Overview")

    info_col1, info_col2, info_col3 = st.columns(3)
    info_col1.metric("Rows", df.shape[0])
    info_col2.metric("Columns", df.shape[1])
    info_col3.metric("Duplicated rows", int(df.duplicated().sum()))

    with st.expander("📄 Original Data Preview", expanded=True):
        st.dataframe(df.head(20), use_container_width=True)

    # =====================================================
    # BODY = SEND REQUEST TO BACKEND
    # =====================================================
    if run_cleaning:
        payload = {
            "drop_empty_rows": drop_empty_rows_option,
            "remove_repeated_header_rows": remove_repeated_header_rows_option,
            "repeated_header_column": repeated_header_column,
            "repeated_header_value": repeated_header_value,
            "cast_numeric": cast_numeric_option,
            "numeric_columns": numeric_columns,
            "cast_datetime": cast_datetime_option,
            "datetime_column": datetime_column,
            "datetime_format": datetime_format if datetime_format else None,
            "drop_na": drop_na_option,
            "drop_na_subset": drop_na_subset,
            "drop_duplicates": drop_duplicates_option,
            "duplicate_subset": duplicate_subset,
            "drop_columns": drop_columns_option,
            "columns_to_drop": columns_to_drop,
        }

        files = {
            "file": (uploaded_file.name, uploaded_file.getvalue(), "text/csv"),
        }

        data = {
            "options_json": json.dumps(payload),
        }

        try:
            with st.spinner("Sending data to backend..."):
                response = requests.post(
                    f"{BACKEND_URL}/cleaning/preview",
                    files=files,
                    data=data,
                    timeout=60,
                )
        except requests.RequestException as exc:
            st.error(f"Could not connect to backend: {exc}")
            st.stop()

        if response.status_code != 200:
            st.error(f"Backend error: {response.text}")
            st.stop()

        result = response.json()

        # -------------------------------------------------
        # Metrics
        # -------------------------------------------------
        rows_delta = (
            f"-{result['rows_removed']}" if result["rows_removed"] > 0 else "0"
        )
        cols_delta = (
            f"-{result['cols_removed']}" if result["cols_removed"] > 0 else "0"
        )

        metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
        metric_col1.metric("Rows before", result["rows_before"])
        metric_col2.metric("Rows after", result["rows_after"], delta=rows_delta)
        metric_col3.metric("Columns before", result["cols_before"])
        metric_col4.metric("Columns after", result["cols_after"], delta=cols_delta)

        # -------------------------------------------------
        # Applied steps
        # -------------------------------------------------
        st.subheader("📋 Applied Steps Summary")
        if result["applied_steps"]:
            summary_df = pd.DataFrame(result["applied_steps"])
            st.dataframe(summary_df, use_container_width=True)
        else:
            st.info("No cleaning steps were applied.")

        # -------------------------------------------------
        # Clean preview
        # -------------------------------------------------
        with st.expander("🧼 Cleaned Data Preview", expanded=True):
            preview_df = pd.DataFrame(result["preview"])
            st.dataframe(preview_df, use_container_width=True)