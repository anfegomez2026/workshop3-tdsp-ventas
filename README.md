# Pronóstico de ventas mensuales – Workshop 3 (TDSP)

Proyecto de series de tiempo para predecir las ventas mensuales de una tienda de artículos para el hogar y oficina, desarrollado con la metodología **Team Data Science Process (TDSP)** de Microsoft.

## Ciclo de vida TDSP
| Fase | Estado | Entregables |
|---|---|---|
| 1. Entendimiento del negocio | ✅ Completa | `Docs/Project/Charter.md` |
| 2. Adquisición y entendimiento de datos | ✅ Completa | `Docs/Data_Report/`, `Code/01_...`, `Sample_Data/` |
| 3. Modelado | ✅ Completa | `Docs/Model/Model_Report.md`, `Code/02_Modeling/` |
| 4. Despliegue | ✅ Completa | `Code/03_Deployment/`, Azure ML Model Registry |
| 5. Aceptación del cliente | ✅ Completa | `Docs/Project/Informe_Final.md` |

## Resultados clave
- **Modelo campeón:** Holt-Winters multiplicativo · MAPE 2017 = 20,8% · supera al baseline en 19,6% (MAE).
- **Retador AutoML (Azure ML):** StackEnsemble · MAPE validación 18,9% → prueba 30,1% (sobreajuste).
- **Pronóstico 2018:** USD 777.728 (+6,1% vs 2017); picos en septiembre, noviembre y diciembre.
- **Despliegue:** pipeline batch mensual + modelos registrados en Azure ML + dashboard Power BI.

## Estructura
- `Docs/Project` – Project Charter e informe final
- `Docs/Data_Report` – Data Report y diccionario de datos
- `Docs/Model` – Model Report
- `Code/` – Notebooks por fase TDSP (Google Colab)
- `Sample_Data/Raw` – Datos originales (CSV de la fuente)
- `Sample_Data/Processed` – Serie mensual total y por categoría

## Herramientas
Python (Google Colab) · Azure Machine Learning · Power BI · GitHub (versionado y tablero ágil)

## Equipo
Proyecto individual: **Andres Gomez** asume los roles TDSP de Project Lead / Solution Architect y Data Scientist.
