from collections import defaultdict

class Grafo:
    def __init__(self):
        self.adj_list = defaultdict(dict)
        self.estudiantes = {}
    
    def agregar_estudiante(self, id_estudiante, nombre, carrera):
        """Agrega un estudiante al grafo"""
        self.estudiantes[id_estudiante] = {
            'nombre': nombre,
            'carrera': carrera
        }
        if id_estudiante not in self.adj_list:
            self.adj_list[id_estudiante] = {}
    
    def eliminar_estudiante(self, id_estudiante):
        """Elimina un estudiante y todas sus amistades"""
        if id_estudiante not in self.estudiantes:
            return False
        
        # Eliminar amistades donde este estudiante es parte
        for amigo_id in list(self.adj_list[id_estudiante].keys()):
            if amigo_id in self.adj_list:
                self.adj_list[amigo_id].pop(id_estudiante, None)
        
        # Eliminar el estudiante del grafo
        self.adj_list.pop(id_estudiante, None)
        self.estudiantes.pop(id_estudiante, None)
        return True
    
    def agregar_amistad(self, id1, id2, peso=1):
        """Agrega una relacion de amistad con peso entre dos estudiantes"""
        if id1 in self.estudiantes and id2 in self.estudiantes:
            self.adj_list[id1][id2] = peso
            self.adj_list[id2][id1] = peso
            return True
        return False
    
    def actualizar_peso_amistad(self, id1, id2, nuevo_peso):
        """Actualiza el peso de una amistad existente"""
        if self.son_amigos(id1, id2):
            self.adj_list[id1][id2] = nuevo_peso
            self.adj_list[id2][id1] = nuevo_peso
            return True
        return False
    
    def eliminar_amistad(self, id1, id2):
        """Elimina una relacion de amistad"""
        if self.son_amigos(id1, id2):
            self.adj_list[id1].pop(id2, None)
            self.adj_list[id2].pop(id1, None)
            return True
        return False
    
    def obtener_amigos(self, id_estudiante):
        """Retorna la lista de IDs de amigos de un estudiante"""
        return list(self.adj_list[id_estudiante].keys())
    
    def obtener_peso_amistad(self, id1, id2):
        """Retorna el peso de la amistad entre dos estudiantes"""
        if self.son_amigos(id1, id2):
            return self.adj_list[id1][id2]
        return None
    
    def son_amigos(self, id1, id2):
        """Verifica si dos estudiantes son amigos"""
        return id2 in self.adj_list.get(id1, {})
    
    def obtener_info_estudiante(self, id_estudiante):
        """Retorna la informacion de un estudiante"""
        return self.estudiantes.get(id_estudiante)
    
    def __str__(self):
        result = "Grafo de Amistades:\n"
        for estudiante in self.adj_list:
            amigos = self.obtener_amigos(estudiante)
            result += f"{self.estudiantes[estudiante]['nombre']}: {[self.estudiantes[amigo]['nombre'] for amigo in amigos]}\n"
        return result
