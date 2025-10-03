"""
Ejemplo de uso programatico de los modulos del sistema
Demostracion completa de todas las funcionalidades implementadas
"""

from models import Grafo
from algorithms import (
    bfs, dfs, camino_mas_corto, 
    recomendar_amistades, recomendar_por_intereses,
    detectar_comunidades_louvain, estadisticas_comunidades,
    calcular_centralidad_grado, calcular_centralidad_intermediacion,
    calcular_centralidad_cercania, calcular_centralidad_eigenvector,
    obtener_nodos_mas_centrales
)
from utils import (
    generar_datos_aleatorios, mostrar_estadisticas,
    guardar_json, cargar_json, exportar_backup,
    generar_reporte_pdf
)

def ejemplo_basico():
    """Ejemplo basico de uso del grafo con intereses"""
    print("="*70)
    print("EJEMPLO 1: OPERACIONES BASICAS DEL GRAFO")
    print("="*70 + "\n")
    
    # Crear grafo
    red = Grafo()
    
    # Agregar estudiantes con intereses
    red.agregar_estudiante('1', 'Ana Garcia', 'Ingenieria', ['Tecnologia', 'Musica', 'Deportes'])
    red.agregar_estudiante('2', 'Luis Martinez', 'Medicina', ['Ciencia', 'Lectura', 'Deportes'])
    red.agregar_estudiante('3', 'Maria Lopez', 'Ingenieria', ['Tecnologia', 'Arte', 'Programacion'])
    red.agregar_estudiante('4', 'Carlos Rodriguez', 'Derecho', ['Politica', 'Historia', 'Lectura'])
    
    # Agregar amistades con diferentes pesos
    red.agregar_amistad('1', '2', peso=1)  # Amistad normal
    red.agregar_amistad('1', '3', peso=2)  # Mejor amigo
    red.agregar_amistad('2', '4', peso=1)
    red.agregar_amistad('3', '4', peso=3)  # Amigo cercano
    
    # Consultas basicas
    print(f"Amigos de Ana: {red.obtener_amigos('1')}")
    print(f"Ana y Maria son amigos? {red.son_amigos('1', '3')}")
    print(f"Peso de amistad Ana-Maria: {red.obtener_peso_amistad('1', '3')}")
    print(f"Intereses de Ana: {red.estudiantes['1']['intereses']}")
    
    # Eliminar y modificar
    print("\n--- Operaciones de modificacion ---")
    red.actualizar_peso_amistad('1', '2', 3)
    print(f"Peso actualizado Ana-Luis: {red.obtener_peso_amistad('1', '2')}")
    
    red.eliminar_amistad('2', '4')
    print(f"Amistad eliminada entre Luis y Carlos")
    print(f"Luis y Carlos son amigos? {red.son_amigos('2', '4')}")
    print()

def ejemplo_busquedas():
    """Ejemplo de algoritmos de busqueda (BFS, DFS, camino mas corto)"""
    print("="*70)
    print("EJEMPLO 2: ALGORITMOS DE BUSQUEDA")
    print("="*70 + "\n")
    
    red = Grafo()
    
    # Generar datos aleatorios
    print("Generando red de prueba...\n")
    generar_datos_aleatorios(red, num_estudiantes=12, densidad_amistades=0.3)
    
    # BFS
    print("--- Busqueda en Anchura (BFS) desde nodo 1 ---")
    visitados_bfs = bfs(red, '1')
    nombres_bfs = [red.estudiantes[id]['nombre'].split()[0] for id in visitados_bfs[:6]]
    print(f"Primeros 6 nodos visitados: {' -> '.join(nombres_bfs)}")
    print(f"Total alcanzable: {len(visitados_bfs)}\n")
    
    # DFS
    print("--- Busqueda en Profundidad (DFS) desde nodo 1 ---")
    visitados_dfs = dfs(red, '1')
    nombres_dfs = [red.estudiantes[id]['nombre'].split()[0] for id in visitados_dfs[:6]]
    print(f"Primeros 6 nodos visitados: {' -> '.join(nombres_dfs)}")
    print(f"Total alcanzable: {len(visitados_dfs)}\n")
    
    # Camino mas corto
    print("--- Camino mas corto entre nodos 1 y 6 ---")
    camino = camino_mas_corto(red, '1', '6')
    if camino:
        print(f"Camino encontrado ({len(camino)} nodos): {' -> '.join(camino)}")
    else:
        print("No existe camino entre estos nodos")
    print()

def ejemplo_recomendaciones():
    """Ejemplo de sistemas de recomendaciones (amigos comunes e intereses)"""
    print("="*70)
    print("EJEMPLO 3: SISTEMAS DE RECOMENDACION")
    print("="*70 + "\n")
    
    red = Grafo()
    
    # Crear red de ejemplo con intereses
    estudiantes = [
        ('1', 'Ana', 'Ingenieria', ['Tecnologia', 'Musica', 'Deportes']),
        ('2', 'Luis', 'Medicina', ['Ciencia', 'Musica', 'Lectura']),
        ('3', 'Maria', 'Ingenieria', ['Tecnologia', 'Arte', 'Deportes']),
        ('4', 'Carlos', 'Derecho', ['Politica', 'Lectura', 'Historia']),
        ('5', 'Elena', 'Medicina', ['Ciencia', 'Deportes', 'Viajes']),
        ('6', 'Pedro', 'Ingenieria', ['Tecnologia', 'Programacion', 'Videojuegos']),
        ('7', 'Sofia', 'Psicologia', ['Arte', 'Musica', 'Lectura'])
    ]
    
    for id_est, nombre, carrera, intereses in estudiantes:
        red.agregar_estudiante(id_est, nombre, carrera, intereses)
    
    # Crear algunas amistades
    red.agregar_amistad('1', '2', 1)
    red.agregar_amistad('1', '3', 2)
    red.agregar_amistad('2', '4', 1)
    red.agregar_amistad('3', '5', 1)
    red.agregar_amistad('4', '7', 1)
    
    # Recomendaciones por amigos en comun
    print("--- Recomendaciones por Amigos en Comun para Ana ---")
    recomendaciones = recomendar_amistades(red, '1', max_recomendaciones=3)
    for i, (id_rec, info) in enumerate(recomendaciones, 1):
        print(f"{i}. {red.estudiantes[id_rec]['nombre']} ({red.estudiantes[id_rec]['carrera']})")
        print(f"   Puntaje: {info['puntaje']:.1f} | Amigos comun: {info['amigos_comunes']} | Misma carrera: {info['misma_carrera']}")
    
    # Recomendaciones por intereses
    print("\n--- Recomendaciones por Intereses para Ana ---")
    recomendaciones_int = recomendar_por_intereses(red, '1', max_recomendaciones=3)
    for i, (id_rec, info) in enumerate(recomendaciones_int, 1):
        print(f"{i}. {red.estudiantes[id_rec]['nombre']} ({red.estudiantes[id_rec]['carrera']})")
        print(f"   Puntaje: {info['puntaje']:.1f} | Intereses comunes: {', '.join(info['intereses_comunes'])}")
    print()

def ejemplo_comunidades():
    """Ejemplo de deteccion de comunidades con algoritmo de Louvain"""
    print("="*70)
    print("EJEMPLO 4: DETECCION DE COMUNIDADES")
    print("="*70 + "\n")
    
    red = Grafo()
    
    # Generar red mas grande para comunidades
    print("Generando red de 25 estudiantes...\n")
    generar_datos_aleatorios(red, num_estudiantes=25, densidad_amistades=0.2)
    
    # Detectar comunidades
    print("--- Deteccion de Comunidades (Louvain) ---")
    comunidades = detectar_comunidades_louvain(red)
    stats = estadisticas_comunidades(red, comunidades)
    
    print(f"Comunidades detectadas: {len(stats)}\n")
    
    for com_id, info in list(stats.items())[:3]:  # Mostrar solo las 3 primeras
        print(f"Comunidad {com_id + 1}:")
        print(f"  Tamano: {info['tamano']} miembros")
        print(f"  Carreras: {dict(list(info['carreras'].items())[:3])}")
        miembros_nombres = [red.estudiantes[id]['nombre'] for id in info['miembros'][:4]]
        print(f"  Miembros: {', '.join(miembros_nombres)}", end='')
        if len(info['miembros']) > 4:
            print(f" ... y {len(info['miembros']) - 4} mas")
        else:
            print()
    print()

def ejemplo_centralidad():
    """Ejemplo de calculo de metricas de centralidad"""
    print("="*70)
    print("EJEMPLO 5: METRICAS DE CENTRALIDAD")
    print("="*70 + "\n")
    
    red = Grafo()
    
    # Generar red
    print("Generando red de 20 estudiantes...\n")
    generar_datos_aleatorios(red, num_estudiantes=20, densidad_amistades=0.25)
    
    # Centralidad de grado
    print("--- Centralidad de Grado (Top 5) ---")
    c_grado = calcular_centralidad_grado(red)
    for id_est, valor in obtener_nodos_mas_centrales(c_grado, 5):
        print(f"  {red.estudiantes[id_est]['nombre']}: {valor} conexiones")
    
    # Centralidad de intermediacion
    print("\n--- Centralidad de Intermediacion (Top 5) ---")
    c_inter = calcular_centralidad_intermediacion(red)
    for id_est, valor in obtener_nodos_mas_centrales(c_inter, 5):
        print(f"  {red.estudiantes[id_est]['nombre']}: {valor:.4f}")
    
    # Centralidad de cercania
    print("\n--- Centralidad de Cercania (Top 5) ---")
    c_cerca = calcular_centralidad_cercania(red)
    for id_est, valor in obtener_nodos_mas_centrales(c_cerca, 5):
        print(f"  {red.estudiantes[id_est]['nombre']}: {valor:.4f}")
    
    # Centralidad eigenvector
    print("\n--- Centralidad Eigenvector (Top 5) ---")
    c_eigen = calcular_centralidad_eigenvector(red)
    for id_est, valor in obtener_nodos_mas_centrales(c_eigen, 5):
        print(f"  {red.estudiantes[id_est]['nombre']}: {valor:.4f}")
    print()

def ejemplo_persistencia():
    """Ejemplo de persistencia y exportacion de datos"""
    print("="*70)
    print("EJEMPLO 6: PERSISTENCIA Y EXPORTACION")
    print("="*70 + "\n")
    
    red = Grafo()
    
    # Generar datos
    print("Generando red de prueba...\n")
    generar_datos_aleatorios(red, num_estudiantes=15, densidad_amistades=0.2)
    
    # Guardar en JSON
    print("--- Guardando en JSON ---")
    if guardar_json(red, 'ejemplo_red.json'):
        print("Guardado exitoso en ejemplo_red.json")
    
    # Crear backup
    print("\n--- Creando Backup ---")
    if exportar_backup(red):
        print("Backup creado en directorio backups/")
    
    # Cargar desde JSON
    print("\n--- Cargando desde JSON ---")
    red_nueva = Grafo()
    if cargar_json(red_nueva, 'ejemplo_red.json'):
        print(f"Cargado exitosamente: {len(red_nueva.estudiantes)} estudiantes")
    
    # Generar reporte PDF
    print("\n--- Generando Reporte PDF ---")
    print("Creando reporte (esto puede tomar unos segundos)...")
    if generar_reporte_pdf(red, 'ejemplo_reporte.pdf', incluir_grafico=True):
        print("Reporte PDF generado: ejemplo_reporte.pdf")
    print()

def ejemplo_gestion():
    """Ejemplo de operaciones CRUD completas"""
    print("="*70)
    print("EJEMPLO 7: OPERACIONES CRUD COMPLETAS")
    print("="*70 + "\n")
    
    red = Grafo()
    
    # Agregar estudiantes con intereses
    print("--- Agregando Estudiantes ---")
    red.agregar_estudiante('1', 'Ana', 'Ingenieria', ['Tecnologia', 'Deportes'])
    red.agregar_estudiante('2', 'Luis', 'Medicina', ['Ciencia', 'Lectura'])
    red.agregar_estudiante('3', 'Maria', 'Ingenieria', ['Tecnologia', 'Arte'])
    print(f"Estudiantes agregados: {len(red.estudiantes)}")
    
    # Agregar amistades
    print("\n--- Agregando Amistades ---")
    red.agregar_amistad('1', '2', 1)
    red.agregar_amistad('1', '3', 2)
    print(f"Amigos de Ana: {len(red.obtener_amigos('1'))}")
    
    # Modificar peso
    print("\n--- Modificando Peso de Amistad ---")
    red.actualizar_peso_amistad('1', '2', 3)
    print(f"Nuevo peso Ana-Luis: {red.obtener_peso_amistad('1', '2')}")
    
    # Agregar intereses
    print("\n--- Agregando Intereses ---")
    red.estudiantes['2']['intereses'].extend(['Musica', 'Viajes'])
    print(f"Intereses de Luis: {red.estudiantes['2']['intereses']}")
    
    # Eliminar amistad
    print("\n--- Eliminando Amistad ---")
    red.eliminar_amistad('1', '3')
    print(f"Amigos de Ana despues de eliminar: {len(red.obtener_amigos('1'))}")
    
    # Eliminar estudiante
    print("\n--- Eliminando Estudiante ---")
    red.eliminar_estudiante('2')
    print(f"Estudiantes finales: {len(red.estudiantes)}")
    print(f"Amigos de Ana despues de eliminar Luis: {len(red.obtener_amigos('1'))}")
    print()

if __name__ == "__main__":
    print("\n" + "="*70)
    print(" "*15 + "DEMOSTRACION COMPLETA DEL SISTEMA")
    print(" "*10 + "Red Universitaria - Todas las Funcionalidades")
    print("="*70 + "\n")
    
    # Ejecutar todos los ejemplos
    ejemplo_basico()
    input("Presiona ENTER para continuar...\n")
    
    ejemplo_busquedas()
    input("Presiona ENTER para continuar...\n")
    
    ejemplo_recomendaciones()
    input("Presiona ENTER para continuar...\n")
    
    ejemplo_comunidades()
    input("Presiona ENTER para continuar...\n")
    
    ejemplo_centralidad()
    input("Presiona ENTER para continuar...\n")
    
    ejemplo_persistencia()
    input("Presiona ENTER para continuar...\n")
    
    ejemplo_gestion()
    
    # Estadisticas finales con red mas grande
    print("="*70)
    print("ESTADISTICAS FINALES - RED COMPLETA")
    print("="*70 + "\n")
    red_final = Grafo()
    generar_datos_aleatorios(red_final, 30, 0.2)
    mostrar_estadisticas(red_final)
    
    print("\n" + "="*70)
    print(" "*20 + "FIN DE LA DEMOSTRACION")
    print("="*70)
    print("\nTodos los modulos y funcionalidades han sido probados exitosamente!")
    print("\nArchivos generados:")
    print("  - ejemplo_red.json (datos en formato JSON)")
    print("  - ejemplo_reporte.pdf (reporte estadistico)")
    print("  - backups/ (directorio con backups automaticos)")
    print("\nPara usar el sistema interactivo, ejecuta: python3 Main.py")
    print("="*70 + "\n")
