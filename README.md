# Evaluador de Madurez en Industria 4.0 con IA

**Trabajo de Titulación**  
**PyMEs Ecuatorianas** – Diagnóstico automático + Hoja de Ruta personalizada

## Descripción del Problema
Las PyMEs ecuatorianas enfrentan dificultades para evaluar su **nivel de madurez en Industria 4.0** (Tecnología, Producto y Cliente) y definir un roadmap claro y accionable.

## Solución Propuesta
Pipeline completo que integra tres componentes clave:

- **Random Forest Classifier** (4 modelos): Predice los niveles de madurez (1-Inicial, 2-Moderado, 3-Medio, 4-Avanzado) en las 3 dimensiones + **nivel final ponderado** a partir de 13 preguntas del cuestionario.
- **K-Means Clustering**: Agrupa las empresas según sus perfiles de madurez similares, permitiendo recomendaciones más focalizadas por segmento.
- **Interpretive Structural Modeling (ISM)**: Genera una **hoja de ruta jerárquica personalizada** con variables driver clave y niveles prioritarios.

El sistema entrega diagnóstico preciso, agrupación por clusters y recomendaciones estratégicas accionables en segundos.

## Características Principales
- Predicción automática en las 3 dimensiones + **Nivel Final ponderado**
- Agrupación de PyMEs mediante **Clustering (K-Means)**
- Hoja de ruta ISM con drivers clave y niveles priorizados
- Código modular, reproducible y listo para producción
- Validación robusta (Macro F1 entre 0.71 y 0.84 según dimensión)

## Pipeline del Sistema
1. Respuestas del cuestionario (13 preguntas)
2. Preprocesamiento
3. Predicción con modelos Random Forest (4 targets)
4. **Clustering K-Means** → Agrupación por perfil similar
5. **ISM + Level Partitioning** → Hoja de ruta jerárquica
6. Recomendaciones personalizadas por empresa y por cluster

## Instalación

```bash
git clone https://github.com/pablonovillo/evaluador-madurez-industria-4.0.git
cd evaluador-madurez-industria-4.0
pip install -r requirements.txt
```
Paso Obligatorio: Descargar el Modelo Entrenado
El archivo rf_madurez_models.joblib (~16 MB) no está en GitHub por su tamaño.
Descargar rf_madurez_models.joblib
Instrucciones:

Descarga el archivo desde el siguiente link:
https://drive.google.com/drive/u/0/folders/1Bz-CM9lRi5OeFUckIHhmgV1JqzeO1I5j
Crea la carpeta models/ en la raíz del proyecto (si no existe).
Coloca el archivo rf_madurez_models.joblibdentro de la carpeta models/.

Cómo Ejecutar el Prototipo
```bash
python main.py
```
Uso como módulo en Python
```bash
from rf_madurez import rf_predict

answers = {
    'A.1.1': 3, 'A.1.2': 2, 'A.1.3': 4, 'A.1.4': 3, 'A.2.1': 2, 'A.2.2': 3,
    'B.1.1': 1, 'B.1.2': 2, 'B.1.3': 1, 'B.1.4': 2,
    'C.1.1': 2, 'C.1.2': 3, 'C.1.3': 2
}

resultado = rf_predict(answers)
print(resultado)
```
Estructura del Proyecto
├── main.py                     # Script principal interactivo

├── rf_madurez.py               # Predicción con Random Forest (4 modelos)

├── requirements.txt

├── models/                     ← (descargar modelo aquí)

├── data/                       # Archivos de ejemplo

├── outputs/                    # Resultados generados

├── notebooks/

│   ├── Classifier_v2_2_ONLY_CLASSIFIER.ipynb   # Entrenamiento y métricas

│   └── Recomendacion.ipynb                     # ISM + hoja de ruta

└── REFLEXION.md

Notebooks de Desarrollo

notebooks/Classifier_v2_2_ONLY_CLASSIFIER.ipynb → Entrenamiento Random Forest + métricas (incluye clustering)
notebooks/Recomendacion.ipynb → Hoja de ruta ISM completa

Métricas del Modelo

Macro F1 Dimensiones: entre 0.71 y 0.84
Ver notebook del clasificador para reportes detallados y análisis de clustering.

Autores:
José Toscano
Sylvia Novillo
Pablo Novillo 
