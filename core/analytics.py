from dataclasses import dataclass
from typing import Literal, Dict, Any

import numpy as np
import pandas as pd

from .consumption import SeasonalConsumptionParams, seasonal_consumption
from .inflation import (
    scale_inflation,
    monthly_percent_to_log_rate,
    piecewise_pi_t,
    MONTH_LABELS,
)
from .deflator import build_deflator
from .integration import (
    integrate_rectangles,
    integrate_trapezoidal,
    integrate_simpson,
)

IntegrationMethod = Literal["Simpson", "Trapecios", "Rectángulos"]


@dataclass
class ScenarioConfig:
    """Configuración completa de un escenario de simulación."""

    consumption: SeasonalConsumptionParams
    inflation_percent: np.ndarray  # 12 valores en %
    inflation_factor: float  # κ
    method: IntegrationMethod  # método numérico


def build_time_grid(num_steps: int = 600):
    t = np.linspace(0.0, 12.0, num_steps + 1)
    dt = t[1] - t[0]
    return t, dt


def compute_scenario(config: ScenarioConfig) -> Dict[str, Any]:
    """Ejecuta todos los cálculos del escenario y devuelve resultados y series."""
    # Escalar inflación (%)
    inflation_scaled = scale_inflation(
        config.inflation_percent,
        # usamos un dataclass-like simple
        type("Tmp", (), {"factor": config.inflation_factor})(),
    )
    # Malla temporal
    t, dt = build_time_grid(num_steps=600)

    # Consumo nominal
    c_t = seasonal_consumption(t, config.consumption)

    # π(t) y deflactor
    pi_monthly = monthly_percent_to_log_rate(inflation_scaled)
    pi_t = piecewise_pi_t(pi_monthly, t)
    D_t = build_deflator(pi_t, dt)
    f_t = c_t * D_t  # integrando: consumo real

    # Método numérico
    if config.method == "Simpson":
        integrate = integrate_simpson
    elif config.method == "Trapecios":
        integrate = integrate_trapezoidal
    else:
        integrate = integrate_rectangles

    G_nom = integrate(c_t, dt)
    G_real = integrate(f_t, dt)
    delta = G_nom - G_real

    # Gasto real acumulado (para curva)
    G_real_acum = np.zeros_like(f_t)
    for k in range(1, len(f_t)):
        G_real_acum[k] = G_real_acum[k - 1] + 0.5 * (f_t[k - 1] + f_t[k]) * dt

    # Resumen mensual (aproximación en puntos medios)
    meses = np.arange(12)
    t_mid = meses + 0.5
    c_mid = seasonal_consumption(t_mid, config.consumption)
    pi_mid = piecewise_pi_t(pi_monthly, t_mid)

    # deflactor en 12 meses: malla refinada
    t12, dt12 = np.linspace(0.0, 12.0, 12 * 10 + 1, retstep=True)
    pi12 = piecewise_pi_t(pi_monthly, t12)
    D12 = build_deflator(pi12, dt12)
    D_mid = np.interp(t_mid, t12, D12)

    real_mid = c_mid * D_mid

    df_mensual = pd.DataFrame(
        {
            "Mes": MONTH_LABELS,
            "Inflación mensual (%)": np.round(inflation_scaled, 3),
            "Consumo nominal estimado (COP)": np.round(c_mid, 0),
            "Consumo real estimado (COP)": np.round(real_mid, 0),
        }
    )

    df_tiempo = pd.DataFrame(
        {
            "t_mes": t,
            "Consumo nominal (COP/mes)": c_t,
            "π(t) (mes^-1)": pi_t,
            "Deflactor D(t)": D_t,
            "Consumo real instantáneo (COP/mes)": f_t,
            "Gasto real acumulado (COP)": G_real_acum,
        }
    )

    # Métricas adicionales
    inflation_avg = float(np.mean(inflation_scaled))
    inflation_accum_log = float(np.sum(pi_monthly))
    inflation_accum_pct = (np.exp(inflation_accum_log) - 1.0) * 100.0

    metrics = {
        "G_nom": G_nom,
        "G_real": G_real,
        "delta": delta,
        "inflation_avg_pct": inflation_avg,
        "inflation_accum_pct": inflation_accum_pct,
    }

    return {
        "t": t,
        "dt": dt,
        "c_t": c_t,
        "pi_t": pi_t,
        "D_t": D_t,
        "f_t": f_t,
        "G_real_acum": G_real_acum,
        "df_mensual": df_mensual,
        "df_tiempo": df_tiempo,
        "metrics": metrics,
        "inflation_scaled": inflation_scaled,
    }
