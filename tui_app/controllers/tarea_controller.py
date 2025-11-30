# tui_app/controllers/tarea_controller.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from core.storage import GestorAlmacenamiento
from core.managers import TareaManager

class TareaController:
    """
    Controlador que conecta las pantallas TUI con el Manager y Storage.
    Maneja la lógica de presentación y formateo de datos.
    """
    
    def __init__(self):
        # Inicializar las dependencias (igual que en tus pantallas)
        self.gestor = GestorAlmacenamiento("sqlite")
        self.manager = TareaManager(self.gestor)
    
    def crear_tarea(self, form_data: dict) -> dict:
        """
        Crea una nueva tarea desde los datos del formulario.
        
        Args:
            form_data: Diccionario con datos del formulario
            
        Returns:
            dict: Resultado de la operación {success, message, data}
        """
        try:
            # Extraer datos del formulario
            titulo = form_data.get('titulo', '').strip()
            descripcion = form_data.get('descripcion', '').strip()
            prioridad = form_data.get('prioridad', 'media')
            proyecto = form_data.get('proyecto', '').strip() or None
            usuario = form_data.get('usuario', 'tui_user')
            
            # Validar campos obligatorios
            if not titulo:
                return {
                    'success': False,
                    'message': 'ERROR: El título es obligatorio',
                    'data': None
                }
            
            if not prioridad:
                return {
                    'success': False, 
                    'message': 'ERROR: Debe seleccionar una prioridad',
                    'data': None
                }
            
            # Usar el Manager para crear la tarea (igual que en tu código)
            nueva_tarea = self.manager.crear_tarea(
                titulo=titulo,
                descripcion=descripcion or "",
                prioridad=prioridad,
                proyecto=proyecto,
                usuario=usuario
            )
            
            return {
                'success': True,
                'message': f'ÉXITO: Tarea "{titulo}" creada',
                'data': {
                    'id': nueva_tarea.id,
                    'titulo': nueva_tarea.titulo,
                    'prioridad': nueva_tarea.prioridad
                }
            }
            
        except ValueError as e:
            # Error de validación del Manager
            return {
                'success': False,
                'message': f'{str(e)}',
                'data': None
            }
        except Exception as e:
            # Error inesperado
            return {
                'success': False,
                'message': f'ERROR: {str(e)}',
                'data': None
            }
    
    def obtener_todas_tareas(self, usuario: str = None) -> dict:
        try:
            if usuario is None:
                tareas = self.gestor.cargar_tareas()  # Todas las tareas
                mensaje_usuario = "todas las tareas"
            else:
                tareas = self.gestor.cargar_tareas(usuario)  # Solo del usuario
                mensaje_usuario = f"tareas de '{usuario}'"
            
            tareas_formateadas = []
            
            for tarea in tareas:
                # Verificar que tenga los atributos básicos
                if not hasattr(tarea, 'titulo') or not hasattr(tarea, 'id'):
                    continue
                
                # Obtener datos
                titulo = tarea.titulo
                tarea_id = tarea.id
                estado = getattr(tarea, 'estado', 'pendiente')
                prioridad = getattr(tarea, 'prioridad', 'media')
                proyecto = getattr(tarea, 'proyecto', None)
                tarea_usuario = getattr(tarea, 'usuario', 'desconocido')
                
                # Emojis
                estado_emoji = {"pendiente": "⏳", "en_progreso": "🎨", "completada": "🎉"}
                prioridad_emoji = {"alta": "🔴", "media": "🟡", "baja": "🟢"}
                
                display_text = f"{tarea_id}. {titulo} - {estado_emoji.get(estado)} {estado} - {prioridad_emoji.get(prioridad)}"
                
                tareas_formateadas.append({
                    'id': tarea_id,
                    'titulo': titulo,
                    'descripcion': getattr(tarea, 'descripcion', ''),
                    'prioridad': prioridad,
                    'proyecto': proyecto,
                    'estado': estado,
                    'fecha_creacion': getattr(tarea, 'fecha_creacion', None),
                    'usuario': tarea_usuario,
                    'display_text': display_text,
                    'display_detalles': f"Proyecto: {proyecto or 'Sin proyecto'} | Usuario: {tarea_usuario}"
                })
            
            return {
                'success': True,
                'message': f'Encontradas {len(tareas_formateadas)} {mensaje_usuario}',
                'data': tareas_formateadas
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error cargando tareas: {str(e)}',
                'data': []
            }
    
    def obtener_tareas_usuario(self, usuario: str = "tui_user") -> dict:
        """
        Método específico para obtener tareas de un usuario particular.
        """
        return self.obtener_todas_tareas(usuario)

    def obtener_estadisticas(self, usuario: str = None) -> dict:
        """
        Obtiene estadísticas formateadas para la UI.
        
        Returns:
            dict: {success, message, data}
        """
        try:
            tareas = self.gestor.cargar_tareas(usuario)
            
            # Calcular estadísticas (igual que en tu TaskListScreen)
            total = len(tareas)
            pendientes = sum(1 for t in tareas if t.estado == "pendiente")
            en_progreso = sum(1 for t in tareas if t.estado == "en_progreso")
            completadas = sum(1 for t in tareas if t.estado == "completada")
            
            # Calcular por prioridad
            alta = sum(1 for t in tareas if t.prioridad == "alta")
            media = sum(1 for t in tareas if t.prioridad == "media")
            baja = sum(1 for t in tareas if t.prioridad == "baja")
            
            # Tareas vencidas y próximas a vencer (usando tu manager)
            vencidas = self.manager.obtener_tareas_vencidas(usuario)
            proximas = self.manager.obtener_tareas_proximas_a_vencer(3, usuario)
            
            return {
                'success': True,
                'message': 'Estadísticas calculadas',
                'data': {
                    'total_tareas': total,
                    'por_estado': {
                        'pendiente': pendientes,
                        'en_progreso': en_progreso,
                        'completada': completadas
                    },
                    'por_prioridad': {
                        'alta': alta,
                        'media': media,
                        'baja': baja
                    },
                    'tareas_vencidas': len(vencidas),
                    'tareas_proximas': len(proximas),
                    'porcentaje_completadas': (completadas / total * 100) if total > 0 else 0
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error calculando estadísticas: {str(e)}',
                'data': {}
            }
    
    def buscar_tareas(self, search_term: str, usuario: str = None) -> dict:
        """
        Busca tareas por término (igual que en tu TaskListScreen).
        
        Returns:
            dict: {success, message, data}
        """
        try:
            tareas = self.gestor.cargar_tareas(usuario)
            
            if search_term:
                tareas = [t for t in tareas if search_term.lower() in t.titulo.lower()]
            
            # Formatear resultados
            tareas_formateadas = []
            for tarea in tareas:
                if hasattr(tarea, 'id'):
                    estado_emoji = {"pendiente": "⏳", "en_progreso": "🎨", "completada": "🎉"}
                    prioridad_emoji = {"alta": "🔴", "media": "🟡", "baja": "🟢"}
                    
                    estado = tarea.estado or "pendiente"
                    prioridad = tarea.prioridad or "media"
                    
                    display_text = f"{tarea.id}. {tarea.titulo} - {estado_emoji.get(estado)} {estado} - {prioridad_emoji.get(prioridad)}"
                    
                    tareas_formateadas.append({
                        'id': tarea.id,
                        'titulo': tarea.titulo,
                        'display_text': display_text,
                        'estado': estado,
                        'prioridad': prioridad
                    })
            
            return {
                'success': True,
                'message': f'{len(tareas_formateadas)} tareas encontradas para "{search_term}"',
                'data': tareas_formateadas
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error buscando tareas: {str(e)}',
                'data': []
            }
    
    def cambiar_estado_tarea(self, tarea_id: int, usuario: str = None) -> dict:
        """
        Cambia el estado de una tarea (igual que en tu TaskListScreen).
        
        Returns:
            dict: {success, message, data}
        """
        try:
            tareas = self.gestor.cargar_tareas(usuario)
            tarea = next((t for t in tareas if hasattr(t, 'id') and t.id == tarea_id), None)
            
            if not tarea:
                return {
                    'success': False,
                    'message': f'Tarea con ID {tarea_id} no encontrada',
                    'data': None
                }
            
            # Cambiar estado en ciclo (igual que en tu código)
            if tarea.estado == "pendiente":
                new_status = "en_progreso"
                emoji = "🎨"
            elif tarea.estado == "en_progreso":
                new_status = "completada" 
                emoji = "🎉"
            else:
                new_status = "pendiente"
                emoji = "⏳"
            
            tarea.estado = new_status
            self.gestor.guardar_tarea(tarea)
            
            return {
                'success': True,
                'message': f'{emoji} Tarea "{tarea.titulo}" ahora está: {new_status}',
                'data': {
                    'tarea_id': tarea_id,
                    'nuevo_estado': new_status,
                    'titulo': tarea.titulo
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error cambiando estado: {str(e)}',
                'data': None
            }
        
    def actualizar_tarea(self, tarea_id, datos_actualizados):
        """Actualizar una tarea existente usando el GestorAlmacenamiento."""
        try:
            # Cargar todas las tareas
            tareas = self.gestor.cargar_tareas()
            
            # Buscar la tarea específica
            tarea = None
            for t in tareas:
                if hasattr(t, 'id') and t.id == tarea_id:
                    tarea = t
                    break
            
            if not tarea:
                return {
                    'success': False,
                    'message': f'Tarea con ID {tarea_id} no encontrada'
                }
            
            # Guardar el título original para el mensaje
            titulo_original = tarea.titulo
            
            # Actualizar campos
            if 'titulo' in datos_actualizados:
                tarea.titulo = datos_actualizados['titulo']
            if 'descripcion' in datos_actualizados:
                tarea.descripcion = datos_actualizados['descripcion']
            if 'prioridad' in datos_actualizados:
                tarea.prioridad = datos_actualizados['prioridad']
            if 'proyecto' in datos_actualizados:
                tarea.proyecto = datos_actualizados['proyecto']
            
            # Guardar cambios usando el gestor
            self.gestor.guardar_tarea(tarea)
            
            return {
                'success': True,
                'message': f'Tarea "{titulo_original}" actualizada correctamente',
                'data': self._tarea_to_dict(tarea)
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error actualizando tarea: {str(e)}'
            }
    
    def eliminar_tarea(self, tarea_id):
        """Eliminar una tarea - CON DEPURACIÓN."""
        try:
            print(f"Iniciando eliminación de tarea ID: {tarea_id}")
            
            # Verificar que el gestor y almacenamiento existen
            if not hasattr(self, 'gestor'):
                return {'success': False, 'message': 'Gestor no disponible'}
            
            if not hasattr(self.gestor, 'almacenamiento'):
                return {'success': False, 'message': 'Almacenamiento no disponible'}
            
            print(f"Gestor: {type(self.gestor)}")
            print(f"Almacenamiento: {type(self.gestor.almacenamiento)}")
            print(f"Métodos disponibles: {[m for m in dir(self.gestor.almacenamiento) if not m.startswith('_')]}")
            
            # Obtener información de la tarea
            tareas = self.gestor.cargar_tareas()
            tarea_a_eliminar = None
            
            for tarea in tareas:
                if hasattr(tarea, 'id') and tarea.id == tarea_id:
                    tarea_a_eliminar = tarea
                    break
            
            if not tarea_a_eliminar:
                print(f"Tarea {tarea_id} no encontrada en la lista")
                return {
                    'success': False,
                    'message': f'Tarea con ID {tarea_id} no encontrada'
                }
            
            print(f"Tarea encontrada: '{tarea_a_eliminar.titulo}' (ID: {tarea_a_eliminar.id})")
            
            # Contar tareas antes
            count_antes = len(tareas)
            print(f"Tareas antes de eliminar: {count_antes}")
            
            # Eliminar la tarea
            print("Ejecutando eliminación...")
            resultado = self.gestor.eliminar_tarea(tarea_id)
            print(f"Resultado de eliminación: {resultado}")
            
            if resultado:
                # Verificar que se eliminó
                tareas_despues = self.gestor.cargar_tareas()
                count_despues = len(tareas_despues)
                print(f"Tareas después de eliminar: {count_despues}")
                
                tarea_verificada = None
                for tarea in tareas_despues:
                    if hasattr(tarea, 'id') and tarea.id == tarea_id:
                        tarea_verificada = tarea
                        break
                
                if not tarea_verificada:
                    print("¡Tarea eliminada correctamente!")
                    return {
                        'success': True,
                        'message': f'Tarea "{tarea_a_eliminar.titulo}" eliminada correctamente'
                    }
                else:
                    print("La tarea sigue existiendo después de eliminar")
                    return {
                        'success': False,
                        'message': f'La tarea "{tarea_a_eliminar.titulo}" no se eliminó correctamente'
                    }
            else:
                print("El método eliminar_tarea retornó False")
                return {
                    'success': False,
                    'message': f'Error en el proceso de eliminación de "{tarea_a_eliminar.titulo}"'
                }
                
        except Exception as e:
            print(f"Error eliminando tarea: {e}")
            return {
                'success': False,
                'message': f'Error eliminando tarea: {str(e)}'
            }
    
    def _tarea_to_dict(self, tarea):
        """Convertir objeto tarea a diccionario para la UI."""
        return {
            'id': tarea.id,
            'titulo': tarea.titulo,
            'descripcion': getattr(tarea, 'descripcion', ''),
            'prioridad': getattr(tarea, 'prioridad', 'media'),
            'proyecto': getattr(tarea, 'proyecto', None),
            'estado': getattr(tarea, 'estado', 'pendiente'),
            'fecha_creacion': getattr(tarea, 'fecha_creacion', None),
            'usuario': getattr(tarea, 'usuario', 'desconocido')
        }