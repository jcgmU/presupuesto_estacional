import re
import numpy as np
import streamlit as st

from utils.formatting import format_currency
from core.consumption import SeasonalConsumptionParams
from core.inflation import (
    get_default_inflation_dataframe,
    DEFAULT_INFLATION_PERCENT,
)
from typing import Tuple


def money_input(label: str, key: str, default: int, help: str | None = None) -> float:
    """
    Campo de texto para dinero en COP con formato automático:
    - Muestra siempre: $ 1.500.000
    - Guarda el valor numérico limpio en session_state[key + "_value"]
    Devuelve ese valor numérico como float.
    """

    value_key = key + "_value"

    # Inicializar el estado la primera vez
    if key not in st.session_state:
        st.session_state[key] = f"$ {default:,.0f}".replace(",", ".")
        st.session_state[value_key] = float(default)

    def _format_callback():
        raw = str(st.session_state.get(key, ""))
        # Dejar solo dígitos
        digits = re.sub(r"[^\d]", "", raw)
        if digits == "":
            st.session_state[value_key] = 0.0
            st.session_state[key] = ""
            return
        num = int(digits)
        st.session_state[value_key] = float(num)
        st.session_state[key] = f"$ {num:,.0f}".replace(",", ".")

    st.text_input(
        label,
        key=key,
        help=help,
        on_change=_format_callback,
    )

    return float(st.session_state[value_key])


def render_sidebar() -> Tuple[SeasonalConsumptionParams, np.ndarray, float, str]:
    with st.sidebar:
        # Header tipo dashboard
        st.markdown(
            """
            <div class="sidebar-header">
              <div class="sidebar-avatar">C</div>
              <div>
                <div class="sidebar-hello">Bienvenido de nuevo</div>
                <div class="sidebar-name">Planificador Estacional</div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="sidebar-section-title">Configuración</div>',
            unsafe_allow_html=True,
        )
        st.write(
            "Completa estos pasos de izquierda a derecha. No necesitas saber matemáticas para usar la herramienta 😊"
        )

        # -------- Gasto mensual (con formato de moneda) ----------
        st.markdown(
            '<div class="sidebar-section-title">Gasto mensual</div>',
            unsafe_allow_html=True,
        )

        alpha = money_input(
            "¿Cuánto gastas en un mes típico? (COP)",
            key="alpha_input",
            default=1_500_000,
            help="Piensa en un mes normal, sin vacaciones ni compras grandes.",
        )

        # -------- Variación entre meses (como %) ----------
        st.markdown(
            '<div class="sidebar-section-title">Cómo se mueve tu gasto durante el año</div>',
            unsafe_allow_html=True,
        )

        variacion_pct = st.slider(
            "¿Qué tanta diferencia hay entre tus meses más baratos y más caros? (en %)",
            min_value=0,
            max_value=50,
            value=10,
            format="%d%%",
            help=(
                "Este valor va de 0% (casi todos los meses gastas lo mismo) "
                "a 50% (hay meses donde gastas hasta un 50% más que en otros)."
            ),
        )
        st.caption(
            f"Rango del control: **0%** (muy estable) a **50%** (muy variable). "
            f"Valor actual: **{variacion_pct}%**."
        )

        estacionalidad_pct = st.slider(
            "¿Cuánto pesan los meses especiales? (navidad, vacaciones, temporada escolar…) (en %)",
            min_value=0,
            max_value=30,
            value=5,
            format="%d%%",
            help=(
                "Este valor va de 0% (no se nota la temporada) a 30% (los meses especiales "
                "suben bastante tu gasto)."
            ),
        )
        st.caption(
            f"Rango del control: **0%** (sin temporada marcada) a **30%** (temporadas muy fuertes). "
            f"Valor actual: **{estacionalidad_pct}%**."
        )

        # Convertimos de % a proporción para el modelo
        beta_prop = variacion_pct / 100.0
        gamma_prop = estacionalidad_pct / 100.0

        beta = beta_prop * alpha
        gamma = gamma_prop * alpha

        gasto_max = alpha + beta
        gasto_min = alpha - beta

        st.caption(
            f"Con estos valores, tu gasto mensual se mueve aproximadamente entre "
            f"**{gasto_min:,.0f} COP** en meses más tranquilos y "
            f"**{gasto_max:,.0f} COP** en meses más costosos."
        )

        params = SeasonalConsumptionParams(alpha=alpha, beta=beta, gamma=gamma)

        # -------- Inflación ----------
        st.markdown(
            '<div class="sidebar-section-title">Precios e inflación</div>',
            unsafe_allow_html=True,
        )

        use_default = st.checkbox(
            "Usar datos de ejemplo DANE",
            value=True,
            help="Si quieres, puedes dejar esta opción marcada y trabajar con un escenario real de inflación reciente.",
        )

        if use_default:
            df_inf = get_default_inflation_dataframe()
            st.caption(
                "Inflación mensual de referencia (puedes desmarcar la casilla para editarla)."
            )
            st.dataframe(df_inf, hide_index=True)
            inflation_array = DEFAULT_INFLATION_PERCENT.copy()
        else:
            df_inf_edit = get_default_inflation_dataframe()
            st.caption("Modifica las cifras según el escenario que quieras analizar.")
            df_inf = st.data_editor(df_inf_edit, hide_index=True)
            inflation_array = df_inf["Inflación mensual (%)"].to_numpy(dtype=float)

        # -------- Escenario ----------
        st.markdown(
            '<div class="sidebar-section-title">Escenario de precios</div>',
            unsafe_allow_html=True,
        )

        escenario = st.radio(
            "Elige cómo de fuerte imaginas la inflación:",
            [
                "Base (tal como está)",
                "Más baja (optimista)",
                "Más alta (crítica)",
                "Personalizado",
            ],
        )

        if escenario == "Base (tal como está)":
            k = 1.0
            st.caption("Usas exactamente las tasas de inflación mostradas arriba.")
        elif escenario == "Más baja (optimista)":
            k = 0.8
            st.caption(
                "Supone que la inflación termina siendo un 20% más baja de lo que aparece en la tabla."
            )
        elif escenario == "Más alta (crítica)":
            k = 1.2
            st.caption(
                "Supone que la inflación termina siendo un 20% más alta de lo que aparece en la tabla."
            )
        else:
            k = st.slider(
                "Multiplicador de inflación",
                0.2,
                2.0,
                1.0,
                help="1.0 significa que usas tal cual los datos de la tabla. 2.0 duplica todas las tasas; 0.5 las reduce a la mitad.",
            )

        # -------- Método numérico ----------
        st.markdown(
            '<div class="sidebar-section-title">Forma de cálculo</div>',
            unsafe_allow_html=True,
        )

        metodo_label = st.selectbox(
            "¿Qué nivel de detalle quieres en el cálculo?",
            [
                "Estándar (recomendado)",
                "Rápido (menos preciso)",
                "Conservador (suma un poco de margen)",
            ],
            index=0,
            help=(
                "Todas las opciones usan tus mismos datos. "
                "La diferencia está en qué tan fino es el cálculo año completo."
            ),
        )

        if metodo_label.startswith("Estándar"):
            method = "Simpson"  # más preciso
        elif metodo_label.startswith("Rápido"):
            method = "Rectángulos"  # más simple
        else:
            method = "Trapecios"  # intermedio / conservador

        st.markdown('<hr class="sidebar-divider" />', unsafe_allow_html=True)
        st.caption(
            "Tip: cambia solo una cosa a la vez (por ejemplo, el escenario de inflación) y observa cómo se mueven los indicadores y las curvas."
        )

        return params, inflation_array, k, method
