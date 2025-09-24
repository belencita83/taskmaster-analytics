# core/managers/tarea_manager.py
from datetime import datetime, timedelta
from ..models import Tarea

class TareaManager:
    """Manager especializado para operaciones con tareas."""
    
    def __init__(self, storage):
        self.storage = storage
    
    def crear_tarea(self, titulo, descripcion="", prioridad="media", proyecto=None, usuario="sistema"):
        """Crea una nueva tarea con validaciones."""
        if not titulo or len(titulo.strip()) == 0:
            raise ValueError("El título de la tarea no puede estar vacío")
        
        if prioridad not in ["baja", "media", "alta"]:
            raise ValueError("Prioridad debe ser: baja, media o alta")
        
        tarea = Tarea(
            titulo=titulo.strip(),
            descripcion=descripcion.strip(),
            prioridad=prioridad,
            proyecto=proyecto.strip() if proyecto else None,
            usuario=usuario
        )
        tarea.fecha_creacion = datetime.now()
        
        if self.storage.guardar_tarea(tarea):
            return tarea
        else:
            raise Exception("Error guardando la tarea en la base de datos")
    
    def obtener_tareas_por_estado(self, estado, usuario=None):
        """Obtiene tareas filtradas por estado."""
        tareas = self.storage.cargar_tareas(usuario)
        return [t for t in tareas if t.estado == estado]
    
    def obtener_tareas_por_proyecto(self, proyecto, usuario=None):
        """Obtiene tareas filtradas por proyecto."""
        tareas = self.storage.cargar_tareas(usuario)
        return [t for t in tareas if t.proyecto == proyecto]
    
    def obtener_tareas_vencidas(self, usuario=None):
        """Obtiene tareas pendientes que están vencidas."""
        tareas = self.storage.cargar_tareas(usuario)
        hoy = datetime.now().date()
        
        vencidas = []
        for tarea in tareas:
            if (tarea.estado == "pendiente" and 
                tarea.fecha_vencimiento and 
                datetime.fromisoformat(tarea.fecha_vencimiento).date() < hoy):
                vencidas.append(tarea)
        
        return vencidas
    
    def obtener_tareas_proximas_a_vencer(self, dias=3, usuario=None):
        """Obtiene tareas que vencen en los próximos días."""
        tareas = self.storage.cargar_tareas(usuario)
        hoy = datetime.now().date()
        fecha_limite = hoy + timedelta(days=dias)
        
        proximas = []
        for tarea in tareas:
            if (tarea.estado == "pendiente" and tarea.fecha_vencimiento):
                fecha_venc = datetime.fromisoformat(tarea.fecha_vencimiento).date()
                if hoy <= fecha_venc <= fecha_limite:
                    proximas.append(tarea)
        
        return proximas