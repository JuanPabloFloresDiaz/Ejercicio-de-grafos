def mostrar_estadisticas(grafo):
    """Muestra estadisticas basicas del grafo"""
    print("\n" + "="*50)
    print("ESTADISTICAS DE LA RED")
    print("="*50)
    
    num_estudiantes = len(grafo.estudiantes)
    if num_estudiantes == 0:
        print("No hay estudiantes en la red")
        return
    
    num_amistades = sum(len(amigos) for amigos in grafo.adj_list.values()) // 2
    
    print(f"Total de estudiantes: {num_estudiantes}")
    print(f"Total de amistades: {num_amistades}")
    
    if num_amistades > 0:
        print(f"Promedio de amigos por estudiante: {num_amistades*2/num_estudiantes:.2f}")
    
    # Estudiantes por carrera
    carreras = {}
    for info in grafo.estudiantes.values():
        carrera = info['carrera']
        carreras[carrera] = carreras.get(carrera, 0) + 1
    
    print("\nEstudiantes por carrera:")
    for carrera, cantidad in sorted(carreras.items(), key=lambda x: x[1], reverse=True):
        print(f"  {carrera}: {cantidad} estudiantes")
    
    # Estudiantes mas populares
    popularidad = []
    for id_est in grafo.estudiantes:
        num_amigos = len(grafo.obtener_amigos(id_est))
        popularidad.append((grafo.estudiantes[id_est]['nombre'], num_amigos))
    
    popularidad.sort(key=lambda x: x[1], reverse=True)
    print("\nEstudiantes mas populares:")
    for nombre, amigos in popularidad[:5]:
        print(f"  {nombre}: {amigos} amigos")
    
    # Distribucion de pesos de amistades
    pesos = {}
    for id1 in grafo.adj_list:
        for id2, peso in grafo.adj_list[id1].items():
            pesos[peso] = pesos.get(peso, 0) + 1
    
    if pesos:
        print("\nDistribucion de intensidad de amistades:")
        for peso, cantidad in sorted(pesos.items()):
            tipo = "Normal" if peso == 1 else "Mejor amigo" if peso == 2 else "Amigo cercano"
            print(f"  Nivel {peso} ({tipo}): {cantidad // 2} amistades")
