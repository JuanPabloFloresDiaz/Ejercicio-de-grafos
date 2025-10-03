class Estudiante:
    def __init__(self, id_estudiante, nombre, carrera, intereses=None):
        self.id = id_estudiante
        self.nombre = nombre
        self.carrera = carrera
        self.intereses = intereses if intereses else []
    
    def __repr__(self):
        return f"Estudiante(id={self.id}, nombre={self.nombre}, carrera={self.carrera})"
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'carrera': self.carrera,
            'intereses': self.intereses
        }
