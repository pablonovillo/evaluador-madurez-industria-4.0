# Reflexión Final - Trabajo de Titulación

**Evaluador de Madurez en Industria 4.0 con IA para PyMEs Ecuatorianas**

## 1. Logros alcanzados

El principal logro de este proyecto fue el desarrollo de un prototipo funcional que integra tres técnicas de inteligencia artificial de manera efectiva:

- **Random Forest Classifier**: Se entrenaron cuatro modelos supervisados que predicen con buena precisión los niveles de madurez en las dimensiones de Tecnología, Producto, Cliente y el **nivel final ponderado**. Las métricas obtenidas (Macro F1 entre 0.71 y 0.84) demuestran un rendimiento sólido considerando el tamaño y desbalance del dataset.
- **Clustering (K-Means)**: Se incorporó agrupación no supervisada para identificar perfiles similares de PyMEs, lo que permite entregar recomendaciones más focalizadas por segmento.
- **Interpretive Structural Modeling (ISM)**: Se implementó el modelado estructural para generar hojas de ruta jerárquicas personalizadas, identificando variables "driver" clave y niveles prioritarios de intervención.

El sistema es capaz de entregar un diagnóstico completo y accionable en pocos segundos a partir de solo 13 preguntas, cumpliendo con el objetivo principal del proyecto.

## 2. Uso de retroalimentación recibida

Durante el desarrollo se recibieron varias retroalimentaciones importantes que fueron incorporadas:

- Se mejoró la modularidad del código, separando la lógica de predicción en `rf_madurez.py` y creando un `main.py` interactivo fácil de usar.
- Se añadió la predicción del **nivel final ponderado**, tal como se solicitó.
- Se fortaleció la documentación técnica (README.md) con instrucciones claras de instalación, descarga del modelo y ejecución.
- Se implementó manejo de errores robusto (especialmente para la carga del modelo) y se mejoró la presentación de resultados.
- Se estructuró el repositorio de forma profesional (carpetas models, data, outputs, notebooks), facilitando la reproducibilidad.

## 3. Limitaciones identificadas

A pesar de los buenos resultados, el prototipo presenta algunas limitaciones:

- El dataset utilizado (276 respuestas) es relativamente pequeño y presenta desbalance de clases, especialmente en los niveles "Avanzado" e "Inicial".
- La integración completa de **Clustering** y **ISM** aún se encuentra principalmente en los notebooks. No está totalmente automatizada dentro del `main.py`.
- No se incluyó una interfaz gráfica (web o desktop), por lo que la interacción actual es solo por consola.
- El modelo depende de un archivo `.joblib` grande, lo que complica el despliegue en algunos entornos.
- Falta validación cruzada más exhaustiva y prueba con nuevas empresas externas al dataset original.

## 4. Mejoras futuras

Para llevar este prototipo a un nivel de producto real, se proponen las siguientes mejoras:

- Desarrollar una **interfaz web** (con Streamlit o Gradio) para facilitar su uso por parte de las PyMEs.
- Integrar completamente el **Clustering** y el **ISM** dentro del flujo principal (`main.py`), generando automáticamente la hoja de ruta recomendada.
- Ampliar y balancear el dataset recolectando más respuestas de PyMEs ecuatorianas.
- Implementar un sistema de **explicabilidad** (SHAP o LIME) para que las empresas entiendan por qué se asignó determinado nivel.
- Crear una versión deployable en la nube (Heroku, Render o AWS) con almacenamiento del modelo en la nube.
- Incluir la posibilidad de generar reportes en PDF con la hoja de ruta y recomendaciones personalizadas.

## 5. Conclusión y aprendizaje

Este proyecto me permitió aplicar de forma integrada técnicas de aprendizaje supervisado, no supervisado y modelado estructural, combinando aspectos técnicos con un problema real del sector productivo ecuatoriano.

Aprendí la importancia de la modularidad, la documentación clara y la reproducibilidad en proyectos de IA, así como la necesidad de equilibrar complejidad técnica con usabilidad para el usuario final.

Estoy satisfecho con el resultado obtenido y motivado para continuar desarrollando esta herramienta, con el objetivo de que pueda ser utilizada por asociaciones empresariales o cámaras de comercio para apoyar la transformación digital de las PyMEs en Ecuador.

**Fecha:** Abril 2026  
**Autores:** 
José Toscano
Sylvia Novillo
Pablo Novillo
