# test_tarea.py
import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from core.models import Tarea

# Crear una tarea de prueba
tarea_test = Tarea("Testear la aplicación", "Verificar que todo funcione", "alta", "Desarrollo")
print("✅ Tarea creada exitosamente!")
print(f"Tarea: {tarea_test}")
print(f"Título: {tarea_test.titulo}")
print(f"Estado: {tarea_test.estado}")