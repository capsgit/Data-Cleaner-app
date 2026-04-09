from pydantic import BaseModel, Field


class CleaningRequest(BaseModel):
    """
    Cleaning end-point. -> entrance

    Frontend (Streamlit) send THIS options
    as JSON to backend.
    """

    drop_empty_rows: bool = False

    remove_repeated_header_rows: bool = False
    repeated_header_column: str | None = None
    repeated_header_value: str | None = None

    cast_numeric: bool = False
    numeric_columns: list[str] = Field(default_factory=list)

    cast_datetime: bool = False
    datetime_column: str | None = None
    datetime_format: str | None = None

    drop_na: bool = False
    drop_na_subset: list[str] = Field(default_factory=list)

    drop_duplicates: bool = False
    duplicate_subset: list[str] = Field(default_factory=list)

    drop_columns: bool = False
    columns_to_drop: list[str] = Field(default_factory=list)