# core/analytics.py
from datetime import datetime, timedelta
from collections import defaultdict

class AnalyticsEngine:
    """Motor de análisis avanzado para métricas de productividad."""
    
    def __init__(self, tarea_manager):
        self.tarea_manager = tarea_manager
    
    def generar_matriz_metricas(self, usuario=None, periodo_dias=30):
        """
        Genera una matriz completa de métricas como sistema de calificación.
        """
        tareas = self.tarea_manager.storage.cargar_tareas(usuario)
        fecha_inicio = datetime.now() - timedelta(days=periodo_dias)
        
        # Filtrar tareas del período
        tareas_periodo = [
            t for t in tareas 
            if t.fecha_creacion and t.fecha_creacion >= fecha_inicio
        ]
        
        matriz = {
            'periodo_analisis': f"Últimos {periodo_dias} días",
            'fecha_generacion': datetime.now().isoformat(),
            'usuario': usuario or 'todos',
            
            # MÉTRICAS PRINCIPALES (CALIFICACIONES)
            'calificaciones': self._calcular_calificaciones(tareas_periodo),
            
            # MATRIZ DE PRODUCTIVIDAD
            'matriz_productividad': self._generar_matriz_productividad(tareas_periodo),
            
            # ANÁLISIS TEMPORAL
            'analisis_temporal': self._analizar_tendencias_temporales(tareas_periodo),
            
            # EFICIENCIA POR PROYECTO
            'eficiencia_proyectos': self._calcular_eficiencia_proyectos(tareas_periodo),
            
            # SCORE FINAL
            'score_final': self._calcular_score_final(tareas_periodo)
        }
        
        return matriz
    
    def _calcular_calificaciones(self, tareas):
        """Calcula calificaciones individuales por categoría (0-100)."""
        total_tareas = len(tareas)
        if total_tareas == 0:
            return {
                'completitud': 0,
                'puntualidad': 0,
                'priorizacion': 0,
                'consistencia': 0,
                'velocidad': 0
            }
        
        # Completitud (% de tareas completadas)
        completadas = sum(1 for t in tareas if t.estado == "completada")
        calif_completitud = (completadas / total_tareas) * 100
        
        # Puntualidad (% de tareas completadas a tiempo)
        tareas_completadas = [t for t in tareas if t.estado == "completada"]
        a_tiempo = 0
        for tarea in tareas_completadas:
            if (tarea.fecha_vencimiento and tarea.fecha_completada and
                tarea.fecha_completada <= self._parse_fecha(tarea.fecha_vencimiento)):
                a_tiempo += 1
        
        calif_puntualidad = (a_tiempo / len(tareas_completadas) * 100) if tareas_completadas else 0
        
        # Priorización (% de tareas de alta prioridad completadas)
        tareas_alta_prioridad = [t for t in tareas if t.prioridad == "alta"]
        alta_completadas = sum(1 for t in tareas_alta_prioridad if t.estado == "completada")
        calif_priorizacion = (alta_completadas / len(tareas_alta_prioridad) * 100) if tareas_alta_prioridad else 100
        
        # Consistencia (Distribución uniforme de trabajo)
        calif_consistencia = self._calcular_consistencia(tareas)
        
        # Velocidad (Tiempo promedio de completado)
        calif_velocidad = self._calcular_velocidad(tareas)
        
        return {
            'completitud': round(calif_completitud, 1),
            'puntualidad': round(calif_puntualidad, 1),
            'priorizacion': round(calif_priorizacion, 1),
            'consistencia': round(calif_consistencia, 1),
            'velocidad': round(calif_velocidad, 1)
        }
    
    def _generar_matriz_productividad(self, tareas):
        """Genera matriz de productividad por día de la semana."""
        dias_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
        matriz = {dia: {'creadas': 0, 'completadas': 0} for dia in dias_semana}
        
        for tarea in tareas:
            if tarea.fecha_creacion:
                dia_creacion = tarea.fecha_creacion.strftime('%A')
                dia_creacion_es = self._traducir_dia(dia_creacion)
                if dia_creacion_es in matriz:
                    matriz[dia_creacion_es]['creadas'] += 1
            
            if tarea.estado == "completada" and tarea.fecha_completada:
                dia_completado = tarea.fecha_completada.strftime('%A')
                dia_completado_es = self._traducir_dia(dia_completado)
                if dia_completado_es in matriz:
                    matriz[dia_completado_es]['completadas'] += 1
        
        return matriz
    
    def _analizar_tendencias_temporales(self, tareas):
        """Analiza tendencias de productividad por semana."""
        tendencias = defaultdict(lambda: {'creadas': 0, 'completadas': 0})
        
        for tarea in tareas:
            if tarea.fecha_creacion:
                semana = tarea.fecha_creacion.strftime('%Y-%U')
                tendencias[semana]['creadas'] += 1
            
            if tarea.estado == "completada" and tarea.fecha_completada:
                semana = tarea.fecha_completada.strftime('%Y-%U')
                tendencias[semana]['completadas'] += 1
        
        # Ordenar por semana
        tendencias_ordenadas = dict(sorted(tendencias.items()))
        return tendencias_ordenadas
    
    def _calcular_eficiencia_proyectos(self, tareas):
        """Calcula eficiencia por proyecto."""
        proyectos = set(t.proyecto for t in tareas if t.proyecto)
        eficiencia = {}
        
        for proyecto in proyectos:
            tareas_proyecto = [t for t in tareas if t.proyecto == proyecto]
            total = len(tareas_proyecto)
            completadas = sum(1 for t in tareas_proyecto if t.estado == "completada")
            eficiencia[proyecto] = {
                'total_tareas': total,
                'completadas': completadas,
                'porcentaje_completado': (completadas / total * 100) if total > 0 else 0,
                'tareas_pendientes': total - completadas
            }
        
        return eficiencia
    
    def _calcular_consistencia(self, tareas):
        """Calcula consistencia en la distribución del trabajo."""
        if len(tareas) < 7:
            return 100
        
        tareas_por_dia = defaultdict(int)
        for tarea in tareas:
            if tarea.fecha_creacion:
                dia = tarea.fecha_creacion.strftime('%A')
                tareas_por_dia[dia] += 1
        
        if len(tareas_por_dia) > 0:
            promedio = len(tareas) / 7
            diferencias = sum(abs(count - promedio) for count in tareas_por_dia.values())
            max_diferencia_posible = len(tareas)
            
            if max_diferencia_posible > 0:
                return max(0, 100 - (diferencias / max_diferencia_posible * 100))
        
        return 100
    
    def _calcular_velocidad(self, tareas):
        """Calcula velocidad promedio de completado."""
        tareas_completadas = [
            t for t in tareas 
            if t.estado == "completada" and t.fecha_creacion and t.fecha_completada
        ]
        
        if not tareas_completadas:
            return 100
        
        tiempos = []
        for tarea in tareas_completadas:
            try:
                tiempo = (tarea.fecha_completada - tarea.fecha_creacion).total_seconds() / 3600
                tiempos.append(tiempo)
            except (ValueError, AttributeError, TypeError):
                continue
        
        if not tiempos:
            return 100
        
        tiempo_promedio = sum(tiempos) / len(tiempos)
        if tiempo_promedio <= 48:
            return 100
        else:
            return max(0, 100 - (tiempo_promedio - 48) / 24 * 10)
    
    def _calcular_score_final(self, tareas):
        """Calcula score final ponderado."""
        calificaciones = self._calcular_calificaciones(tareas)
        
        pesos = {
            'completitud': 0.30,
            'puntualidad': 0.25, 
            'priorizacion': 0.20,
            'consistencia': 0.15,
            'velocidad': 0.10
        }
        
        score_final = sum(calificaciones[categoria] * peso 
                         for categoria, peso in pesos.items())
        
        return round(score_final, 1)
    
    def _traducir_dia(self, dia_ingles):
        """Traduce día de inglés a español."""
        traducciones = {
            'Monday': 'Lunes',
            'Tuesday': 'Martes', 
            'Wednesday': 'Miércoles',
            'Thursday': 'Jueves',
            'Friday': 'Viernes',
            'Saturday': 'Sábado',
            'Sunday': 'Domingo'
        }
        return traducciones.get(dia_ingles, dia_ingles)
    
    def _parse_fecha(self, fecha_str):
        """Convierte string de fecha a datetime object de forma segura."""
        if not fecha_str or not isinstance(fecha_str, str):
            return None
        
        try:
            return datetime.fromisoformat(fecha_str)
        except (ValueError, AttributeError):
            return None