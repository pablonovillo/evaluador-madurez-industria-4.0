import os
import sys
import pandas as pd
from datetime import datetime

# ====================== IMPORTAR PREDICTOR ======================
try:
    from rf_madurez import rf_predict
    print("✅ Módulo rf_madurez.py cargado correctamente")
except ImportError as e:
    print(f"❌ Error al importar rf_madurez.py: {e}")
    sys.exit(1)

print("=" * 85)
print("   EVALUADOR DE MADUREZ INDUSTRIA 4.0 - PyMEs ECUATORIANAS")
print("=" * 85)
print("   Random Forest → Diagnóstico + Nivel Final\n")


def main():
    print("¿Cómo deseas ingresar las respuestas?")
    print("1. Manualmente (13 preguntas)")
    print("2. Usar ejemplo predefinido")
    
    opcion = input("\nElige una opción (1 o 2): ").strip()

    if opcion == "1":
        answers = obtener_respuestas_manual()
    else:
        answers = obtener_respuestas_ejemplo()

    print("\n🔄 Procesando diagnóstico con IA...\n")

    try:
        resultado = rf_predict(answers)

        print("\n" + "=" * 80)
        print("📊 RESULTADOS DE MADUREZ")
        print("=" * 80)

        for dim, (nivel_num, nivel_texto) in resultado.items():
            if dim == "Nivel_Final":
                print(f"{'NIVEL FINAL':<15} → Nivel {nivel_num} | {nivel_texto}  ← Madurez general")
            else:
                print(f"{dim.upper():<15} → Nivel {nivel_num} | {nivel_texto}")

        print("=" * 80)

        # Hoja de ruta simplificada
        print("\n📋 RECOMENDACIONES PRIORITARIAS")
        print("-" * 60)
        print("Enfócate primero en completar el nivel actual de cada dimensión.\n")

        for dim, (nivel_num, _) in resultado.items():
            if dim == "Nivel_Final":
                continue
            siguiente = min(nivel_num + 1, 4)
            print(f"→ {dim.upper():<12} (Nivel actual: {nivel_num})")
            print(f"   Recomendación: Avanzar hacia el Nivel {siguiente}")
            print()

        # Guardar resultado
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = "OUTPUTS"
        os.makedirs(output_dir, exist_ok=True)

        df_result = pd.DataFrame({
            "Dimensión": list(resultado.keys()),
            "Nivel": [v[0] for v in resultado.values()],
            "Descripción": [v[1] for v in resultado.values()]
        })

        csv_path = os.path.join(output_dir, f"diagnostico_{timestamp}.csv")
        df_result.to_csv(csv_path, index=False, encoding='utf-8-sig')

        print(f"✅ Resultado guardado en: {csv_path}")

    except Exception as e:
        print(f"❌ Error durante la ejecución: {e}")


def obtener_respuestas_manual():
    print("\nIngresa las respuestas (1 a 4):\n")
    questions = {
        'A.1.1': 'Tecnología Q1', 'A.1.2': 'Tecnología Q2', 'A.1.3': 'Tecnología Q3',
        'A.1.4': 'Tecnología Q4', 'A.2.1': 'Tecnología Q5', 'A.2.2': 'Tecnología Q6',
        'B.1.1': 'Producto Q1', 'B.1.2': 'Producto Q2', 'B.1.3': 'Producto Q3',
        'B.1.4': 'Producto Q4',
        'C.1.1': 'Cliente Q1', 'C.1.2': 'Cliente Q2', 'C.1.3': 'Cliente Q3'
    }
    answers = {}
    for code, desc in questions.items():
        while True:
            try:
                val = int(input(f"  {code} ({desc}): "))
                if 1 <= val <= 4:
                    answers[code] = val
                    break
                print("  → Ingresa un número entre 1 y 4")
            except:
                print("  → Ingresa solo números")
    return answers


def obtener_respuestas_ejemplo():
    print("Usando ejemplo predefinido...")
    return {
        'A.1.1': 3, 'A.1.2': 2, 'A.1.3': 4, 'A.1.4': 3, 'A.2.1': 2, 'A.2.2': 3,
        'B.1.1': 1, 'B.1.2': 2, 'B.1.3': 1, 'B.1.4': 2,
        'C.1.1': 2, 'C.1.2': 3, 'C.1.3': 2
    }


if __name__ == "__main__":
    main()
