import pandas as pd
import streamlit as st


def render_file_uploader() -> object:
    left_col, center_col, right_col = st.columns([3, 2, 3])

    with center_col:
        uploaded_file = st.file_uploader(
            label="",
            type=["csv"],
        )

    return uploaded_file


def read_uploaded_csv(uploaded_file) -> pd.DataFrame:
    try:
        return pd.read_csv(uploaded_file)
    except Exception as exc:
        st.error(f"Error reading CSV: {exc}")
        st.stop()