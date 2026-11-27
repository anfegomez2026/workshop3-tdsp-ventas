# Diccionario de datos

Fuente: CSV publicado en Google Sheets · 9.994 filas · 21 columnas · 0 nulos. Cada fila es una línea de pedido (un producto dentro de una orden).

| Variable | Tipo | Descripción | Uso en el proyecto |
|---|---|---|---|
| Row ID | entero | Identificador de la línea | Control de calidad (único) |
| Order ID | texto | Identificador del pedido | Conteo de pedidos |
| Order Date | fecha (mes/día/año) | Fecha del pedido | **Índice de la serie de tiempo** |
| Ship Date | fecha (mes/día/año) | Fecha de envío | Validación (≥ Order Date) |
| Ship Mode | categoría | Modo de envío | EDA |
| Customer ID | texto | Identificador del cliente | EDA |
| Customer Name | texto | Nombre del cliente | No se usa |
| Segment | categoría | Consumer, Corporate, Home Office | EDA |
| Country | categoría | País (solo United States) | Validación |
| City / State | categoría | Ciudad y estado | EDA |
| Postal Code | texto | Código postal (leído como texto para conservar ceros) | No se usa |
| Region | categoría | West, East, Central, South | EDA |
| Product ID | texto | Identificador del producto | EDA |
| Category | categoría | Furniture, Office Supplies, Technology | Serie por categoría |
| Sub-Category | categoría | Subcategoría del producto | EDA |
| Product Name | texto | Nombre del producto | No se usa |
| **Sales** | decimal (USD) | Valor de venta de la línea | **Variable objetivo (suma mensual)** |
| Quantity | entero | Unidades vendidas | EDA |
| Discount | decimal (0–0,8) | Descuento aplicado | EDA / insights |
| Profit | decimal (USD) | Utilidad de la línea (puede ser negativa) | EDA / insights |

## Datasets derivados (`Sample_Data/Processed`)
| Archivo | Contenido |
|---|---|
| `ventas_mensuales.csv` | `Month` (inicio de mes), `Sales` (suma mensual) – 48 filas |
| `ventas_mensuales_categoria.csv` | `Order Date` (mes) + ventas mensuales de Furniture, Office Supplies y Technology |
