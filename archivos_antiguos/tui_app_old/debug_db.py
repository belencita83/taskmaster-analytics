# tui_app/debug_db.py
import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from core.storage import GestorAlmacenamiento

def debug_database():
    print("🔍 DEBUG - CONEXIÓN A BASE DE DATOS")
    print("=" * 50)
    
    try:
        gestor = GestorAlmacenamiento("sqlite")
        tareas = gestor.cargar_tareas()
        
        print(f"✅ Conexión exitosa")
        print(f"📊 Tareas encontradas: {len(tareas)}")
        
        for tarea in tareas[:3]:  # Mostrar primeras 3
            print(f"  - {tarea.titulo} ({tarea.estado})")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    debug_database()