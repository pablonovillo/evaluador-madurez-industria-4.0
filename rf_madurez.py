import numpy as np
import joblib
import os

def rf_predict(answers_dict):
    """
    Predice los niveles de madurez usando los 4 modelos Random Forest.
    Devuelve las 3 dimensiones + el nivel final ponderado.
    
    answers_dict: diccionario con claves 'A.1.1', 'B.1.1', etc. y valores del 1 al 4.
    """
    mapping = {
        'A.1.1': 'Puntaje_Dim1_Q1', 'A.1.2': 'Puntaje_Dim1_Q2', 'A.1.3': 'Puntaje_Dim1_Q3',
        'A.1.4': 'Puntaje_Dim1_Q4', 'A.2.1': 'Puntaje_Dim1_Q5', 'A.2.2': 'Puntaje_Dim1_Q6',
        'B.1.1': 'Puntaje_Dim2_Q1', 'B.1.2': 'Puntaje_Dim2_Q2', 'B.1.3': 'Puntaje_Dim2_Q3',
        'B.1.4': 'Puntaje_Dim2_Q4',
        'C.1.1': 'Puntaje_Dim3_Q1', 'C.1.2': 'Puntaje_Dim3_Q2', 'C.1.3': 'Puntaje_Dim3_Q3'
    }

    feature_order = [
        'Puntaje_Dim1_Q1', 'Puntaje_Dim1_Q2', 'Puntaje_Dim1_Q3', 'Puntaje_Dim1_Q4',
        'Puntaje_Dim1_Q5', 'Puntaje_Dim1_Q6',
        'Puntaje_Dim2_Q1', 'Puntaje_Dim2_Q2', 'Puntaje_Dim2_Q3', 'Puntaje_Dim2_Q4',
        'Puntaje_Dim3_Q1', 'Puntaje_Dim3_Q2', 'Puntaje_Dim3_Q3'
    ]

    # Construir vector de características (default 1 si falta alguna respuesta)
    features = []
    for feat in feature_order:
        original_key = next((k for k, v in mapping.items() if v == feat), None)
        value = answers_dict.get(original_key, 1)
        features.append(value)

    X_input = np.array(features).reshape(1, -1)

    # Ruta robusta al modelo (funciona tanto en Google Drive como en local)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_path = os.path.join(base_dir, 'models', 'rf_madurez_models.joblib')

    if not os.path.exists(model_path):
        # Alternativa: buscar en la misma carpeta del script (útil en Colab/Drive)
        model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'rf_madurez_models.joblib')
        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"❌ Modelo no encontrado en:\n{model_path}\n\n"
                "→ Coloca 'rf_madurez_models.joblib' en la carpeta 'models/'"
            )

    models = joblib.load(model_path)

    level_map = {1: "Inicial", 2: "Moderado", 3: "Medio", 4: "Avanzado"}

    # Predicciones de los 4 modelos
    pred_dim1 = int(models['dim1_nivel'].predict(X_input)[0])
    pred_dim2 = int(models['dim2_nivel'].predict(X_input)[0])
    pred_dim3 = int(models['dim3_nivel'].predict(X_input)[0])
    pred_final = int(models['nivel_final'].predict(X_input)[0])

    return {
        'Tecnologia': (pred_dim1, level_map[pred_dim1]),
        'Producto':   (pred_dim2, level_map[pred_dim2]),
        'Cliente':    (pred_dim3, level_map[pred_dim3]),
        'Nivel_Final': (pred_final, level_map[pred_final])
    }


# ==================== PRUEBA RÁPIDA ====================
if __name__ == "__main__":
    print("✅ rf_madurez.py cargado correctamente (versión con Nivel_Final)\n")
    
    # Ejemplo de prueba
    ejemplo = {
        'A.1.1': 3, 'A.1.2': 2, 'A.1.3': 4, 'A.1.4': 3, 'A.2.1': 2, 'A.2.2': 3,
        'B.1.1': 1, 'B.1.2': 2, 'B.1.3': 1, 'B.1.4': 2,
        'C.1.1': 2, 'C.1.2': 3, 'C.1.3': 2
    }
    
    resultado = rf_predict(ejemplo)
    print("Resultado de prueba:")
    for key, (num, texto) in resultado.items():
        print(f"• {key:12}: Nivel {num} → {texto}")if __name__ == "__main__":
    print("✅ rf_madurez.py cargado correctamente (versión con Nivel_Final)")
    
    # Ejemplo de prueba
    ejemplo = {
        'A.1.1': 3, 'A.1.2': 2, 'A.1.3': 4, 'A.1.4': 3, 'A.2.1': 2, 'A.2.2': 3,
        'B.1.1': 1, 'B.1.2': 2, 'B.1.3': 1, 'B.1.4': 2,
        'C.1.1': 2, 'C.1.2': 3, 'C.1.3': 2
    }
    
    resultado = rf_predict(ejemplo)
    print("\nResultado de prueba:")
    for key, (num, texto) in resultado.items():
        print(f"• {key:12}: Nivel {num} → {texto}")
