import random

NOMBRES = [
    'Ana', 'Luis', 'Maria', 'Carlos', 'Elena', 'Pedro', 'Sofia', 'Miguel',
    'Laura', 'Diego', 'Carmen', 'Javier', 'Isabel', 'Fernando', 'Patricia',
    'Roberto', 'Lucia', 'Antonio', 'Marta', 'Jose', 'Cristina', 'Manuel',
    'Raquel', 'Francisco', 'Beatriz', 'Sergio', 'Alicia', 'David', 'Rosa'
]

APELLIDOS = [
    'Garcia', 'Martinez', 'Lopez', 'Rodriguez', 'Torres', 'Sanchez',
    'Ramirez', 'Fernandez', 'Gomez', 'Diaz', 'Ruiz', 'Hernandez',
    'Jimenez', 'Moreno', 'Alvarez', 'Romero', 'Navarro', 'Gutierrez'
]

CARRERAS = [
    'Ingenieria', 'Medicina', 'Derecho', 'Psicologia', 'Arquitectura',
    'Administracion', 'Economia', 'Diseno', 'Comunicacion', 'Enfermeria'
]

INTERESES = [
    'Deportes', 'Musica', 'Cine', 'Lectura', 'Tecnologia', 'Arte', 'Videojuegos',
    'Fotografia', 'Viajes', 'Cocina', 'Moda', 'Teatro', 'Baile', 'Ciencia',
    'Politica', 'Naturaleza', 'Historia', 'Literatura', 'Programacion'
]

def generar_datos_aleatorios(grafo, num_estudiantes=30, densidad_amistades=0.15):
    """
    Genera datos aleatorios para testing
    
    Args:
        grafo: Instancia del grafo a poblar
        num_estudiantes: Cantidad de estudiantes a generar
        densidad_amistades: Probabilidad de amistad entre dos estudiantes (0-1)
    """
    print(f"\nGenerando {num_estudiantes} estudiantes aleatorios...")
    
    # Generar estudiantes
    ids_generados = []
    for i in range(1, num_estudiantes + 1):
        nombre = f"{random.choice(NOMBRES)} {random.choice(APELLIDOS)}"
        carrera = random.choice(CARRERAS)
        id_est = str(i)
        
        # Generar intereses aleatorios (2-5 intereses por estudiante)
        num_intereses = random.randint(2, 5)
        intereses = random.sample(INTERESES, num_intereses)
        
        grafo.agregar_estudiante(id_est, nombre, carrera, intereses)
        ids_generados.append(id_est)
    
    print(f"Estudiantes generados: {num_estudiantes}")
    
    # Generar amistades aleatorias
    amistades_creadas = 0
    for i, id1 in enumerate(ids_generados):
        for id2 in ids_generados[i+1:]:
            if random.random() < densidad_amistades:
                # Peso aleatorio: 80% peso 1, 15% peso 2, 5% peso 3
                rand = random.random()
                if rand < 0.80:
                    peso = 1
                elif rand < 0.95:
                    peso = 2
                else:
                    peso = 3
                
                grafo.agregar_amistad(id1, id2, peso)
                amistades_creadas += 1
    
    print(f"Amistades generadas: {amistades_creadas}")
    print(f"Densidad real: {amistades_creadas / (num_estudiantes * (num_estudiantes - 1) / 2):.2%}")
    
    return ids_generados
