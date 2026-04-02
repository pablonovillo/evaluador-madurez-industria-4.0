import os
import sys
import pandas as pd
import numpy as np
from datetime import datetime

# ====================== CONFIGURACIÓN DE RUTAS ======================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "models")

# ====================== IMPORTAR PREDICTOR ======================
try:
    from rf_madurez import rf_predict
    print("✅ Módulo rf_madurez.py cargado correctamente")
except ImportError as e:
    print("❌ No se pudo importar rf_madurez.py")
    print(f"   Error: {e}")
    sys.exit(1)

print("=" * 90)
print("   EVALUADOR DE MADUREZ EN INDUSTRIA 4.0 - PyMEs ECUATORIANAS")
print("=" * 90)
print("   Random Forest + ISM → Diagnóstico + Hoja de Ruta Personalizada\n")


def main():
    print("¿Cómo deseas ingresar las respuestas del cuestionario?")
    print("1. Manualmente (13 preguntas)")
    print("2. Desde archivo CSV (data/ejemplo_respuestas.csv)")
    
    opcion = input("\nElige una opción (1 o 2): ").strip()

    if opcion == "1":
        answers = obtener_respuestas_manual()
    elif opcion == "2":
        answers = obtener_respuestas_csv()
    else:
        print("⚠️ Opción inválida → Se usará modo manual por defecto.")
        answers = obtener_respuestas_manual()

    print("\n🔄 Procesando diagnóstico completo con IA...\n")

    try:
        # 1. Predicción con Random Forest (3 dimensiones + Nivel_Final)
        resultado_rf = rf_predict(answers)

        # 2. Preparar features para posible clustering futuro
        feature_order = [
            'A.1.1','A.1.2','A.1.3','A.1.4','A.2.1','A.2.2',
            'B.1.1','B.1.2','B.1.3','B.1.4',
            'C.1.1','C.1.2','C.1.3'
        ]
        features = [answers.get(k, 1) for k in feature_order]
        X_input = np.array(features).reshape(1, -1)

        # Mostrar resultados
        print("\n" + "=" * 80)
        print("📊 RESULTADOS DE MADUREZ")
        print("=" * 80)

        for dim, (nivel_num, nivel_texto) in resultado_rf.items():
            if dim == "Nivel_Final":
                print(f"{'NIVEL FINAL':<18} → Nivel {nivel_num} | {nivel_texto}  ← Madurez general ponderada")
            else:
                print(f"{dim.upper():<18} → Nivel {nivel_num} | {nivel_texto}")

        print("=" * 80)

        # 3. Hoja de ruta simplificada (basada en niveles)
        print("\n📋 HOJA DE RUTA PRIORITARIA (Recomendaciones)")
        print("-" * 80)
        print("Consejo: Enfócate primero en completar el **Nivel actual** de cada dimensión.\n")

        for dim, (nivel_num, _) in resultado_rf.items():
            if dim == "Nivel_Final":
                continue
            print(f"→ {dim.upper():<12} (Nivel actual: {nivel_num})")
            siguiente = min(nivel_num + 1, 4)
            print(f"   Recomendación: Avanzar hacia el **Nivel {siguiente}**")
            print("   Drivers clave: Ver variables base en el notebook de ISM (Recomendacion.ipynb)\n")

        # 4. Guardar resultado
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = os.path.join(BASE_DIR, "outputs")
        os.makedirs(output_dir, exist_ok=True)

        df_result = pd.DataFrame({
            "Dimensión": list(resultado_rf.keys()),
            "Nivel": [v[0] for v in resultado_rf.values()],
            "Descripción": [v[1] for v in resultado_rf.values()]
        })

        csv_path = os.path.join(output_dir, f"diagnostico_{timestamp}.csv")
        df_result.to_csv(csv_path, index=False, encoding='utf-8')

        print(f"✅ Diagnóstico guardado correctamente:")
        print(f"   → {csv_path}")

    except FileNotFoundError as e:
        print(f"\n❌ Error: Modelo no encontrado → {e}")
        print("   → Verifica que 'rf_madurez_models.joblib' esté en la carpeta 'models/'")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()


def obtener_respuestas_manual():
    print("\nIngresa las respuestas (valor del 1 al 4):\n")
    questions = {
        'A.1.1': 'Tecnología - Procesamiento de datos Q1',
        'A.1.2': 'Tecnología - Procesamiento de datos Q2',
        'A.1.3': 'Tecnología - Procesamiento de datos Q3',
        'A.1.4': 'Tecnología - Procesamiento de datos Q4',
        'A.2.1': 'Tecnología - Interconexión Q5',
        'A.2.2': 'Tecnología - Interconexión Q6',
        'B.1.1': 'Producto - Sensores y actuadores Q1',
        'B.1.2': 'Producto - Sensores y actuadores Q2',
        'B.1.3': 'Producto - Sensores y actuadores Q3',
        'B.1.4': 'Producto - Sensores y actuadores Q4',
        'C.1.1': 'Cliente - Servicios IT Q1',
        'C.1.2': 'Cliente - Servicios IT Q2',
        'C.1.3': 'Cliente - Servicios IT Q3'
    }

    answers = {}
    for code, desc in questions.items():
        while True:
            try:
                val = int(input(f"   {code} → {desc}: "))
                if 1 <= val <= 4:
                    answers[code] = val
                    break
                else:
                    print("   → Por favor ingresa un número entre 1 y 4")
            except ValueError:
                print("   → Ingresa solo números")
    return answers


def obtener_respuestas_csv():
    ruta = os.path.join(BASE_DIR, "data", "ejemplo_respuestas.csv")
    os.makedirs(os.path.dirname(ruta), exist_ok=True)

    if not os.path.exists(ruta):
        ejemplo = pd.DataFrame([{
            'A.1.1':3,'A.1.2':2,'A.1.3':4,'A.1.4':3,'A.2.1':2,'A.2.2':3,
            'B.1.1':1,'B.1.2':2,'B.1.3':1,'B.1.4':2,
            'C.1.1':2,'C.1.2':3,'C.1.3':2
        }])
        ejemplo.to_csv(ruta, index=False)
        print(f"📄 Archivo de ejemplo creado en: {ruta}")

    df = pd.read_csv(ruta)
    answers = df.iloc[0].to_dict()
    print(f"✅ Respuestas cargadas desde archivo CSV")
    return answers


if __name__ == "__main__":
    main()
