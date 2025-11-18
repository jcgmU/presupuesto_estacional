import numpy as np
import pandas as pd
from dataclasses import dataclass

MONTH_LABELS = [
    "Sep-24",
    "Oct-24",
    "Nov-24",
    "Dic-24",
    "Ene-25",
    "Feb-25",
    "Mar-25",
    "Abr-25",
    "May-25",
    "Jun-25",
    "Jul-25",
    "Ago-25",
]

# Serie de ejemplo: variación % mensual (DANE Sep-2024 – Ago-2025)
DEFAULT_INFLATION_PERCENT = np.array(
    [0.24, -0.13, 0.27, 0.46, 1.14, 0.82, 0.52, 0.66, 0.32, 0.10, 0.28, 0.19],
    dtype=float,
)


@dataclass
class InflationScenarioConfig:
    """
    Configuración de escenario inflacionario.
    factor: escala global (0.2–2.0) aplicada a las tasas mensuales.
    """

    factor: float = 1.0


def get_default_inflation_dataframe() -> pd.DataFrame:
    """Devuelve DataFrame de inflación mensual de ejemplo."""
    return pd.DataFrame(
        {
            "Mes": MONTH_LABELS,
            "Inflación mensual (%)": DEFAULT_INFLATION_PERCENT.copy(),
        }
    )


def scale_inflation(
    inflation_percent: np.ndarray, scenario: InflationScenarioConfig
) -> np.ndarray:
    """
    Escala las tasas de inflación mensual (%) por el factor del escenario.
    """
    return np.array(inflation_percent, dtype=float) * float(scenario.factor)


def monthly_percent_to_log_rate(monthly_percent: np.ndarray) -> np.ndarray:
    """
    Convierte inflación mensual en % a tasas logarítmicas mensuales π_m = ln(1 + p_m).
    p_m se interpreta como proporción (p/100).
    """
    p = np.array(monthly_percent, dtype=float) / 100.0
    return np.log1p(p)


def piecewise_pi_t(pi_monthly: np.ndarray, t: np.ndarray) -> np.ndarray:
    """
    Construye función pieza-constante π(t) a partir de 12 tasas logarítmicas π_m.
    t se asume en meses en [0, 12].
    """
    if len(pi_monthly) != 12:
        raise ValueError("Se esperaban 12 valores de inflación mensual.")
    t_clipped = np.clip(t, 0.0, 11.9999)
    month_index = np.floor(t_clipped).astype(int)  # 0..11
    return pi_monthly[month_index]
