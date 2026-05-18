# Backend conversion checklist

## 1. Renombrar mentalmente el dominio
- [ ] Pasar de `cleaning` a `preparation`
- [ ] Mantener `cleaning` solo como submódulo si sigue existiendo
- [ ] Definir que el objetivo ya no es “limpiar”, sino “preparar con trazabilidad”

## 2. Crear entidades centrales
- [ ] DatasetProfile
- [ ] PreparationPlan
- [ ] TransformationStep
- [ ] CellChange
- [ ] ValidationIssue
- [ ] PreparationResult

## 3. Crear audit log
- [ ] Registrar fila afectada
- [ ] Registrar columna afectada
- [ ] Guardar valor anterior
- [ ] Guardar valor nuevo
- [ ] Guardar acción aplicada
- [ ] Guardar método usado
- [ ] Guardar estado: success / failed / warning
- [ ] Guardar razón o explicación

## 4. Separar transformaciones
- [ ] Drop empty rows
- [ ] Remove repeated headers
- [ ] Cast numeric
- [ ] Cast datetime
- [ ] Drop duplicates
- [ ] Drop columns
- [ ] Replace values
- [ ] Impute values

## 5. Agregar estados de celda
- [ ] original
- [ ] modified
- [ ] imputed
- [ ] failed
- [ ] flagged
- [ ] deleted
- [ ] manual_review

## 6. Crear módulo de imputación
- [ ] SimpleImputer mean / median / most_frequent
- [ ] Constant value imputer
- [ ] KNNImputer
- [ ] IterativeImputer
- [ ] Marcar celdas donde la imputación no sea confiable
- [ ] Guardar método y parámetros usados

## 7. Crear validaciones
- [ ] Missing values
- [ ] Tipo incorrecto
- [ ] Outliers
- [ ] Valores imposibles
- [ ] Categorías desconocidas
- [ ] Duplicados
- [ ] Reglas por columna

## 8. Rediseñar endpoints
- [ ] `/preparation/profile`
- [ ] `/preparation/plan`
- [ ] `/preparation/run`
- [ ] `/preparation/audit-log`
- [ ] `/preparation/export`
- [ ] Mantener endpoints viejos temporalmente si quieres compatibilidad

## 9. Preparar respuesta para frontend avanzado
- [ ] Resumen global
- [ ] Preview original
- [ ] Preview preparado
- [ ] Lista de cambios por celda
- [ ] Lista de errores/fallos
- [ ] Métricas antes/después
- [ ] Recomendaciones de preparación

## 10. Tests
- [ ] Test para cada transformación
- [ ] Test para audit log
- [ ] Test para imputación simple
- [ ] Test para fallos de imputación
- [ ] Test para respuesta del endpoint