# ism_roadmap.py - Versión con Gráficos ISM Reales

import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.backends.backend_pdf import PdfPages
import os
import warnings
warnings.filterwarnings('ignore')
# Configuración para Colab
import matplotlib.pyplot as plt




# ==================== DESCRIPTORES ====================
dim_variables = {
    'Tecnologia': [
        ('A.1.1', 'No se realiza procesamiento de datos en el entorno de producción.'),
        ('A.1.2', 'Almacenamiento de datos con fines de documentación.'),
        ('A.1.3', 'Análisis de datos para el monitoreo.'),
        ('A.1.4', 'Evaluación automática de datos para planificación.'),
        ('A.2.1', 'No existe interconexión con otras áreas.'),
        ('A.2.2', 'Intercambio vía correo/telecomunicaciones.'),
        ('A.2.3', 'Formatos de datos uniformes y reglas definidas.'),
        ('A.2.4', 'Servidores vinculados y TI en red.'),
        ('A.3.1', 'No existe comunicación M2M.'),
        ('A.3.2', 'Interfaz de bus de campo.'),
        ('A.3.3', 'Interfaz Ethernet industrial.'),
        ('A.3.4', 'Máquinas con acceso a Internet y servicios web.'),
        ('A.4.1', 'No existe intercambio H2M.'),
        ('A.4.2', 'Interfaces locales de usuario.'),
        ('A.4.3', 'Monitoreo y control centralizado/descentralizado.'),
        ('A.4.4', 'Interfaces móviles, RA/RV.'),
        ('A.5.1', 'Intercambio mediante correo o telecomunicaciones.'),
        ('A.5.2', 'Servidores centrales de datos.'),
        ('A.5.3', 'Portales basados en Internet.'),
        ('A.5.4', 'Intercambio automatizado con proveedores y clientes.'),
        ('A.6.1', 'Sistemas de producción rígidos.'),
        ('A.6.2', 'Sistemas de producción flexibles.'),
        ('A.6.3', 'Diseños modulares.'),
        ('A.6.4', 'Producción impulsada por componentes modulares.')
    ],
    'Producto': [
        ('B.1.1', 'El producto no usa sensores y actuadores.'),
        ('B.1.2', 'Sensores / actuadores integrados.'),
        ('B.1.3', 'Lecturas procesadas por el producto.'),
        ('B.1.4', 'Adaptación autónoma según datos.'),
        ('B.2.1', 'Sin interfaces.'),
        ('B.2.2', 'Señales básicas I/O.'),
        ('B.2.3', 'Interfaces de bus de campo.'),
        ('B.2.4', 'Interfaces Ethernet e Internet.'),
        ('B.3.1', 'Sin almacenamiento o intercambio.'),
        ('B.3.2', 'Identificación individual.'),
        ('B.3.3', 'Almacenamiento pasivo.'),
        ('B.3.4', 'Almacenamiento para intercambio autónomo.'),
        ('B.4.1', 'Sin monitoreo.'),
        ('B.4.2', 'Detección de fallas.'),
        ('B.4.3', 'Registro de condiciones operativas.'),
        ('B.4.4', 'Pronóstico y control adaptativo autónomo.')
    ],
    'Cliente': [
        ('C.1.1', 'Sin servicios de IT al cliente.'),
        ('C.1.2', 'Servicios vía portales en línea.'),
        ('C.1.3', 'Ejecución de servicios directamente en el producto.'),
        ('C.1.4', 'Servicios autónomos e integración completa.'),
        ('C.2.1', 'Venta simple de productos estandarizados.'),
        ('C.2.2', 'Venta + consultoría.'),
        ('C.2.3', 'Adaptación a especificaciones del cliente.'),
        ('C.2.4', 'Venta adicional de servicios.'),
        ('C.3.1', 'Diseño altamente estandarizado.'),
        ('C.3.2', 'Moderada adaptación.'),
        ('C.3.3', 'Alto nivel de adaptación.'),
        ('C.3.4', 'Diseño según requerimiento específico.')
    ]
}

# ==================== GENERAR ROADMAPS ISM COMPLETOS (con SSIM real) ====================
print("🔄 Calculando niveles ISM y matrices SSIM... (esto puede tardar 5-10 segundos)")

def crear_ssim(dim_name):
    codes = [v[0] for v in dim_variables[dim_name]]
    n = len(codes)


    if dim_name == 'Tecnologia':
        triangular = [
            ['V','V','V','O','V','V','V','V','V','V','V','X','V','V','V','X','V','V','V','X','V','V','V'],  # A.1.1
            ['V','V','V','V','V','V','V','A','V','V','V','A','V','V','V','A','V','V','V','A','V','V'],      # A.1.2
            ['V','V','V','A','V','X','A','A','V','V','A','A','V','A','A','A','V','A','A','A','V'],        # A.1.3
            ['V','A','O','A','V','A','A','A','V','A','A','A','A','A','A','O','V','V','A','A'],            # A.1.4
            ['O','O','O','O','V','V','V','V','V','V','V','X','V','V','V','X','V','V','V'],                # A.2.1
            ['V','V','V','A','V','V','A','A','V','A','A','A','V','V','X','A','V','V'],                   # A.2.2
            ['V','V','A','O','V','V','A','A','V','V','A','A','V','X','A','A','V'],                       # A.2.3
            ['V','V','A','O','V','A','A','A','V','A','A','A','A','A','A','A'],                           # A.2.4
            ['O','O','O','O','V','V','V','V','V','V','V','X','V','V','V'],                               # A.3.1
            ['V','V','V','A','V','V','V','A','V','V','X','A','V','V'],                                   # A.3.2
            ['V','V','A','O','V','V','V','A','V','V','A','A','V'],                                       # A.3.3
            ['V','V','A','O','V','A','A','A','V','X','A','A'],                                           # A.3.4
            ['V','V','V','O','V','V','V','O','V','V','V'],                                               # A.4.1
            ['V','V','V','O','V','V','X','A','V','V'],                                                   # A.4.2
            ['V','V','A','O','V','V','A','A','V'],                                                       # A.4.3
            ['O','O','O','O','X','A','A','A'],                                                           # A.4.4
            ['V','V','V','O','V','V','V'],                                                               # A.5.1
            ['V','V','V','O','V','V'],                                                                   # A.5.2
            ['V','O','O','O','V'],                                                                       # A.5.3
            ['V','A','O','O'],                                                                           # A.5.4
            ['V','V','V'],                                                                               # A.6.1
            ['V','V'],                                                                                   # A.6.2
            ['V'],                                                                                       # A.6.3
            []                                                                                           # A.6.4
        ]
    elif dim_name == 'Producto':

        triangular = [
            ['V','V','V','V','V','V','V','V','V','V','V','V','V','V','V'],   # B.1.1
            ['V','V','V','O','V','V','V','A','V','V','V','A','V','V'],       # B.1.2
            ['V','V','V','A','V','V','A','A','V','A','A','A','V'],           # B.1.3
            ['X','A','A','A','A','A','A','A','O','A','A','A'],               # B.1.4
            ['V','V','V','V','V','V','V','X','V','V','V'],                   # B.2.1
            ['V','V','V','O','V','V','V','A','V','V'],                       # B.2.2
            ['V','V','V','O','V','V','V','O','V'],                           # B.2.3
            ['V','A','A','O','X','A','A','O'],                               # B.2.4
            ['V','V','V','V','V','V','V'],                                   # B.3.1
            ['V','V','V','A','V','V'],                                       # B.3.2
            ['V','V','V','A','V'],                                           # B.3.3
            ['V','X','A','A'],                                               # B.3.4
            ['V','V','V'],                                                   # B.4.1
            ['V','V'],                                                       # B.4.2
            ['V'],                                                           # B.4.3
            []                                                               # B.4.4
        ]
    elif dim_name == 'Cliente':
        triangular = [
            ['V','V','O','O','V','V','V','A','V','V','V'],   # C.1.1
            ['V','V','O','O','V','V','X','A','V','V'],       # C.1.2
            ['A','A','O','O','V','A','A','A','V'],           # C.1.3
            ['A','A','O','O','A','A','A','A'],               # C.1.4
            ['O','O','O','X','V','V','V'],                   # C.2.1
            ['V','V','X','A','V','V'],                       # C.2.2
            ['V','X','A','A','V'],                           # C.2.3
            ['X','A','A','A'],                               # C.2.4
            ['V','V','V'],                                   # C.3.1
            ['V','V'],                                       # C.3.2
            ['V'],                                           # C.3.3
            []                                               # C.3.4
        ]

    # Construir matriz completa
    ssim_np = np.full((n, n), '', dtype='<U1')
    row_idx = 0
    for i in range(n):
        col_idx = n - 1
        for sym in triangular[i]:
            ssim_np[i, col_idx] = sym
            col_idx -= 1
    # Simetría
    for i in range(n):
        for j in range(i + 1, n):
            if ssim_np[i, j] == 'V':
                ssim_np[j, i] = 'A'
            elif ssim_np[i, j] == 'A':
                ssim_np[j, i] = 'V'
            elif ssim_np[i, j] == 'X':
                ssim_np[j, i] = 'X'
            elif ssim_np[i, j] == 'O':
                ssim_np[j, i] = 'O'
    np.fill_diagonal(ssim_np, '')

    return pd.DataFrame(ssim_np, index=codes, columns=codes)

# -------------------------------------------------------------------
# 1. SSIM → Initial Reachability Matrix (IRM)
# -------------------------------------------------------------------
def ssim_to_irm(ssim_df):
    """
    Convierte la SSIM (símbolos V/A/X/O) a la Initial Reachability Matrix.
    - V → 1 (i afecta a j)
    - A → 0
    - X → 1 (mutuo)
    - O → 0
    - Diagonal = 1
    """
    irm = ssim_df.copy().astype(str)
    mapping = {'V': 1, 'A': 0, 'X': 1, 'O': 0, '': 0}

    for i in range(irm.shape[0]):
        for j in range(irm.shape[1]):
            sym = irm.iloc[i, j]
            irm.iloc[i, j] = mapping.get(sym, 0)

    np.fill_diagonal(irm.values, 1)
    irm = irm.astype(int)
    return irm

# -------------------------------------------------------------------
# 2. Initial Reachability Matrix → Final Reachability Matrix (FRM)
#    (Transitive closure con Warshall / Floyd-Warshall)
# -------------------------------------------------------------------
def irm_to_frm(irm_df):
    """Calcula la matriz de alcance final (transitive closure)."""
    frm = irm_df.values.copy().astype(int)
    n = frm.shape[0]

    for k in range(n):
        for i in range(n):
            for j in range(n):
                frm[i, j] = frm[i, j] or (frm[i, k] and frm[k, j])

    return pd.DataFrame(frm, index=irm_df.index, columns=irm_df.columns)

# -------------------------------------------------------------------
# 3. Level Partitioning (iterativo)
# -------------------------------------------------------------------
def level_partitioning(frm_df, variable_names=None):
    """
    Devuelve los niveles jerárquicos y los conjuntos Reachability / Antecedent / Intersection.
    Nivel I = variables más dependientes (top)
    Nivel más alto = variables driver (base de la hoja de ruta)
    """
    if variable_names is None:
        variable_names = frm_df.index.tolist()

    n = frm_df.shape[0]
    variables = list(range(n))
    levels = {}
    level_counter = 1
    remaining = set(variables)

    reachability_sets = {}
    antecedent_sets = {}

    while remaining:
        reachability = {}
        antecedent = {}
        intersection = {}

        for i in remaining:
            # Reachability set: columnas donde frm[i,j] == 1
            reachability[i] = {j for j in remaining if frm_df.iloc[i, j] == 1}
            # Antecedent set: filas donde frm[j,i] == 1
            antecedent[i] = {j for j in remaining if frm_df.iloc[j, i] == 1}
            intersection[i] = reachability[i] & antecedent[i]

        # Variables del nivel actual: Reachability == Intersection
        current_level = [i for i in remaining if reachability[i] == intersection[i]]

        levels[level_counter] = [variable_names[i] for i in current_level]

        # Guardar conjuntos para reporte
        for i in current_level:
            reachability_sets[variable_names[i]] = [variable_names[j] for j in reachability[i]]
            antecedent_sets[variable_names[i]] = [variable_names[j] for j in antecedent[i]]

        remaining -= set(current_level)
        level_counter += 1

    # Invertimos el orden de niveles para que Nivel 1 sea el driver (base)
    max_level = len(levels)
    final_levels = {}
    for old_level, vars_list in levels.items():
        new_level = max_level - old_level + 1
        final_levels[new_level] = vars_list

    return final_levels, reachability_sets, antecedent_sets


def generar_roadmap(dim_name):
    codes = [v[0] for v in dim_variables[dim_name]]
    var_descriptors = {v[0]: v[1] for v in dim_variables[dim_name]}

    ssim_df = crear_ssim(dim_name)
    irm_df = ssim_to_irm(ssim_df)
    frm_df = irm_to_frm(irm_df)

    levels, _, _ = level_partitioning(frm_df, codes)

    driving = frm_df.sum(axis=1).sort_values(ascending=False)

    return {
        'ssim': ssim_df,
        'levels': levels,
        'driving_power': driving
    }


# Ahora generamos los roadmaps reales
print("✅ Función crear_ssim cargada correctamente.")
roadmap_tec  = generar_roadmap('Tecnologia')
roadmap_prod = generar_roadmap('Producto')
roadmap_cli  = generar_roadmap('Cliente')

print("✅ Roadmaps ISM con SSIM generados correctamente para las 3 dimensiones.\n")

# ==================== GRÁFICO ISM CON ESTADO ACTUAL (Versión para PDF + Colab) ====================
# Verde = Hasta el nivel actual (completado)
# Naranja = Siguiente nivel (objetivo inmediato)
# Gris = Niveles superiores (pendientes)
# ==================================================================================================
def plot_ism_digraph_hierarchical_con_estado(roadmap_data, dim_name, current_level, figsize=(24, 17)):
    ssim_df = roadmap_data['ssim']
    levels = roadmap_data['levels']
    level_of = {var: lvl for lvl, vars_list in levels.items() for var in vars_list}

    G = nx.DiGraph()
    for lvl_num, var_list in sorted(levels.items()):
        for var in var_list:
            G.add_node(var, subset=lvl_num)

    # Relaciones reales basadas en SSIM
    n = ssim_df.shape[0]
    for i in range(n):
        source = ssim_df.index[i]
        lvl_s = level_of.get(source, 1)
        for j in range(n):
            if i == j: continue
            sym = ssim_df.iloc[i, j]
            target = ssim_df.columns[j]
            lvl_t = level_of.get(target, 1)
            if sym in ['V', 'X'] and (lvl_t == lvl_s + 1 or lvl_s == lvl_t):
                G.add_edge(source, target)
            if sym == 'X' and (lvl_t == lvl_s + 1 or lvl_s == lvl_t):
                G.add_edge(target, source)

    pos = nx.multipartite_layout(G, subset_key='subset', align='horizontal', scale=2.2)
    for node in pos:
        x, y = pos[node]
        lvl = level_of.get(node, 1)
        pos[node] = (x * 3.0, (lvl - 1) * 2.8)

    # Colores
    node_colors = []
    for node in G.nodes():
        node_level = level_of.get(node, 1)
        if node_level <= current_level:
            node_colors.append('#4CAF50')
        elif node_level == current_level + 1:
            node_colors.append('#FF9800')
        else:
            node_colors.append('#E0E0E0')

    # Crear figura
    fig = plt.figure(figsize=figsize)
    nx.draw_networkx_nodes(G, pos, node_size=3600, node_color=node_colors,
                           edgecolors='#263549', linewidths=3.5)
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold')
    nx.draw_networkx_edges(G, pos, arrows=True, arrowstyle='->', arrowsize=26,
                           edge_color='#2C3E50', width=2.3, connectionstyle='arc3,rad=0.22')

    plt.title(f"Diagrama ISM - {dim_name}\n"
              f"Nivel actual: {current_level} | Verde = Completado | "
              f"Naranja = Siguiente nivel | Gris = Pendiente",
              fontsize=19, pad=50, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()

    return fig   # ← Devolvemos la figura para poder guardarla en PDF
    
    
# ==================== RECOMENDACIÓN DINÁMICA ====================
def generar_recomendacion_dinamica(pyme_name, current_levels):
    print(f"\nHOJA DE RUTA PERSONALIZADA PARA: {pyme_name}")
    print("="*110)

    for dim_name in ['Tecnologia', 'Producto', 'Cliente']:
        print(f"\nDIMENSIÓN: {dim_name.upper()}")
        print("-" * 80)

        roadmap_dict = {
            'Tecnologia': roadmap_tec,
            'Producto': roadmap_prod,
            'Cliente': roadmap_cli
        }
        roadmap_data = roadmap_dict[dim_name]

        levels = roadmap_data['levels']
        var_descriptors = {v[0]: v[1] for v in dim_variables[dim_name]}
        current_lvl = current_levels[dim_name]

        print(f"Nivel actual: **{current_lvl}** → Recomendación para llegar al siguiente nivel:\n")

        # Solo mostramos el nivel actual y el siguiente (máximo 2 niveles)
        for lvl_num in sorted(levels.keys()):
            if lvl_num < current_lvl:
                continue  # saltamos niveles ya superados

            if lvl_num == current_lvl:
                priority = "🟢 PRIORIDAD ALTA - NIVEL ACTUAL (enfocarse aquí primero)"
            elif lvl_num == current_lvl + 1:
                priority = "🟠 SIGUIENTE NIVEL (objetivo inmediato)"
            else:
                break  # no mostramos niveles más lejanos

            print(f"\nNIVEL {lvl_num} → {priority}")
            print("-" * 70)

            for code in levels[lvl_num]:
                desc = var_descriptors.get(code, code)
                short_desc = desc if len(desc) <= 120 else desc[:117] + "..."
                print(f"   • {code}: {short_desc}")

        # Top 5 Drivers más importantes para esta dimensión
        driving = roadmap_data['driving_power'].head(5)
        print(f"\n🔥 5 VARIABLES DRIVER más influyentes (prioridad alta para avanzar):")
        for code in driving.index:
            desc = var_descriptors.get(code, code)[:95]
            print(f"   {code} → {desc}...")

        print("\n" + "-"*80)

    print("\n" + "="*110)
    print("Consejo: Enfócate primero en completar el **Nivel actual** de cada dimensión.")
    print("Las variables DRIVER son las que más impacto tienen para avanzar.")


# ==================== FUNCIÓN PRINCIPAL ====================
def generar_roadmaps_completos_con_estado(pyme_name, current_levels, cluster_info=None):
    """
    cluster_info: tupla (cluster_id, cluster_nombre)  Ejemplo: (2, "Intermedios Equilibrados")
    """
    print("\n" + "="*95)
    print("📋 HOJA DE RUTA ISM + DIAGRAMAS JERÁRQUICOS")
    print("="*95)

    os.makedirs("OUTPUTS", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_path = os.path.join("OUTPUTS", f"diagnostico_{timestamp}.pdf")

    # Mapa de niveles
    level_map = {1: "Inicial", 2: "Moderado", 3: "Medio", 4: "Avanzado"}

    with PdfPages(pdf_path) as pdf:
        # =============================================
        # PÁGINA 1: Resultados Random Forest + CLUSTER (ACTUALIZADA)
        # =============================================
        fig = plt.figure(figsize=(12, 9))   # Un poco más alta para incluir el cluster
        plt.axis('off')
        
        plt.text(0.5, 0.92, "EVALUADOR DE MADUREZ INDUSTRIA 4.0", 
                 ha='center', fontsize=18, fontweight='bold')
        plt.text(0.5, 0.86, "Random Forest + ISM Roadmap + Clustering", 
                 ha='center', fontsize=14, style='italic')
        plt.text(0.5, 0.80, f"PyME: {pyme_name}", 
                 ha='center', fontsize=12, fontweight='bold')

        # Calcular niveles
        tech_lvl   = current_levels.get('Tecnologia', 2)
        prod_lvl   = current_levels.get('Producto', 2)
        client_lvl = current_levels.get('Cliente', 2)
        
        final_num = round(0.4 * tech_lvl + 0.35 * prod_lvl + 0.25 * client_lvl)
        final_num = max(1, min(4, final_num))

        # === TEXTO DE RESULTADOS ===
        rf_text = f"""RESULTADOS DE MADUREZ
=====================================================================================
TECNOLOGIA      → Nivel {tech_lvl} | {level_map[tech_lvl]}
PRODUCTO        → Nivel {prod_lvl} | {level_map[prod_lvl]}
CLIENTE         → Nivel {client_lvl} | {level_map[client_lvl]}
NIVEL FINAL     → Nivel {final_num} | {level_map[final_num]}   ← Madurez general
====================================================================================="""

        plt.text(0.5, 0.58, rf_text, ha='center', va='center', 
                 fontsize=11, fontfamily='monospace')

        # === MOSTRAR INFORMACIÓN DEL CLÚSTER ===
        if cluster_info and len(cluster_info) == 2:
            cluster_id, cluster_nombre = cluster_info
            cluster_text = f"""ANÁLISIS POR CLÚSTER
=====================================================================================
Esta PyME pertenece al clúster:

       → {cluster_nombre}
          (Cluster {cluster_id})

Este grupo representa PyMEs con características similares en su nivel 
de madurez Industria 4.0.
====================================================================================="""
            plt.text(0.5, 0.32, cluster_text, ha='center', va='center', 
                     fontsize=10.5, fontfamily='monospace')
        else:
            plt.text(0.5, 0.32, "ANÁLISIS POR CLÚSTER: No disponible", 
                     ha='center', fontsize=10, color='gray')

        pdf.savefig(fig, bbox_inches='tight')
        plt.close(fig)

        # =============================================
        # PÁGINAS 2-4: Diagramas ISM (sin cambios)
        # =============================================
        dimension_map = {
            'Tecnologia': ("Tecnología", roadmap_tec),
            'Producto':   ("Producto", roadmap_prod),
            'Cliente':    ("Cliente", roadmap_cli)
        }

        for dim_key in ['Tecnologia', 'Producto', 'Cliente']:
            nivel = current_levels.get(dim_key, 2)
            dim_display, roadmap_data = dimension_map[dim_key]

            print(f"   → Generando diagrama ISM para {dim_display} (Nivel {nivel})")

            fig = plot_ism_digraph_hierarchical_con_estado(
                roadmap_data=roadmap_data,
                dim_name=dim_display,
                current_level=nivel,
                figsize=(24, 17)
            )
            pdf.savefig(fig, bbox_inches='tight')
            plt.close(fig)

        # =============================================
        # PÁGINA FINAL: HOJA DE RUTA TEXTUAL (sin cambios)
        # =============================================
        fig = plt.figure(figsize=(20, 32))
        ax = fig.add_axes([0.06, 0.04, 0.88, 0.92])
        ax.axis('off')

        y = 0.97
        plt.text(0.5, y, f"HOJA DE RUTA PERSONALIZADA PARA: {pyme_name}", 
                 ha='center', fontsize=15, fontweight='bold')
        y -= 0.01

        for dim_name in ['Tecnologia', 'Producto', 'Cliente']:
            plt.text(0.02, y, f"DIMENSIÓN: {dim_name.upper()}", 
                     fontsize=13.5, fontweight='bold')
            y -= 0.01

            roadmap_data = {'Tecnologia': roadmap_tec, 'Producto': roadmap_prod, 'Cliente': roadmap_cli}[dim_name]
            levels = roadmap_data['levels']
            var_descriptors = {v[0]: v[1] for v in dim_variables[dim_name]}
            current_lvl = current_levels.get(dim_name, 2)

            plt.text(0.02, y, f"Nivel actual: **{current_lvl}** → Recomendación para llegar al siguiente nivel:", 
                     fontsize=11)
            y -= 0.01

            for lvl_num in sorted(levels.keys()):
                if lvl_num < current_lvl: continue
                if lvl_num == current_lvl:
                    priority = "🟢 PRIORIDAD ALTA - NIVEL ACTUAL"
                elif lvl_num == current_lvl + 1:
                    priority = "🟠 SIGUIENTE NIVEL (objetivo inmediato)"
                else:
                    break

                plt.text(0.02, y, f"NIVEL {lvl_num} → {priority}", 
                         fontsize=10.8, fontweight='bold')
                y -= 0.01

                for code in levels[lvl_num]:
                    desc = var_descriptors.get(code, code)
                    short_desc = desc if len(desc) <= 135 else desc[:132] + "..."
                    plt.text(0.06, y, f"• {code}: {short_desc}", fontsize=10)
                    y -= 0.016

                y -= 0.008

            # Drivers
            driving = roadmap_data['driving_power'].head(5)
            plt.text(0.02, y, "🔥 5 VARIABLES DRIVER más influyentes:", 
                     fontsize=11, fontweight='bold')
            y -= 0.01
            for code in driving.index:
                desc = var_descriptors.get(code, code)[:118]
                if len(desc) == 118: desc += "..."
                plt.text(0.06, y, f"{code} → {desc}", fontsize=10)
                y -= 0.01

            y -= 0.02

        # Consejo final
        consejo = """Consejo: Enfócate primero en completar el **Nivel actual** de cada dimensión.
Las variables DRIVER son las que más impacto tienen para avanzar."""

        plt.text(0.02, 0.11, consejo, fontsize=11.5, style='italic',
                 bbox=dict(boxstyle="round,pad=1", facecolor="#f0f4f8", 
                           edgecolor="#2c3e50", linewidth=1.2))

        plt.text(0.02, 0.05, f"Reporte generado: {timestamp}", 
                 fontsize=9, color='gray')

        pdf.savefig(fig, bbox_inches='tight')
        plt.close()

    print(f"\n✅ Reporte PDF completo guardado en:")
    print(f"   {pdf_path}")

    generar_recomendacion_dinamica(pyme_name, current_levels)
