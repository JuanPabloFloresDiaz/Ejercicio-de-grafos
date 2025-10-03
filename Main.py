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
    cargar_datos, 
    guardar_datos,
    visualizar_grafo, 
    generar_datos_aleatorios,
    mostrar_estadisticas,
    guardar_json,
    cargar_json,
    exportar_backup,
    generar_reporte_pdf
)

def interfaz_principal(grafo):
    """Interfaz de usuario para interactuar con el sistema"""
    while True:
        print("\n" + "="*70)
        print(" "*15 + "SISTEMA DE GESTION DE RED UNIVERSITARIA")
        print("="*70)
        print("\n📊 CONSULTAS Y BUSQUEDAS:")
        print("  1.  Ver todos los estudiantes")
        print("  2.  Ver amistades de un estudiante")
        print("  3.  Buscar por nombre o carrera")
        print("  4.  Ver intereses de un estudiante")
        print("  5.  Encontrar camino entre estudiantes")
        print("  6.  Busqueda BFS desde un estudiante")
        print("  7.  Busqueda DFS desde un estudiante")
        
        print("\n🤝 RECOMENDACIONES:")
        print("  8.  Recomendar amistades (por amigos comunes)")
        print("  9.  Recomendar amistades (por intereses)")
        
        print("\n👥 GESTION DE ESTUDIANTES:")
        print(" 10.  Agregar estudiante")
        print(" 11.  Eliminar estudiante")
        print(" 12.  Modificar datos de estudiante")
        print(" 13.  Agregar/Eliminar intereses")
        
        print("\n💫 GESTION DE AMISTADES:")
        print(" 14.  Agregar amistad")
        print(" 15.  Eliminar amistad")
        print(" 16.  Modificar peso de amistad")
        
        print("\n📈 ANALISIS AVANZADO:")
        print(" 17.  Ver estadisticas generales")
        print(" 18.  Detectar comunidades (Louvain)")
        print(" 19.  Calcular centralidad de nodos")
        print(" 20.  Analizar nodos mas influyentes")
        
        print("\n🎨 VISUALIZACION:")
        print(" 21.  Visualizar grafo completo")
        print(" 22.  Generar reporte PDF")
        
        print("\n💾 DATOS Y PERSISTENCIA:")
        print(" 23.  Guardar en CSV")
        print(" 24.  Guardar en JSON")
        print(" 25.  Cargar desde JSON")
        print(" 26.  Crear backup")
        print(" 27.  Generar datos aleatorios")
        
        print("\n 0.  Salir del sistema")
        print("="*70)

        opcion = input("\n👉 Seleccione una opcion: ").strip()

        if opcion == '1':
            print("\n" + "="*60)
            print("LISTA DE ESTUDIANTES")
            print("="*60)
            if not grafo.estudiantes:
                print("No hay estudiantes registrados")
            else:
                for id_est, info in sorted(grafo.estudiantes.items()):
                    num_amigos = len(grafo.obtener_amigos(id_est))
                    print(f"ID: {id_est:3} | {info['nombre']:25} | {info['carrera']:20} | Amigos: {num_amigos}")

        elif opcion == '2':
            id_est = input("ID del estudiante: ").strip()
            if id_est in grafo.estudiantes:
                amigos = grafo.obtener_amigos(id_est)
                print(f"\nAmigos de {grafo.estudiantes[id_est]['nombre']}:")
                if not amigos:
                    print("  Este estudiante no tiene amigos registrados")
                else:
                    for amigo_id in amigos:
                        info_amigo = grafo.estudiantes[amigo_id]
                        peso = grafo.obtener_peso_amistad(id_est, amigo_id)
                        tipo = "Normal" if peso == 1 else "Mejor amigo" if peso == 2 else "Amigo cercano"
                        print(f"  - {info_amigo['nombre']} ({info_amigo['carrera']}) - Nivel: {peso} ({tipo})")
            else:
                print("Error: Estudiante no encontrado")

        elif opcion == '3':
            id_est = input("ID del estudiante: ").strip()
            if id_est in grafo.estudiantes:
                recomendaciones = recomendar_amistades(grafo, id_est)
                if recomendaciones:
                    print(f"\nRecomendaciones para {grafo.estudiantes[id_est]['nombre']}:")
                    for i, (id_rec, info) in enumerate(recomendaciones, 1):
                        estudiante = grafo.estudiantes[id_rec]
                        print(f"{i}. {estudiante['nombre']} ({estudiante['carrera']})")
                        print(f"   Puntaje: {info['puntaje']:.1f} | Amigos en comun: {info['amigos_comunes']} | Misma carrera: {'Si' if info['misma_carrera'] else 'No'}")
                else:
                    print("No hay recomendaciones disponibles")
            else:
                print("Error: Estudiante no encontrado")

        elif opcion == '4':
            id1 = input("ID del primer estudiante: ").strip()
            id2 = input("ID del segundo estudiante: ").strip()
            camino = camino_mas_corto(grafo, id1, id2)
            if camino:
                print(f"\nCamino mas corto ({len(camino)} nodos):")
                print(" -> ".join(camino))
            else:
                print("No existe conexion entre estos estudiantes")

        elif opcion == '5':
            id_est = input("ID del estudiante inicial: ").strip()
            if id_est in grafo.estudiantes:
                visitados = bfs(grafo, id_est)
                print(f"\nRecorrido BFS desde {grafo.estudiantes[id_est]['nombre']}:")
                nombres = [grafo.estudiantes[id]['nombre'] for id in visitados]
                print(" -> ".join(nombres))
                print(f"\nTotal de nodos alcanzables: {len(visitados)}")
            else:
                print("Error: Estudiante no encontrado")

        elif opcion == '6':
            id_est = input("ID del estudiante inicial: ").strip()
            if id_est in grafo.estudiantes:
                visitados = dfs(grafo, id_est)
                print(f"\nRecorrido DFS desde {grafo.estudiantes[id_est]['nombre']}:")
                nombres = [grafo.estudiantes[id]['nombre'] for id in visitados]
                print(" -> ".join(nombres))
                print(f"\nTotal de nodos alcanzables: {len(visitados)}")
            else:
                print("Error: Estudiante no encontrado")

        elif opcion == '7':
            print("\n--- Agregar Estudiante ---")
            id_est = input("ID: ").strip()
            if id_est in grafo.estudiantes:
                print("Error: Ya existe un estudiante con ese ID")
            else:
                nombre = input("Nombre completo: ").strip()
                carrera = input("Carrera: ").strip()
                grafo.agregar_estudiante(id_est, nombre, carrera)
                print(f"Estudiante {nombre} agregado exitosamente")

        elif opcion == '8':
            id_est = input("ID del estudiante a eliminar: ").strip()
            if id_est in grafo.estudiantes:
                nombre = grafo.estudiantes[id_est]['nombre']
                confirmar = input(f"Confirmar eliminacion de {nombre}? (s/n): ").strip().lower()
                if confirmar == 's':
                    grafo.eliminar_estudiante(id_est)
                    print(f"Estudiante {nombre} eliminado exitosamente")
                else:
                    print("Operacion cancelada")
            else:
                print("Error: Estudiante no encontrado")

        elif opcion == '9':
            print("\n--- Agregar Amistad ---")
            id1 = input("ID del primer estudiante: ").strip()
            id2 = input("ID del segundo estudiante: ").strip()
            if id1 == id2:
                print("Error: No puede crear amistad consigo mismo")
            elif grafo.son_amigos(id1, id2):
                print("Error: Ya existe una amistad entre estos estudiantes")
            else:
                peso = input("Peso de la amistad (1=Normal, 2=Mejor amigo, 3=Amigo cercano) [1]: ").strip()
                peso = int(peso) if peso.isdigit() and int(peso) in [1, 2, 3] else 1
                if grafo.agregar_amistad(id1, id2, peso):
                    print("Amistad agregada exitosamente")
                else:
                    print("Error: Uno o ambos estudiantes no existen")

        elif opcion == '10':
            print("\n--- Eliminar Amistad ---")
            id1 = input("ID del primer estudiante: ").strip()
            id2 = input("ID del segundo estudiante: ").strip()
            if grafo.eliminar_amistad(id1, id2):
                print("Amistad eliminada exitosamente")
            else:
                print("Error: No existe amistad entre estos estudiantes")

        elif opcion == '11':
            print("\n--- Modificar Peso de Amistad ---")
            id1 = input("ID del primer estudiante: ").strip()
            id2 = input("ID del segundo estudiante: ").strip()
            if not grafo.son_amigos(id1, id2):
                print("Error: No existe amistad entre estos estudiantes")
            else:
                peso_actual = grafo.obtener_peso_amistad(id1, id2)
                print(f"Peso actual: {peso_actual}")
                nuevo_peso = input("Nuevo peso (1=Normal, 2=Mejor amigo, 3=Amigo cercano): ").strip()
                if nuevo_peso.isdigit() and int(nuevo_peso) in [1, 2, 3]:
                    grafo.actualizar_peso_amistad(id1, id2, int(nuevo_peso))
                    print("Peso actualizado exitosamente")
                else:
                    print("Error: Peso invalido")

        elif opcion == '12':
            mostrar_estadisticas(grafo)

        elif opcion == '13':
            if not grafo.estudiantes:
                print("Error: No hay estudiantes para visualizar")
            else:
                print("Generando visualizacion...")
                visualizar_grafo(grafo)

        elif opcion == '14':
            print("\n--- Generar Datos Aleatorios ---")
            print("ADVERTENCIA: Esto eliminara todos los datos actuales")
            confirmar = input("Continuar? (s/n): ").strip().lower()
            if confirmar == 's':
                num_est = input("Numero de estudiantes [30]: ").strip()
                num_est = int(num_est) if num_est.isdigit() else 30
                densidad = input("Densidad de amistades (0.0-1.0) [0.15]: ").strip()
                try:
                    densidad = float(densidad) if densidad else 0.15
                    densidad = max(0.0, min(1.0, densidad))
                except:
                    densidad = 0.15
                
                # Limpiar grafo actual
                grafo.estudiantes.clear()
                grafo.adj_list.clear()
                
                generar_datos_aleatorios(grafo, num_est, densidad)
                print("\nDatos aleatorios generados exitosamente")
            else:
                print("Operacion cancelada")

        elif opcion == '15':
            print("\n--- Guardar Cambios ---")
            if guardar_datos(grafo):
                print("Datos guardados exitosamente")
            else:
                print("Error al guardar los datos")

        elif opcion == '0':
            print("\nCerrando sistema...")
            guardar = input("Guardar cambios antes de salir? (s/n): ").strip().lower()
            if guardar == 's':
                guardar_datos(grafo)
            print("Hasta luego!")
            break

        else:
            print("Error: Opcion no valida")

def main():
    """Punto de entrada principal del sistema"""
    print("="*60)
    print("SISTEMA DE GESTION DE RED UNIVERSITARIA")
    print("="*60)
    
    red_universitaria = Grafo()
    
    # Intentar cargar datos existentes
    if not cargar_datos(red_universitaria, 'estudiantes.csv', 'amistades.csv'):
        print("\nNo se encontraron archivos de datos.")
        opcion = input("Generar datos aleatorios para pruebas? (s/n): ").strip().lower()
        if opcion == 's':
            generar_datos_aleatorios(red_universitaria, 20, 0.2)
            guardar_datos(red_universitaria)
        else:
            print("Iniciando con red vacia...")
    
    print(f"\nRed cargada: {len(red_universitaria.estudiantes)} estudiantes")
    
    # Ejecutar interfaz
    interfaz_principal(red_universitaria)

if __name__ == "__main__":
    main()