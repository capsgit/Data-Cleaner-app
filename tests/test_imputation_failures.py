import pandas as pd

from src.preparation.entities import ImputationConfig
from src.preparation.pipeline import PreparationPipeline


def test_median_imputation_on_text_column_creates_issue():

    df = pd.DataFrame(
        {
            "id": [1, 2, 3],
            "city": ["Berlin", None, "Paris"],
        }
    )

    config = ImputationConfig(
        enabled=True,
        method="median",
        columns=["city"],
    )

    pipeline = PreparationPipeline()

    result = pipeline.run(
        df=df,
        imputation_config=config,
    )

    assert result.dataframe["city"].isna().sum() == 1

    assert len(result.issues) == 1

    issue = result.issues[0]

    assert issue.column == "city"
    assert issue.issue_type == "INVALID_IMPUTATION_METHOD"
    assert issue.severity == "error"

    imputation_changes = [
        change
        for change in result.audit_log
        if change.action == "IMPUTE_VALUE"
    ]

    assert len(imputation_changes) == 0