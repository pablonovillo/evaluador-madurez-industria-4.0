import os
import sys
import pandas as pd
from datetime import datetime

# Importar el predictor actualizado
try:
    from rf_madurez import rf_predict
except ImportError:
    print("❌ No se encontró el archivo rf_madurez.py")
    print("   Asegúrate de que esté en la misma carpeta que main.py")
    sys.exit(1)

print("=" * 85)
print("   EVALUADOR DE MADUREZ EN INDUSTRIA 4.0 - PyMEs ECUATORIANAS")
print("=" * 85)
print("   Random Forest + ISM → Diagnóstico + Hoja de Ruta Personalizada\n")

def main():
    print("¿Cómo deseas ingresar las respuestas del cuestionario?")
    print("1. Manualmente (responder las 13 preguntas)")
    print("2. Desde archivo CSV (data/ejemplo_respuestas.csv)")
    opcion = input("\nElige una opción (1 o 2): ").strip()

    if opcion == "1":
        answers = obtener_respuestas_manual()
    elif opcion == "2":
        answers = obtener_respuestas_csv()
    else:
        print("Opción inválida. Se usará el modo manual.")
        answers = obtener_respuestas_manual()

    # Realizar predicción
    print("\n🔄 Realizando predicción con los modelos Random Forest...")
    try:
        resultado = rf_predict(answers)

        # Mostrar resultados
        print("\n" + "=" * 70)
        print("RESULTADOS DE MADUREZ INDUSTRIA 4.0")
        print("=" * 70)
        print(f"{'Dimensión':<12} {'Nivel':<8} {'Descripción'}")
        print("-" * 70)
        
        for dim, (nivel_num, nivel_texto) in resultado.items():
            if dim == "Nivel_Final":
                print(f"{'Nivel Final':<12} {nivel_num:<8} {nivel_texto} ← Madurez general ponderada")
            else:
                print(f"{dim:<12} {nivel_num:<8} {nivel_texto}")

        print("=" * 70)

        # Guardar resultado en outputs/
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = "outputs"
        os.makedirs(output_dir, exist_ok=True)

        df_result = pd.DataFrame({
            "Dimensión": list(resultado.keys()),
            "Nivel": [v[0] for v in resultado.values()],
            "Descripción": [v[1] for v in resultado.values()]
        })

        ruta_resultado = f"{output_dir}/madurez_resultado_{timestamp}.csv"
        df_result.to_csv(ruta_resultado, index=False)

        print(f"\n✅ Resultado guardado en: {ruta_resultado}")
        print("   Puedes abrir este archivo con Excel para revisarlo.")

    except FileNotFoundError as e:
        print(f"\n❌ {e}")
        print("\nSolución:")
        print("1. Descarga 'rf_madurez_models.joblib' desde Google Drive:")
        print("   → https://drive.google.com/drive/folders/1Bz-CM9lRi5OeFUckIHhmgV1JqzeO1I5j?usp=sharing")
        print("2. Crea la carpeta 'models/' en la raíz del proyecto (si no existe)")
        print("3. Coloca el archivo dentro de la carpeta 'models/'")
    except Exception as e:
        print(f"❌ Error inesperado durante la predicción: {e}")

    print("\n📋 Nota:")
    print("   La hoja de ruta completa con ISM (niveles prioritarios y drivers) se encuentra")
    print("   en el notebook: notebooks/Recomendacion.ipynb")


def obtener_respuestas_manual():
    print("\nIngresa las respuestas (valores del 1 al 4) para cada pregunta:\n")
    mapping = {
        'A.1.1': 'Tecnología Q1', 'A.1.2': 'Tecnología Q2', 'A.1.3': 'Tecnología Q3',
        'A.1.4': 'Tecnología Q4', 'A.2.1': 'Tecnología Q5', 'A.2.2': 'Tecnología Q6',
        'B.1.1': 'Producto Q1',   'B.1.2': 'Producto Q2',   'B.1.3': 'Producto Q3',
        'B.1.4': 'Producto Q4',
        'C.1.1': 'Cliente Q1',    'C.1.2': 'Cliente Q2',    'C.1.3': 'Cliente Q3'
    }
    
    answers = {}
    for codigo, descripcion in mapping.items():
        while True:
            try:
                valor = int(input(f"  {codigo} ({descripcion}): "))
                if 1 <= valor <= 4:
                    answers[codigo] = valor
                    break
                else:
                    print("     → Ingresa un número entre 1 y 4.")
            except ValueError:
                print("     → Ingresa un número válido (1-4).")
    return answers


def obtener_respuestas_csv():
    ruta = "data/ejemplo_respuestas.csv"
    if not os.path.exists(ruta):
        print(f"❌ No se encontró el archivo {ruta}. Creando ejemplo básico...")
        os.makedirs("data", exist_ok=True)
        ejemplo = pd.DataFrame([{
            'A.1.1':3, 'A.1.2':2, 'A.1.3':4, 'A.1.4':3, 'A.2.1':2, 'A.2.2':3,
            'B.1.1':1, 'B.1.2':2, 'B.1.3':1, 'B.1.4':2,
            'C.1.1':2, 'C.1.2':3, 'C.1.3':2
        }])
        ejemplo.to_csv(ruta, index=False)
        print(f"   Archivo de ejemplo creado en {ruta}")
    
    df = pd.read_csv(ruta)
    answers = df.iloc[0].to_dict()
    print(f"✅ Cargadas respuestas de ejemplo desde {ruta}")
    return answers


if __name__ == "__main__":
    main()
