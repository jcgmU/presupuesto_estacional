import streamlit as st

from core.analytics import ScenarioConfig, compute_scenario
from core.consumption import SeasonalConsumptionParams
from core.inflation import DEFAULT_INFLATION_PERCENT
from ui.theming import inject_global_css
from ui.sidebar import render_sidebar
from ui.cards import render_kpi_row
from ui.charts import render_main_charts
from ui.tables import render_monthly_table


def main():
    st.set_page_config(
        page_title="Planificador Inteligente de Presupuesto Estacional",
        layout="wide",
    )

    inject_global_css()

    # Sidebar → parámetros de simulación
    params, inflation_array, k, method = render_sidebar()

    # Configuración de escenario (capa core)
    scenario_config = ScenarioConfig(
        consumption=params,
        inflation_percent=(
            inflation_array
            if inflation_array is not None
            else DEFAULT_INFLATION_PERCENT
        ),
        inflation_factor=k,
        method=method,  # "Simpson" | "Trapecios" | "Rectángulos"
    )

    # Cálculos
    results = compute_scenario(scenario_config)
    metrics = results["metrics"]
    df_tiempo = results["df_tiempo"]
    df_mensual = results["df_mensual"]

    # Layout principal
    # Layout principal
    st.title("📊 Planificador Inteligente de Presupuesto Estacional")
    st.markdown(
        """
        Esta herramienta te ayuda a responder una pregunta sencilla:

        **¿Cuánto vas a gastar realmente en el año, teniendo en cuenta que los precios cambian?**

        A partir de tu **gasto mensual promedio** y una **trayectoria de inflación**:

        - estima cuánto gastarías en el año si los precios no cambiaran,
        - calcula cuánto equivale ese gasto en **“pesos de hoy”**,
        - muestra cuánto **poder adquisitivo pierdes** por la inflación
          y cómo se reparte eso a lo largo del año.
        """
    )

    with st.expander("🧭 Guía rápida: ¿qué estoy viendo en la pantalla?"):
        st.markdown(
            """
            - **Tarjetas de arriba** → resumen del año:
              gasto nominal, gasto real y pérdida de poder adquisitivo.
            - **Gráfico “Perfil de consumo”** → muestra cómo se reparte tu gasto
              mes a mes, con y sin efecto de la inflación.
            - **Gráfico “Gasto real acumulado”** → muestra cuánto llevas gastado
              en el año a precios de hoy.
            - **Tabla mensual** → detalle por mes: inflación, gasto nominal y real.
            - **Descarga CSV** → para que puedas analizar o presentar los resultados
              en otra herramienta (Excel, pandas, etc.).
            """
        )

    # KPIs
    render_kpi_row(metrics)

    st.markdown("---")

    # Gráficos principales
    render_main_charts(df_tiempo)

    st.markdown("---")

    # Tabla mensual
    render_monthly_table(df_mensual)

    # Descarga
    st.subheader("Descargar series completas")
    csv_data = df_tiempo.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Descargar CSV",
        data=csv_data,
        file_name="presupuesto_estacional_series.csv",
        mime="text/csv",
    )

    st.caption(
        "Esta herramienta es una aproximación educativa al gasto real anual con inflación y "
        "consumo estacional. No reemplaza asesoría financiera profesional."
    )


if __name__ == "__main__":
    main()
