import pandas as pd

from src.preparation.entities import ImputationConfig
from src.preparation.pipeline import PreparationPipeline


def test_median_imputation_generates_audit_entries():

    df = pd.DataFrame(
        {
            "name": ["Ana", "Luis", "Maria"],
            "age": [22, None, 30],
        }
    )

    config = ImputationConfig(
        enabled=True,
        method="median",
        columns=["age"],
    )

    pipeline = PreparationPipeline()

    result = pipeline.run(
        df=df,
        imputation_config=config,
    )

    assert result.dataframe.loc[1, "age"] == 26

    assert result.profile_before["missing_total"] == 1

    assert result.profile_after["missing_total"] == 0

    imputation_changes = [
        change
        for change in result.audit_log
        if change.action == "IMPUTE_VALUE"
    ]

    assert len(imputation_changes) == 1

    assert imputation_changes[0].column == "age"

    assert imputation_changes[0].method == "median"

    assert imputation_changes[0].status == "imputed"