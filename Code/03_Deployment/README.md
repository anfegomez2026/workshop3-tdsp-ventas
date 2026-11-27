# Fase 4 – Despliegue

| Componente | Descripción |
|---|---|
| `batch_forecast.py` | Pipeline batch reproducible: ingesta → agregación → reentrenamiento del campeón → pronóstico 12 meses → exporta CSV para Power BI y el modelo `.pkl` |
| Azure ML – Model Registry | `ventas-holtwinters-champion` (campeón, v1) y `ventas-automl-stackensemble` (retador, v1) |
| `Dashboard_Ventas_2018.pbix` | Dashboard de consumo para el negocio (histórico + pronóstico + comparación de modelos) |

**Decisión de arquitectura:** el pronóstico es mensual, por lo que se despliega en modo *batch* (se ejecuta al cierre de cada mes) en lugar de un endpoint en tiempo real, que tendría costo por hora sin aportar valor al caso de uso.
