from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import StreamingResponse

from backend.services.cleaning_pipeline import CleaningPipeline
from backend.services.cleaning_input import (
    build_cleaning_options,
    parse_cleaning_request,
    read_csv_upload,
)
from src.cleaning.cleaner import DataCleaner
from src.utils.logger import build_logger

router = APIRouter(prefix="/cleaning", tags=["cleaning"])

logger = build_logger("backend_api")
cleaner = DataCleaner(logger=logger)
pipeline = CleaningPipeline(cleaner=cleaner)

@router.get("/health")
def health_check() -> dict:
    """
    Endpoint to test the health of the backend
    """
    return {"status": "ok"}

def _prepare_cleaning_input(file: UploadFile, options_json: str):
    df = read_csv_upload(file)
    request_model = parse_cleaning_request(options_json)
    options = build_cleaning_options(request_model)
    return df, options

@router.post("/preview")
async def clean_preview(
    file: UploadFile = File(...),
    options_json: str = Form(...),
) -> dict:
    """
    Return:
    - basic metrics
    - applied steps
    - preview cleaned dataframe
    """
    try:
        df, options = _prepare_cleaning_input(file, options_json)
        return pipeline.run_preview(df, options)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Cleaning preview failed: {exc}",
        ) from exc


@router.post("/download-csv")
async def download_cleaned_csv(
    file: UploadFile = File(...),
    options_json: str = Form(...),
):
    try:
        df, options = _prepare_cleaning_input(file, options_json)
        csv_content = pipeline.run_download_csv(df, options)
        return StreamingResponse(
            iter([csv_content]),
            media_type="text/csv",
            headers={
                "Content-Disposition": "attachment; filename=cleaned_data.csv"
            },
        )
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"CSV generation failed: {exc}",
        ) from exc

@router.post("/download-report")
async def download_report(
    file: UploadFile = File(...),
    options_json: str = Form(...),
):
    try:
        df, options = _prepare_cleaning_input(file, options_json)
        html_content = pipeline.run_download_report(df, options)

        return StreamingResponse(
            iter([html_content]),
            media_type="text/html",
            headers={
                "Content-Disposition": "attachment; filename=data_profile_report.html"
            },
        )
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"HTML report generation failed: {exc}",
        ) from exc