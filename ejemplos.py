"""
Ejemplo de uso programatico de los modulos del sistema
"""

from models import Grafo
from algorithms import bfs, dfs, camino_mas_corto, recomendar_amistades
from utils import generar_datos_aleatorios, mostrar_estadisticas

def ejemplo_basico():
    """Ejemplo basico de uso del grafo"""
    print("=== EJEMPLO BASICO ===\n")
    
    # Crear grafo
    red = Grafo()
    
    # Agregar estudiantes
    red.agregar_estudiante('1', 'Ana Garcia', 'Ingenieria')
    red.agregar_estudiante('2', 'Luis Martinez', 'Medicina')
    red.agregar_estudiante('3', 'Maria Lopez', 'Ingenieria')
    red.agregar_estudiante('4', 'Carlos Rodriguez', 'Derecho')
    
    # Agregar amistades con diferentes pesos
    red.agregar_amistad('1', '2', peso=1)  # Amistad normal
    red.agregar_amistad('1', '3', peso=2)  # Mejor amigo
    red.agregar_amistad('2', '4', peso=1)
    
    # Consultas
    print(f"Amigos de Ana: {red.obtener_amigos('1')}")
    print(f"Ana y Maria son amigos? {red.son_amigos('1', '3')}")
    print(f"Peso de amistad Ana-Maria: {red.obtener_peso_amistad('1', '3')}")
    print()

def ejemplo_busquedas():
    """Ejemplo de algoritmos de busqueda"""
    print("=== EJEMPLO BUSQUEDAS ===\n")
    
    red = Grafo()
    
    # Generar datos aleatorios
    generar_datos_aleatorios(red, num_estudiantes=10, densidad_amistades=0.3)
    
    # BFS
    print("Busqueda BFS desde nodo 1:")
    visitados_bfs = bfs(red, '1')
    print(f"Nodos visitados: {visitados_bfs}\n")
    
    # DFS
    print("Busqueda DFS desde nodo 1:")
    visitados_dfs = dfs(red, '1')
    print(f"Nodos visitados: {visitados_dfs}\n")
    
    # Camino mas corto
    print("Camino mas corto entre nodo 1 y 5:")
    camino = camino_mas_corto(red, '1', '5')
    if camino:
        print(f"Camino: {' -> '.join(camino)}\n")
    else:
        print("No existe camino\n")

def ejemplo_recomendaciones():
    """Ejemplo de sistema de recomendaciones"""
    print("=== EJEMPLO RECOMENDACIONES ===\n")
    
    red = Grafo()
    
    # Crear red de ejemplo
    for i in range(1, 8):
        red.agregar_estudiante(str(i), f"Estudiante {i}", "Ingenieria" if i % 2 == 0 else "Medicina")
    
    # Crear algunas amistades
    red.agregar_amistad('1', '2', 1)
    red.agregar_amistad('1', '3', 2)
    red.agregar_amistad('2', '4', 1)
    red.agregar_amistad('3', '4', 1)
    red.agregar_amistad('4', '5', 1)
    red.agregar_amistad('5', '6', 1)
    
    # Obtener recomendaciones
    recomendaciones = recomendar_amistades(red, '1', max_recomendaciones=3)
    
    print("Recomendaciones para Estudiante 1:")
    for id_rec, info in recomendaciones:
        print(f"  - {red.estudiantes[id_rec]['nombre']}")
        print(f"    Puntaje: {info['puntaje']:.1f}")
        print(f"    Amigos en comun: {info['amigos_comunes']}")
        print(f"    Misma carrera: {info['misma_carrera']}\n")

def ejemplo_gestion():
    """Ejemplo de operaciones CRUD"""
    print("=== EJEMPLO GESTION ===\n")
    
    red = Grafo()
    
    # Agregar estudiantes
    red.agregar_estudiante('1', 'Ana', 'Ingenieria')
    red.agregar_estudiante('2', 'Luis', 'Medicina')
    red.agregar_estudiante('3', 'Maria', 'Ingenieria')
    
    print(f"Estudiantes iniciales: {len(red.estudiantes)}")
    
    # Agregar amistades
    red.agregar_amistad('1', '2', 1)
    red.agregar_amistad('1', '3', 1)
    
    print(f"Amigos de Ana: {len(red.obtener_amigos('1'))}")
    
    # Modificar peso
    red.actualizar_peso_amistad('1', '2', 3)
    print(f"Nuevo peso Ana-Luis: {red.obtener_peso_amistad('1', '2')}")
    
    # Eliminar amistad
    red.eliminar_amistad('1', '3')
    print(f"Amigos de Ana despues de eliminar: {len(red.obtener_amigos('1'))}")
    
    # Eliminar estudiante
    red.eliminar_estudiante('2')
    print(f"Estudiantes finales: {len(red.estudiantes)}")
    print(f"Amigos de Ana despues de eliminar Luis: {len(red.obtener_amigos('1'))}\n")

if __name__ == "__main__":
    ejemplo_basico()
    ejemplo_busquedas()
    ejemplo_recomendaciones()
    ejemplo_gestion()
    
    print("\n=== ESTADISTICAS FINALES ===")
    red = Grafo()
    generar_datos_aleatorios(red, 20, 0.2)
    mostrar_estadisticas(red)
