import matplotlib.pyplot as plt
import networkx as nx

def visualizar_grafo(grafo):
    """Visualiza el grafo usando networkx y matplotlib"""
    G = nx.Graph()
    
    # Agregar nodos
    for id_est, info in grafo.estudiantes.items():
        G.add_node(info['nombre'], carrera=info['carrera'])
    
    # Agregar aristas con pesos
    for id1 in grafo.adj_list:
        for id2, peso in grafo.adj_list[id1].items():
            nombre1 = grafo.estudiantes[id1]['nombre']
            nombre2 = grafo.estudiantes[id2]['nombre']
            G.add_edge(nombre1, nombre2, weight=peso)
    
    plt.figure(figsize=(14, 10))
    
    # Colores por carrera
    carreras = list(set(info['carrera'] for info in grafo.estudiantes.values()))
    colores_disponibles = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#F7DC6F']
    color_map = {}
    
    for i, carrera in enumerate(carreras):
        color_map[carrera] = colores_disponibles[i % len(colores_disponibles)]
    
    node_colors = [color_map[grafo.estudiantes[id]['carrera']] for id in grafo.estudiantes]
    
    # Layout
    pos = nx.spring_layout(G, k=1.5, iterations=50)
    
    # Dibujar nodos
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=1000, alpha=0.9)
    
    # Dibujar etiquetas
    nx.draw_networkx_labels(G, pos, font_size=9, font_weight='bold')
    
    # Dibujar aristas con grosor segun peso
    edges = G.edges()
    weights = [G[u][v]['weight'] for u, v in edges]
    nx.draw_networkx_edges(G, pos, width=[w * 1.5 for w in weights], alpha=0.5)
    
    # Leyenda
    for carrera, color in color_map.items():
        plt.plot([], [], 'o', color=color, label=carrera, markersize=10)
    plt.legend(loc='upper left', fontsize=10)
    
    plt.title("Red de Amistades Universitarias", fontsize=16, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()
    plt.show()
