"""
Módulo para calcular métricas de centralidad en grafos de redes sociales.
Incluye centralidad de intermediación, cercanía, eigenvector y de grado.
"""

import networkx as nx
from collections import defaultdict


class CentralidadCalculator:
    """Clase para calcular diferentes métricas de centralidad en un grafo"""
    
    def __init__(self, grafo):
        """Inicializa el calculador con un grafo de estudiantes"""
        self.grafo = grafo
        self.nx_graph = self._convertir_a_networkx()
    
    def _convertir_a_networkx(self):
        """Convierte el grafo personalizado a NetworkX para usar sus algoritmos"""
        G = nx.Graph()
        
        # Agregar nodos
        for id_estudiante, info in self.grafo.estudiantes.items():
            G.add_node(id_estudiante, **info)
        
        # Agregar aristas
        for id1 in self.grafo.adj_list:
            for id2 in self.grafo.adj_list[id1]:
                if not G.has_edge(id1, id2):  # Evitar duplicados
                    G.add_edge(id1, id2)
        
        return G
    
    def calcular_centralidad_grado(self):
        """
        Calcula la centralidad de grado (número de conexiones directas)
        Retorna: dict con {id_estudiante: centralidad}
        """
        centralidad = {}
        for id_estudiante in self.grafo.estudiantes:
            centralidad[id_estudiante] = len(self.grafo.obtener_amigos(id_estudiante))
        return centralidad
    
    def calcular_centralidad_intermediacion(self):
        """
        Calcula la centralidad de intermediación (betweenness centrality)
        Mide qué tan importante es un nodo para conectar otros nodos
        """
        if len(self.nx_graph.nodes()) < 3:
            return {node: 0.0 for node in self.nx_graph.nodes()}
        return nx.betweenness_centrality(self.nx_graph)
    
    def calcular_centralidad_cercania(self):
        """
        Calcula la centralidad de cercanía (closeness centrality)
        Mide qué tan cerca está un nodo de todos los demás
        """
        if not nx.is_connected(self.nx_graph):
            # Para grafos no conectados, calcular por componentes
            centralidad = {}
            for component in nx.connected_components(self.nx_graph):
                subgrafo = self.nx_graph.subgraph(component)
                if len(subgrafo.nodes()) > 1:
                    centrality_component = nx.closeness_centrality(subgrafo)
                    centralidad.update(centrality_component)
                else:
                    centralidad.update({node: 0.0 for node in component})
            return centralidad
        return nx.closeness_centrality(self.nx_graph)
    
    def calcular_centralidad_eigenvector(self):
        """
        Calcula la centralidad de eigenvector
        Mide la influencia de un nodo basándose en la importancia de sus conexiones
        """
        try:
            if not nx.is_connected(self.nx_graph):
                # Para grafos no conectados, usar el componente más grande
                componentes = list(nx.connected_components(self.nx_graph))
                componente_principal = max(componentes, key=len)
                subgrafo = self.nx_graph.subgraph(componente_principal)
                
                centralidad = {}
                if len(subgrafo.nodes()) > 1:
                    centrality_component = nx.eigenvector_centrality(subgrafo, max_iter=1000)
                    centralidad.update(centrality_component)
                
                # Asignar 0 a nodos no conectados al componente principal
                for node in self.nx_graph.nodes():
                    if node not in centralidad:
                        centralidad[node] = 0.0
                
                return centralidad
            
            return nx.eigenvector_centrality(self.nx_graph, max_iter=1000)
        except nx.PowerIterationFailedConvergence:
            # Si no converge, usar valores uniformes
            return {node: 1.0/len(self.nx_graph.nodes()) for node in self.nx_graph.nodes()}
    
    def calcular_todas_centralidades(self):
        """
        Calcula todas las métricas de centralidad
        Retorna: dict con todas las métricas organizadas por estudiante
        """
        centralidades = {
            'grado': self.calcular_centralidad_grado(),
            'intermediacion': self.calcular_centralidad_intermediacion(),
            'cercania': self.calcular_centralidad_cercania(),
            'eigenvector': self.calcular_centralidad_eigenvector()
        }
        
        # Reorganizar por estudiante
        resultado = {}
        for id_estudiante in self.grafo.estudiantes:
            resultado[id_estudiante] = {
                'nombre': self.grafo.estudiantes[id_estudiante]['nombre'],
                'carrera': self.grafo.estudiantes[id_estudiante]['carrera'],
                'centralidad_grado': centralidades['grado'].get(id_estudiante, 0),
                'centralidad_intermediacion': centralidades['intermediacion'].get(id_estudiante, 0.0),
                'centralidad_cercania': centralidades['cercania'].get(id_estudiante, 0.0),
                'centralidad_eigenvector': centralidades['eigenvector'].get(id_estudiante, 0.0)
            }
        
        return resultado
    
    def obtener_nodos_mas_centrales(self, tipo_centralidad='grado', top_n=5):
        """
        Obtiene los nodos más centrales según una métrica específica
        
        Args:
            tipo_centralidad: 'grado', 'intermediacion', 'cercania', 'eigenvector'
            top_n: número de nodos a retornar
        
        Returns:
            Lista de tuplas (id_estudiante, nombre, valor_centralidad)
        """
        todas_centralidades = self.calcular_todas_centralidades()
        
        campo_centralidad = f'centralidad_{tipo_centralidad}'
        
        # Ordenar por el tipo de centralidad especificado
        nodos_ordenados = sorted(
            todas_centralidades.items(),
            key=lambda x: x[1][campo_centralidad],
            reverse=True
        )
        
        resultado = []
        for i, (id_estudiante, datos) in enumerate(nodos_ordenados[:top_n]):
            resultado.append((
                id_estudiante,
                datos['nombre'],
                datos[campo_centralidad],
                datos['carrera']
            ))
        
        return resultado
    
    def generar_reporte_centralidad(self):
        """
        Genera un reporte completo de centralidad
        Retorna: string con el reporte formateado
        """
        todas_centralidades = self.calcular_todas_centralidades()
        
        reporte = []
        reporte.append("=" * 60)
        reporte.append("REPORTE DE CENTRALIDAD DE NODOS")
        reporte.append("=" * 60)
        reporte.append("")
        
        # Resumen general
        reporte.append(f"Total de estudiantes: {len(todas_centralidades)}")
        reporte.append(f"Total de conexiones: {sum(len(self.grafo.adj_list[id]) for id in self.grafo.adj_list) // 2}")
        reporte.append("")
        
        # Top 3 por cada métrica
        metricas = ['grado', 'intermediacion', 'cercania', 'eigenvector']
        nombres_metricas = {
            'grado': 'Centralidad de Grado (Más Conectados)',
            'intermediacion': 'Centralidad de Intermediación (Conectores Clave)',
            'cercania': 'Centralidad de Cercanía (Más Accesibles)',
            'eigenvector': 'Centralidad de Eigenvector (Más Influyentes)'
        }
        
        for metrica in metricas:
            reporte.append(f"🏆 {nombres_metricas[metrica]}:")
            top_nodos = self.obtener_nodos_mas_centrales(metrica, 3)
            
            for i, (id_est, nombre, valor, carrera) in enumerate(top_nodos, 1):
                reporte.append(f"  {i}. {nombre} ({carrera}) - Valor: {valor:.3f}")
            reporte.append("")
        
        # Tabla detallada
        reporte.append("📊 TABLA DETALLADA DE CENTRALIDADES:")
        reporte.append("-" * 60)
        reporte.append(f"{'Estudiante':<20} {'Grado':<8} {'Interm.':<8} {'Cercan.':<8} {'Eigenve.':<8}")
        reporte.append("-" * 60)
        
        # Ordenar por centralidad de grado para la tabla
        estudiantes_ordenados = sorted(
            todas_centralidades.items(),
            key=lambda x: x[1]['centralidad_grado'],
            reverse=True
        )
        
        for id_est, datos in estudiantes_ordenados:
            nombre_corto = datos['nombre'][:18] + ".." if len(datos['nombre']) > 20 else datos['nombre']
            reporte.append(
                f"{nombre_corto:<20} "
                f"{datos['centralidad_grado']:<8} "
                f"{datos['centralidad_intermediacion']:<8.3f} "
                f"{datos['centralidad_cercania']:<8.3f} "
                f"{datos['centralidad_eigenvector']:<8.3f}"
            )
        
        reporte.append("")
        reporte.append("💡 INTERPRETACIÓN:")
        reporte.append("- Grado: Número de amigos directos")
        reporte.append("- Intermediación: Capacidad de conectar grupos diferentes")
        reporte.append("- Cercanía: Facilidad para llegar a otros estudiantes")
        reporte.append("- Eigenvector: Influencia basada en conexiones importantes")
        
        return "\n".join(reporte)


def mostrar_menu_centralidad(grafo):
    """
    Muestra un menú interactivo para explorar centralidades
    """
    from Teclado import Teclado
    
    calculator = CentralidadCalculator(grafo)
    
    while True:
        print("\n" + "="*50)
        print("ANÁLISIS DE CENTRALIDAD DE NODOS")
        print("="*50)
        print("1. Ver reporte completo de centralidad")
        print("2. Top estudiantes por centralidad de grado")
        print("3. Top estudiantes por centralidad de intermediación")
        print("4. Top estudiantes por centralidad de cercanía")
        print("5. Top estudiantes por centralidad de eigenvector")
        print("6. Comparar centralidades de un estudiante específico")
        print("7. Volver al menú principal")
        
        opcion = Teclado.read_integer("Selecciona una opción (1-7):", min_value=1, max_value=7)
        
        if opcion == 1:
            print(calculator.generar_reporte_centralidad())
            input("\nPresiona Enter para continuar...")
        
        elif opcion in [2, 3, 4, 5]:
            tipos = ['', 'grado', 'intermediacion', 'cercania', 'eigenvector']
            tipo = tipos[opcion]
            
            top_n = Teclado.read_integer("¿Cuántos estudiantes mostrar?", min_value=1, max_value=20)
            top_estudiantes = calculator.obtener_nodos_mas_centrales(tipo, top_n)
            
            nombres_tipos = {
                'grado': 'Grado (Más Conectados)',
                'intermediacion': 'Intermediación (Conectores Clave)',
                'cercania': 'Cercanía (Más Accesibles)',
                'eigenvector': 'Eigenvector (Más Influyentes)'
            }
            
            print(f"\n🏆 TOP {top_n} - CENTRALIDAD DE {nombres_tipos[tipo].upper()}:")
            print("-" * 60)
            
            for i, (id_est, nombre, valor, carrera) in enumerate(top_estudiantes, 1):
                print(f"{i:2d}. {nombre:<25} ({carrera:<12}) - {valor:.3f}")
            
            input("\nPresiona Enter para continuar...")
        
        elif opcion == 6:
            print("\nEstudiantes disponibles:")
            for id_est, info in grafo.estudiantes.items():
                print(f"ID: {id_est} - {info['nombre']}")
            
            id_estudiante = Teclado.read_text("ID del estudiante a analizar:")
            
            if id_estudiante in grafo.estudiantes:
                todas_centralidades = calculator.calcular_todas_centralidades()
                datos = todas_centralidades[id_estudiante]
                
                print(f"\n📊 ANÁLISIS DE CENTRALIDAD - {datos['nombre']}")
                print("=" * 50)
                print(f"Carrera: {datos['carrera']}")
                print(f"Centralidad de Grado: {datos['centralidad_grado']}")
                print(f"Centralidad de Intermediación: {datos['centralidad_intermediacion']:.3f}")
                print(f"Centralidad de Cercanía: {datos['centralidad_cercania']:.3f}")
                print(f"Centralidad de Eigenvector: {datos['centralidad_eigenvector']:.3f}")
                
                # Mostrar posición relativa
                for tipo in ['grado', 'intermediacion', 'cercania', 'eigenvector']:
                    top_list = calculator.obtener_nodos_mas_centrales(tipo, len(grafo.estudiantes))
                    posicion = next((i+1 for i, (id_est, _, _, _) in enumerate(top_list) if id_est == id_estudiante), "N/A")
                    print(f"Posición en ranking de {tipo}: #{posicion}")
            else:
                print("Estudiante no encontrado.")
            
            input("\nPresiona Enter para continuar...")
        
        elif opcion == 7:
            break
        
        else:
            print("Opción no válida.")