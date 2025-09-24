# console_app/app.py
import sys
import os
from datetime import datetime

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.models import Tarea
from core.storage import GestorAlmacenamiento

from core.managers import TareaManager, ReporteManager
from core.exportadores import ExportadorReportes

from core.analytics import AnalyticsEngine
from core.visualizacion import VisualizadorMetricas

class TaskMasterApp:
    def __init__(self):
        self.gestor = GestorAlmacenamiento("sqlite")
        self.tarea_manager = TareaManager(self.gestor)
        self.reporte_manager = ReporteManager(self.tarea_manager)
        self.analytics_engine = AnalyticsEngine(self.tarea_manager)  # ← NUEVO
        self.visualizador = VisualizadorMetricas()  # ← NUEVO
        self.exportador = ExportadorReportes()
        self.tareas = self.gestor.cargar_tareas()
        self.proximo_id = max([t.id for t in self.tareas], default=0) + 1

    def mostrar_menu_principal(self):
        """Muestra el menú principal y maneja las opciones."""
        while True:
            print("\n" + "="*50)
            print("🎯 TASKMASTER ANALYTICS - Menú Principal")
            print("="*50)
            print("1. 📝 Crear nueva tarea")
            print("2. 📋 Listar todas las tareas")
            print("3. ✅ Marcar tarea como completada")
            print("4. ❌ Eliminar tarea")
            print("5. 📊 Ver dashboard de productividad")
            print("6. 📈 Matriz avanzada de métricas")
            print("7. 📤 Exportar reportes")
            print("0. 💾 Guardar y salir")
            print("="*50)

            opcion = input("Selecciona una opción (1-6): ").strip()

            if opcion == "1":
                self.crear_tarea()
            elif opcion == "2":
                self.listar_tareas()
            elif opcion == "3":
                self.marcar_completada()
            elif opcion == "4":
                self.eliminar_tarea()
            elif opcion == "5":
                self.mostrar_dashboard()
            elif opcion == "6":
                self.mostrar_matriz_metricas()
            elif opcion == "7":
                self.exportar_reportes()
            elif opcion == "0":
                self.guardar_y_salir()
                break
            else:
                print("❌ Opción no válida. Intenta de nuevo.")

    def crear_tarea(self):
        """Crea una nueva tarea."""
        print("\n" + "-"*30)
        print("📝 CREAR NUEVA TAREA")
        print("-"*30)
        
        titulo = input("Título de la tarea: ").strip()
        if not titulo:
            print("❌ El título no puede estar vacío.")
            return

        descripcion = input("Descripción (opcional): ").strip()
        
        print("\nPrioridades disponibles:")
        print("1. 🔴 Alta")
        print("2. 🟡 Media")  
        print("3. 🔵 Baja")
        
        prioridad_opcion = input("Selecciona prioridad (1-3, default 2): ").strip()
        prioridades = {"1": "alta", "2": "media", "3": "baja"}
        prioridad = prioridades.get(prioridad_opcion, "media")
        
        proyecto = input("Proyecto (opcional): ").strip() or None
        fecha_vencimiento = input("Fecha de vencimiento (YYYY-MM-DD, opcional): ").strip() or None

        # Crear la nueva tarea
        nueva_tarea = Tarea(
            titulo=titulo,
            descripcion=descripcion,
            prioridad=prioridad,
            proyecto=proyecto,
            fecha_vencimiento=fecha_vencimiento
        )
        
        nueva_tarea.id = self.proximo_id
        nueva_tarea.fecha_creacion = datetime.now()
        self.proximo_id += 1
        
        if self.gestor.guardar_tarea(nueva_tarea):
            self.tareas.append(nueva_tarea)
            print(f"✅ Tarea '{titulo}' creada exitosamente!")
        else:
            print("❌ Error guardando la tarea")

    def listar_tareas(self):
        """Lista todas las tareas."""
        print("\n" + "-"*50)
        print("📋 LISTA DE TAREAS")
        print("-"*50)
        
        if not self.tareas:
            print("No hay tareas registradas.")
            return
        
        for i, tarea in enumerate(self.tareas, 1):
            print(f"{i}. {tarea}")
            if tarea.descripcion:
                print(f"   📄 {tarea.descripcion}")
            if tarea.proyecto:
                print(f"   📂 Proyecto: {tarea.proyecto}")
            print()

    def marcar_completada(self):
        """Marca una tarea como completada."""
        if not self.tareas:
            print("❌ No hay tareas para marcar como completadas.")
            return
        
        self.listar_tareas()
        try:
            numero = int(input("\nNúmero de la tarea a marcar como completada: ")) - 1
            if 0 <= numero < len(self.tareas):
                tarea = self.tareas[numero]
                tarea.marcar_completada()
                tarea.fecha_completada = datetime.now()
                tarea.actualizar_auditoria("usuario_actual")
                if self.gestor.guardar_tarea(tarea):
                    print(f"✅ Tarea '{tarea.titulo}' marcada como COMPLETADA!")
                else:
                    print("❌ Error actualizando la tarea")
            else:
                print("❌ Número de tarea no válido.")
        except ValueError:
            print("❌ Por favor ingresa un número válido.")

    def eliminar_tarea(self):
        """Elimina una tarea."""
        if not self.tareas:
            print("❌ No hay tareas para eliminar.")
            return
        
        self.listar_tareas()
        try:
            numero = int(input("\nNúmero de la tarea a eliminar: ")) - 1
            if 0 <= numero < len(self.tareas):
                tarea = self.tareas[numero]
                if self.gestor.eliminar_tarea(tarea.id):
                    self.tareas.pop(numero)
                    print(f"🗑️ Tarea '{tarea.titulo}' eliminada exitosamente!")
                else:
                    print("❌ Error eliminando la tarea")
            else:
                print("❌ Número de tarea no válido.")
        except ValueError:
            print("❌ Por favor ingresa un número válido.")

    def mostrar_dashboard(self):
        """Muestra un dashboard simple con métricas."""
        print("\n" + "="*50)
        print("📊 DASHBOARD DE PRODUCTIVIDAD")
        print("="*50)
        
        total_tareas = len(self.tareas)
        completadas = sum(1 for t in self.tareas if t.estado == "completada")
        pendientes = total_tareas - completadas
        
        print(f"📈 Total de tareas: {total_tareas}")
        print(f"✅ Completadas: {completadas}")
        print(f"⏳ Pendientes: {pendientes}")
        
        if total_tareas > 0:
            porcentaje = (completadas / total_tareas) * 100
            print(f"📊 Porcentaje de completado: {porcentaje:.1f}%")
        
        # Tareas por prioridad
        print("\n🎯 Tareas por prioridad:")
        for prioridad in ["alta", "media", "baja"]:
            count = sum(1 for t in self.tareas if t.prioridad == prioridad)
            print(f"   {prioridad.capitalize()}: {count}")

    def exportar_reportes(self):
        """Exporta reportes en diferentes formatos."""
        print("\n" + "="*50)
        print("📤 EXPORTAR REPORTES")
        print("="*50)
        
        # Generar reporte
        reporte = self.reporte_manager.generar_reporte_completo()
        
        print("Formatos disponibles:")
        print("1. 📊 CSV (Excel)")
        print("2. 🔤 JSON")
        print("3. 📝 Texto")
        
        opcion = input("Selecciona formato (1-3): ").strip()
        
        try:
            if opcion == "1":
                archivo = self.exportador.exportar_csv(reporte)
                print(f"✅ Reporte exportado a: {archivo}")
            elif opcion == "2":
                archivo = self.exportador.exportar_json(reporte)
                print(f"✅ Reporte exportado a: {archivo}")
            elif opcion == "3":
                archivo = self.exportador.exportar_texto(reporte)
                print(f"✅ Reporte exportado a: {archivo}")
            else:
                print("❌ Opción no válida")
        except Exception as e:
            print(f"❌ Error exportando reporte: {e}")

    def mostrar_matriz_metricas(self):
        """Muestra la matriz avanzada de métricas."""
        print("\n" + "="*50)
        print("📈 MATRIZ AVANZADA DE MÉTRICAS")
        print("="*50)
        try:
            # Generar matriz de métricas
            matriz = self.analytics_engine.generar_matriz_metricas()
            # Mostrar visualización
            self.visualizador.mostrar_matriz_metricas(matriz)
            # Mostrar recomendaciones
            print("\n💡 RECOMENDACIONES:")
            print("-" * 50)
            recomendaciones = self.visualizador.generar_recomendaciones(matriz)
            for i, recomendacion in enumerate(recomendaciones, 1):
                print(f"{i}. {recomendacion}")
            # Opción para exportar
            exportar = input("\n¿Exportar matriz a JSON? (s/n): ").strip().lower()
            if exportar == 's':
                from core.exportadores import ExportadorReportes
                exportador = ExportadorReportes()
                archivo = exportador.exportar_json(matriz, "matriz_metricas.json")
                print(f"✅ Matriz exportada a: {archivo}")
        except Exception as e:
            print(f"❌ Error generando matriz de métricas: {e}")
    
    def guardar_y_salir(self):
        """Guarda todas las tareas y sale."""
        self.gestor.guardar_tareas(self.tareas)
        print("💾 Todos los datos han sido guardados exitosamente!")
        print("👋 ¡Hasta pronto!")

def main():
    """Función principal de la aplicación."""
    print("🚀 Iniciando TaskMaster Analytics...")
    app = TaskMasterApp()
    app.mostrar_menu_principal()

if __name__ == "__main__":
    main()