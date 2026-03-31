# =========================================================
# TESTS PARA steps.py
# =========================================================
# Idea:
# - cada función se prueba por separado
# - usamos DataFrames pequeños (controlados)
# =========================================================

import pandas as pd

from src.cleaning.steps import (
    drop_empty_rows,
    cast_numeric,
    drop_duplicates,
    drop_columns,
    drop_na,
)


# ---------------------------------------------------------
# TEST 1: drop_empty_rows
# ---------------------------------------------------------
# Pseudocódigo:
# crear df con filas vacías
# aplicar función
# comprobar que desaparecen
# ---------------------------------------------------------
def test_drop_empty_rows_removes_fully_empty_rows():
    df = pd.DataFrame({
        "A": [1, None, None],
        "B": [2, None, None],
    })

    result = drop_empty_rows(df)

    assert len(result) == 1


# ---------------------------------------------------------
# TEST 2: cast_numeric
# ---------------------------------------------------------
# Pseudocódigo:
# columna con números y texto
# convertir
# verificar que texto -> NaN
# ---------------------------------------------------------
def test_cast_numeric_converts_invalid_values_to_nan():
    df = pd.DataFrame({
        "price": ["10", "20", "abc"]
    })

    result = cast_numeric(df, ["price"])

    assert result["price"].isna().sum() == 1


# ---------------------------------------------------------
# TEST 3: drop_duplicates
# ---------------------------------------------------------
def test_drop_duplicates_removes_duplicate_rows():
    df = pd.DataFrame({
        "A": [1, 1, 2]
    })

    result = drop_duplicates(df)

    assert len(result) == 2


# ---------------------------------------------------------
# TEST 4: drop_columns
# ---------------------------------------------------------
def test_drop_columns_removes_selected_columns():
    df = pd.DataFrame({
        "A": [1],
        "B": [2],
    })

    result = drop_columns(df, ["B"])

    assert "B" not in result.columns


# ---------------------------------------------------------
# TEST 5: drop_na
# ---------------------------------------------------------
def test_drop_na_removes_rows_with_missing_values():
    df = pd.DataFrame({
        "A": [1, None, 3]
    })

    result = drop_na(df)

    assert len(result) == 2