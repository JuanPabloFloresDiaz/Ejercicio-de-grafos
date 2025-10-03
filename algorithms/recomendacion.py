def recomendar_amistades(grafo, id_estudiante, max_recomendaciones=5):
    """
    Recomienda amistades basandose en:
    - Amigos en comun (peso x2)
    - Misma carrera (+1 punto)
    - Peso de amistades existentes (mejores amigos pesan mas)
    """
    if id_estudiante not in grafo.estudiantes:
        return []
    
    recomendaciones = {}
    amigos_actuales = set(grafo.obtener_amigos(id_estudiante))
    carrera_estudiante = grafo.estudiantes[id_estudiante]['carrera']
    
    for posible_amigo in grafo.estudiantes:
        if posible_amigo == id_estudiante or posible_amigo in amigos_actuales:
            continue
        
        amigos_posible = set(grafo.obtener_amigos(posible_amigo))
        amigos_comunes = amigos_actuales.intersection(amigos_posible)
        
        # Calcular puntaje base
        puntaje = len(amigos_comunes) * 2
        
        # Bonus por peso de amistades comunes (si son mejores amigos)
        for amigo_comun in amigos_comunes:
            peso = grafo.obtener_peso_amistad(id_estudiante, amigo_comun)
            if peso and peso > 1:
                puntaje += (peso - 1) * 0.5
        
        # Bonus por misma carrera
        if grafo.estudiantes[posible_amigo]['carrera'] == carrera_estudiante:
            puntaje += 1
        
        if puntaje > 0:
            recomendaciones[posible_amigo] = {
                'puntaje': puntaje,
                'amigos_comunes': len(amigos_comunes),
                'misma_carrera': grafo.estudiantes[posible_amigo]['carrera'] == carrera_estudiante
            }
    
    recomendaciones_ordenadas = sorted(
        recomendaciones.items(),
        key=lambda x: x[1]['puntaje'],
        reverse=True
    )[:max_recomendaciones]
    
    return recomendaciones_ordenadas
