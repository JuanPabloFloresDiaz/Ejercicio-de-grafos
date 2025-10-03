import matplotlib.pyplot as plt
import networkx as nx

LAYOUTS = {
    'spring': lambda G: nx.spring_layout(G, k=1.5, iterations=50),
    'circular': lambda G: nx.circular_layout(G),
    'kamada_kawai': lambda G: nx.kamada_kawai_layout(G),
    'shell': lambda G: nx.shell_layout(G),
    'spectral': lambda G: nx.spectral_layout(G),
    'random': lambda G: nx.random_layout(G)
}

def visualizar_grafo_avanzado(grafo, layout='spring', mostrar_pesos=True, mostrar_comunidades=False, comunidades=None):
    """
    Visualiza el grafo con opciones avanzadas de layout y estilo
    
    Args:
        grafo: Instancia del grafo
        layout: Tipo de layout ('spring', 'circular', 'kamada_kawai', 'shell', 'spectral', 'random')
        mostrar_pesos: Si mostrar los pesos de las aristas
        mostrar_comunidades: Si colorear nodos por comunidades
        comunidades: Diccionario de comunidades (id_est: comunidad)
    """
    G = nx.Graph()
    
    # Agregar nodos
    for id_est, info in grafo.estudiantes.items():
        G.add_node(id_est, nombre=info['nombre'], carrera=info['carrera'])
    
    # Agregar aristas con pesos
    for id1 in grafo.adj_list:
        for id2, peso in grafo.adj_list[id1].items():
            if not G.has_edge(id1, id2):
                G.add_edge(id1, id2, weight=peso)
    
    plt.figure(figsize=(16, 12))
    
    # Obtener layout
    if layout in LAYOUTS:
        pos = LAYOUTS[layout](G)
    else:
        pos = LAYOUTS['spring'](G)
    
    # Determinar colores de nodos
    if mostrar_comunidades and comunidades:
        # Colorear por comunidades
        num_comunidades = len(set(comunidades.values()))
        colores_comunidades = plt.cm.Set3(range(num_comunidades))
        node_colors = [colores_comunidades[comunidades.get(id_est, 0)] for id_est in G.nodes()]
    else:
        # Colorear por carrera
        carreras = list(set(info['carrera'] for info in grafo.estudiantes.values()))
        colores_disponibles = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E2']
        color_map = {}
        
        for i, carrera in enumerate(carreras):
            color_map[carrera] = colores_disponibles[i % len(colores_disponibles)]
        
        node_colors = [color_map[grafo.estudiantes[id_est]['carrera']] for id_est in G.nodes()]
    
    # Dibujar nodos
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=1200, alpha=0.9, edgecolors='black', linewidths=2)
    
    # Dibujar etiquetas
    labels = {id_est: grafo.estudiantes[id_est]['nombre'].split()[0] for id_est in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels, font_size=10, font_weight='bold')
    
    # Dibujar aristas con grosor segun peso
    edges = G.edges()
    weights = [G[u][v]['weight'] for u, v in edges]
    nx.draw_networkx_edges(G, pos, width=[w * 2 for w in weights], alpha=0.6, edge_color='gray')
    
    # Mostrar pesos en aristas
    if mostrar_pesos:
        edge_labels = {(u, v): f"{G[u][v]['weight']}" for u, v in G.edges() if G[u][v]['weight'] > 1}
        nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=8)
    
    # Leyenda
    if mostrar_comunidades and comunidades:
        for i in range(num_comunidades):
            plt.plot([], [], 'o', color=colores_comunidades[i], label=f'Comunidad {i+1}', markersize=10)
    else:
        for carrera, color in color_map.items():
            plt.plot([], [], 'o', color=color, label=carrera, markersize=10)
    
    plt.legend(loc='upper left', fontsize=10, framealpha=0.9)
    
    titulo = f"Red de Amistades - Layout: {layout.capitalize()}"
    if mostrar_comunidades:
        titulo += " (Comunidades)"
    
    plt.title(titulo, fontsize=18, fontweight='bold', pad=20)
    plt.axis('off')
    plt.tight_layout()
    plt.show()

def visualizar_grafo(grafo):
    """Visualizacion basica para compatibilidad"""
    visualizar_grafo_avanzado(grafo, layout='spring', mostrar_pesos=True)
