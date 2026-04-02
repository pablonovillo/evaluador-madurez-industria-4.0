import os
import pandas as pd
from datetime import datetime

# ====================== IMPORTAR PREDICTOR ======================
try:
    from rf_madurez import rf_predict
    print("✅ Módulo rf_madurez.py cargado correctamente")
except ImportError as e:
    print(f"❌ Error al importar rf_madurez.py: {e}")
    exit(1)

print("=" * 90)
print("   EVALUADOR DE MADUREZ INDUSTRIA 4.0 - PyMEs ECUATORIANAS")
print("=" * 90)
print("   Random Forest + Nivel Final ponderado\n")


def main():
    print("Opciones disponibles:")
    print("1. Analizar una PyME desde Google Sheets")
    print("2. Ingresar respuestas manualmente")
    print("3. Usar ejemplo de prueba")
    
    opcion = input("\nElige una opción (1, 2 o 3): ").strip()

    if opcion == "1":
        answers, nombre_empresa = intentar_cargar_desde_sheets()
    elif opcion == "2":
        answers = obtener_respuestas_manual()
        nombre_empresa = "PyME ingresada manualmente"
    else:
        answers = obtener_respuestas_ejemplo()
        nombre_empresa = "Ejemplo de prueba"

    print(f"\nAnalizando: **{nombre_empresa}**")
    print("🔄 Procesando diagnóstico...\n")

    try:
        resultado = rf_predict(answers)

        print("\n" + "=" * 80)
        print("📊 RESULTADOS DE MADUREZ")
        print("=" * 80)

        for dim, (nivel_num, nivel_texto) in resultado.items():
            if dim == "Nivel_Final":
                print(f"{'NIVEL FINAL':<18} → Nivel {nivel_num} | {nivel_texto}   ← Madurez general ponderada")
            else:
                print(f"{dim.upper():<18} → Nivel {nivel_num} | {nivel_texto}")

        print("=" * 80)

        print("\n📋 RECOMENDACIONES PARA AVANZAR")
        print("-" * 70)
        for dim, (nivel_num, _) in resultado.items():
            if dim == "Nivel_Final":
                continue
            siguiente = min(nivel_num + 1, 4)
            print(f"→ {dim.upper():<12} (Nivel actual: {nivel_num}) → Subir a Nivel {siguiente}")

        # Guardar
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

    except Exception as e:
        print(f"❌ Error: {e}")


def intentar_cargar_desde_sheets():
    """Intenta cargar desde Google Sheets de forma segura"""
    try:
        from google.colab import auth
        import gspread
        from google.auth import default

        print("🔐 Autenticando con Google Sheets...")
        auth.authenticate_user()
        creds, _ = default()
        gc = gspread.authorize(creds)

        SHEET_ID = "1Pbq8S0XWGX3tor_QMDiKpJYoH6EfEZfweDD_P1Dlwmc"
        sheet = gc.open_by_key(SHEET_ID)
        ws = sheet.worksheet("Responses2")

        data = ws.get_all_values()
        df = pd.DataFrame(data[1:], columns=data[0])

        puntaje_cols = [col for col in df.columns if col.startswith('Puntaje_Dim')]
        for col in puntaje_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        print(f"✅ Cargados {len(df)} registros de PyMEs")

        # Mostrar lista
        print("\nPyMEs disponibles:")
        for i, row in df.iterrows():
            nombre = row.get('Nombre de la empresa', f"PyME {i+1}")
            print(f"{i+1:3d}. {nombre}")

        while True:
            try:
                num = int(input("\nIngresa el número de la PyME a analizar: "))
                if 1 <= num <= len(df):
                    idx = num - 1
                    nombre = df.iloc[idx].get('Nombre de la empresa', f"PyME {num}")
                    answers = obtener_respuestas_de_pyme(df, idx)
                    return answers, nombre
                else:
                    print("Número fuera de rango")
            except:
                print("Por favor ingresa un número válido")

    except Exception as e:
        print(f"⚠️ No se pudo acceder a Google Sheets: {e}")
        print("Volviendo a modo manual...\n")
        answers = obtener_respuestas_manual()
        return answers, "PyME ingresada manualmente"


def obtener_respuestas_de_pyme(df, idx):
    row = df.iloc[idx]
    mapping = {
        'Puntaje_Dim1_Q1': 'A.1.1', 'Puntaje_Dim1_Q2': 'A.1.2', 'Puntaje_Dim1_Q3': 'A.1.3',
        'Puntaje_Dim1_Q4': 'A.1.4', 'Puntaje_Dim1_Q5': 'A.2.1', 'Puntaje_Dim1_Q6': 'A.2.2',
        'Puntaje_Dim2_Q1': 'B.1.1', 'Puntaje_Dim2_Q2': 'B.1.2', 'Puntaje_Dim2_Q3': 'B.1.3',
        'Puntaje_Dim2_Q4': 'B.1.4',
        'Puntaje_Dim3_Q1': 'C.1.1', 'Puntaje_Dim3_Q2': 'C.1.2', 'Puntaje_Dim3_Q3': 'C.1.3'
    }
    answers = {}
    for sheet_col, key in mapping.items():
        if sheet_col in row and pd.notna(row[sheet_col]):
            answers[key] = int(row[sheet_col])
        else:
            answers[key] = 1
    return answers


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
