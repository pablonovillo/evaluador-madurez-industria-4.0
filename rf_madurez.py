import numpy as np
import joblib
import os

def rf_predict(answers_dict):
    """
    Predice los niveles de madurez usando los 3 modelos Random Forest.
    answers_dict: diccionario con claves como 'A.1.1', 'B.1.1', etc. y valores 1-4.
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

    # Construir vector de features (default 1 si falta alguna respuesta)
    features = []
    for feat in feature_order:
        # Buscar la clave original (A.1.1, etc.)
        original_key = next((k for k, v in mapping.items() if v == feat), None)
        value = answers_dict.get(original_key, 1)
        features.append(value)

    X_input = np.array(features).reshape(1, -1)

    # Ruta robusta al modelo (busca en carpeta 'models' relativa al proyecto)
    model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models', 'rf_madurez_models.joblib')

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"❌ Modelo no encontrado en: {model_path}\n"
                                "Descarga rf_madurez_models.joblib desde Google Drive y colócalo en la carpeta 'models/'")

    models = joblib.load(model_path)

    level_map = {1: "Inicial", 2: "Moderado", 3: "Medio", 4: "Avanzado"}

    return {
        'Tecnologia': (int(models['dim1_nivel'].predict(X_input)[0]), level_map[int(models['dim1_nivel'].predict(X_input)[0])]),
        'Producto':   (int(models['dim2_nivel'].predict(X_input)[0]), level_map[int(models['dim2_nivel'].predict(X_input)[0])]),
        'Cliente':    (int(models['dim3_nivel'].predict(X_input)[0]), level_map[int(models['dim3_nivel'].predict(X_input)[0])])
    }


if __name__ == "__main__":
    # Prueba rápida
    print("✅ rf_madurez.py cargado correctamente")
    print("Ejemplo de uso:")
    print("from rf_madurez import rf_predict")