# Informe Final – Fase 5: Aceptación del cliente

**Proyecto:** Pronóstico de ventas mensuales – Workshop 3 (TDSP)
**Responsable:** Andres Gomez (Project Lead / Solution Architect + Data Scientist)

## 1. Resumen ejecutivo
Se construyó y desplegó un modelo de series de tiempo que pronostica las ventas mensuales de la tienda para los próximos 12 meses. Tras comparar 10 modelos en Python y más de 40 en Azure AutoML, el modelo seleccionado es **Holt-Winters multiplicativo**, con un error medio de **20,8% (MAPE)** en el año de prueba 2017, superando al método de referencia ("mismo mes del año anterior") en **19,6% de error absoluto**. El pronóstico de 2018 suma **USD 777.728 (+6,1% vs 2017)**, con picos en septiembre, noviembre y diciembre.

## 2. Cumplimiento de objetivos del Charter
| Objetivo / métrica | Meta | Resultado | Estado |
|---|---|---|---|
| Pronóstico mensual a 12 meses | Sí | Pronóstico 2018 generado y desplegado | ✅ |
| Superar al ingenuo estacional | Sí | MAE −19,6%, MAPE 20,8% vs 24,5% | ✅ |
| MAPE en prueba | ≤ 15% | 20,8% | ❌ |
| MASE | < 1 | 1,24 (métrica mal especificada; ver Model Report) | ❌ |
| Despliegue consumible por el negocio | Sí | Pipeline batch + Model Registry + Power BI | ✅ |

**Valoración:** el modelo es útil para planeación (supera claramente al método actual de referencia), pero su precisión no alcanza la meta del 15%. Se acepta para **planeación por rangos/escenarios**, no para compromisos puntuales de inventario.

## 3. Respuestas a las preguntas de negocio
| Pregunta | Respuesta |
|---|---|
| ¿Cuánto se venderá en 2018? | USD ~778 mil (escenario conservador, Holt-Winters) a ~880 mil (escenario optimista, crecimiento ~20% estimado por SARIMA). |
| ¿Hay crecimiento? | Sí: +51% entre 2014 y 2017 (~15% anual compuesto), acelerado desde 2016. |
| ¿Temporada alta y baja? | Alta: septiembre, noviembre y diciembre (~43% de las ventas anuales). Baja: enero y febrero (febrero vende ~1/3 de un mes promedio). |
| ¿Qué categorías impulsan las ventas? | Technology (36%), Furniture (32%) y Office Supplies (31%) con el mismo patrón estacional. |

## 4. Recomendaciones al negocio
1. **Inventario y compras:** reforzar el stock desde agosto para atender septiembre y desde octubre para noviembre–diciembre.
2. **Personal:** planear contrataciones temporales para el último cuatrimestre.
3. **Temporada baja:** impulsar campañas comerciales en enero–febrero para suavizar la caída.
4. **Política de descuentos:** el análisis mostró ventas con pérdida asociadas a descuentos de hasta 80%; revisar topes de descuento.
5. **Planeación por escenarios:** presupuestar con el rango conservador–optimista, no con un único número.

## 5. Despliegue y entrega
| Componente | Ubicación | Uso |
|---|---|---|
| Pipeline batch `batch_forecast.py` | `Code/03_Deployment/` (GitHub) | Se ejecuta al cierre de cada mes: reentrena y genera el pronóstico |
| Notebook de ejecución | `Code/03_Deployment/03_Deployment.ipynb` | Ejecuta el pipeline directamente desde el repositorio |
| Modelo campeón | Azure ML Model Registry: `ventas-holtwinters-champion` v1 | Versión oficial del modelo |
| Modelo retador | Azure ML Model Registry: `ventas-automl-stackensemble` v1 | Referencia para futuras comparaciones |
| Dashboard | `Code/03_Deployment/Dashboard_Ventas_2018.pbix` | Consumo por gerencia |

**Decisión de arquitectura:** despliegue *batch* mensual (no endpoint en tiempo real), porque el pronóstico se usa una vez al mes y un endpoint generaría costo por hora sin aportar valor.

## 6. Plan de monitoreo y reentrenamiento (MLOps)
- **Cada mes:** comparar ventas reales vs pronóstico y registrar el error (MAPE).
- **Disparador de reentrenamiento:** MAPE móvil de 3 meses > 25% o cambio estructural del negocio (nuevas categorías, cambios de precios).
- **Proceso:** ejecutar el pipeline, comparar campeón vs retador en el último año, registrar la nueva versión en Azure ML solo si mejora.

## 7. Trazabilidad TDSP
| Fase | Entregables | Ubicación |
|---|---|---|
| 1. Entendimiento del negocio | Project Charter | `Docs/Project/Charter.md` |
| 2. Adquisición y entendimiento de datos | Notebook, Data Report, Diccionario, datos crudos y procesados, Data Assets versionados en Azure | `Code/01_...`, `Docs/Data_Report/`, `Sample_Data/` |
| 3. Modelado | Notebook de modelado, Model Report, experimento AutoML | `Code/02_Modeling/`, `Docs/Model/`, Azure ML |
| 4. Despliegue | Pipeline batch, modelos registrados, dashboard | `Code/03_Deployment/`, Azure ML Model Registry |
| 5. Aceptación del cliente | Este informe | `Docs/Project/Informe_Final.md` |
| Gestión ágil | Tablero de 4 sprints | GitHub Projects: *Workshop 3 – TDSP* |

## 8. Lecciones aprendidas
1. **Validar con datos que el modelo nunca vio:** AutoML mostró 18,9% de MAPE en validación cruzada pero 30,1% en 2017 (sobreajuste). Sin un set de prueba independiente se habría elegido el peor modelo.
2. **Con poca historia, gana lo simple:** modelos estacionales clásicos superaron a modelos de ML y ensambles complejos.
3. **Definir el criterio de selección antes de ver resultados** evita elegir la métrica a conveniencia.
4. **Especificar bien las métricas de éxito:** el MASE debió escalarse con el periodo de prueba.
5. **Cuidar formatos de datos:** fechas mes/día/año, separadores decimales y formatos de fecha en Azure generaron errores que se detectaron validando cada paso.
6. **La configuración importa en AutoML:** con series cortas hubo que desactivar rezagos y ventanas móviles y usar pasos de validación pequeños.

## 9. Próximos pasos
- Incorporar variables exógenas (promociones, descuentos, feriados) y más historia.
- Probar un ensamble Holt-Winters aditivo + multiplicativo.
- Pronósticos por categoría y región para decisiones de inventario más finas.
- Automatizar la ejecución mensual con GitHub Actions o una programación en Azure ML.
