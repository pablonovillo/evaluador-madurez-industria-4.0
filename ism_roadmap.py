# ism_roadmap.py - Versión mejorada y limpia
import pandas as pd

dim_variables = {
    'Tecnologia': [
        ('A.1.1', 'No se realiza procesamiento de datos en el entorno de producción.'),
        ('A.1.2', 'Almacenamiento de datos con fines de documentación en el entorno de la producción.'),
        ('A.1.3', 'Análisis de datos para el monitoreo del entorno de producción.'),
        ('A.1.4', 'Evaluación automática de datos para la planificación y control de procesos.'),
        ('A.2.1', 'No existe interconexión del entorno de producción con otras áreas de negocio.'),
        ('A.2.2', 'Intercambio de información a través de correo o telecomunicaciones.'),
        ('A.2.3', 'Formatos de datos uniformes y reglas definidas para intercambio.'),
        ('A.2.4', 'Servidores de datos vinculados y soluciones de TI totalmente en red.'),
        ('A.3.1', 'No existe comunicación M2M en el entorno de producción.'),
        ('A.3.2', 'Existe interfaz de bus de campo en el entorno de producción.'),
        ('A.3.3', 'Interfaz Ethernet industrial en el entorno de producción.'),
        ('A.3.4', 'Las máquinas tienen acceso a Internet y servicios web (M2M).'),
        ('A.4.1', 'No existe intercambio de información H2M en el entorno de producción.'),
        ('A.4.2', 'Uso de interfaces locales de usuario en el entorno de producción.'),
        ('A.4.3', 'Monitoreo y control de la producción centralizado o descentralizado.'),
        ('A.4.4', 'Uso de interfaces móviles, realidad aumentada o virtual.'),
        ('A.5.1', 'Intercambio de información mediante correo o telecomunicaciones.'),
        ('A.5.2', 'Servidores centrales de datos en la producción.'),
        ('A.5.3', 'Portales basados en Internet para intercambio de datos.'),
        ('A.5.4', 'Intercambio automatizado de información con proveedores y clientes.'),
        ('A.6.1', 'Sistemas de producción rígidos y poca proporción de piezas idénticas.'),
        ('A.6.2', 'Uso de sistemas de producción flexibles.'),
        ('A.6.3', 'Sistemas flexibles y diseños modulares.'),
        ('A.6.4', 'Plan de producción impulsado por componentes modulares.')
    ],
    'Producto': [
        ('B.1.1', 'El producto no usa sensores y actuadores.'),
        ('B.1.2', 'El producto tiene sensores / actuadores integrados.'),
        ('B.1.3', 'Las lecturas de los sensores son procesadas por el producto.'),
        ('B.1.4', 'El producto adapta su comportamiento de forma autónoma.'),
        ('B.2.1', 'El producto no dispone de interfaces.'),
        ('B.2.2', 'El producto envía o recibe señales básicas de entrada/salida.'),
        ('B.2.3', 'El producto dispone de interfaces de bus de campo.'),
        ('B.2.4', 'El producto dispone de interfaces Ethernet e Internet.'),
        ('B.3.1', 'El producto no tiene funcionalidades de almacenamiento o intercambio.'),
        ('B.3.2', 'El producto permite identificación individual.'),
        ('B.3.3', 'El producto dispone de almacenamiento pasivo de datos.'),
        ('B.3.4', 'El producto cuenta con almacenamiento para intercambio autónomo.'),
        ('B.4.1', 'No existe monitoreo por parte del producto.'),
        ('B.4.2', 'El producto permite detección de fallas.'),
        ('B.4.3', 'El producto permite registro de condiciones operativas.'),
        ('B.4.4', 'El producto permite pronóstico y control adaptativo autónomo.')
    ],
    'Cliente': [
        ('C.1.1', 'No se ofrecen servicios de IT al cliente relacionados con el producto.'),
        ('C.1.2', 'Servicios disponibles a través de portales en línea.'),
        ('C.1.3', 'El cliente dispone de ejecución de servicios de IT directamente mediante el producto.'),
        ('C.1.4', 'Servicios de IT ejecutados de manera autónoma.'),
        ('C.2.1', 'Venta simple de productos estandarizados.'),
        ('C.2.2', 'Venta y consultoría asociada al producto.'),
        ('C.2.3', 'Venta, consultoría y adaptación a especificaciones del cliente.'),
        ('C.2.4', 'Venta adicional de servicios y funcionalidades.'),
        ('C.3.1', 'Diseño altamente estandarizado orientado a bajo precio.'),
        ('C.3.2', 'Diseño con partes que permiten moderada adaptación.'),
        ('C.3.3', 'Diseño con alto nivel de adaptación al cliente.'),
        ('C.3.4', 'Diseño depende completamente del requerimiento específico del cliente.')
    ]
}

def generar_roadmap(dim_name):
    print(f"\n📌 HOJA DE RUTA ISM - {dim_name.upper()}")

    # Niveles y drivers (basados en tu salida anterior)
    if dim_name == 'Tecnologia':
        levels = {1: ['A.1.1','A.2.1','A.3.1','A.4.1'], 2: ['A.5.1'], 3: ['A.1.2'], 
                  4: ['A.6.1'], 5: ['A.1.3','A.1.4','A.2.2','A.2.3','A.2.4','A.3.2','A.3.3','A.3.4','A.4.2','A.4.3','A.5.2','A.5.3','A.6.2','A.6.3'],
                  6: ['A.4.4','A.5.4'], 7: ['A.6.4']}
        drivers = ['A.1.1', 'A.2.1', 'A.3.1', 'A.4.1', 'A.5.1']

    elif dim_name == 'Producto':
        levels = {1: ['B.1.1'], 2: ['B.2.1','B.3.1'], 3: ['B.1.2'], 
                  4: ['B.1.3','B.1.4','B.2.2','B.2.3','B.2.4','B.3.2','B.3.3','B.3.4','B.4.1','B.4.2','B.4.3','B.4.4']}
        drivers = ['B.1.1', 'B.2.1', 'B.3.1']

    else:  # Cliente
        levels = {1: ['C.3.1','C.2.1','C.1.1'], 2: ['C.1.2','C.2.2','C.3.2'], 
                  3: ['C.1.3','C.2.3','C.3.3'], 4: ['C.1.4','C.2.4','C.3.4']}
        drivers = ['C.3.1', 'C.2.1', 'C.1.1']

    var_descriptors = dict(dim_variables[dim_name])

    print(f"   Drivers clave (implementar primero): {', '.join(drivers[:5])}")
    print("\n   Recomendación por niveles:")

    for lvl in sorted(levels.keys()):
        priority = "🔴 PRIORIDAD ALTA - DRIVERS" if lvl == 1 else \
                   "🟠 PRIORIDAD MEDIA" if lvl <= 3 else "🟢 PRIORIDAD BAJA"
        print(f"\n   NIVEL {lvl} → {priority}")
        for code in levels[lvl]:
            desc = var_descriptors.get(code, code)
            print(f"      • {code}: {desc[:95]}{'...' if len(desc)>95 else ''}")

    return {'levels': levels, 'drivers': drivers}


def generar_roadmaps_completos():
    print("\n" + "="*95)
    print("📋 HOJA DE RUTA ISM - RECOMENDACIONES ESTRATÉGICAS")
    print("="*95)
    for dim in ['Tecnologia', 'Producto', 'Cliente']:
        generar_roadmap(dim)
    print("\n" + "="*95)
    print("Consejo final: Enfócate primero en los **Drivers (Nivel 1)** y en subir tu **Nivel actual** según el Random Forest.")
    print("="*95)