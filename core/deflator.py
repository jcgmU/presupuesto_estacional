import numpy as np


def build_deflator(pi_t: np.ndarray, dt: float) -> np.ndarray:
    """
    Construye el deflactor continuo D(t) ≈ exp(-∫ π(s) ds)
    usando integración por trapecios sobre la malla uniforme.
    """
    integral_pi = np.zeros_like(pi_t)
    for k in range(1, len(pi_t)):
        integral_pi[k] = integral_pi[k - 1] + 0.5 * (pi_t[k - 1] + pi_t[k]) * dt
    return np.exp(-integral_pi)
