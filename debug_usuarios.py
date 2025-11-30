# debug_usuarios.py
import sys
sys.path.append('.')
from core.storage import GestorAlmacenamiento

gestor = GestorAlmacenamiento('sqlite')
tareas = gestor.cargar_tareas()

print("🔍 ANÁLISIS DE USUARIOS POR TAREA")
print("=" * 60)

usuarios = {}
for tarea in tareas:
    usuario = getattr(tarea, 'usuario', 'sin_usuario')
    if usuario not in usuarios:
        usuarios[usuario] = []
    usuarios[usuario].append(tarea)

print(f"📊 DISTRIBUCIÓN POR USUARIO:")
for usuario, tareas_usuario in usuarios.items():
    print(f"   👤 '{usuario}': {len(tareas_usuario)} tareas")
    for tarea in tareas_usuario:
        print(f"      - ID {tarea.id}: {tarea.titulo}")

print("=" * 60)
print(f"🎯 TOTAL: {len(tareas)} tareas")
print(f"🔍 Usuario por defecto del controlador: 'tui_user'")