# console_app/app.py
import sys
import os
from datetime import datetime

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.models import Tarea
from core.storage import GestorAlmacenamiento

class TaskMasterApp:
    def __init__(self):
        self.gestor = GestorAlmacenamiento()
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
            print("6. 💾 Guardar y salir")
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
        
        self.tareas.append(nueva_tarea)
        print(f"✅ Tarea '{titulo}' creada exitosamente!")

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
                print(f"✅ Tarea '{tarea.titulo}' marcada como COMPLETADA!")
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
                tarea = self.tareas.pop(numero)
                print(f"🗑️ Tarea '{tarea.titulo}' eliminada exitosamente!")
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