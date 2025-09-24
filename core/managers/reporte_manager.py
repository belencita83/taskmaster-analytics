# core/managers/reporte_manager.py
from datetime import datetime, timedelta
import csv
import json

class ReporteManager:
    """Manager especializado para generación de reportes."""
    
    def __init__(self, tarea_manager):
        self.tarea_manager = tarea_manager
    
    def generar_reporte_completo(self, usuario=None):
        """Genera un reporte completo con todas las métricas."""
        tareas = self.tarea_manager.storage.cargar_tareas(usuario)
        
        reporte = {
            'fecha_generacion': datetime.now().isoformat(),
            'usuario': usuario or 'todos',
            'resumen': self._generar_resumen(tareas),
            'tareas_por_estado': self._contar_por_estado(tareas),
            'tareas_por_prioridad': self._contar_por_prioridad(tareas),
            'tareas_por_proyecto': self._contar_por_proyecto(tareas),
            'tareas_vencidas': len(self.tarea_manager.obtener_tareas_vencidas(usuario)),
            'tareas_proximas_vencer': len(self.tarea_manager.obtener_tareas_proximas_a_vencer(3, usuario)),
            'eficiencia_semanal': self._calcular_eficiencia_semanal(tareas)
        }
        
        return reporte
    
    def _generar_resumen(self, tareas):
        total = len(tareas)
        completadas = sum(1 for t in tareas if t.estado == "completada")
        pendientes = total - completadas
        
        return {
            'total_tareas': total,
            'completadas': completadas,
            'pendientes': pendientes,
            'porcentaje_completado': (completadas / total * 100) if total > 0 else 0
        }
    
    def _contar_por_estado(self, tareas):
        estados = ["pendiente", "en_progreso", "completada"]
        return {estado: sum(1 for t in tareas if t.estado == estado) for estado in estados}
    
    def _contar_por_prioridad(self, tareas):
        prioridades = ["baja", "media", "alta"]
        return {prioridad: sum(1 for t in tareas if t.prioridad == prioridad) for prioridad in prioridades}
    
    def _contar_por_proyecto(self, tareas):
        proyectos = set(t.proyecto for t in tareas if t.proyecto)
        return {proyecto: sum(1 for t in tareas if t.proyecto == proyecto) for proyecto in proyectos}
    
    def _calcular_eficiencia_semanal(self, tareas):
        # Tareas completadas en los últimos 7 días
        una_semana_atras = datetime.now() - timedelta(days=7)
        completadas_recientes = [
            t for t in tareas 
            if t.estado == "completada" and t.fecha_completada and 
            datetime.fromisoformat(t.fecha_completada) >= una_semana_atras
        ]
        
        return len(completadas_recientes)