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
        """Eliminar una tarea - LLAMANDO AL MÉTODO CORRECTO."""
        try:
            # Llamar al método eliminar_tarea del SQLiteStorage
            resultado = self.almacenamiento.eliminar_tarea(tarea_id)
            
            if resultado:
                print(f"Tarea ID {tarea_id} eliminada correctamente")
                return True
            else:
                print(f"No se pudo eliminar la tarea ID {tarea_id}")
                return False
                
        except Exception as e:
            print(f"Error en GestorAlmacenamiento.eliminar_tarea: {str(e)}")
            return False