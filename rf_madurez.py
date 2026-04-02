import numpy as np
import pandas as pd
import joblib
import os
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

def rf_predict(answers_dict):
    """
    Predice los niveles de madurez usando Random Forest.
    answers_dict: diccionario con las 13 respuestas (ej: {'A.1.1': 3, ...})
    """
    # Mapeo de preguntas a columnas del modelo
    mapping = {
        'A.1.1': 'Puntaje_Dim1_Q1', 'A.1.2': 'Puntaje_Dim1_Q2', 'A.1.3': 'Puntaje_Dim1_Q3',
        'A.1.4': 'Puntaje_Dim1_Q4', 'A.2.1': 'Puntaje_Dim1_Q5', 'A.2.2': 'Puntaje_Dim1_Q6',
        'B.1.1': 'Puntaje_Dim2_Q1', 'B.1.2': 'Puntaje_Dim2_Q2', 'B.1.3': 'Puntaje_Dim2_Q3',
        'B.1.4': 'Puntaje_Dim2_Q4',
        'C.1.1': 'Puntaje_Dim3_Q1', 'C.1.2': 'Puntaje_Dim3_Q2', 'C.1.3': 'Puntaje_Dim3_Q3'
    }

    feature_order = list(mapping.values())

    # Crear vector de características
    features = [answers_dict.get(key, 1) for key in mapping.keys()]
    
    # Convertir a DataFrame con nombres de columnas (evita warnings)
    X_input = pd.DataFrame([features], columns=feature_order)

    # Ruta del modelo (compatible con Google Drive)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(base_dir, 'MODELS', 'rf_madurez_models.joblib')

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"❌ Modelo no encontrado en: {model_path}\n"
                                f"   Asegúrate de que rf_madurez_models.joblib esté en la carpeta MODELS/")

    # Cargar modelos
    models = joblib.load(model_path)

    # Mapas de niveles
    level_map = {1: "Inicial", 2: "Moderado", 3: "Medio", 4: "Avanzado"}

    def get_level(pred):
        if isinstance(pred, str):
            return {"Inicial":1, "Moderado":2, "Medio":3, "Avanzado":4}.get(pred.strip(), 2)
        return int(pred)

    # Predicciones
    d1 = get_level(models['dim1_nivel'].predict(X_input)[0])   # Tecnología
    d2 = get_level(models['dim2_nivel'].predict(X_input)[0])   # Producto
    d3 = get_level(models['dim3_nivel'].predict(X_input)[0])   # Cliente

    # Nivel Final ponderado (ajustado a tus preferencias anteriores)
    final_num = round(0.4 * d1 + 0.35 * d2 + 0.25 * d3)
    final_num = max(1, min(4, final_num))

    return {
        'Tecnologia': (d1, level_map[d1]),
        'Producto':   (d2, level_map[d2]),
        'Cliente':    (d3, level_map[d3]),
        'Nivel_Final': (final_num, level_map[final_num])
    }


# ====================== PRUEBA RÁPIDA ======================
if __name__ == "__main__":
    print("✅ rf_madurez.py cargado correctamente \n")
    
    ejemplo = {
        'A.1.1':3, 'A.1.2':2, 'A.1.3':4, 'A.1.4':3, 'A.2.1':2, 'A.2.2':3,
        'B.1.1':1, 'B.1.2':2, 'B.1.3':1, 'B.1.4':2,
        'C.1.1':2, 'C.1.2':3, 'C.1.3':2
    }
    
    resultado = rf_predict(ejemplo)
    for k, (n, t) in resultado.items():
        print(f"• {k:12} → Nivel {n} | {t}")
