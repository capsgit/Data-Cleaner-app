from dataclasses import dataclass, field


@dataclass
class CleaningOptions:
    """
    Define the configurable options for the cleaning process and the related type.
    """
    drop_empty_rows: bool = False
    remove_repeated_header_rows: bool = False
    repeated_header_column: str | None = None
    repeated_header_value: str | None = None

    cast_numeric: bool = False
    numeric_columns: list[str] = field(default_factory=list)

    cast_datetime: bool = False
    datetime_column: str | None = None
    datetime_format: str | None = None

    drop_na: bool = False
    drop_na_subset: list[str] = field(default_factory=list)

    drop_duplicates: bool = False
    duplicate_subset: list[str] = field(default_factory=list)

    drop_columns: bool = False
    columns_to_drop: list[str] = field(default_factory=list)