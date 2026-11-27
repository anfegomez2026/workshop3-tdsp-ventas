# Data Report – Adquisición y entendimiento de datos

Notebook: `Code/01_Data_Acquisition_and_Understanding/`

## 1. Ingesta
- Lectura directa desde la URL con `pandas` (no Excel), declarando el formato de fecha `%m/%d/%Y` para evitar confundir día y mes.
- Pipeline reproducible: al volver a ejecutar el notebook se actualiza todo si cambia la fuente.

## 2. Calidad de datos
| Validación | Resultado |
|---|---|
| Valores nulos | 0 |
| Filas duplicadas | 0 |
| Row ID único | Sí |
| Envíos con fecha anterior al pedido | 0 |
| Ventas ≤ 0 | 0 |
| Descuentos fuera de [0, 1] | 0 |
| Rango de fechas | 2014-01-03 → 2017-12-30 |
| Pedidos / clientes / productos | 5.009 / 793 / 1.862 |

- `Sales` por línea está muy sesgada a la derecha (media $229,86; mediana $54,49; máximo $22.638,48).
- 1.167 líneas atípicas (regla IQR, 11,7%) **se conservan**: son compras reales y eliminarlas subestimaría las ventas. Su efecto se diluye al agregar por mes.
- Hay líneas con pérdida (Profit mínimo −$6.599,98) asociadas a descuentos de hasta 80%.

## 3. Transformación
- Agregación de `Sales` por mes de `Order Date` → **48 meses completos**, sin meses faltantes ni en cero.
- Serie adicional mensual por categoría.

## 4. Tendencia
| Año | Ventas (USD) | Crecimiento |
|---|---|---|
| 2014 | 484.247 | – |
| 2015 | 470.533 | −2,8% |
| 2016 | 609.206 | +29,5% |
| 2017 | 733.215 | +20,4% |

Crecimiento de ~51% en el periodo (~15% anual compuesto), acelerado desde 2016.

## 5. Estacionalidad
Índice estacional (1 = mes promedio):

| Ene | Feb | Mar | Abr | May | Jun | Jul | Ago | Sep | Oct | Nov | Dic |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0,50 | 0,31 | 1,07 | 0,72 | 0,81 | 0,80 | 0,77 | 0,83 | 1,61 | 1,05 | 1,84 | 1,70 |

- Temporada alta: septiembre, noviembre y diciembre (~43% de las ventas anuales).
- Temporada baja: enero y febrero.
- La amplitud estacional crece con el nivel (relación amplitud/media ≈ 1,6 estable) → **estacionalidad multiplicativa** → se modela log(ventas).

## 6. Categorías
Technology 36,4% · Furniture 32,3% · Office Supplies 31,3%. Las tres comparten el patrón estacional → se modela el total.

## 7. Descomposición STL (periodo 12, robusta)
- Fuerza de la estacionalidad: **0,86** (fuerte).
- Fuerza de la tendencia: **0,53** (moderada).

## 8. Estacionariedad (ADF + KPSS)
| Serie | n | ADF p | KPSS p | Conclusión |
|---|---|---|---|---|
| Original | 48 | 0,0002 | 0,0187 | Mixto |
| Log | 48 | 0,0000 | 0,0100 | Mixto |
| Log + diff(1) | 47 | 0,0000 | ≥0,10 | Estacionaria |
| Log + diff(12) | 36 | 0,0000 | ≥0,10 | Estacionaria |
| Log + diff(12) + diff(1) | 35 | 0,0000 | ≥0,10 | Estacionaria |

## 9. ACF / PACF
- Log(ventas): picos significativos en rezago 1 (~0,3) y **rezago 12 (~0,5)** → estacionalidad anual confirmada.
- Doble diferencia: ACF en rezago 1 ≈ −0,5 → posible sobrediferenciación; PACF significativa en rezagos 1 y 2.

## 10. Meses atípicos (|z| > 2 en residuo STL)
| Mes | Ventas | z |
|---|---|---|
| 2016-05 | 56.988 | +2,91 |
| 2016-11 | 79.412 | −2,62 |
| 2016-12 | 96.999 | +2,61 |

No se corrigen (ventas reales, pocos datos, STL robusta). Hipótesis: desplazamiento de demanda entre noviembre y diciembre de 2016.

## 11. Conclusiones para el modelado
1. Datos de alta calidad; no se requirió imputación.
2. Tendencia creciente y estacionalidad anual fuerte y multiplicativa.
3. Se modela log(ventas) con una diferencia estacional (D=1).
4. Candidatos: ingenuo estacional (baseline), Holt-Winters multiplicativo, SARIMA(1,0,0)(1,1,0)₁₂ con drift, SARIMA(0,1,1)(0,1,1)₁₂ (aerolínea), auto-ARIMA, modelo de ML con rezagos y AutoML de Azure ML.
5. Riesgos: historia corta (4 ciclos) y atípicos en 2016.
