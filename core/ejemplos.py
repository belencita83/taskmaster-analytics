# ejemplos.py - Datos de ejemplo para la demo
from core.managers import TareaManager
from core.storage import GestorAlmacenamiento

def crear_datos_ejemplo():
    gestor = GestorAlmacenamiento("sqlite")
    manager = TareaManager(gestor)
    
    ejemplos = [
        ("Completar proyecto Python", "Terminar TaskMaster Analytics", "alta", "Universidad"),
        ("Estudiar para examen", "Repasar temas 1-5", "alta", "Estudios"),
        ("Hacer ejercicio", "30 minutos de cardio", "media", "Salud"),
        ("Leer libro técnico", "Avanzar 2 capítulos", "baja", "Desarrollo Personal"),
    ]
    
    for titulo, desc, prioridad, proyecto in ejemplos:
        try:
            manager.crear_tarea(titulo, desc, prioridad, proyecto, "demo")
            print(f"✅ Creada: {titulo}")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    crear_datos_ejemplo()