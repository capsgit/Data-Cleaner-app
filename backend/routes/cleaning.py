import io
import json

import pandas as pd
from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from backend.schemas.cleaning import CleaningRequest
from src.cleaning.cleaner import DataCleaner
from src.cleaning.options import CleaningOptions
from src.utils.logger import build_logger


router = APIRouter(prefix="/cleaning", tags=["cleaning"])

logger = build_logger("backend_api")
cleaner = DataCleaner(logger=logger)


@router.get("/health")
def health_check() -> dict:
    """
    Endpoint to test the health of the backend
    """
    return {"status": "ok"}


@router.post("/preview")
async def clean_preview(
    file: UploadFile = File(...),
    options_json: str = Form(...),
) -> dict:
    """
    Get:
    - a CSV file
    - cleaning options in JSON format (string)

    Return:
    - basic metrics
    - applicated steps
    - preview clean dataframe
    """

    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported.")

    try:
        content = await file.read()
        df = pd.read_csv(io.BytesIO(content))
    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to read CSV file: {exc}",
        ) from exc

    try:
        raw_options = json.loads(options_json)
        request_model = CleaningRequest(**raw_options)
    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid cleaning options: {exc}",
        ) from exc

    options = CleaningOptions(
        drop_empty_rows=request_model.drop_empty_rows,
        remove_repeated_header_rows=request_model.remove_repeated_header_rows,
        repeated_header_column=request_model.repeated_header_column,
        repeated_header_value=request_model.repeated_header_value,
        cast_numeric=request_model.cast_numeric,
        numeric_columns=request_model.numeric_columns,
        cast_datetime=request_model.cast_datetime,
        datetime_column=request_model.datetime_column,
        datetime_format=request_model.datetime_format,
        drop_na=request_model.drop_na,
        drop_na_subset=request_model.drop_na_subset,
        drop_duplicates=request_model.drop_duplicates,
        duplicate_subset=request_model.duplicate_subset,
        drop_columns=request_model.drop_columns,
        columns_to_drop=request_model.columns_to_drop,
    )

    try:
        result = cleaner.clean_dataframe(df, options)
        cleaned_df = result.cleaned_df
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Cleaning process failed: {exc}",
        ) from exc

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