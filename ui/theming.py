import streamlit as st

PALETTE = {
    "bg": "#F4F1E9",  # fondo general beige
    "sidebar_bg": "#1F1F24",  # sidebar oscuro
    "card_bg": "#FFFFFF",
    "card_alt": "#F9F6EE",
    "primary": "#4E5AC7",
    "success": "#3BAA6E",
    "warning": "#E89A3C",
    "text_main": "#272727",
    "text_muted": "#777777",
    "border_soft": "#E0DED5",
}


def inject_global_css():
    css = f"""
    <style>
    /* --------- Fuente global tipo SaaS --------- */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class^="css"], .stApp {{
        font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }}

    .stApp {{
        background-color: {PALETTE["bg"]};
    }}

    /* --------- Sidebar oscuro estilo dashboard --------- */
    [data-testid="stSidebar"] {{
        background: {PALETTE["sidebar_bg"]};
        color: #F7F7F7;
        padding-top: 1rem;
        padding-bottom: 2rem;
    }}

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h4,
    [data-testid="stSidebar"] h5,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span {{
        color: #F7F7F7 !important;
    }}

    /* Corregimos colores dentro de la tabla de inflación del sidebar */
    [data-testid="stSidebar"] [data-testid="stDataFrame"] span {{
        color: #111111 !important;
    }}

    /* Header del sidebar (avatar + nombre) */
    .sidebar-header {{
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1.5rem;
        padding: 0.75rem 0.5rem 0.75rem 0.25rem;
    }}

    .sidebar-avatar {{
        width: 40px;
        height: 40px;
        border-radius: 999px;
        background: linear-gradient(135deg, #FACC6B, #F97373);
        display: flex;
        align-items: center;
        justify-content: center;
        color: #1F1F24;
        font-weight: 600;
        font-size: 1rem;
    }}

    .sidebar-hello {{
        font-size: 0.75rem;
        color: #A3A3B0;
        margin-bottom: 0.1rem;
    }}

    .sidebar-name {{
        font-size: 0.95rem;
        font-weight: 600;
        color: #FFFFFF;
    }}

    .sidebar-section-title {{
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #A3A3B0 !important;
        margin-top: 0.75rem;
        margin-bottom: 0.25rem;
    }}

    hr.sidebar-divider {{
        border: none;
        border-top: 1px solid rgba(255,255,255,0.12);
        margin: 0.75rem 0 0.75rem 0;
    }}

    /* --------- KPI cards estilo tarjetas redondeadas --------- */
    .kpi-card {{
        border-radius: 24px;
        padding: 18px 22px;
        background: {PALETTE["card_bg"]};
        box-shadow: 0 18px 40px rgba(15, 23, 42, 0.06);
        border: 1px solid {PALETTE["border_soft"]};
    }}

    .kpi-title {{
        font-size: 0.85rem;
        font-weight: 500;
        color: {PALETTE["text_muted"]};
        margin-bottom: 0.35rem;
    }}

    .kpi-value {{
        font-size: 1.4rem;
        font-weight: 600;
        color: {PALETTE["text_main"]};
        margin-bottom: 0.1rem;
    }}

    .kpi-sub {{
        font-size: 0.78rem;
        color: {PALETTE["text_muted"]};
        line-height: 1.2;
        white-space: pre-line;
    }}

    /* --------- Zona principal: separador suave entre header y contenido --------- */
    section.main > div:first-child {{
        padding-top: 0.5rem;
    }}

    /* Botones y sliders con color primario */
    .stButton>button {{
        border-radius: 999px;
        background: {PALETTE["primary"]};
        color: white;
        border: none;
        padding: 0.4rem 1.2rem;
        font-weight: 500;
    }}
    .stButton>button:hover {{
        filter: brightness(1.05);
    }}

    .stSlider > div[data-baseweb="slider"] > div {{
        background: rgba(255,255,255,0.10);
    }}
    .stSlider [data-baseweb="slider"] > div > div {{
        background: {PALETTE["primary"]};
    }}

    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
