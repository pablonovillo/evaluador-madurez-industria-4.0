import os
import sys
import pandas as pd
import numpy as np
from datetime import datetime
import joblib

# Importar el predictor
try:
    from rf_madurez import rf_predict
except ImportError:
    print("❌ No se encontró rf_madurez.py")
    sys.exit(1)

print("=" * 90)
print("   EVALUADOR DE MADUREZ INDUSTRIA 4.0 - PyMEs ECUATORIANAS")
print("=" * 90)
print("   Random Forest + Clustering + ISM → Diagnóstico + Hoja de Ruta\n")

# Cargar modelo de clustering (debe estar en models/)
try:
    clustering_model = joblib.load('models/kmeans_model.joblib')
    print("✅ Modelo de Clustering cargado correctamente")
except:
    clustering_model = None
    print("⚠️  Modelo de Clustering no encontrado. Se omitirá la agrupación por cluster.")

def main():
    print("¿Cómo deseas ingresar las respuestas?")
    print("1. Manualmente (13 preguntas)")
    print("2. Desde archivo CSV (data/ejemplo_respuestas.csv)")
    opcion = input("\nElige una opción (1 o 2): ").strip()

    if opcion == "1":
        answers = obtener_respuestas_manual()
    elif opcion == "2":
        answers = obtener_respuestas_csv()
    else:
        print("Opción inválida → Se usará modo manual.")
        answers = obtener_respuestas_manual()

    print("\n🔄 Procesando diagnóstico completo...")

    try:
        # 1. Predicción con Random Forest
        resultado_rf = rf_predict(answers)

        # 2. Preparar vector para clustering (usamos las mismas 13 features)
        features = [answers.get(k, 1) for k in [
            'A.1.1','A.1.2','A.1.3','A.1.4','A.2.1','A.2.2',
            'B.1.1','B.1.2','B.1.3','B.1.4',
            'C.1.1','C.1.2','C.1.3'
        ]]
        X_cluster = np.array(features).reshape(1, -1)

        # 3. Clustering (si el modelo existe)
        cluster = None
        if clustering_model is not None:
            cluster = int(clustering_model.predict(X_cluster)[0])
            print(f"✅ Empresa asignada al Cluster: {cluster}")

        # Mostrar resultados
        print("\n" + "=" * 75)
        print("RESULTADOS DE MADUREZ")
        print("=" * 75)
        for dim, (nivel_num, nivel_texto) in resultado_rf.items():
            if dim == "Nivel_Final":
                print(f"{'Nivel Final':<15} → Nivel {nivel_num} | {nivel_texto}  ← Madurez general ponderada")
            else:
                print(f"{dim:<15} → Nivel {nivel_num} | {nivel_texto}")

        if cluster is not None:
            print(f"{'Cluster':<15} → {cluster} (perfil similar de PyMEs)")

        print("=" * 75)

        # 4. Hoja de ruta simplificada ISM (basada en niveles)
        print("\n📋 HOJA DE RUTA PRIORITARIA (simplificada)")
        print("-" * 60)
        print("Enfócate primero en completar el **Nivel actual** de cada dimensión.")
        print("Las variables driver son las que más impacto tienen para avanzar.\n")

        for dim, (nivel_num, _) in resultado_rf.items():
            if dim == "Nivel_Final": 
                continue
            print(f"→ {dim.upper():<12} (Nivel actual: {nivel_num})")
            print(f"   Recomendación: Avanzar hacia el Nivel {nivel_num + 1 if nivel_num < 4 else 4}")
            print("   Drivers clave: Completar variables base de la dimensión (ver notebook ISM)")
            print()

        # Guardar resultado completo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = "outputs"
        os.makedirs(output_dir, exist_ok=True)

        df_result = pd.DataFrame({
            "Dimensión": list(resultado_rf.keys()),
            "Nivel": [v[0] for v in resultado_rf.values()],
            "Descripción": [v[1] for v in resultado_rf.values()]
        })

        if cluster is not None:
            df_result.loc[len(df_result)] = ["Cluster", cluster, f"Grupo {cluster}"]

        df_result.to_csv(f"{output_dir}/diagnostico_completo_{timestamp}.csv", index=False)

        print(f"✅ Resultado completo guardado en: {output_dir}/diagnostico_completo_{timestamp}.csv")

    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print("   → Asegúrate de descargar el modelo desde Google Drive y colocarlo en la carpeta 'models/'")
    except Exception as e:
        print(f"❌ Error durante el procesamiento: {e}")


def obtener_respuestas_manual():
    print("\nIngresa las respuestas (1 al 4):\n")
    questions = {
        'A.1.1': 'Tecnología Q1', 'A.1.2': 'Tecnología Q2', 'A.1.3': 'Tecnología Q3',
        'A.1.4': 'Tecnología Q4', 'A.2.1': 'Tecnología Q5', 'A.2.2': 'Tecnología Q6',
        'B.1.1': 'Producto Q1',   'B.1.2': 'Producto Q2',   'B.1.3': 'Producto Q3',
        'B.1.4': 'Producto Q4',
        'C.1.1': 'Cliente Q1',    'C.1.2': 'Cliente Q2',    'C.1.3': 'Cliente Q3'
    }
    
    answers = {}
    for code, desc in questions.items():
        while True:
            try:
                val = int(input(f"  {code} ({desc}): "))
                if 1 <= val <= 4:
                    answers[code] = val
                    break
                print("     → Valor entre 1 y 4")
            except:
                print("     → Ingresa un número")
    return answers


def obtener_respuestas_csv():
    ruta = "data/ejemplo_respuestas.csv"
    if not os.path.exists(ruta):
        os.makedirs("data", exist_ok=True)
        ejemplo = pd.DataFrame([{
            'A.1.1':3,'A.1.2':2,'A.1.3':4,'A.1.4':3,'A.2.1':2,'A.2.2':3,
            'B.1.1':1,'B.1.2':2,'B.1.3':1,'B.1.4':2,
            'C.1.1':2,'C.1.2':3,'C.1.3':2
        }])
        ejemplo.to_csv(ruta, index=False)
        print(f"Archivo de ejemplo creado: {ruta}")
    
    df = pd.read_csv(ruta)
    answers = df.iloc[0].to_dict()
    print(f"✅ Respuestas de ejemplo cargadas desde {ruta}")
    return answers


if __name__ == "__main__":
    main()
