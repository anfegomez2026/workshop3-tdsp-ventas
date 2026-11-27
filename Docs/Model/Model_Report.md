# Model Report – Fase 3: Modelado

Notebook: `Code/02_Modeling/02_Modeling.ipynb`

## 1. Diseño experimental
- **Serie:** ventas mensuales totales, enero 2014 – diciembre 2017 (48 meses).
- **Partición temporal:** entrenamiento 2014–2016 (36 meses) · prueba 2017 (12 meses). Sin mezcla aleatoria para respetar el orden temporal.
- **Validación adicional:** backtesting con origen móvil (entrenamiento hasta dic-16, mar-17, jun-17 y sep-17; horizonte de 3 meses).
- **Métricas:** MAE, RMSE, MAPE y MASE (escala = error in-sample del ingenuo estacional).
- **Criterio de selección (definido antes de ver resultados):** menor MAPE en 2017.

## 2. Modelos evaluados
| Familia | Modelos | Justificación |
|---|---|---|
| Baselines | Ingenuo, Ingenuo estacional | Referencia mínima a superar |
| Suavizamiento exponencial | Holt-Winters aditivo y multiplicativo | Tendencia + estacionalidad; el EDA indicó estacionalidad multiplicativa |
| SARIMA (sobre log) | (1,0,0)(1,1,0)₁₂+drift, (0,1,1)(0,1,1)₁₂ aerolínea, búsqueda en grilla por AIC (72 combinaciones, D=1) | Órdenes sugeridos por ACF/PACF y pruebas ADF/KPSS |
| Machine Learning | Regresión lineal sobre log (tendencia + dummies de mes), Random Forest (lag12 + mes + tendencia) | Enfoque alternativo basado en variables |

## 3. Resultados (prueba 2017 + backtesting)
| # | Modelo | MAE | RMSE | MAPE % | MASE | MAPE backtest % |
|---|---|---|---|---|---|---|
| 1 | **Holt-Winters multiplicativo** | 12.432 | 16.384 | **20,77** | 1,24 | 20,81 |
| 2 | Regresión log (tendencia + mes) | 12.797 | 15.124 | 22,00 | 1,28 | 23,22 |
| 3 | Holt-Winters aditivo | **11.453** | **12.541** | 22,59 | **1,14** | **19,81** |
| 4 | Random Forest (lag12 + mes + t) | 12.116 | 14.738 | 22,60 | 1,21 | 23,08 |
| 5 | SARIMA auto (0,0,0)(0,1,0)₁₂ + drift | 13.343 | 17.143 | 24,26 | 1,33 | 24,47 |
| 6 | SARIMA(1,0,0)(1,1,0)₁₂ + drift | 13.419 | 17.275 | 24,46 | 1,34 | 24,08 |
| 7 | Ingenuo estacional (baseline) | 15.468 | 18.986 | 24,52 | 1,55 | 24,52 |
| 8 | SARIMA(0,1,1)(0,1,1)₁₂ aerolínea | 14.681 | 19.007 | 27,64 | 1,47 | 25,72 |
| 9 | SARIMA auto (2,1,0)(0,1,0)₁₂ | 15.557 | 19.440 | 28,67 | 1,55 | 30,87 |
| 10 | Ingenuo | 39.473 | 44.192 | 97,32 | 3,94 | 65,41 |

## 4. Análisis crítico
1. **Ganador:** Holt-Winters multiplicativo (menor MAPE, criterio predefinido). Mejora al baseline en 19,6% en MAE, 13,7% en RMSE y 3,8 puntos de MAPE, y es estable en el backtesting (20,8% vs 20,8% en prueba).
2. **No hay un dominador absoluto:** Holt-Winters aditivo tiene el menor MAE, RMSE, MASE y MAPE de backtesting. El multiplicativo gana en MAPE porque se equivoca menos en los meses bajos (enero–febrero), donde el MAPE penaliza más. Ambos están técnicamente empatados; se mantiene el criterio definido a priori para evitar seleccionar métricas a conveniencia.
3. **La estacionalidad es lo esencial:** el modelo ingenuo sin estacionalidad tiene MAPE 97%; cualquier modelo estacional baja a ~21–29%.
4. **SARIMA:** la búsqueda por AIC eligió (0,0,0)(0,1,0)₁₂ con constante, es decir, "el mismo mes del año pasado × crecimiento". La constante (0,179 en log) implica **~19,6% de crecimiento anual** (IC 95%: 4%–37%). Residuos sin autocorrelación (Ljung-Box p = 0,80 y 0,77) y aproximadamente normales: el modelo es estadísticamente válido, pero solo mejora levemente al baseline. Los órdenes sugeridos por ACF/PACF no superaron al modelo más simple (parsimonia).
5. **Machine Learning:** competitivo pero no superior con solo 36 meses. El Random Forest no extrapola la tendencia (aplana los picos de noviembre–diciembre 2017); la regresión sobrestimó diciembre.
6. **MASE > 1 en todos los modelos:** la escala del MASE se calcula con errores de 2015–2016, y 2017 tuvo un nivel de ventas mayor (errores absolutos más grandes). La comparación correcta es contra el baseline en el mismo periodo de prueba, donde el modelo sí lo supera.

## 5. Cumplimiento de las métricas del Charter
| Meta | Resultado | Estado |
|---|---|---|
| MAPE ≤ 15% | 20,77% | ❌ No alcanzada |
| Superar al ingenuo estacional | MAE −19,6%, MAPE −3,8 pts | ✅ Cumplida |
| MASE < 1 | 1,24 | ❌ (métrica mal especificada, ver punto 6) |

La meta de MAPE no se alcanzó por la alta volatilidad mensual y la historia corta (3 ciclos de entrenamiento). Se documenta como lección aprendida.

## 6. Pronóstico 2018 (Holt-Winters multiplicativo reentrenado con 2014–2017)
| Mes | Pronóstico (USD) |
|---|---|
| Ene | 33.566 |
| Feb | 20.237 |
| Mar | 69.241 |
| Abr | 46.547 |
| May | 53.122 |
| Jun | 52.167 |
| Jul | 49.764 |
| Ago | 54.741 |
| Sep | 102.456 |
| Oct | 69.511 |
| Nov | 118.841 |
| Dic | 107.534 |
| **Total** | **777.728** (+6,1% vs 2017) |

**Observación:** Holt-Winters proyecta un crecimiento conservador (+6%), mientras el SARIMA estima ~20% anual. Se recomienda planear con escenarios (conservador vs optimista).

## 7. Benchmark en Azure ML – AutoML (retador)
- **Configuración:** previsión de series temporales, objetivo `Sales`, tiempo `Month`, frecuencia mensual, horizonte 12, métrica primaria NRMSE, validación cruzada 3 pliegues (paso 1), descomposición STL (estacionalidad + tendencia), feriados de EE. UU., sin rezagos ni ventanas móviles (por historia corta), ensambles habilitados, límite de 30 min, cómputo serverless Standard_DS3_v2.
- **Datos:** `ventas_train_v2` (2014–2016) y `ventas_test_2017` (2017), registrados y versionados como Data Assets.
- **Exploración:** más de 40 modelos; lideran ElasticNet y ensambles; los modelos de árboles (RandomForest, ExtraTrees, LightGBM, XGBoost) quedan al final, coherente con su incapacidad de extrapolar tendencia.
- **Mejor modelo:** StackEnsemble (iteración 39).

| Métrica | AutoML – validación cruzada (2014–2016) | AutoML – prueba 2017 | Holt-Winters mult. – prueba 2017 |
|---|---|---|---|
| MAPE % | 18,85 | **30,06** | **20,77** |
| MAE | 6.989 | 13.641 | 12.432 |
| RMSE | 8.931 | 16.587 | 16.384 |
| R² | 0,79 | 0,59 | – |
| NRMSE | 0,097 | 0,179 | – |

**Análisis:** el StackEnsemble luce excelente en validación cruzada (MAPE 18,9%) pero en el set de prueba independiente cae a 30,1%, peor que Holt-Winters (20,8%) e incluso que el ingenuo estacional (24,5%). Es **sobreajuste**, advertido por la propia plataforma ("StackEnsemble ... might run into overfitting"). Seleccionar por la métrica de validación habría llevado al peor modelo; el set de prueba independiente evitó esa decisión.

## 8. Decisión final
- **Modelo campeón:** Holt-Winters multiplicativo (Colab) → se despliega.
- **Modelo retador:** AutoML StackEnsemble (Azure ML) → se registra como referencia, no se despliega a producción.

## 9. Lecciones aprendidas
- Definir el criterio de selección antes de ver resultados evita sesgos.
- Con pocos datos, los modelos simples y estacionales compiten igual o mejor que modelos complejos.
- El MASE debe escalarse con el mismo periodo de evaluación o complementarse con la comparación directa contra el baseline.
- Una métrica de validación cruzada favorable no garantiza buen desempeño futuro: siempre contrastar con un set de prueba independiente (caso AutoML).
- Mejoras futuras: ensamble de Holt-Winters aditivo + multiplicativo, variables exógenas (descuentos, promociones) y más historia.
