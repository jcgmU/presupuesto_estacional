import streamlit as st
from utils.formatting import format_currency, format_percent


def render_kpi_row(metrics: dict):
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        _kpi_card(
            title="Gasto nominal anual",
            value=format_currency(metrics["G_nom"]),
            subtitle="Suma de todo lo que pagarías en el año si los precios se quedaran como hoy.",
        )
    with col2:
        _kpi_card(
            title="Gasto real anual",
            value=format_currency(metrics["G_real"]),
            subtitle="Lo mismo, pero expresado en “pesos de hoy” después de descontar la inflación.",
        )
    with col3:
        _kpi_card(
            title="Pérdida de poder adquisitivo",
            value=format_currency(metrics["delta"]),
            subtitle="Es la parte del gasto que se explica solo por el aumento de precios.",
        )
    with col4:
        sub = (
            f"Inflación promedio del año: {format_percent(metrics['inflation_avg_pct'])}\n"
            f"Inflación acumulada: {format_percent(metrics['inflation_accum_pct'])}"
        )
        _kpi_card(
            title="Inflación del periodo",
            value="",
            subtitle=sub,
        )


def _kpi_card(title: str, value: str, subtitle: str):
    st.markdown(
        f"""
        <div class="kpi-card">
          <div class="kpi-title">{title}</div>
          <div class="kpi-value">{value}</div>
          <div class="kpi-sub">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
