from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
import matplotlib.pyplot as plt
import networkx as nx
import os
import tempfile

def generar_reporte_pdf(grafo, archivo='reporte_red_universitaria.pdf', incluir_grafico=True):
    """
    Genera un reporte PDF completo con estadisticas de la red
    
    Args:
        grafo: Instancia del grafo
        archivo: Nombre del archivo PDF de salida
        incluir_grafico: Si incluir visualizacion del grafo
    """
    doc = SimpleDocTemplate(archivo, pagesize=letter)
    elementos = []
    styles = getSampleStyleSheet()
    
    # Estilo personalizado
    titulo_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2C3E50'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    subtitulo_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#34495E'),
        spaceAfter=12,
        spaceBefore=12
    )
    
    # Titulo
    elementos.append(Paragraph("Reporte de Red Universitaria", titulo_style))
    elementos.append(Paragraph(f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}", styles['Normal']))
    elementos.append(Spacer(1, 0.3*inch))
    
    # Seccion 1: Resumen Ejecutivo
    elementos.append(Paragraph("1. Resumen Ejecutivo", subtitulo_style))
    
    num_estudiantes = len(grafo.estudiantes)
    num_amistades = sum(len(amigos) for amigos in grafo.adj_list.values()) // 2
    
    resumen = [
        ['Metrica', 'Valor'],
        ['Total de estudiantes', str(num_estudiantes)],
        ['Total de amistades', str(num_amistades)],
        ['Promedio de amigos', f'{num_amistades*2/num_estudiantes:.2f}' if num_estudiantes > 0 else '0'],
        ['Densidad de red', f'{(num_amistades / (num_estudiantes * (num_estudiantes - 1) / 2) * 100):.2f}%' if num_estudiantes > 1 else '0%']
    ]
    
    tabla_resumen = Table(resumen, colWidths=[3*inch, 2*inch])
    tabla_resumen.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498DB')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elementos.append(tabla_resumen)
    elementos.append(Spacer(1, 0.3*inch))
    
    # Seccion 2: Distribucion por Carrera
    elementos.append(Paragraph("2. Distribucion por Carrera", subtitulo_style))
    
    carreras = {}
    for info in grafo.estudiantes.values():
        carrera = info['carrera']
        carreras[carrera] = carreras.get(carrera, 0) + 1
    
    datos_carreras = [['Carrera', 'Estudiantes', 'Porcentaje']]
    for carrera, cantidad in sorted(carreras.items(), key=lambda x: x[1], reverse=True):
        porcentaje = (cantidad / num_estudiantes * 100) if num_estudiantes > 0 else 0
        datos_carreras.append([carrera, str(cantidad), f'{porcentaje:.1f}%'])
    
    tabla_carreras = Table(datos_carreras, colWidths=[2.5*inch, 1.5*inch, 1.5*inch])
    tabla_carreras.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2ECC71')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
    ]))
    
    elementos.append(tabla_carreras)
    elementos.append(Spacer(1, 0.3*inch))
    
    # Seccion 3: Estudiantes Mas Populares
    elementos.append(Paragraph("3. Estudiantes Mas Populares", subtitulo_style))
    
    popularidad = []
    for id_est in grafo.estudiantes:
        num_amigos = len(grafo.obtener_amigos(id_est))
        popularidad.append((grafo.estudiantes[id_est]['nombre'], num_amigos, grafo.estudiantes[id_est]['carrera']))
    
    popularidad.sort(key=lambda x: x[1], reverse=True)
    
    datos_populares = [['Nombre', 'Amigos', 'Carrera']]
    for nombre, amigos, carrera in popularidad[:10]:
        datos_populares.append([nombre, str(amigos), carrera])
    
    tabla_populares = Table(datos_populares, colWidths=[2.5*inch, 1*inch, 2*inch])
    tabla_populares.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E74C3C')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lavender),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elementos.append(tabla_populares)
    elementos.append(Spacer(1, 0.3*inch))
    
    # Seccion 4: Distribucion de Pesos de Amistades
    elementos.append(Paragraph("4. Intensidad de Amistades", subtitulo_style))
    
    pesos = {}
    for id1 in grafo.adj_list:
        for id2, peso in grafo.adj_list[id1].items():
            pesos[peso] = pesos.get(peso, 0) + 1
    
    datos_pesos = [['Nivel', 'Tipo', 'Cantidad']]
    tipos = {1: 'Normal', 2: 'Mejor amigo', 3: 'Amigo cercano'}
    for peso in sorted(pesos.keys()):
        cantidad = pesos[peso] // 2
        datos_pesos.append([str(peso), tipos.get(peso, 'Especial'), str(cantidad)])
    
    tabla_pesos = Table(datos_pesos, colWidths=[1.5*inch, 2*inch, 1.5*inch])
    tabla_pesos.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#9B59B6')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elementos.append(tabla_pesos)
    
    # Agregar grafico si se solicita
    if incluir_grafico and num_estudiantes > 0:
        elementos.append(PageBreak())
        elementos.append(Paragraph("5. Visualizacion de la Red", subtitulo_style))
        
        # Generar grafico temporal
        temp_img = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        temp_img.close()
        
        try:
            _generar_grafico_para_pdf(grafo, temp_img.name)
            img = Image(temp_img.name, width=6*inch, height=4.5*inch)
            elementos.append(img)
        except Exception as e:
            elementos.append(Paragraph(f"Error al generar grafico: {str(e)}", styles['Normal']))
        finally:
            if os.path.exists(temp_img.name):
                os.unlink(temp_img.name)
    
    # Construir PDF
    try:
        doc.build(elementos)
        return True
    except Exception as e:
        print(f"Error al generar PDF: {e}")
        return False

def _generar_grafico_para_pdf(grafo, archivo):
    """Genera un grafico del grafo para incluir en el PDF"""
    G = nx.Graph()
    
    for id_est, info in grafo.estudiantes.items():
        G.add_node(id_est, nombre=info['nombre'])
    
    for id1 in grafo.adj_list:
        for id2, peso in grafo.adj_list[id1].items():
            if not G.has_edge(id1, id2):
                G.add_edge(id1, id2, weight=peso)
    
    plt.figure(figsize=(10, 8))
    
    # Layout
    pos = nx.spring_layout(G, k=1.5, iterations=50)
    
    # Colores por carrera
    carreras = list(set(info['carrera'] for info in grafo.estudiantes.values()))
    colores = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']
    color_map = {}
    
    for i, carrera in enumerate(carreras):
        color_map[carrera] = colores[i % len(colores)]
    
    node_colors = [color_map[grafo.estudiantes[id_est]['carrera']] for id_est in G.nodes()]
    
    # Dibujar
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=800, alpha=0.8)
    labels = {id_est: grafo.estudiantes[id_est]['nombre'].split()[0] for id_est in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels, font_size=8, font_weight='bold')
    
    edges = G.edges()
    weights = [G[u][v]['weight'] for u, v in edges]
    nx.draw_networkx_edges(G, pos, width=[w * 1.5 for w in weights], alpha=0.5)
    
    plt.title("Red de Amistades Universitarias", fontsize=14, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(archivo, format='png', dpi=150, bbox_inches='tight')
    plt.close()
