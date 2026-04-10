import pandas as pd
import streamlit as st


def render_dataset_overview(df: pd.DataFrame) -> None:
    st.subheader("📊 Dataset Overview")

    info_col1, info_col2, info_col3 = st.columns(3)
    info_col1.metric("Rows", df.shape[0])
    info_col2.metric("Columns", df.shape[1])
    info_col3.metric("Duplicated rows", int(df.duplicated().sum()))

    with st.expander("📄 Original Data Preview", expanded=True):
        st.dataframe(df.head(20), use_container_width=True)


def render_preview_results(result: dict) -> None:
    rows_delta = f"-{result['rows_removed']}" if result["rows_removed"] > 0 else "0"
    cols_delta = f"-{result['cols_removed']}" if result["cols_removed"] > 0 else "0"

    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    metric_col1.metric("Rows before", result["rows_before"])
    metric_col2.metric("Rows after", result["rows_after"], delta=rows_delta)
    metric_col3.metric("Columns before", result["cols_before"])
    metric_col4.metric("Columns after", result["cols_after"], delta=cols_delta)

    st.subheader("📋 Applied Steps Summary")
    if result["applied_steps"]:
        summary_df = pd.DataFrame(result["applied_steps"])
        st.dataframe(summary_df, use_container_width=True)
    else:
        st.info("No cleaning steps were applied.")

    with st.expander("🧼 Cleaned Data Preview", expanded=True):
        preview_df = pd.DataFrame(result["preview"])
        st.dataframe(preview_df, use_container_width=True)


def render_download_buttons(csv_response, html_response) -> None:
    if csv_response is not None and csv_response.status_code == 200:
        st.download_button(
            label="📥 Download Cleaned CSV",
            data=csv_response.content,
            file_name="cleaned_data.csv",
            mime="text/csv",
        )
    else:
        st.error("Failed to generate CSV")

    if html_response is not None and html_response.status_code == 200:
        st.download_button(
            label="📄 Download HTML Report",
            data=html_response.content,
            file_name="report.html",
            mime="text/html",
        )
    else:
        st.warning("HTML report not available")