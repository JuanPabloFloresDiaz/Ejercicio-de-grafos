import csv

def cargar_datos(grafo, archivo_estudiantes='estudiantes.csv', archivo_amistades='amistades.csv'):
    """Carga estudiantes y amistades desde archivos CSV"""
    
    # Cargar estudiantes
    try:
        with open(archivo_estudiantes, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                grafo.agregar_estudiante(
                    row['id'],
                    row['nombre'],
                    row['carrera']
                )
        print(f"Estudiantes cargados: {len(grafo.estudiantes)}")
    except FileNotFoundError:
        print(f"Archivo {archivo_estudiantes} no encontrado")
        return False
    
    # Cargar amistades
    try:
        with open(archivo_amistades, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                peso = int(row.get('peso', 1))
                grafo.agregar_amistad(row['id1'], row['id2'], peso)
        print("Amistades cargadas exitosamente")
    except FileNotFoundError:
        print(f"Archivo {archivo_amistades} no encontrado")
        return False
    
    return True

def guardar_datos(grafo, archivo_estudiantes='estudiantes.csv', archivo_amistades='amistades.csv'):
    """Guarda el estado actual del grafo en archivos CSV"""
    
    # Guardar estudiantes
    try:
        with open(archivo_estudiantes, 'w', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['id', 'nombre', 'carrera'])
            writer.writeheader()
            for id_est, info in grafo.estudiantes.items():
                writer.writerow({
                    'id': id_est,
                    'nombre': info['nombre'],
                    'carrera': info['carrera']
                })
        print(f"Estudiantes guardados en {archivo_estudiantes}")
    except Exception as e:
        print(f"Error al guardar estudiantes: {e}")
        return False
    
    # Guardar amistades (evitar duplicados)
    try:
        amistades_guardadas = set()
        with open(archivo_amistades, 'w', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['id1', 'id2', 'peso'])
            writer.writeheader()
            for id1 in grafo.adj_list:
                for id2, peso in grafo.adj_list[id1].items():
                    if (id1, id2) not in amistades_guardadas and (id2, id1) not in amistades_guardadas:
                        writer.writerow({
                            'id1': id1,
                            'id2': id2,
                            'peso': peso
                        })
                        amistades_guardadas.add((id1, id2))
        print(f"Amistades guardadas en {archivo_amistades}")
    except Exception as e:
        print(f"Error al guardar amistades: {e}")
        return False
    
    return True
