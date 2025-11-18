import numpy as np
from dataclasses import dataclass


@dataclass
class SeasonalConsumptionParams:
    """
    Parámetros del modelo de consumo estacional:
    c(t) = α + β cos(ω t) + γ sin(ω t),  ω = 2π/12
    """

    alpha: float  # consumo promedio mensual (COP/mes)
    beta: float  # amplitud coseno (COP/mes)
    gamma: float  # amplitud seno (COP/mes)


OMEGA = 2.0 * np.pi / 12.0


def seasonal_consumption(
    t: np.ndarray, params: SeasonalConsumptionParams
) -> np.ndarray:
    """
    Calcula c(t) para un arreglo de tiempos t (en meses).
    """
    return (
        params.alpha
        + params.beta * np.cos(OMEGA * t)
        + params.gamma * np.sin(OMEGA * t)
    )
