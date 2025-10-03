"""
Algoritmo de deteccion de comunidades usando Louvain
"""
import networkx as nx
from collections import defaultdict

def detectar_comunidades_louvain(grafo):
    """
    Detecta comunidades en el grafo usando el algoritmo de Louvain
    Retorna diccionario con id_estudiante: comunidad
    """
    if not grafo.estudiantes:
        return {}
    
    # Crear grafo de NetworkX
    G = nx.Graph()
    
    for id_est in grafo.estudiantes:
        G.add_node(id_est)
    
    for id1 in grafo.adj_list:
        for id2, peso in grafo.adj_list[id1].items():
            G.add_edge(id1, id2, weight=peso)
    
    # Usar algoritmo de Louvain (greedy modularity)
    try:
        from networkx.algorithms import community
        comunidades = community.greedy_modularity_communities(G, weight='weight')
        
        # Convertir a diccionario
        resultado = {}
        for i, comunidad in enumerate(comunidades):
            for nodo in comunidad:
                resultado[nodo] = i
        
        return resultado
    except ImportError:
        # Fallback: usar componentes conectados
        componentes = nx.connected_components(G)
        resultado = {}
        for i, componente in enumerate(componentes):
            for nodo in componente:
                resultado[nodo] = i
        return resultado

def estadisticas_comunidades(grafo, comunidades):
    """
    Calcula estadisticas sobre las comunidades detectadas
    """
    if not comunidades:
        return {}
    
    stats = defaultdict(lambda: {
        'tamano': 0,
        'carreras': defaultdict(int),
        'miembros': []
    })
    
    for id_est, comunidad in comunidades.items():
        stats[comunidad]['tamano'] += 1
        stats[comunidad]['miembros'].append(id_est)
        carrera = grafo.estudiantes[id_est]['carrera']
        stats[comunidad]['carreras'][carrera] += 1
    
    return dict(stats)
