# Data Preparation Assistant - Core Design

## 1. Problema
La app actual limpia datos, pero no permite preparación trazable ni imputación inteligente.

## 2. Nuevo objetivo
Transformar datasets con reglas, ML y auditoría celda por celda.

## 3. Entidades principales
- Dataset
- PreparationPlan
- TransformationStep
- CellChange
- ValidationIssue
- PreparedDataset

## 4. Principio central
Ningún cambio ocurre sin dejar rastro.

## 5. Estados de celda
original, modified, imputed, failed, flagged, deleted, manual_review

## 6. Primera versión
- upload CSV
- profile dataset
- detectar missing values
- aplicar imputación simple
- generar audit log
- mostrar antes/después