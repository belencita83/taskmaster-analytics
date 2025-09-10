# console_app/app.py
import sys
import os

# AÑADIR ESTAS 2 LÍNEAS CRUCIALES - Solucionan el error "No module named 'core'"
# Esto le dice a Python dónde encontrar los módulos de tu proyecto
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import datetime
from core.models import Tarea
from core.storage import GestorAlmacenamiento

def main():
    print("🚀 Probando el núcleo de TaskMaster Analytics...")
    
    # 1. Crear nuestro gestor de almacenamiento
    gestor = GestorAlmacenamiento()
    
    # 2. Cargar tareas existentes (debería ser una lista vacía la primera vez)
    tareas = gestor.cargar_tareas()
    print(f"📊 Tareas cargadas: {len(tareas)}")
    
    # 3. Crear una nueva tarea de prueba si no hay tareas
    if len(tareas) == 0:
        print("📝 Creando una tarea de prueba...")
        nueva_tarea = Tarea(
            titulo="Aprender a programar en Python",
            descripcion="Completar el proyecto TaskMaster Analytics",
            prioridad="alta",
            proyecto="Estudios"
        )
        nueva_tarea.id = 1  # En el futuro esto será automático
        nueva_tarea.fecha_creacion = datetime.now()
        
        tareas.append(nueva_tarea)
        
        # 4. Guardar las tareas
        gestor.guardar_tareas(tareas)
        print("✅ Tarea guardada exitosamente!")
    
    # 5. Mostrar todas las tareas
    print("\n📋 Lista de tareas:")
    for tarea in tareas:
        print(f"  - {tarea}")

if __name__ == "__main__":
    main()