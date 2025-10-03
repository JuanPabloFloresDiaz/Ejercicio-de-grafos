import json
import os
from datetime import datetime

def guardar_json(grafo, archivo='red_universitaria.json'):
    """Guarda el grafo completo en formato JSON"""
    data = {
        'metadata': {
            'fecha_exportacion': datetime.now().isoformat(),
            'num_estudiantes': len(grafo.estudiantes),
            'num_amistades': sum(len(amigos) for amigos in grafo.adj_list.values()) // 2
        },
        'estudiantes': [],
        'amistades': []
    }
    
    # Guardar estudiantes
    for id_est, info in grafo.estudiantes.items():
        data['estudiantes'].append({
            'id': id_est,
            'nombre': info['nombre'],
            'carrera': info['carrera'],
            'intereses': info.get('intereses', [])
        })
    
    # Guardar amistades (evitar duplicados)
    amistades_guardadas = set()
    for id1 in grafo.adj_list:
        for id2, peso in grafo.adj_list[id1].items():
            if (id1, id2) not in amistades_guardadas and (id2, id1) not in amistades_guardadas:
                data['amistades'].append({
                    'id1': id1,
                    'id2': id2,
                    'peso': peso
                })
                amistades_guardadas.add((id1, id2))
    
    try:
        with open(archivo, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error al guardar JSON: {e}")
        return False

def cargar_json(grafo, archivo='red_universitaria.json'):
    """Carga el grafo desde un archivo JSON"""
    if not os.path.exists(archivo):
        return False
    
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Limpiar grafo actual
        grafo.estudiantes.clear()
        grafo.adj_list.clear()
        
        # Cargar estudiantes
        for est in data['estudiantes']:
            grafo.agregar_estudiante(
                est['id'],
                est['nombre'],
                est['carrera'],
                est.get('intereses', [])
            )
        
        # Cargar amistades
        for amistad in data['amistades']:
            grafo.agregar_amistad(
                amistad['id1'],
                amistad['id2'],
                amistad.get('peso', 1)
            )
        
        print(f"Datos cargados desde {archivo}")
        print(f"Estudiantes: {len(grafo.estudiantes)}, Amistades: {len(data['amistades'])}")
        return True
    except Exception as e:
        print(f"Error al cargar JSON: {e}")
        return False

def exportar_backup(grafo, directorio='backups'):
    """Crea un backup con timestamp del grafo"""
    if not os.path.exists(directorio):
        os.makedirs(directorio)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    archivo = os.path.join(directorio, f'backup_{timestamp}.json')
    
    return guardar_json(grafo, archivo)
