# Project Charter – Pronóstico de ventas mensuales

## 1. Contexto del negocio
Una tienda de artículos para el hogar y oficina en Estados Unidos (categorías Furniture, Office Supplies y Technology) necesita anticipar sus ventas mensuales para planear inventario, compras, personal y metas comerciales.

## 2. Objetivo
Pronosticar las **ventas mensuales totales de los próximos 12 meses** mediante modelos de series de tiempo.

## 3. Preguntas de negocio
- ¿Cuánto se venderá en cada uno de los próximos 12 meses?
- ¿Las ventas tienen tendencia de crecimiento?
- ¿Cuáles son los meses de temporada alta y baja?
- ¿Qué categorías impulsan las ventas?

## 4. Alcance
**Incluye:** limpieza y agregación mensual, análisis exploratorio, comparación de modelos (baseline ingenuo estacional, Holt-Winters/ETS, SARIMA, modelo de ML y AutoML), despliegue en Azure ML y dashboard en Power BI.
**Excluye:** integración con sistemas transaccionales en producción.

## 5. Datos
- **Fuente:** CSV publicado en Google Sheets (URL del enunciado), leído directamente con Python para preservar el formato de fechas (mes/día/año).
- **Volumen:** 9.994 líneas de pedido, 21 variables, sin valores nulos.
- **Periodo:** enero 2014 – diciembre 2017 (48 meses).
- **Variable objetivo:** suma mensual de `Sales` según `Order Date` (la venta ocurre al ordenar; el envío es logística).

## 6. Métricas de éxito
| Métrica | Meta |
|---|---|
| MAPE en el set de prueba (2017) | ≤ 15% |
| MASE frente al modelo ingenuo estacional | < 1 (superar el baseline) |
| RMSE / MAE | Menor entre los modelos comparados |

## 7. Esquema de validación
- Entrenamiento: 2014–2016 (36 meses, 3 ciclos estacionales).
- Prueba: 2017 (12 meses, un ciclo completo).
- Modelo final reentrenado con 2014–2017 para pronosticar 2018.

## 8. Equipo y roles (TDSP)
| Rol | Integrante | Responsabilidades |
|---|---|---|
| Project Lead / Solution Architect | [Nombre] | Charter, tablero ágil, Azure ML, despliegue, Power BI |
| Data Scientist | [Nombre] | Datos, EDA, modelos y evaluación |

## 9. Arquitectura
Google Sheets (CSV) → Google Colab / Python (EDA y modelos) → GitHub (versionado) → Azure ML (dataset versionado, AutoML, registro de modelo y endpoint) → Power BI (consumo del pronóstico).

## 10. Plan ágil
| Sprint | Fechas | Fases TDSP | Entregables |
|---|---|---|---|
| 1 | 25–26 nov | Negocio + Datos | Charter, repositorio, Data Report, EDA |
| 2 | 27–28 nov | Modelado | Modelos en Colab, AutoML en Azure ML, Model Report |
| 3 | 29 nov | Despliegue + Aceptación | Endpoint/batch en Azure ML, dashboard Power BI, informe final |
| 4 | 30 nov – 1 dic | Comunicación | Guion, grabación y edición del video |

## 11. Riesgos
- Historia corta: solo 48 observaciones mensuales (4 ciclos).
- Meses atípicos (mayo, noviembre y diciembre de 2016).
- Cambios de formato en el CSV de origen.
