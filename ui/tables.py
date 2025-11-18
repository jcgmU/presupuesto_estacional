import streamlit as st
import pandas as pd
import plotly.express as px

from utils.formatting import format_currency, format_percent


def render_monthly_table(df_mensual: pd.DataFrame):
    st.subheader("Detalle mes a mes")
    st.markdown(
        """
        Aquí puedes ver, para cada mes:

        - la inflación que estás suponiendo,
        - el gasto mensual a precios de ese momento,
        - y el mismo gasto convertido a "pesos de hoy".

        Úsalo para identificar meses particularmente caros o sensibles a la inflación.
        """
    )

    # ----- Copia SOLO para mostrar, con formato humano -----
    df_display = df_mensual.copy()

    # Inflación en formato porcentual
    df_display["Inflación mensual (%)"] = df_display["Inflación mensual (%)"].map(
        lambda x: format_percent(x, 2)
    )

    # Columnas en pesos con signo y separadores de miles
    for col in ["Consumo nominal estimado (COP)", "Consumo real estimado (COP)"]:
        df_display[col] = df_display[col].map(format_currency)

    st.dataframe(df_display, hide_index=True, use_container_width=True)

    # ----- Gráfico de barras: usamos el DataFrame numérico original -----
    df_plot = df_mensual.set_index("Mes")[
        [
            "Consumo nominal estimado (COP)",
            "Consumo real estimado (COP)",
        ]
    ].reset_index()

    fig_bar = px.bar(
        df_plot,
        x="Mes",
        y=["Consumo nominal estimado (COP)", "Consumo real estimado (COP)"],
        barmode="group",
        labels={"value": "COP", "variable": "Tipo de consumo"},
    )
    fig_bar.update_layout(
        margin=dict(l=10, r=10, t=40, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )

    st.plotly_chart(fig_bar, use_container_width=True)


def render_annual_summary(df_anual: pd.DataFrame):
    st.subheader("Resumen anual")
    st.markdown(
        """
        Aquí puedes ver un resumen anual de tu presupuesto, tanto en términos nominales como reales.

        Úsalo para entender cómo la inflación afecta tu poder adquisitivo año tras año.
        """
    )

    st.dataframe(df_anual, hide_index=True, use_container_width=True)

    df_plot = df_anual.set_index("Año")[
        [
            "Consumo nominal estimado (COP)",
            "Consumo real estimado (COP)",
        ]
    ].reset_index()

    fig_bar = px.bar(
        df_plot,
        x="Año",
        y=["Consumo nominal estimado (COP)", "Consumo real estimado (COP)"],
        barmode="group",
        labels={"value": "COP", "variable": "Tipo de consumo"},
    )
    fig_bar.update_layout(
        margin=dict(l=10, r=10, t=40, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )

    st.plotly_chart(fig_bar, use_container_width=True)
