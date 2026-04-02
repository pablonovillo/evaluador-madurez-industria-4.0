import os
import pandas as pd
from datetime import datetime

# Importar módulos del proyecto
from rf_madurez import rf_predict
from ism_roadmap import generar_roadmaps_completos   # ← Nueva importación

print("=" * 95)
print("   EVALUADOR DE MADUREZ INDUSTRIA 4.0 + ISM ROADMAP")
print("=" * 95)


def main():
    print("\nOpciones disponibles:")
    print("1. Ingresar respuestas manualmente")
    print("2. Usar ejemplo de prueba")
    
    opcion = input("\nElige (1 o 2): ").strip()

    if opcion == "1":
        answers = obtener_respuestas_manual()
        nombre = "PyME ingresada manualmente"
    else:
        answers = obtener_respuestas_ejemplo()
        nombre = "Ejemplo de prueba"

    print(f"\nAnalizando: **{nombre}**")
    print("🔄 Procesando diagnóstico...\n")

    # 1. Predicción con Random Forest
    resultado = rf_predict(answers)

    # 2. Mostrar resultados RF
    print("\n" + "=" * 80)
    print("📊 RESULTADOS DE MADUREZ (Random Forest)")
    print("=" * 80)
    for dim, (nivel_num, nivel_texto) in resultado.items():
        if dim == "Nivel_Final":
            print(f"{'NIVEL FINAL':<18} → Nivel {nivel_num} | {nivel_texto}  ← Madurez general")
        else:
            print(f"{dim.upper():<18} → Nivel {nivel_num} | {nivel_texto}")
    print("=" * 80)

    # 3. Generar Hoja de Ruta ISM (lo más importante para recomendaciones)
    generar_roadmaps_completos()

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
    print(f"\n✅ Diagnóstico guardado en: {csv_path}")


def obtener_respuestas_manual():
    print("\nIngresa las respuestas (1-4):\n")
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
                print("  → Valor entre 1 y 4")
            except:
                print("  → Ingresa un número")
    return answers


def obtener_respuestas_ejemplo():
    return {
        'A.1.1': 3, 'A.1.2': 2, 'A.1.3': 4, 'A.1.4': 3, 'A.2.1': 2, 'A.2.2': 3,
        'B.1.1': 1, 'B.1.2': 2, 'B.1.3': 1, 'B.1.4': 2,
        'C.1.1': 2, 'C.1.2': 3, 'C.1.3': 2
    }


if __name__ == "__main__":
    main()
