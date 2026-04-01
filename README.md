# evaluador-madurez-industria-4.0
Evaluador de Madurez en Industria 4.0 con IA (Random Forest + Clustering + ISM) para PyMEs ecuatorianas
# Evaluador de Madurez en Industria 4.0 con IA

**Trabajo de Titulación**  
**PyMEs Ecuatorianas** – Diagnóstico automático + Hoja de Ruta personalizada usando Random Forest + ISM

## Descripción del Problema
Las PyMEs ecuatorianas enfrentan dificultades para evaluar su **nivel de madurez en Industria 4.0** (Tecnología, Producto y Cliente) y definir un roadmap claro y accionable.

## Solución Propuesta
Pipeline completo que combina:
- **Random Forest Classifier** (3 modelos): Predice el nivel de madurez (1-Inicial, 2-Moderado, 3-Medio, 4-Avanzado) a partir de 13 preguntas del cuestionario.
- **Interpretive Structural Modeling (ISM)**: Genera una **hoja de ruta jerárquica personalizada** con variables driver y niveles prioritarios.

El sistema entrega diagnóstico preciso y recomendaciones estratégicas en segundos.

## Características Principales
- Predicción automática en las 3 dimensiones + nivel ponderado
- Hoja de ruta ISM con niveles y variables driver priorizadas
- Código modular y reproducible
- Validación robusta (Macro F1 entre 0.71 y 0.84 según dimensión)

## Estructura del Proyecto
├── main.py                     # Script principal (recomendado)
├── rf_madurez.py               # Módulo de predicción Random Forest
├── requirements.txt
├── data/                       # Archivos de ejemplo
├── models/                     # ← Descargar modelo aquí
├── outputs/                    # Resultados generados
├── notebooks/                  # Notebooks de desarrollo
└── REFLEXION.md

## Requisitos
- Python 3.9 o superior

## Instalación

```bash
git clone https://github.com/pablonovillo/evaluador-madurez-industria-4.0.git
cd evaluador-madurez-industria-4.0
pip install -r requirements.txt
