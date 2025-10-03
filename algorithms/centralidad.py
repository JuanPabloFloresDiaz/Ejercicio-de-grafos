import networkx as nx

def calcular_centralidad_grado(grafo):
    """Calcula la centralidad de grado para cada nodo"""
    centralidad = {}
    for id_est in grafo.estudiantes:
        centralidad[id_est] = len(grafo.obtener_amigos(id_est))
    return centralidad

def calcular_centralidad_intermediacion(grafo):
    """Calcula la centralidad de intermediacion (betweenness)"""
    G = nx.Graph()
    
    for id_est in grafo.estudiantes:
        G.add_node(id_est)
    
    for id1 in grafo.adj_list:
        for id2, peso in grafo.adj_list[id1].items():
            G.add_edge(id1, id2, weight=peso)
    
    return nx.betweenness_centrality(G, weight='weight')

def calcular_centralidad_cercania(grafo):
    """Calcula la centralidad de cercania (closeness)"""
    G = nx.Graph()
    
    for id_est in grafo.estudiantes:
        G.add_node(id_est)
    
    for id1 in grafo.adj_list:
        for id2, peso in grafo.adj_list[id1].items():
            G.add_edge(id1, id2, weight=peso)
    
    return nx.closeness_centrality(G, distance='weight')

def calcular_centralidad_eigenvector(grafo):
    """Calcula la centralidad de vector propio (eigenvector)"""
    G = nx.Graph()
    
    for id_est in grafo.estudiantes:
        G.add_node(id_est)
    
    for id1 in grafo.adj_list:
        for id2, peso in grafo.adj_list[id1].items():
            G.add_edge(id1, id2, weight=peso)
    
    try:
        return nx.eigenvector_centrality(G, weight='weight', max_iter=1000)
    except:
        # Si no converge, retornar centralidad de grado normalizada
        return calcular_centralidad_grado(grafo)

def obtener_nodos_mas_centrales(centralidad, top_n=5):
    """Retorna los top N nodos mas centrales"""
    return sorted(centralidad.items(), key=lambda x: x[1], reverse=True)[:top_n]
