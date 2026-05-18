import pandas as pd

from src.preparation.pipeline import PreparationPipeline


def test_remove_empty_rows_generates_audit_log():

    df = pd.DataFrame(
        {
            "name": ["Ana", None],
            "age": [22, None],
        }
    )

    pipeline = PreparationPipeline()

    result = pipeline.run(df)

    assert result.summary.rows_before == 2
    assert result.summary.rows_after == 1

    assert len(result.audit_log) == 1

    change = result.audit_log[0]

    assert change.action == "DROP_ROW"
    assert change.status == "deleted"