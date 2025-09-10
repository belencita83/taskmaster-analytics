# core/models.py

class Tarea:
    """Clase que representa una tarea individual."""
    
    def __init__(self, titulo, descripcion="", prioridad="media", proyecto=None, fecha_vencimiento=None):
        # Información básica
        self.titulo = titulo
        self.descripcion = descripcion
        self.proyecto = proyecto  # Nombre del proyecto al que pertenece
        
        # Estados y prioridad
        self.estado = "pendiente"  # Puede ser: pendiente, en_progreso, completada
        self.prioridad = prioridad  # Puede ser: baja, media, alta
        
        # Fechas
        self.fecha_creacion = None  # Se establecerá al guardar
        self.fecha_vencimiento = fecha_vencimiento
        self.fecha_completada = None
        
        # Identificador único (para poder buscar y modificar tareas específicas)
        self.id = None

    def marcar_completada(self):
        """Marca la tarea como completada y establece la fecha de finalización."""
        self.estado = "completada"
        # Aquí se debería establecer la fecha actual. Lo haremos en el storage.

    def __str__(self):
        """Representación en string de la tarea, útil para imprimir."""
        emoji_estado = {"pendiente": "⏳", "en_progreso": "🚧", "completada": "✅"}
        emoji_prioridad = {"baja": "🔵", "media": "🟡", "alta": "🔴"}
        return f"{emoji_estado[self.estado]} {emoji_prioridad[self.prioridad]} {self.titulo}"