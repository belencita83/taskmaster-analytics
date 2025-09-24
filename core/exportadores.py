# core/exportadores.py
import csv
import json
from datetime import datetime

class ExportadorReportes:
    """Sistema profesional de exportación de reportes."""
    
    @staticmethod
    def exportar_csv(reporte, filename=None):
        """Exporta reporte a formato CSV."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"reporte_tareas_{timestamp}.csv"
        
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            
            # Encabezados
            writer.writerow(['REPORTE DE TAREAS - TASKMASTER ANALYTICS'])
            writer.writerow(['Fecha generación:', reporte['fecha_generacion']])
            writer.writerow(['Usuario:', reporte['usuario']])
            writer.writerow([])
            
            # Resumen
            writer.writerow(['RESUMEN GENERAL'])
            resumen = reporte['resumen']
            writer.writerow(['Total tareas:', resumen['total_tareas']])
            writer.writerow(['Completadas:', resumen['completadas']])
            writer.writerow(['Pendientes:', resumen['pendientes']])
            writer.writerow(['Porcentaje completado:', f"{resumen['porcentaje_completado']:.1f}%"])
            writer.writerow([])
            
            # Tareas por estado
            writer.writerow(['TAREAS POR ESTADO'])
            for estado, cantidad in reporte['tareas_por_estado'].items():
                writer.writerow([estado.capitalize(), cantidad])
            writer.writerow([])
            
            # Tareas por prioridad
            writer.writerow(['TAREAS POR PRIORIDAD'])
            for prioridad, cantidad in reporte['tareas_por_prioridad'].items():
                writer.writerow([prioridad.capitalize(), cantidad])
            writer.writerow([])
            
            # Métricas adicionales
            writer.writerow(['MÉTRICAS ADICIONALES'])
            writer.writerow(['Tareas vencidas:', reporte['tareas_vencidas']])
            writer.writerow(['Tareas próximas a vencer:', reporte['tareas_proximas_vencer']])
            writer.writerow(['Eficiencia semanal:', reporte['eficiencia_semanal']])
        
        return filename
    
    @staticmethod
    def exportar_json(reporte, filename=None):
        """Exporta reporte a formato JSON."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"reporte_tareas_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(reporte, file, indent=2, ensure_ascii=False)
        
        return filename
    
    @staticmethod
    def exportar_texto(reporte, filename=None):
        """Exporta reporte a formato de texto legible."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"reporte_tareas_{timestamp}.txt"
        
        with open(filename, 'w', encoding='utf-8') as file:
            file.write("="*60 + "\n")
            file.write("           REPORTE DE TAREAS - TASKMASTER ANALYTICS\n")
            file.write("="*60 + "\n\n")
            
            file.write(f"Fecha generación: {reporte['fecha_generacion']}\n")
            file.write(f"Usuario: {reporte['usuario']}\n\n")
            
            # Resumen
            resumen = reporte['resumen']
            file.write("RESUMEN GENERAL:\n")
            file.write(f"  • Total tareas: {resumen['total_tareas']}\n")
            file.write(f"  • Completadas: {resumen['completadas']}\n")
            file.write(f"  • Pendientes: {resumen['pendientes']}\n")
            file.write(f"  • Porcentaje completado: {resumen['porcentaje_completado']:.1f}%\n\n")
            
            # Tareas por estado
            file.write("TAREAS POR ESTADO:\n")
            for estado, cantidad in reporte['tareas_por_estado'].items():
                file.write(f"  • {estado.capitalize()}: {cantidad}\n")
            file.write("\n")
            
            # Tareas por prioridad
            file.write("TAREAS POR PRIORIDAD:\n")
            for prioridad, cantidad in reporte['tareas_por_prioridad'].items():
                file.write(f"  • {prioridad.capitalize()}: {cantidad}\n")
            file.write("\n")
            
            # Métricas adicionales
            file.write("MÉTRICAS ADICIONALES:\n")
            file.write(f"  • Tareas vencidas: {reporte['tareas_vencidas']}\n")
            file.write(f"  • Tareas próximas a vencer: {reporte['tareas_proximas_vencer']}\n")
            file.write(f"  • Eficiencia semanal: {reporte['eficiencia_semanal']}\n")
        
        return filename