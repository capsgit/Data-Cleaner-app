import pandas as pd

from src.preparation.pipeline import PreparationPipeline


df = pd.DataFrame(
    {
        "name": ["Ana", None],
        "age": [22, None],
    }
)

pipeline = PreparationPipeline()

result = pipeline.run(df)

print("\n=== SUMMARY ===")
print(result.summary)

print("\n=== AUDIT LOG ===")

for change in result.audit_log:
    print(change)

print("\n=== RESULT DF ===")
print(result.dataframe)