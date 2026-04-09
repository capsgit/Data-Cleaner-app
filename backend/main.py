from fastapi import FastAPI

from backend.routes.cleaning import router as cleaning_router


app = FastAPI(
    title="Data Cleaner API",
    description="Backend API for the Data Cleaner App",
    version="1.0.0",
)

app.include_router(cleaning_router)


@app.get("/")
def root() -> dict:
    """
    Endpoint.
    """
    return {
        "message": "Data Cleaner API is running",
        "docs": "/docs",
    }