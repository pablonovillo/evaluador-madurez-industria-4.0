import numpy as np
import joblib
import os

def rf_predict(answers_dict):
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

    features = [answers_dict.get(next((k for k, v in mapping.items() if v == feat), None), 1) 
                for feat in feature_order]

    X_input = np.array(features).reshape(1, -1)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(base_dir, 'MODELS', 'rf_madurez_models.joblib')

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Modelo no encontrado en {model_path}")

    models = joblib.load(model_path)

    level_map = {1: "Inicial", 2: "Moderado", 3: "Medio", 4: "Avanzado"}
    text_map = {"Inicial":1, "Moderado":2, "Medio":3, "Avanzado":4}

    def get_level(pred):
        if isinstance(pred, str):
            return text_map.get(pred.strip(), 2)
        return int(pred)

    d1 = get_level(models['dim1_nivel'].predict(X_input)[0])
    d2 = get_level(models['dim2_nivel'].predict(X_input)[0])
    d3 = get_level(models['dim3_nivel'].predict(X_input)[0])

    final_num = round(d1*0.4 + d2*0.3 + d3*0.3)
    final_num = max(1, min(4, final_num))

    return {
        'Tecnologia': (d1, level_map[d1]),
        'Producto':   (d2, level_map[d2]),
        'Cliente':    (d3, level_map[d3]),
        'Nivel_Final': (final_num, level_map[final_num])
    }


if __name__ == "__main__":
    print("✅ rf_madurez.py cargado correctamente\n")
    ejemplo = {'A.1.1':3,'A.1.2':2,'A.1.3':4,'A.1.4':3,'A.2.1':2,'A.2.2':3,
               'B.1.1':1,'B.1.2':2,'B.1.3':1,'B.1.4':2,
               'C.1.1':2,'C.1.2':3,'C.1.3':2}
    resultado = rf_predict(ejemplo)
    for k, (n, t) in resultado.items():
        print(f"• {k:12}: Nivel {n} → {t}")
