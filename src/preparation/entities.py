from dataclasses import dataclass, field
from typing import Any, Literal


CellStatus = Literal[
    "original",
    "modified",
    "imputed",
    "failed",
    "flagged",
    "deleted",
    "manual_review",
]


@dataclass
class CellChange:
    row_id: int
    column: str | None
    old_value: Any
    new_value: Any
    action: str
    method: str
    status: CellStatus
    reason: str | None = None


@dataclass
class PreparationSummary:
    rows_before: int
    rows_after: int
    columns_before: int
    columns_after: int
    total_changes: int


@dataclass
class PreparationResult:
    dataframe: Any
    summary: PreparationSummary
    audit_log: list[CellChange] = field(default_factory=list)