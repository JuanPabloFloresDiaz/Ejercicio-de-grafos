from collections import deque

def bfs(grafo, id_inicio):
    """
    Busqueda en anchura (BFS) desde un nodo inicial
    Retorna lista de IDs en orden de visita
    """
    if id_inicio not in grafo.estudiantes:
        return []
    
    visitados = []
    cola = deque([id_inicio])
    visitado_set = {id_inicio}
    
    while cola:
        actual = cola.popleft()
        visitados.append(actual)
        
        for vecino in grafo.obtener_amigos(actual):
            if vecino not in visitado_set:
                visitado_set.add(vecino)
                cola.append(vecino)
    
    return visitados

def dfs(grafo, id_inicio, visitados=None):
    """
    Busqueda en profundidad (DFS) desde un nodo inicial
    Retorna lista de IDs en orden de visita
    """
    if id_inicio not in grafo.estudiantes:
        return []
    
    if visitados is None:
        visitados = []
    
    visitados.append(id_inicio)
    
    for vecino in grafo.obtener_amigos(id_inicio):
        if vecino not in visitados:
            dfs(grafo, vecino, visitados)
    
    return visitados

def camino_mas_corto(grafo, id_inicio, id_fin):
    """
    Encuentra el camino mas corto entre dos estudiantes usando BFS
    Retorna lista de nombres del camino o None si no existe
    """
    if id_inicio not in grafo.estudiantes or id_fin not in grafo.estudiantes:
        return None
    
    if id_inicio == id_fin:
        return [grafo.estudiantes[id_inicio]['nombre']]
    
    visitado = set()
    cola = deque([(id_inicio, [id_inicio])])
    
    while cola:
        actual, camino = cola.popleft()
        
        if actual == id_fin:
            return [grafo.estudiantes[id]['nombre'] for id in camino]
        
        visitado.add(actual)
        for vecino in grafo.obtener_amigos(actual):
            if vecino not in visitado:
                cola.append((vecino, camino + [vecino]))
                visitado.add(vecino)
    
    return None
