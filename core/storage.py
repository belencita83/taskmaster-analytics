from .sqlite_storage import SQLiteStorage
from .models import Tarea

class GestorAlmacenamiento:
    """Factory para elegir el tipo de almacenamiento."""
    
    def __init__(self, tipo_almacenamiento="sqlite", db_path="data/taskmaster.db"):
        if tipo_almacenamiento == "sqlite":
            self.almacenamiento = SQLiteStorage(db_path)
        else:
            raise ValueError("Tipo de almacenamiento no soportado")
    
    def cargar_tareas(self, usuario=None):
        return self.almacenamiento.cargar_tareas(usuario)
    
    def guardar_tarea(self, tarea):
        return self.almacenamiento.guardar_tarea(tarea)
    
    def guardar_tareas(self, tareas):
        # Para compatibilidad con código existente
        for tarea in tareas:
            self.guardar_tarea(tarea)
        return True
    
    def eliminar_tarea(self, tarea_id):
        return self.almacenamiento.eliminar_tarea(tarea_id)