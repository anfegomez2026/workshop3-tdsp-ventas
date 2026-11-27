"""
Fase 4 TDSP – Despliegue: pronóstico batch mensual (modelo campeón Holt-Winters multiplicativo).

Pipeline reproducible:
  1. Ingesta del CSV de origen (misma URL del proyecto).
  2. Agregación mensual de ventas.
  3. Reentrenamiento del modelo campeón con toda la historia.
  4. Pronóstico de los próximos 12 meses.
  5. Exporta: pronostico.csv, ventas_real_y_pronostico_pbi.csv (consumo Power BI) y modelo_holtwinters.pkl.

Uso:  python batch_forecast.py
Se ejecuta cada mes (p. ej. con una tarea programada o un pipeline de CI/CD) al cerrar el mes.
"""
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing

URL = ("https://docs.google.com/spreadsheets/d/e/2PACX-1vSR7UD5-D1NVWyP8lgQ7R7QaN-FiZX8mkHI3piBLe7h34eYuqX7Kjt111lk1Y_jmQ"
       "/pub?gid=1926354761&single=true&output=csv")
HORIZONTE = 12


def cargar_serie(url: str = URL) -> pd.Series:
    df = pd.read_csv(url)
    df["Order Date"] = pd.to_datetime(df["Order Date"], format="%m/%d/%Y")
    y = df.set_index("Order Date")["Sales"].resample("MS").sum().rename("Sales")
    y.index.name = "Month"
    return y


def entrenar(y: pd.Series):
    return ExponentialSmoothing(y, trend="add", seasonal="mul", seasonal_periods=12).fit()


def main():
    y = cargar_serie()
    modelo = entrenar(y)
    modelo.save("modelo_holtwinters.pkl")

    fut = pd.date_range(y.index[-1] + pd.offsets.MonthBegin(1), periods=HORIZONTE, freq="MS")
    pron = pd.Series(modelo.forecast(HORIZONTE).values, index=fut, name="Pronostico")
    pron.index.name = "Month"
    pron.round(2).to_csv("pronostico.csv")

    pbi = pd.concat([
        y.rename("Ventas").to_frame().assign(Tipo="Real"),
        pron.rename("Ventas").to_frame().assign(Tipo="Pronóstico"),
    ])
    pbi.index.name = "Mes"
    pbi["Ventas"] = pbi["Ventas"].round(0).astype(int)
    pbi.to_csv("ventas_real_y_pronostico_pbi.csv", encoding="utf-8-sig")

    print(f"Historia: {y.index.min():%Y-%m} a {y.index.max():%Y-%m} | "
          f"Pronóstico {fut[0]:%Y-%m} a {fut[-1]:%Y-%m} | Total: {pron.sum():,.0f}")


if __name__ == "__main__":
    main()
