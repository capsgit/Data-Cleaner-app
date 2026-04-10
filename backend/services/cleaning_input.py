import io
import json

import pandas as pd
from fastapi import HTTPException, UploadFile

from backend.schemas.cleaning import CleaningRequest
from src.cleaning.options import CleaningOptions


def parse_cleaning_request(options_json: str) -> CleaningRequest:
    raw_options = json.loads(options_json)
    return CleaningRequest(**raw_options)


def build_cleaning_options(request_model: CleaningRequest) -> CleaningOptions:
    return CleaningOptions(**request_model.model_dump())


def read_csv_upload(file: UploadFile) -> pd.DataFrame:
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported.")

    try:
        content = file.file.read()
        return pd.read_csv(io.BytesIO(content))
    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to read CSV file: {exc}",
        ) from exc
