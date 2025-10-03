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
    """Interfaz de usuario mejorada para interactuar con el sistema"""
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

        # =============== CONSULTAS Y BUSQUEDAS ===============
        if opcion == '1':
            print("\n" + "="*70)
            print(" "*25 + "LISTA DE ESTUDIANTES")
            print("="*70)
            if not grafo.estudiantes:
                print("❌ No hay estudiantes registrados")
            else:
                for id_est, info in sorted(grafo.estudiantes.items()):
                    num_amigos = len(grafo.obtener_amigos(id_est))
                    intereses = info.get('intereses', [])
                    num_intereses = len(intereses)
                    print(f"ID: {id_est:3} | {info['nombre']:25} | {info['carrera']:20} | Amigos: {num_amigos:2} | Intereses: {num_intereses}")

        elif opcion == '2':
            id_est = input("\n📝 ID del estudiante: ").strip()
            if id_est in grafo.estudiantes:
                amigos = grafo.obtener_amigos(id_est)
                print(f"\n{'='*70}")
                print(f"👥 Amigos de {grafo.estudiantes[id_est]['nombre']}:")
                print(f"{'='*70}")
                if not amigos:
                    print("  Este estudiante no tiene amigos registrados")
                else:
                    for amigo_id in amigos:
                        info_amigo = grafo.estudiantes[amigo_id]
                        peso = grafo.obtener_peso_amistad(id_est, amigo_id)
                        tipo = "Normal" if peso == 1 else "Mejor amigo" if peso == 2 else "Amigo cercano"
                        print(f"  • {info_amigo['nombre']:25} ({info_amigo['carrera']:15}) - Nivel: {peso} ({tipo})")
            else:
                print("❌ Error: Estudiante no encontrado")

        elif opcion == '3':
            print("\n--- Buscar Estudiante ---")
            termino = input("Ingrese nombre o carrera a buscar: ").strip().lower()
            resultados = []
            for id_est, info in grafo.estudiantes.items():
                if termino in info['nombre'].lower() or termino in info['carrera'].lower():
                    resultados.append((id_est, info))
            
            if resultados:
                print(f"\n✅ Se encontraron {len(resultados)} resultados:")
                for id_est, info in resultados:
                    print(f"  ID: {id_est:3} | {info['nombre']:25} | {info['carrera']}")
            else:
                print("❌ No se encontraron resultados")

        elif opcion == '4':
            id_est = input("\n📝 ID del estudiante: ").strip()
            if id_est in grafo.estudiantes:
                info = grafo.estudiantes[id_est]
                print(f"\n{'='*70}")
                print(f"Estudiante: {info['nombre']}")
                print(f"Carrera: {info['carrera']}")
                intereses = info.get('intereses', [])
                if intereses:
                    print(f"Intereses ({len(intereses)}):")
                    for i, interes in enumerate(intereses, 1):
                        print(f"  {i}. {interes}")
                else:
                    print("No tiene intereses registrados")
                print("="*70)
            else:
                print("❌ Error: Estudiante no encontrado")

        elif opcion == '5':
            id1 = input("\n📝 ID del primer estudiante: ").strip()
            id2 = input("📝 ID del segundo estudiante: ").strip()
            if id1 in grafo.estudiantes and id2 in grafo.estudiantes:
                camino = camino_mas_corto(grafo, id1, id2)
                if camino:
                    print(f"\n✅ Camino mas corto encontrado ({len(camino)} nodos):")
                    nombres = [grafo.estudiantes[id]['nombre'] for id in camino]
                    print(" → ".join(nombres))
                else:
                    print("❌ No existe conexion entre estos estudiantes")
            else:
                print("❌ Error: Uno o ambos estudiantes no encontrados")

        elif opcion == '6':
            id_est = input("\n📝 ID del estudiante inicial: ").strip()
            if id_est in grafo.estudiantes:
                visitados = bfs(grafo, id_est)
                print(f"\n{'='*70}")
                print(f"🔍 Recorrido BFS desde {grafo.estudiantes[id_est]['nombre']}:")
                print(f"{'='*70}")
                nombres = [grafo.estudiantes[id]['nombre'] for id in visitados[:10]]
                print(" → ".join(nombres))
                if len(visitados) > 10:
                    print(f"... y {len(visitados) - 10} nodos mas")
                print(f"\n✅ Total de nodos alcanzables: {len(visitados)}")
            else:
                print("❌ Error: Estudiante no encontrado")

        elif opcion == '7':
            id_est = input("\n📝 ID del estudiante inicial: ").strip()
            if id_est in grafo.estudiantes:
                visitados = dfs(grafo, id_est)
                print(f"\n{'='*70}")
                print(f"🔍 Recorrido DFS desde {grafo.estudiantes[id_est]['nombre']}:")
                print(f"{'='*70}")
                nombres = [grafo.estudiantes[id]['nombre'] for id in visitados[:10]]
                print(" → ".join(nombres))
                if len(visitados) > 10:
                    print(f"... y {len(visitados) - 10} nodos mas")
                print(f"\n✅ Total de nodos alcanzables: {len(visitados)}")
            else:
                print("❌ Error: Estudiante no encontrado")

        # =============== RECOMENDACIONES ===============
        elif opcion == '8':
            id_est = input("\n📝 ID del estudiante: ").strip()
            if id_est in grafo.estudiantes:
                recomendaciones = recomendar_amistades(grafo, id_est)
                if recomendaciones:
                    print(f"\n{'='*70}")
                    print(f"🤝 Recomendaciones para {grafo.estudiantes[id_est]['nombre']}:")
                    print(f"{'='*70}")
                    for i, (id_rec, info) in enumerate(recomendaciones[:10], 1):
                        estudiante = grafo.estudiantes[id_rec]
                        print(f"\n{i}. {estudiante['nombre']} ({estudiante['carrera']})")
                        print(f"   📊 Puntaje: {info['puntaje']:.1f}")
                        print(f"   👥 Amigos en comun: {info['amigos_comunes']}")
                        print(f"   🎓 Misma carrera: {'✅ Si' if info['misma_carrera'] else '❌ No'}")
                else:
                    print("❌ No hay recomendaciones disponibles")
            else:
                print("❌ Error: Estudiante no encontrado")

        elif opcion == '9':
            id_est = input("\n📝 ID del estudiante: ").strip()
            if id_est in grafo.estudiantes:
                try:
                    recomendaciones = recomendar_por_intereses(grafo, id_est)
                    if recomendaciones:
                        print(f"\n{'='*70}")
                        print(f"🎯 Recomendaciones por intereses para {grafo.estudiantes[id_est]['nombre']}:")
                        print(f"{'='*70}")
                        for i, (id_rec, info) in enumerate(recomendaciones[:10], 1):
                            estudiante = grafo.estudiantes[id_rec]
                            print(f"\n{i}. {estudiante['nombre']} ({estudiante['carrera']})")
                            print(f"   📊 Puntaje: {info['puntaje']:.1f}")
                            print(f"   🎨 Intereses comunes: {', '.join(info['intereses_comunes'])}")
                    else:
                        print("❌ No hay recomendaciones disponibles")
                except Exception as e:
                    print(f"❌ Error al generar recomendaciones: {e}")
            else:
                print("❌ Error: Estudiante no encontrado")

        # =============== GESTION DE ESTUDIANTES ===============
        elif opcion == '10':
            print("\n" + "="*70)
            print(" "*25 + "AGREGAR ESTUDIANTE")
            print("="*70)
            id_est = input("📝 ID: ").strip()
            if id_est in grafo.estudiantes:
                print("❌ Error: Ya existe un estudiante con ese ID")
            else:
                nombre = input("📝 Nombre completo: ").strip()
                carrera = input("📝 Carrera: ").strip()
                
                print("\n¿Desea agregar intereses? (s/n): ", end='')
                agregar_intereses = input().strip().lower()
                intereses = []
                if agregar_intereses == 's':
                    print("Ingrese los intereses (separados por coma):")
                    intereses_str = input("📝 ").strip()
                    if intereses_str:
                        intereses = [i.strip() for i in intereses_str.split(',') if i.strip()]
                
                grafo.agregar_estudiante(id_est, nombre, carrera, intereses)
                print(f"\n✅ Estudiante {nombre} agregado exitosamente")
                if intereses:
                    print(f"   Intereses agregados: {', '.join(intereses)}")

        elif opcion == '11':
            id_est = input("\n📝 ID del estudiante a eliminar: ").strip()
            if id_est in grafo.estudiantes:
                nombre = grafo.estudiantes[id_est]['nombre']
                confirmar = input(f"⚠️  Confirmar eliminacion de {nombre}? (s/n): ").strip().lower()
                if confirmar == 's':
                    grafo.eliminar_estudiante(id_est)
                    print(f"✅ Estudiante {nombre} eliminado exitosamente")
                else:
                    print("❌ Operacion cancelada")
            else:
                print("❌ Error: Estudiante no encontrado")

        elif opcion == '12':
            id_est = input("\n📝 ID del estudiante a modificar: ").strip()
            if id_est in grafo.estudiantes:
                info = grafo.estudiantes[id_est]
                print(f"\nDatos actuales:")
                print(f"  Nombre: {info['nombre']}")
                print(f"  Carrera: {info['carrera']}")
                
                nuevo_nombre = input("\n📝 Nuevo nombre (Enter para mantener): ").strip()
                nueva_carrera = input("📝 Nueva carrera (Enter para mantener): ").strip()
                
                if nuevo_nombre:
                    info['nombre'] = nuevo_nombre
                if nueva_carrera:
                    info['carrera'] = nueva_carrera
                
                print("✅ Datos actualizados exitosamente")
            else:
                print("❌ Error: Estudiante no encontrado")

        elif opcion == '13':
            id_est = input("\n📝 ID del estudiante: ").strip()
            if id_est in grafo.estudiantes:
                info = grafo.estudiantes[id_est]
                intereses = info.get('intereses', [])
                
                print(f"\nIntereses actuales de {info['nombre']}:")
                if intereses:
                    for i, interes in enumerate(intereses, 1):
                        print(f"  {i}. {interes}")
                else:
                    print("  No tiene intereses registrados")
                
                print("\n¿Que desea hacer?")
                print("  1. Agregar interes")
                print("  2. Eliminar interes")
                sub_opcion = input("Opcion: ").strip()
                
                if sub_opcion == '1':
                    nuevo_interes = input("📝 Nuevo interes: ").strip()
                    if nuevo_interes:
                        if 'intereses' not in info:
                            info['intereses'] = []
                        if nuevo_interes not in info['intereses']:
                            info['intereses'].append(nuevo_interes)
                            print(f"✅ Interes '{nuevo_interes}' agregado")
                        else:
                            print("❌ Este interes ya existe")
                elif sub_opcion == '2':
                    if intereses:
                        num = input("Numero del interes a eliminar: ").strip()
                        if num.isdigit() and 1 <= int(num) <= len(intereses):
                            eliminado = intereses.pop(int(num) - 1)
                            print(f"✅ Interes '{eliminado}' eliminado")
                        else:
                            print("❌ Numero invalido")
                    else:
                        print("❌ No hay intereses para eliminar")
            else:
                print("❌ Error: Estudiante no encontrado")

        # =============== GESTION DE AMISTADES ===============
        elif opcion == '14':
            print("\n" + "="*70)
            print(" "*25 + "AGREGAR AMISTAD")
            print("="*70)
            id1 = input("📝 ID del primer estudiante: ").strip()
            id2 = input("📝 ID del segundo estudiante: ").strip()
            if id1 == id2:
                print("❌ Error: No puede crear amistad consigo mismo")
            elif grafo.son_amigos(id1, id2):
                print("❌ Error: Ya existe una amistad entre estos estudiantes")
            else:
                print("\nNivel de amistad:")
                print("  1 = Normal")
                print("  2 = Mejor amigo")
                print("  3 = Amigo cercano")
                peso = input("Seleccione nivel [1]: ").strip()
                peso = int(peso) if peso.isdigit() and int(peso) in [1, 2, 3] else 1
                if grafo.agregar_amistad(id1, id2, peso):
                    print("✅ Amistad agregada exitosamente")
                else:
                    print("❌ Error: Uno o ambos estudiantes no existen")

        elif opcion == '15':
            print("\n" + "="*70)
            print(" "*25 + "ELIMINAR AMISTAD")
            print("="*70)
            id1 = input("📝 ID del primer estudiante: ").strip()
            id2 = input("📝 ID del segundo estudiante: ").strip()
            if grafo.eliminar_amistad(id1, id2):
                print("✅ Amistad eliminada exitosamente")
            else:
                print("❌ Error: No existe amistad entre estos estudiantes")

        elif opcion == '16':
            print("\n" + "="*70)
            print(" "*20 + "MODIFICAR PESO DE AMISTAD")
            print("="*70)
            id1 = input("📝 ID del primer estudiante: ").strip()
            id2 = input("📝 ID del segundo estudiante: ").strip()
            if not grafo.son_amigos(id1, id2):
                print("❌ Error: No existe amistad entre estos estudiantes")
            else:
                peso_actual = grafo.obtener_peso_amistad(id1, id2)
                print(f"\n📊 Peso actual: {peso_actual}")
                print("\nNivel de amistad:")
                print("  1 = Normal")
                print("  2 = Mejor amigo")
                print("  3 = Amigo cercano")
                nuevo_peso = input("📝 Nuevo nivel: ").strip()
                if nuevo_peso.isdigit() and int(nuevo_peso) in [1, 2, 3]:
                    grafo.actualizar_peso_amistad(id1, id2, int(nuevo_peso))
                    print("✅ Peso actualizado exitosamente")
                else:
                    print("❌ Error: Peso invalido")

        # =============== ANALISIS AVANZADO ===============
        elif opcion == '17':
            print("\n" + "="*70)
            print(" "*20 + "ESTADISTICAS GENERALES")
            print("="*70)
            mostrar_estadisticas(grafo)

        elif opcion == '18':
            print("\n" + "="*70)
            print(" "*20 + "DETECCION DE COMUNIDADES")
            print("="*70)
            if len(grafo.estudiantes) < 3:
                print("❌ Se necesitan al menos 3 estudiantes para detectar comunidades")
            else:
                try:
                    print("🔍 Detectando comunidades con algoritmo de Louvain...")
                    comunidades = detectar_comunidades_louvain(grafo)
                    stats = estadisticas_comunidades(grafo, comunidades)
                    
                    print(f"\n✅ Comunidades detectadas: {len(stats)}\n")
                    
                    for com_id, info in stats.items():
                        print(f"\n{'='*70}")
                        print(f"Comunidad #{com_id + 1}")
                        print(f"{'='*70}")
                        print(f"👥 Tamano: {info['tamano']} miembros")
                        print(f"🔗 Conexiones internas: {info['conexiones_internas']}")
                        print(f"🎓 Carreras:")
                        for carrera, count in list(info['carreras'].items())[:5]:
                            print(f"    • {carrera}: {count}")
                        print(f"👤 Miembros:")
                        miembros_nombres = [grafo.estudiantes[id]['nombre'] for id in info['miembros'][:8]]
                        for nombre in miembros_nombres:
                            print(f"    • {nombre}")
                        if len(info['miembros']) > 8:
                            print(f"    ... y {len(info['miembros']) - 8} miembros mas")
                except Exception as e:
                    print(f"❌ Error al detectar comunidades: {e}")

        elif opcion == '19':
            print("\n" + "="*70)
            print(" "*20 + "CENTRALIDAD DE NODOS")
            print("="*70)
            print("\n¿Que tipo de centralidad desea calcular?")
            print("  1. Centralidad de Grado")
            print("  2. Centralidad de Intermediacion")
            print("  3. Centralidad de Cercania")
            print("  4. Centralidad Eigenvector")
            print("  5. Todas las anteriores")
            
            sub_opcion = input("\nOpcion: ").strip()
            
            try:
                if sub_opcion in ['1', '5']:
                    print(f"\n{'='*70}")
                    print("📊 CENTRALIDAD DE GRADO (Top 10)")
                    print(f"{'='*70}")
                    c_grado = calcular_centralidad_grado(grafo)
                    for id_est, valor in obtener_nodos_mas_centrales(c_grado, 10):
                        print(f"  • {grafo.estudiantes[id_est]['nombre']:30} → {valor} conexiones")
                
                if sub_opcion in ['2', '5']:
                    print(f"\n{'='*70}")
                    print("📊 CENTRALIDAD DE INTERMEDIACION (Top 10)")
                    print(f"{'='*70}")
                    c_inter = calcular_centralidad_intermediacion(grafo)
                    for id_est, valor in obtener_nodos_mas_centrales(c_inter, 10):
                        print(f"  • {grafo.estudiantes[id_est]['nombre']:30} → {valor:.4f}")
                
                if sub_opcion in ['3', '5']:
                    print(f"\n{'='*70}")
                    print("📊 CENTRALIDAD DE CERCANIA (Top 10)")
                    print(f"{'='*70}")
                    c_cerca = calcular_centralidad_cercania(grafo)
                    for id_est, valor in obtener_nodos_mas_centrales(c_cerca, 10):
                        print(f"  • {grafo.estudiantes[id_est]['nombre']:30} → {valor:.4f}")
                
                if sub_opcion in ['4', '5']:
                    print(f"\n{'='*70}")
                    print("📊 CENTRALIDAD EIGENVECTOR (Top 10)")
                    print(f"{'='*70}")
                    c_eigen = calcular_centralidad_eigenvector(grafo)
                    for id_est, valor in obtener_nodos_mas_centrales(c_eigen, 10):
                        print(f"  • {grafo.estudiantes[id_est]['nombre']:30} → {valor:.4f}")
                
                if sub_opcion not in ['1', '2', '3', '4', '5']:
                    print("❌ Opcion invalida")
            except Exception as e:
                print(f"❌ Error al calcular centralidad: {e}")

        elif opcion == '20':
            print("\n" + "="*70)
            print(" "*15 + "ANALISIS DE NODOS MAS INFLUYENTES")
            print("="*70)
            try:
                print("\n🔍 Calculando metricas de centralidad...")
                
                c_grado = calcular_centralidad_grado(grafo)
                c_inter = calcular_centralidad_intermediacion(grafo)
                c_cerca = calcular_centralidad_cercania(grafo)
                c_eigen = calcular_centralidad_eigenvector(grafo)
                
                top_5_grado = obtener_nodos_mas_centrales(c_grado, 5)
                top_5_inter = obtener_nodos_mas_centrales(c_inter, 5)
                top_5_cerca = obtener_nodos_mas_centrales(c_cerca, 5)
                top_5_eigen = obtener_nodos_mas_centrales(c_eigen, 5)
                
                # Calcular puntuacion combinada
                puntuaciones = {}
                for id_est in grafo.estudiantes:
                    puntuacion = 0
                    # Sumar posiciones en cada ranking (menor es mejor)
                    for i, (nodo, _) in enumerate(top_5_grado):
                        if nodo == id_est:
                            puntuacion += (5 - i) * 4
                    for i, (nodo, _) in enumerate(top_5_inter):
                        if nodo == id_est:
                            puntuacion += (5 - i) * 3
                    for i, (nodo, _) in enumerate(top_5_cerca):
                        if nodo == id_est:
                            puntuacion += (5 - i) * 2
                    for i, (nodo, _) in enumerate(top_5_eigen):
                        if nodo == id_est:
                            puntuacion += (5 - i) * 1
                    if puntuacion > 0:
                        puntuaciones[id_est] = puntuacion
                
                top_influyentes = sorted(puntuaciones.items(), key=lambda x: x[1], reverse=True)[:10]
                
                print(f"\n{'='*70}")
                print("🌟 TOP 10 NODOS MAS INFLUYENTES")
                print(f"{'='*70}")
                for i, (id_est, puntuacion) in enumerate(top_influyentes, 1):
                    info = grafo.estudiantes[id_est]
                    amigos = len(grafo.obtener_amigos(id_est))
                    print(f"\n{i}. {info['nombre']}")
                    print(f"   Carrera: {info['carrera']}")
                    print(f"   Amigos: {amigos}")
                    print(f"   📊 Puntuacion de influencia: {puntuacion}")
                    
            except Exception as e:
                print(f"❌ Error al analizar nodos influyentes: {e}")

        # =============== VISUALIZACION ===============
        elif opcion == '21':
            if not grafo.estudiantes:
                print("❌ Error: No hay estudiantes para visualizar")
            else:
                print("\n🎨 Generando visualizacion del grafo...")
                try:
                    visualizar_grafo(grafo)
                    print("✅ Visualizacion generada exitosamente")
                except Exception as e:
                    print(f"❌ Error al generar visualizacion: {e}")

        elif opcion == '22':
            if not grafo.estudiantes:
                print("❌ Error: No hay datos para generar el reporte")
            else:
                nombre_archivo = input("\n📝 Nombre del archivo PDF [reporte.pdf]: ").strip()
                if not nombre_archivo:
                    nombre_archivo = "reporte.pdf"
                if not nombre_archivo.endswith('.pdf'):
                    nombre_archivo += '.pdf'
                
                print("\n📄 Generando reporte PDF...")
                print("   (Esto puede tomar unos segundos...)")
                try:
                    if generar_reporte_pdf(grafo, nombre_archivo, incluir_grafico=True):
                        print(f"✅ Reporte generado exitosamente: {nombre_archivo}")
                    else:
                        print("❌ Error al generar el reporte")
                except Exception as e:
                    print(f"❌ Error: {e}")

        # =============== DATOS Y PERSISTENCIA ===============
        elif opcion == '23':
            print("\n" + "="*70)
            print(" "*25 + "GUARDAR EN CSV")
            print("="*70)
            try:
                if guardar_datos(grafo):
                    print("✅ Datos guardados exitosamente en CSV")
                else:
                    print("❌ Error al guardar los datos")
            except Exception as e:
                print(f"❌ Error: {e}")

        elif opcion == '24':
            nombre_archivo = input("\n📝 Nombre del archivo JSON [red.json]: ").strip()
            if not nombre_archivo:
                nombre_archivo = "red.json"
            if not nombre_archivo.endswith('.json'):
                nombre_archivo += '.json'
            
            try:
                if guardar_json(grafo, nombre_archivo):
                    print(f"✅ Datos guardados exitosamente en {nombre_archivo}")
                else:
                    print("❌ Error al guardar los datos")
            except Exception as e:
                print(f"❌ Error: {e}")

        elif opcion == '25':
            nombre_archivo = input("\n📝 Nombre del archivo JSON a cargar: ").strip()
            if not nombre_archivo.endswith('.json'):
                nombre_archivo += '.json'
            
            print("⚠️  ADVERTENCIA: Esto reemplazara todos los datos actuales")
            confirmar = input("¿Continuar? (s/n): ").strip().lower()
            if confirmar == 's':
                try:
                    if cargar_json(grafo, nombre_archivo):
                        print(f"✅ Datos cargados exitosamente desde {nombre_archivo}")
                        print(f"   Estudiantes cargados: {len(grafo.estudiantes)}")
                    else:
                        print("❌ Error al cargar los datos")
                except Exception as e:
                    print(f"❌ Error: {e}")
            else:
                print("❌ Operacion cancelada")

        elif opcion == '26':
            print("\n💾 Creando backup de la red...")
            try:
                if exportar_backup(grafo):
                    print("✅ Backup creado exitosamente en el directorio 'backups/'")
                else:
                    print("❌ Error al crear el backup")
            except Exception as e:
                print(f"❌ Error: {e}")

        elif opcion == '27':
            print("\n" + "="*70)
            print(" "*20 + "GENERAR DATOS ALEATORIOS")
            print("="*70)
            print("⚠️  ADVERTENCIA: Esto eliminara todos los datos actuales")
            confirmar = input("¿Continuar? (s/n): ").strip().lower()
            if confirmar == 's':
                num_est = input("📝 Numero de estudiantes [30]: ").strip()
                num_est = int(num_est) if num_est.isdigit() and int(num_est) > 0 else 30
                densidad = input("📝 Densidad de amistades (0.0-1.0) [0.15]: ").strip()
                try:
                    densidad = float(densidad) if densidad else 0.15
                    densidad = max(0.0, min(1.0, densidad))
                except:
                    densidad = 0.15
                
                # Limpiar grafo actual
                grafo.estudiantes.clear()
                grafo.adj_list.clear()
                
                print(f"\n🔄 Generando {num_est} estudiantes con densidad {densidad}...")
                generar_datos_aleatorios(grafo, num_est, densidad)
                print("✅ Datos aleatorios generados exitosamente")
                print(f"   Estudiantes: {len(grafo.estudiantes)}")
                print(f"   Amistades: {sum(len(amigos) for amigos in grafo.adj_list.values()) // 2}")
            else:
                print("❌ Operacion cancelada")

        elif opcion == '0':
            print("\n" + "="*70)
            print(" "*25 + "CERRANDO SISTEMA")
            print("="*70)
            guardar = input("\n💾 ¿Guardar cambios antes de salir? (s/n): ").strip().lower()
            if guardar == 's':
                print("\n¿En que formato desea guardar?")
                print("  1. CSV")
                print("  2. JSON")
                print("  3. Ambos")
                formato = input("Opcion [3]: ").strip()
                
                try:
                    if formato in ['1', '3', '']:
                        guardar_datos(grafo)
                        print("✅ Guardado en CSV")
                    if formato in ['2', '3', '']:
                        guardar_json(grafo, 'red_backup.json')
                        print("✅ Guardado en JSON")
                except Exception as e:
                    print(f"❌ Error al guardar: {e}")
            
            print("\n👋 ¡Hasta luego!")
            print("="*70)
            break

        else:
            print("❌ Error: Opcion no valida")
            print("   Por favor, seleccione una opcion entre 0 y 27")

def main():
    """Punto de entrada principal del sistema"""
    print("\n" + "="*70)
    print(" "*15 + "SISTEMA DE GESTION DE RED UNIVERSITARIA")
    print(" "*25 + "Version 2.0 - Menu Completo")
    print("="*70)
    
    red_universitaria = Grafo()
    
    # Intentar cargar datos existentes
    print("\n🔍 Buscando archivos de datos...")
    if not cargar_datos(red_universitaria, 'estudiantes.csv', 'amistades.csv'):
        print("❌ No se encontraron archivos CSV.")
        
        # Intentar cargar desde JSON
        try:
            if cargar_json(red_universitaria, 'ejemplo_red.json'):
                print("✅ Datos cargados desde ejemplo_red.json")
            else:
                print("\n📋 No hay datos disponibles.")
                opcion = input("¿Desea generar datos aleatorios para pruebas? (s/n): ").strip().lower()
                if opcion == 's':
                    generar_datos_aleatorios(red_universitaria, 20, 0.2)
                    guardar_datos(red_universitaria)
                    print("✅ Datos generados y guardados")
                else:
                    print("⚠️  Iniciando con red vacia...")
        except:
            print("\n📋 No hay datos disponibles.")
            opcion = input("¿Desea generar datos aleatorios para pruebas? (s/n): ").strip().lower()
            if opcion == 's':
                generar_datos_aleatorios(red_universitaria, 20, 0.2)
                guardar_datos(red_universitaria)
                print("✅ Datos generados y guardados")
            else:
                print("⚠️  Iniciando con red vacia...")
    else:
        print("✅ Datos cargados desde archivos CSV")
    
    print(f"\n📊 Red cargada:")
    print(f"   • Estudiantes: {len(red_universitaria.estudiantes)}")
    print(f"   • Amistades: {sum(len(amigos) for amigos in red_universitaria.adj_list.values()) // 2}")
    
    input("\n📌 Presione ENTER para continuar...")
    
    # Ejecutar interfaz
    interfaz_principal(red_universitaria)

if __name__ == "__main__":
    main()
