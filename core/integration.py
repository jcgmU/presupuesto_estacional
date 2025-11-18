import numpy as np


def integrate_rectangles(f: np.ndarray, dt: float) -> float:
    """
    Regla de rectángulos (puntos medios aproximados con promedio de extremos).
    """
    mid_values = 0.5 * (f[:-1] + f[1:])
    return float(np.sum(mid_values) * dt)


def integrate_trapezoidal(f: np.ndarray, dt: float) -> float:
    """
    Regla del trapecio compuesta.
    """
    return float((f[0] + 2.0 * np.sum(f[1:-1]) + f[-1]) * dt / 2.0)


def integrate_simpson(f: np.ndarray, dt: float) -> float:
    """
    Regla de Simpson compuesta.
    Si el número de subintervalos es impar, se usa Simpson hasta el penúltimo
    y trapecio en el último.
    """
    n = len(f) - 1  # subintervalos
    if n < 2:
        return 0.0
    if n % 2 == 1:
        n_simpson = n - 1
        f_s = f[: n_simpson + 1]
        res_s = (
            (f_s[0] + 2.0 * np.sum(f_s[2:-1:2]) + 4.0 * np.sum(f_s[1::2]) + f_s[-1])
            * dt
            / 3.0
        )
        res_t = (f[n_simpson] + f[n_simpson + 1]) * dt / 2.0
        return float(res_s + res_t)
    else:
        return float(
            (f[0] + 2.0 * np.sum(f[2:-1:2]) + 4.0 * np.sum(f[1::2]) + f[-1]) * dt / 3.0
        )
