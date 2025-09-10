# core/storage.py
import json
import os
from datetime import datetime
from .models import Tarea  # Importamos la clase Tarea desde models.py

class GestorAlmacenamiento:
    """Clase que maneja la carga y guardado de tareas en un archivo JSON."""
    
    def __init__(self, archivo_datos="data/tareas.json"):
        self.archivo_datos = archivo_datos
        # Asegurarse de que el directorio 'data' existe
        os.makedirs(os.path.dirname(archivo_datos), exist_ok=True)

    def cargar_tareas(self):
        """
        Carga todas las tareas desde el archivo JSON.
        Retorna una lista de objetos Tarea.
        """
        # Si el archivo no existe, retorna una lista vacía
        if not os.path.exists(self.archivo_datos):
            return []
        
        try:
            with open(self.archivo_datos, 'r', encoding='utf-8') as archivo:
                datos = json.load(archivo)
                
            tareas = []
            for tarea_data in datos:
                # 1. Crear una nueva tarea con los datos básicos
                tarea = Tarea(
                    titulo=tarea_data['titulo'],
                    descripcion=tarea_data['descripcion'],
                    prioridad=tarea_data['prioridad'],
                    proyecto=tarea_data['proyecto'],
                    fecha_vencimiento=tarea_data['fecha_vencimiento']
                )
                # 2. Establecer todos los demás atributos
                tarea.id = tarea_data['id']
                tarea.estado = tarea_data['estado']
                tarea.fecha_creacion = datetime.fromisoformat(tarea_data['fecha_creacion']) if tarea_data['fecha_creacion'] else None
                tarea.fecha_completada = datetime.fromisoformat(tarea_data['fecha_completada']) if tarea_data['fecha_completada'] else None
                
                tareas.append(tarea)
                
            return tareas
            
        except (json.JSONDecodeError, FileNotFoundError):
            # Si el archivo está corrupto o no se puede leer, retorna una lista vacía
            return []

    def guardar_tareas(self, tareas):
        """
        Guarda una lista de tareas en el archivo JSON.
        """
        # Convertir cada objeto Tarea a un diccionario para poder serializarlo a JSON
        datos_a_guardar = []
        for tarea in tareas:
            tarea_dict = {
                'id': tarea.id,
                'titulo': tarea.titulo,
                'descripcion': tarea.descripcion,
                'estado': tarea.estado,
                'prioridad': tarea.prioridad,
                'proyecto': tarea.proyecto,
                'fecha_creacion': tarea.fecha_creacion.isoformat() if tarea.fecha_creacion else None,
                'fecha_vencimiento': tarea.fecha_vencimiento,
                'fecha_completada': tarea.fecha_completada.isoformat() if tarea.fecha_completada else None
            }
            datos_a_guardar.append(tarea_dict)
        
        # Escribir el archivo JSON
        with open(self.archivo_datos, 'w', encoding='utf-8') as archivo:
            json.dump(datos_a_guardar, archivo, indent=2, ensure_ascii=False)