from src.preparation.entities import CellChange


class AuditLogger:
    def __init__(self):
        self.changes: list[CellChange] = []

    def log(self, change: CellChange):
        self.changes.append(change)

    def get_changes(self) -> list[CellChange]:
        return self.changes

    def count(self) -> int:
        return len(self.changes)