def format_currency(value: float) -> str:
    return f"${value:,.0f}".replace(",", ".")


def format_percent(value: float, decimals: int = 2) -> str:
    return f"{value:.{decimals}f}%"
