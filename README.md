# 📊 Planificador Inteligente de Presupuesto Estacional

Una herramienta interactiva que te ayuda a responder una pregunta fundamental:

> **¿Cuánto vas a gastar realmente en el año, teniendo en cuenta que los precios cambian?**

## 🎯 ¿Qué hace?

El planificador toma tu **gasto mensual promedio** y una **trayectoria de inflación** para:

- 📈 Estimar cuánto gastarías en el año si los precios no cambiaran
- 💱 Calcular cuánto equivale ese gasto en **"pesos de hoy"** (poder adquisitivo real)
- 📉 Mostrar cuánto **poder adquisitivo pierdes** por la inflación
- 📅 Desglosar el impacto mes a mes, considerando tu consumo estacional

## 🚀 Inicio rápido

### Requisitos

- Python 3.9+
- pip o conda

### Instalación

```bash
# Clonar o descargar el proyecto
cd /Users/jcgm/Desktop/presupuesto_estacional

# Crear entorno virtual (recomendado)
python3 -m venv venv
source venv/bin/activate  # En macOS/Linux

# Instalar dependencias
pip install -r requirements.txt
```

### Ejecutar la aplicación

```bash
streamlit run presupuesto_estacional/app.py
```

La aplicación se abrirá en tu navegador en `http://localhost:8501`.

## 📚 Cómo usar

### Paso 1: Gasto mensual

Ingresa tu gasto típico en un mes normal (sin vacaciones ni compras grandes).

### Paso 2: Cómo varía tu gasto

- **Variación entre meses**: cuánta diferencia hay entre tus meses más baratos y más caros
- **Peso de temporadas especiales**: navidad, vacaciones, temporada escolar, etc.

### Paso 3: Inflación

- Usa los datos de ejemplo DANE (recomendado) o edita tus propios valores
- Ajusta el escenario: base, optimista, crítico o personalizado

### Paso 4: Método de cálculo

Elige el nivel de precisión numérica que prefieres.

## 📊 Visualizaciones principales

- **Tarjetas de resumen**: gasto nominal, gasto real y pérdida de poder adquisitivo
- **Perfil de consumo**: comparación mes a mes entre gasto nominal y real
- **Gasto real acumulado**: cuánto llevas gastado a lo largo del año en "pesos de hoy"
- **Tabla mensual**: detalle línea por línea con inflación y conversión a pesos reales
- **Descarga CSV**: exporta los datos para análisis adicional

## 🏗️ Estructura del proyecto

```
presupuesto_estacional/
├── presupuesto_estacional/
│   ├── app.py                 # Entrada principal de Streamlit
│   ├── core/
│   │   ├── analytics.py       # Motor de cálculo principal
│   │   ├── consumption.py     # Modelo de consumo estacional
│   │   ├── inflation.py       # Manejo de tasas de inflación
│   │   ├── deflator.py        # Construcción del deflactor
│   │   └── integration.py     # Métodos de integración numérica
│   ├── ui/
│   │   ├── sidebar.py         # Panel lateral de configuración
│   │   ├── cards.py           # Tarjetas KPI
│   │   ├── charts.py          # Gráficos interactivos
│   │   ├── tables.py          # Tablas de datos
│   │   └── theming.py         # Estilos CSS globales
│   └── utils/
│       └── formatting.py      # Funciones de formato (moneda, %)
├── requirements.txt           # Dependencias Python
└── README.md                  # Este archivo
```

## 🧮 Modelo matemático

El consumo se modela como:

```
c(t) = α + β·cos(ωt) + γ·sin(ωt)
```

Donde:

- **α**: consumo promedio mensual
- **β, γ**: parámetros de variación estacional
- **ω = 2π/12**: frecuencia mensual

La inflación se integra mediante:

```
D(t) = exp(-∫ π(s) ds)
```

Donde **π(t)** es la tasa logarítmica de inflación instantánea.

El gasto real se calcula como:

```
G_real = ∫₀¹² c(t) · D(t) dt
```

Se ofrecen tres métodos de integración:

- **Simpson**: máxima precisión
- **Trapecios**: balance entre precisión y velocidad
- **Rectángulos**: más rápido, menos preciso

## 📌 Limitaciones y aclaraciones

- Esta herramienta es una **aproximación educativa** al gasto real anual con inflación y consumo estacional
- **No reemplaza asesoría financiera profesional**
- Los resultados dependen de la precisión de tus estimaciones de gasto y de la inflación proyectada
- El modelo asume que el patrón estacional se repite uniformemente cada año

## 💡 Casos de uso

- **Planificación personal de presupuesto**: entender cómo la inflación afecta tu poder adquisitivo
- **Análisis de escenarios**: simular diferentes niveles de inflación (optimista, crítico, base)
- **Presentaciones ejecutivas**: mostrar el impacto de la inflación en gastos corporativos
- **Educación financiera**: enseñar conceptos de inflación, deflactores y consumo estacional

## 🛠️ Tecnologías

- **Streamlit**: framework para apps de datos interactivas
- **Pandas**: manipulación y análisis de datos
- **NumPy**: cálculos numéricos y álgebra lineal
- **Plotly**: gráficos interactivos
- **Python 3.9+**: lenguaje base

## 📝 Ejemplo de uso

```python
from core.analytics import ScenarioConfig, compute_scenario
from core.consumption import SeasonalConsumptionParams
from core.inflation import DEFAULT_INFLATION_PERCENT

# Parámetros de consumo
params = SeasonalConsumptionParams(
    alpha=1_500_000,      # gasto promedio
    beta=150_000,         # variación mensual
    gamma=50_000          # estacionalidad
)

# Configuración del escenario
config = ScenarioConfig(
    consumption=params,
    inflation_percent=DEFAULT_INFLATION_PERCENT,
    inflation_factor=1.0,
    method="Simpson"
)

# Ejecutar cálculos
results = compute_scenario(config)
print(f"Gasto nominal: ${results['metrics']['G_nom']:,.0f}")
print(f"Gasto real: ${results['metrics']['G_real']:,.0f}")
print(f"Pérdida: ${results['metrics']['delta']:,.0f}")
```

## 🤝 Contribuciones

Las sugerencias y mejoras son bienvenidas. Por favor:

1. Abre un issue describiendo el problema o la mejora
2. Haz un fork del proyecto
3. Crea una rama (`git checkout -b feature/mi-mejora`)
4. Haz commit de tus cambios
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo licencia MIT. Ver detalles en el archivo LICENSE (si aplica).

## 📧 Contacto

Para preguntas o sugerencias sobre este proyecto, por favor contacta al autor.

---

**Tip:** Cambia solo una cosa a la vez (por ejemplo, el escenario de inflación) y observa cómo se mueven los indicadores y las curvas. ¡Así aprenderás cómo funciona tu presupuesto!
