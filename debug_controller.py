# debug_controller.py
import sys
import os
sys.path.append('.')

from tui_app.controllers.tarea_controller import TareaController

def debug_controller():
    print("🔍 DEPURANDO CONTROLADOR")
    print("=" * 60)
    
    try:
        controller = TareaController()
        resultado = controller.obtener_todas_tareas()
        
        print(f"✅ Resultado éxito: {resultado['success']}")
        print(f"📝 Mensaje: {resultado['message']}")
        print(f"📊 Tareas devueltas: {len(resultado['data'])}")
        print("=" * 60)
        
        if resultado['success']:
            for i, tarea in enumerate(resultado['data']):
                print(f"{i+1:2d}. ID: {tarea['id']} - '{tarea['titulo']}'")
                print(f"     Display: {tarea['display_text']}")
                print("     " + "-" * 40)
        
        print("=" * 60)
        print(f"🎯 CONTROLADOR REPORTÓ: {len(resultado['data'])} tareas")
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_controller()