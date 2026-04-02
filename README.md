# Evaluador de Madurez en Industria 4.0 con IA para PyMEs Ecuatorianas

**Prototipo final - Trabajo de Titulación**

## Descripción del Problema y Solución

Las PyMEs ecuatorianas enfrentan dificultades para evaluar su nivel de madurez en **Industria 4.0** (dimensiones: Tecnología, Producto y Cliente) y definir un roadmap accionable.

**Solución:**  
Un pipeline de IA que combina:
- **Random Forest Classifier** → Predice niveles de madurez (Inicial / Moderado / Medio / Avanzado) a partir de 13 preguntas.
- **Interpretive Structural Modeling (ISM)** → Genera hoja de ruta jerárquica personalizada con drivers prioritarios.
- **Recomendaciones focalizadas** por dimensión y nivel.

El sistema entrega **diagnóstico + roadmap** en segundos.

## Características principales
- Predicción en 3 dimensiones + nivel final ponderado
- Hoja de ruta ISM con variables driver
- Recomendaciones accionables
- Métricas de validación: Macro F1 entre 0.71 y 0.84 (según dimensión)

## Pipeline del Sistema
1. Respuestas del cuestionario (13 preguntas Likert 1-4)
2. Preprocesamiento y vector de características
3. Predicción con 3 modelos Random Forest + nivel final
4. Generación de hoja de ruta ISM + recomendaciones

## Requisitos técnicos
- Python 3.9+
- Ver `requirements.txt`

pip install -r requirements.txt

## Instalación y Ejecución

1. Clona o descarga el repositorio (o accede a la carpeta en Google Drive).
2. Instala las dependencias:
pip install -r requirements.txt
3. Ejecuta el prototipo:
python main.py

##Estructura del proyecto

main.py → Script principal

rf_madurez.py → Módulo de predicción

MODELS/ → Modelos entrenados (.joblib)

NOTEBOOKS/ → Notebooks de desarrollo y validación

DATA/ → Datasets

OUTPUTS/ → Resultados y capturas


##Uso de ejemplo
```bash
from rf_madurez import rf_predict

answers = {
    'A.1.1': 3, 'A.1.2': 2, ...,  # tus 13 respuestas
}

resultado = rf_predict(answers)
print(resultado)
```
## Validación del modelo

Modelos entrenados con RandomForest (n_estimators=500, balanced)
Métricas detalladas en notebooks/Classifier_v2_2_ONLY_CLASSIFIER.ipynb
Evidencias de pruebas en carpeta outputs/

Autores:
José Toscano
Sylvia Novillo
Pablo Novillo
