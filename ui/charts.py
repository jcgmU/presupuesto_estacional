import streamlit as st
import plotly.express as px
import pandas as pd


def render_main_charts(df_tiempo: pd.DataFrame):
    st.subheader("Perfil de consumo nominal vs real")
    st.markdown(
        """
        - La **línea azul oscura** muestra cuánto pagarías cada mes, sin ajustar por inflación.  
        - La **línea azul clara** muestra ese mismo gasto, pero llevado a “pesos de hoy”.
        
        Si las líneas se separan mucho, significa que en esos meses la inflación te está pegando más fuerte.
        """
    )

    df_line = df_tiempo[
        [
            "t_mes",
            "Consumo nominal (COP/mes)",
            "Consumo real instantáneo (COP/mes)",
        ]
    ].copy()
    fig1 = px.line(
        df_line,
        x="t_mes",
        y=[
            "Consumo nominal (COP/mes)",
            "Consumo real instantáneo (COP/mes)",
        ],
        labels={"t_mes": "Tiempo (meses)"},
    )
    fig1.update_layout(margin=dict(l=10, r=10, t=40, b=10))
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("Gasto real acumulado a lo largo del año")
    st.markdown(
        """
        Esta curva te muestra cuánto habrás gastado **acumulado** en el año,
        siempre expresado en “pesos de hoy”.

        Un tramo más inclinado indica que en esos meses se está concentrando
        una parte importante del gasto real.
        """
    )

    fig2 = px.line(
        df_tiempo,
        x="t_mes",
        y="Gasto real acumulado (COP)",
        labels={"t_mes": "Tiempo (meses)"},
    )
    fig2.update_layout(margin=dict(l=10, r=10, t=40, b=10))
    st.plotly_chart(fig2, use_container_width=True)
