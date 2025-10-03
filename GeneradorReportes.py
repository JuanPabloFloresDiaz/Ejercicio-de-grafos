"""
Módulo para generar reportes PDF con estadísticas detalladas del grafo de amistades.
Utiliza ReportLab para crear PDFs profesionales con gráficos y tablas.
"""

import os
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.piecharts import Pie
from reportlab.lib.colors import HexColor
import matplotlib.pyplot as plt
import networkx as nx
import io
import base64
from CentralidadAnalisis import CentralidadCalculator


class GeneradorReportesPDF:
    """Clase para generar reportes PDF completos del análisis de grafos"""
    
    def __init__(self, grafo):
        """Inicializa el generador con un grafo de estudiantes"""
        self.grafo = grafo
        self.calculator = CentralidadCalculator(grafo)
        self.styles = getSampleStyleSheet()
        self._configurar_estilos()
    
    def _configurar_estilos(self):
        """Configura estilos personalizados para el PDF"""
        # Estilo para títulos principales
        self.styles.add(ParagraphStyle(
            name='TituloPersonalizado',
            parent=self.styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        ))
        
        # Estilo para subtítulos
        self.styles.add(ParagraphStyle(
            name='SubtituloPersonalizado',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=20,
            textColor=colors.darkgreen
        ))
        
        # Estilo para texto normal con más espacio
        self.styles.add(ParagraphStyle(
            name='NormalEspaciado',
            parent=self.styles['Normal'],
            spaceAfter=12,
            fontSize=10
        ))
    
    def _crear_grafico_red(self, filename='red_temporal.png'):
        """Crea un gráfico de la red y lo guarda temporalmente"""
        plt.figure(figsize=(10, 8))
        
        # Crear grafo NetworkX
        G = nx.Graph()
        for id_est, info in self.grafo.estudiantes.items():
            G.add_node(id_est, **info)
        
        for id1 in self.grafo.adj_list:
            for id2 in self.grafo.adj_list[id1]:
                if not G.has_edge(id1, id2):
                    G.add_edge(id1, id2)
        
        # Configurar colores por carrera
        carreras = list(set(info['carrera'] for info in self.grafo.estudiantes.values()))
        colores = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8']
        color_map = {carrera: colores[i % len(colores)] for i, carrera in enumerate(carreras)}
        
        node_colors = [color_map[self.grafo.estudiantes[node]['carrera']] for node in G.nodes()]
        
        # Dibujar grafo
        pos = nx.spring_layout(G, k=1, iterations=50, seed=42)
        
        # Nodos
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=800, alpha=0.8)
        
        # Aristas
        nx.draw_networkx_edges(G, pos, alpha=0.5, width=1)
        
        # Etiquetas
        labels = {node: self.grafo.estudiantes[node]['nombre'].split()[0] for node in G.nodes()}
        nx.draw_networkx_labels(G, pos, labels, font_size=8, font_weight='bold')
        
        # Leyenda
        for i, (carrera, color) in enumerate(color_map.items()):
            plt.plot([], [], 'o', color=color, label=carrera, markersize=10)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        plt.title("Red de Amistades Universitarias", fontsize=16, fontweight='bold')
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        return filename
    
    def _crear_grafico_barras_centralidad(self, filename='centralidad_temporal.png'):
        """Crea un gráfico de barras con las centralidades"""
        todas_centralidades = self.calculator.calcular_todas_centralidades()
        
        # Obtener top 8 estudiantes por centralidad de grado
        estudiantes_ordenados = sorted(
            todas_centralidades.items(),
            key=lambda x: x[1]['centralidad_grado'],
            reverse=True
        )[:8]
        
        nombres = [datos['nombre'].split()[0] for _, datos in estudiantes_ordenados]
        grados = [datos['centralidad_grado'] for _, datos in estudiantes_ordenados]
        intermediacion = [datos['centralidad_intermediacion'] for _, datos in estudiantes_ordenados]
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Gráfico de centralidad de grado
        bars1 = ax1.bar(nombres, grados, color='#4ECDC4', alpha=0.8)
        ax1.set_title('Centralidad de Grado\n(Número de Amigos)', fontweight='bold')
        ax1.set_ylabel('Número de Conexiones')
        ax1.tick_params(axis='x', rotation=45)
        
        # Agregar valores en las barras
        for bar, valor in zip(bars1, grados):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                    str(valor), ha='center', va='bottom', fontweight='bold')
        
        # Gráfico de centralidad de intermediación
        bars2 = ax2.bar(nombres, intermediacion, color='#FF6B6B', alpha=0.8)
        ax2.set_title('Centralidad de Intermediación\n(Conectores Clave)', fontweight='bold')
        ax2.set_ylabel('Valor de Intermediación')
        ax2.tick_params(axis='x', rotation=45)
        
        # Agregar valores en las barras
        for bar, valor in zip(bars2, intermediacion):
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                    f'{valor:.2f}', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        return filename
    
    def _crear_grafico_carreras(self, filename='carreras_temporal.png'):
        """Crea un gráfico de torta con la distribución por carreras"""
        carreras = {}
        for info in self.grafo.estudiantes.values():
            carrera = info['carrera']
            carreras[carrera] = carreras.get(carrera, 0) + 1
        
        plt.figure(figsize=(8, 8))
        
        colores = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
        
        wedges, texts, autotexts = plt.pie(
            carreras.values(),
            labels=carreras.keys(),
            autopct='%1.1f%%',
            colors=colores[:len(carreras)],
            startangle=90,
            textprops={'fontsize': 12, 'fontweight': 'bold'}
        )
        
        plt.title('Distribución de Estudiantes por Carrera', 
                 fontsize=16, fontweight='bold', pad=20)
        
        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        return filename
    
    def generar_reporte_completo(self, nombre_archivo=None):
        """
        Genera un reporte PDF completo con todas las estadísticas
        
        Args:
            nombre_archivo: Nombre del archivo PDF. Si no se especifica, se genera automáticamente.
        
        Returns:
            str: Ruta del archivo PDF generado
        """
        if nombre_archivo is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_archivo = f"reporte_red_amistades_{timestamp}.pdf"
        
        # Crear documento PDF
        doc = SimpleDocTemplate(nombre_archivo, pagesize=A4)
        story = []
        
        # Título principal
        titulo = Paragraph(
            "Reporte de Análisis de Red de Amistades Universitarias",
            self.styles['TituloPersonalizado']
        )
        story.append(titulo)
        story.append(Spacer(1, 20))
        
        # Información general
        fecha_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        info_general = Paragraph(
            f"<b>Fecha de generación:</b> {fecha_hora}<br/>"
            f"<b>Total de estudiantes:</b> {len(self.grafo.estudiantes)}<br/>"
            f"<b>Total de amistades:</b> {sum(len(amigos) for amigos in self.grafo.adj_list.values()) // 2}",
            self.styles['NormalEspaciado']
        )
        story.append(info_general)
        story.append(Spacer(1, 20))
        
        # Sección 1: Estadísticas Generales
        story.append(Paragraph("1. Estadísticas Generales", self.styles['SubtituloPersonalizado']))
        
        num_estudiantes = len(self.grafo.estudiantes)
        num_amistades = sum(len(amigos) for amigos in self.grafo.adj_list.values()) // 2
        promedio_amigos = (num_amistades * 2 / num_estudiantes) if num_estudiantes > 0 else 0
        
        # Tabla de estadísticas generales
        datos_tabla_general = [
            ['Métrica', 'Valor'],
            ['Total de estudiantes', str(num_estudiantes)],
            ['Total de amistades', str(num_amistades)],
            ['Promedio de amigos por estudiante', f'{promedio_amigos:.2f}'],
            ['Densidad de la red', f'{(num_amistades * 2) / (num_estudiantes * (num_estudiantes - 1)):.3f}' if num_estudiantes > 1 else '0']
        ]
        
        tabla_general = Table(datos_tabla_general, colWidths=[3*inch, 2*inch])
        tabla_general.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(tabla_general)
        story.append(Spacer(1, 20))
        
        # Gráfico de distribución por carreras
        archivo_carreras = self._crear_grafico_carreras()
        story.append(Paragraph("Distribución por Carreras", self.styles['SubtituloPersonalizado']))
        img_carreras = Image(archivo_carreras, width=5*inch, height=5*inch)
        story.append(img_carreras)
        story.append(PageBreak())
        
        # Sección 2: Visualización de la Red
        story.append(Paragraph("2. Visualización de la Red", self.styles['SubtituloPersonalizado']))
        
        archivo_red = self._crear_grafico_red()
        img_red = Image(archivo_red, width=7*inch, height=5.6*inch)
        story.append(img_red)
        story.append(Spacer(1, 20))
        
        # Sección 3: Análisis de Centralidad
        story.append(Paragraph("3. Análisis de Centralidad", self.styles['SubtituloPersonalizado']))
        
        archivo_centralidad = self._crear_grafico_barras_centralidad()
        img_centralidad = Image(archivo_centralidad, width=7*inch, height=3*inch)
        story.append(img_centralidad)
        story.append(Spacer(1, 20))
        
        # Tabla de centralidades detallada
        todas_centralidades = self.calculator.calcular_todas_centralidades()
        story.append(Paragraph("Tabla Detallada de Centralidades", self.styles['SubtituloPersonalizado']))
        
        datos_tabla_centralidad = [
            ['Estudiante', 'Carrera', 'Grado', 'Intermediación', 'Cercanía', 'Eigenvector']
        ]
        
        estudiantes_ordenados = sorted(
            todas_centralidades.items(),
            key=lambda x: x[1]['centralidad_grado'],
            reverse=True
        )
        
        for id_est, datos in estudiantes_ordenados:
            datos_tabla_centralidad.append([
                datos['nombre'],
                datos['carrera'],
                str(datos['centralidad_grado']),
                f"{datos['centralidad_intermediacion']:.3f}",
                f"{datos['centralidad_cercania']:.3f}",
                f"{datos['centralidad_eigenvector']:.3f}"
            ])
        
        tabla_centralidad = Table(datos_tabla_centralidad, colWidths=[1.8*inch, 1.2*inch, 0.7*inch, 0.9*inch, 0.7*inch, 0.9*inch])
        tabla_centralidad.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
        ]))
        story.append(tabla_centralidad)
        story.append(PageBreak())
        
        # Sección 4: Rankings
        story.append(Paragraph("4. Rankings de Estudiantes", self.styles['SubtituloPersonalizado']))
        
        # Top 5 por cada métrica
        metricas = ['grado', 'intermediacion', 'cercania', 'eigenvector']
        nombres_metricas = {
            'grado': 'Más Conectados (Centralidad de Grado)',
            'intermediacion': 'Conectores Clave (Centralidad de Intermediación)',
            'cercania': 'Más Accesibles (Centralidad de Cercanía)',
            'eigenvector': 'Más Influyentes (Centralidad de Eigenvector)'
        }
        
        for metrica in metricas:
            story.append(Paragraph(nombres_metricas[metrica], self.styles['SubtituloPersonalizado']))
            
            top_estudiantes = self.calculator.obtener_nodos_mas_centrales(metrica, 5)
            
            datos_ranking = [['Posición', 'Estudiante', 'Carrera', 'Valor']]
            for i, (id_est, nombre, valor, carrera) in enumerate(top_estudiantes, 1):
                datos_ranking.append([str(i), nombre, carrera, f"{valor:.3f}"])
            
            tabla_ranking = Table(datos_ranking, colWidths=[0.8*inch, 2.5*inch, 1.5*inch, 1*inch])
            tabla_ranking.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(tabla_ranking)
            story.append(Spacer(1, 15))
        
        # Sección 5: Conclusiones
        story.append(PageBreak())
        story.append(Paragraph("5. Conclusiones y Observaciones", self.styles['SubtituloPersonalizado']))
        
        # Generar conclusiones automáticas
        top_grado = self.calculator.obtener_nodos_mas_centrales('grado', 1)[0]
        top_intermediacion = self.calculator.obtener_nodos_mas_centrales('intermediacion', 1)[0]
        
        conclusiones = f"""
        <b>Análisis de la Red de Amistades:</b><br/><br/>
        
        • <b>Estudiante más conectado:</b> {top_grado[1]} con {top_grado[2]} amigos directos.<br/><br/>
        
        • <b>Conector clave:</b> {top_intermediacion[1]} es quien más conecta diferentes grupos 
        (centralidad de intermediación: {top_intermediacion[2]:.3f}).<br/><br/>
        
        • La red tiene una densidad de {(num_amistades * 2) / (num_estudiantes * (num_estudiantes - 1)):.3f}, 
        lo que indica {'una red bien conectada' if (num_amistades * 2) / (num_estudiantes * (num_estudiantes - 1)) > 0.3 else 'oportunidades de crear más conexiones'}.<br/><br/>
        
        • El promedio de {promedio_amigos:.1f} amigos por estudiante sugiere 
        {'un buen nivel de integración social' if promedio_amigos > 3 else 'potencial para mejorar la integración'}.<br/><br/>
        
        <b>Recomendaciones:</b><br/><br/>
        
        • Considerar organizar actividades que involucren a estudiantes con baja centralidad.<br/>
        • Aprovechar a los conectores clave para facilitar la integración de nuevos estudiantes.<br/>
        • Fomentar actividades inter-carrera para aumentar la diversidad de conexiones.
        """
        
        story.append(Paragraph(conclusiones, self.styles['NormalEspaciado']))
        
        # Generar PDF
        doc.build(story)
        
        # Limpiar archivos temporales
        for archivo in [archivo_red, archivo_carreras, archivo_centralidad]:
            if os.path.exists(archivo):
                os.remove(archivo)
        
        return nombre_archivo
    
    def generar_reporte_estudiante(self, id_estudiante, nombre_archivo=None):
        """
        Genera un reporte PDF específico para un estudiante
        
        Args:
            id_estudiante: ID del estudiante
            nombre_archivo: Nombre del archivo PDF
        
        Returns:
            str: Ruta del archivo PDF generado
        """
        if id_estudiante not in self.grafo.estudiantes:
            raise ValueError(f"Estudiante con ID {id_estudiante} no encontrado")
        
        estudiante_info = self.grafo.estudiantes[id_estudiante]
        
        if nombre_archivo is None:
            nombre_safe = estudiante_info['nombre'].replace(' ', '_')
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_archivo = f"reporte_{nombre_safe}_{timestamp}.pdf"
        
        doc = SimpleDocTemplate(nombre_archivo, pagesize=A4)
        story = []
        
        # Título
        titulo = Paragraph(
            f"Reporte Individual - {estudiante_info['nombre']}",
            self.styles['TituloPersonalizado']
        )
        story.append(titulo)
        story.append(Spacer(1, 20))
        
        # Información básica
        amigos = self.grafo.obtener_amigos(id_estudiante)
        todas_centralidades = self.calculator.calcular_todas_centralidades()
        datos_estudiante = todas_centralidades[id_estudiante]
        
        info_basica = f"""
        <b>Información Personal:</b><br/>
        • Nombre: {estudiante_info['nombre']}<br/>
        • Carrera: {estudiante_info['carrera']}<br/>
        • Número de amigos: {len(amigos)}<br/><br/>
        
        <b>Métricas de Centralidad:</b><br/>
        • Centralidad de Grado: {datos_estudiante['centralidad_grado']}<br/>
        • Centralidad de Intermediación: {datos_estudiante['centralidad_intermediacion']:.3f}<br/>
        • Centralidad de Cercanía: {datos_estudiante['centralidad_cercania']:.3f}<br/>
        • Centralidad de Eigenvector: {datos_estudiante['centralidad_eigenvector']:.3f}<br/>
        """
        
        story.append(Paragraph(info_basica, self.styles['NormalEspaciado']))
        story.append(Spacer(1, 20))
        
        # Lista de amigos
        story.append(Paragraph("Lista de Amigos", self.styles['SubtituloPersonalizado']))
        
        if amigos:
            datos_amigos = [['Nombre', 'Carrera']]
            for amigo_id in amigos:
                amigo_info = self.grafo.estudiantes[amigo_id]
                datos_amigos.append([amigo_info['nombre'], amigo_info['carrera']])
            
            tabla_amigos = Table(datos_amigos, colWidths=[3*inch, 2*inch])
            tabla_amigos.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(tabla_amigos)
        else:
            story.append(Paragraph("No tiene amigos registrados en la red.", self.styles['NormalEspaciado']))
        
        doc.build(story)
        return nombre_archivo


def mostrar_menu_reportes(grafo):
    """
    Muestra un menú interactivo para generar reportes PDF
    """
    from Teclado import Teclado
    
    generador = GeneradorReportesPDF(grafo)
    
    while True:
        print("\n" + "="*50)
        print("GENERACIÓN DE REPORTES PDF")
        print("="*50)
        print("1. Generar reporte completo de la red")
        print("2. Generar reporte individual de un estudiante")
        print("3. Volver al menú principal")
        
        opcion = Teclado.read_integer("Selecciona una opción (1-3):", min_value=1, max_value=3)
        
        if opcion == 1:
            print("\nGenerando reporte completo...")
            try:
                archivo_pdf = generador.generar_reporte_completo()
                print(f"✅ Reporte generado exitosamente: {archivo_pdf}")
                print(f"📁 Ubicación: {os.path.abspath(archivo_pdf)}")
            except Exception as e:
                print(f"❌ Error al generar el reporte: {str(e)}")
            
            input("\nPresiona Enter para continuar...")
        
        elif opcion == 2:
            print("\nEstudiantes disponibles:")
            for id_est, info in grafo.estudiantes.items():
                print(f"ID: {id_est} - {info['nombre']}")
            
            id_estudiante = Teclado.read_text("ID del estudiante:")
            
            if id_estudiante in grafo.estudiantes:
                print(f"\nGenerando reporte para {grafo.estudiantes[id_estudiante]['nombre']}...")
                try:
                    archivo_pdf = generador.generar_reporte_estudiante(id_estudiante)
                    print(f"✅ Reporte generado exitosamente: {archivo_pdf}")
                    print(f"📁 Ubicación: {os.path.abspath(archivo_pdf)}")
                except Exception as e:
                    print(f"❌ Error al generar el reporte: {str(e)}")
            else:
                print("❌ Estudiante no encontrado.")
            
            input("\nPresiona Enter para continuar...")
        
        elif opcion == 3:
            break
        
        else:
            print("Opción no válida.")