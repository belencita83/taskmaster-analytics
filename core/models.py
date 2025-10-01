# core/models.py
from datetime import datetime

class Tarea:
    """Clase que representa una tarea individual con campos de auditoría."""
    
    def __init__(self, titulo, descripcion="", prioridad="media", 
                 proyecto=None, fecha_vencimiento=None, usuario="sistema"):
        # Información básica
        self.titulo = titulo
        self.descripcion = descripcion
        self.proyecto = proyecto
        
        # Estados y prioridad
        self.estado = "pendiente"
        self.prioridad = prioridad
        
        # Fechas
        self.fecha_creacion = None
        self.fecha_vencimiento = fecha_vencimiento
        self.fecha_completada = None
        
        # Identificador único
        self.id = None
        
        # CAMPOS DE AUDITORÍA (nuevos)
        self.creado_por = usuario
        self.actualizado_por = usuario
        self.actualizado_en = None
        self.usuario = usuario

    def marcar_completada(self, usuario="sistema"):
        """Marca la tarea como completada con auditoría."""
        self.estado = "completada"
        self.actualizado_por = usuario
        self.actualizado_en = datetime.now()
        self.fecha_completada = datetime.now()  # ← IMPORTANTE: Establecer fecha

    def actualizar_auditoria(self, usuario="sistema"):
        """Actualiza campos de auditoría."""
        self.actualizado_por = usuario
        self.actualizado_en = datetime.now()

    def __str__(self):
        """Representación en string de la tarea."""
        emoji_estado = {"pendiente": "⏳", "en_progreso": "🚧", "completada": "✅"}
        emoji_prioridad = {"baja": "🔵", "media": "🟡", "alta": "🔴"}
        return f"{emoji_estado[self.estado]} {emoji_prioridad[self.prioridad]} {self.titulo} [by: {self.usuario}]"