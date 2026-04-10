import streamlit as st


def render_cleaning_sidebar(columns: list[str]) -> dict:
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

    return {
        "drop_empty_rows_option": drop_empty_rows_option,
        "remove_repeated_header_rows_option": remove_repeated_header_rows_option,
        "repeated_header_column": repeated_header_column,
        "repeated_header_value": repeated_header_value,
        "cast_numeric_option": cast_numeric_option,
        "numeric_columns": numeric_columns,
        "cast_datetime_option": cast_datetime_option,
        "datetime_column": datetime_column,
        "datetime_format": datetime_format,
        "drop_na_option": drop_na_option,
        "drop_na_subset": drop_na_subset,
        "drop_duplicates_option": drop_duplicates_option,
        "duplicate_subset": duplicate_subset,
        "drop_columns_option": drop_columns_option,
        "columns_to_drop": columns_to_drop,
        "run_cleaning": run_cleaning,
    }