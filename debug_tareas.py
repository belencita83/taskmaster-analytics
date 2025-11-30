# debug_tareas.py
import sys
import os
sys.path.append('.')

from core.storage import GestorAlmacenamiento

def debug_tareas():
    print("🔍 INICIANDO DEPURACIÓN DE TAREAS")
    print("=" * 60)
    
    try:
        gestor = GestorAlmacenamiento('sqlite')
        tareas = gestor.cargar_tareas()
        
        print(f"📊 TOTAL TAREAS ENCONTRADAS: {len(tareas)}")
        print("=" * 60)
        
        tareas_con_id = 0
        tareas_sin_id = 0
        
        for i, tarea in enumerate(tareas):
            tiene_id = hasattr(tarea, 'id')
            titulo = getattr(tarea, 'titulo', 'SIN TITULO')
            estado = getattr(tarea, 'estado', 'SIN ESTADO')
            prioridad = getattr(tarea, 'prioridad', 'SIN PRIORIDAD')
            
            if tiene_id:
                tarea_id = tarea.id
                tareas_con_id += 1
                status = "✅ CON ID"
            else:
                tarea_id = "SIN ID"
                tareas_sin_id += 1
                status = "❌ SIN ID"
            
            print(f"{i+1:2d}. {status}")
            print(f"     ID: {tarea_id}")
            print(f"     Título: '{titulo}'")
            print(f"     Estado: {estado}")
            print(f"     Prioridad: {prioridad}")
            print(f"     Tipo: {type(tarea)}")
            
            # Mostrar todos los atributos disponibles
            atributos = [attr for attr in dir(tarea) if not attr.startswith('_')]
            print(f"     Atributos: {atributos}")
            print("     " + "-" * 40)
        
        print("=" * 60)
        print(f"📈 RESUMEN:")
        print(f"   Total tareas: {len(tareas)}")
        print(f"   Tareas con ID: {tareas_con_id}")
        print(f"   Tareas sin ID: {tareas_sin_id}")
        print(f"   Porcentaje con ID: {(tareas_con_id/len(tareas))*100:.1f}%")
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_tareas()