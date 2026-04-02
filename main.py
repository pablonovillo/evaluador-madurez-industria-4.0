import os
import pandas as pd
from datetime import datetime
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

from rf_madurez import rf_predict
from ism_roadmap import generar_roadmaps_completos

print("=" * 95)
print("   EVALUADOR DE MADUREZ INDUSTRIA 4.0 PARA PyMEs ECUATORIANAS")
print("   Random Forest + ISM Roadmap")
print("=" * 95)


def main():
    print("\nOpciones disponibles:")
    print("1. Ingresar respuestas manualmente (13 preguntas)")
    print("2. Usar ejemplo de prueba")
    
    opcion = input("\nElige una opción (1 o 2): ").strip()

    if opcion == "1":
        answers = obtener_respuestas_manual()
        nombre = "PyME ingresada manualmente"
    else:
        answers = obtener_respuestas_ejemplo()
        nombre = "Ejemplo de prueba"

    print(f"\nAnalizando: **{nombre}**")
    print("🔄 Procesando diagnóstico completo...\n")

    # Predicción Random Forest
    resultado = rf_predict(answers)

    # Mostrar resultados
    print("\n" + "=" * 85)
    print("📊 RESULTADOS DE MADUREZ - RANDOM FOREST")
    print("=" * 85)
    for dim, (nivel_num, nivel_texto) in resultado.items():
        if dim == "Nivel_Final":
            print(f"NIVEL FINAL     → Nivel {nivel_num} | {nivel_texto}   ← Madurez general ponderada")
        else:
            print(f"{dim.upper():<15} → Nivel {nivel_num} | {nivel_texto}")
    print("=" * 85)

    # Hoja de Ruta ISM
    generar_roadmaps_completos()

    # Guardar resultado
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs("OUTPUTS", exist_ok=True)
    df_result = pd.DataFrame({
        "Dimensión": list(resultado.keys()),
        "Nivel": [v[0] for v in resultado.values()],
        "Descripción": [v[1] for v in resultado.values()]
    })
    csv_path = os.path.join("OUTPUTS", f"diagnostico_{timestamp}.csv")
    df_result.to_csv(csv_path, index=False, encoding='utf-8-sig')

    print(f"\n✅ Resultado guardado correctamente en: {csv_path}")
    print("   Carpeta OUTPUTS lista para la entrega.")


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
                val = int(input(f"  {code} - {desc}: "))
                if 1 <= val <= 4:
                    answers[code] = val
                    break
                print("  → Ingresa un número entre 1 y 4")
            except ValueError:
                print("  → Ingresa solo números")
    return answers


def obtener_respuestas_ejemplo():
    return {
        'A.1.1': 3, 'A.1.2': 2, 'A.1.3': 4, 'A.1.4': 3, 'A.2.1': 2, 'A.2.2': 3,
        'B.1.1': 1, 'B.1.2': 2, 'B.1.3': 1, 'B.1.4': 2,
        'C.1.1': 2, 'C.1.2': 3, 'C.1.3': 2
    }


if __name__ == "__main__":
    main()
