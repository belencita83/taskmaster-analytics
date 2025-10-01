# Abre el archivo y pega ESTE contenido completo:

import sqlite3
from datetime import datetime
from .models import Tarea

class SQLiteStorage:
    """Gestor de almacenamiento profesional con SQLite y auditoría."""
    
    def __init__(self, db_path="data/taskmaster.db"):
        self.db_path = db_path
        from .database import DatabaseManager
        self.db_manager = DatabaseManager(db_path)
    
    def cargar_tareas(self, usuario=None):
        """Carga tareas desde SQLite, con filtro por usuario."""
        tareas = []
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                if usuario:
                    cursor.execute('''
                        SELECT * FROM tareas WHERE usuario = ? ORDER BY fecha_creacion DESC
                    ''', (usuario,))
                else:
                    cursor.execute('SELECT * FROM tareas ORDER BY fecha_creacion DESC')
                
                for row in cursor.fetchall():
                    tarea = Tarea(
                        titulo=row['titulo'],
                        descripcion=row['descripcion'],
                        prioridad=row['prioridad'],
                        proyecto=row['proyecto'],
                        fecha_vencimiento=row['fecha_vencimiento'],
                        usuario=row['usuario']
                    )
                    
                    tarea.id = row['id']
                    tarea.estado = row['estado']
                    
                    # ✅ CORRECCIÓN: Validar fechas antes de convertir
                    if row['fecha_creacion']:
                        try:
                            tarea.fecha_creacion = datetime.fromisoformat(row['fecha_creacion'])
                        except (ValueError, AttributeError):
                            tarea.fecha_creacion = None
                    
                    if row['fecha_completada']:
                        try:
                            tarea.fecha_completada = datetime.fromisoformat(row['fecha_completada'])
                        except (ValueError, AttributeError):
                            tarea.fecha_completada = None
                    
                    if row['actualizado_en']:
                        try:
                            tarea.actualizado_en = datetime.fromisoformat(row['actualizado_en'])
                        except (ValueError, AttributeError):
                            tarea.actualizado_en = None
                    
                    tarea.creado_por = row['creado_por']
                    tarea.actualizado_por = row['actualizado_por']
                    
                    tareas.append(tarea)
                    
        except Exception as e:
            print(f"Error cargando tareas: {e}")
            
        return tareas
    
    def guardar_tarea(self, tarea):
        """Guarda una tarea en SQLite con auditoría."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                if tarea.id is None:  # Insertar nueva
                    cursor.execute('''
                        INSERT INTO tareas 
                        (titulo, descripcion, estado, prioridad, proyecto, 
                         fecha_creacion, fecha_vencimiento, fecha_completada,
                         creado_por, actualizado_por, actualizado_en, usuario)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        tarea.titulo, tarea.descripcion, tarea.estado, tarea.prioridad,
                        tarea.proyecto, tarea.fecha_creacion.isoformat() if tarea.fecha_creacion else None,
                        tarea.fecha_vencimiento, tarea.fecha_completada.isoformat() if tarea.fecha_completada else None,
                        tarea.creado_por, tarea.actualizado_por, 
                        tarea.actualizado_en.isoformat() if tarea.actualizado_en else None,
                        tarea.usuario
                    ))
                    tarea.id = cursor.lastrowid
                    
                else:  # Actualizar existente
                    cursor.execute('''
                        UPDATE tareas 
                        SET titulo=?, descripcion=?, estado=?, prioridad=?, proyecto=?,
                            fecha_vencimiento=?, fecha_completada=?, 
                            actualizado_por=?, actualizado_en=?, usuario=?
                        WHERE id=?
                    ''', (
                        tarea.titulo, tarea.descripcion, tarea.estado, tarea.prioridad,
                        tarea.proyecto, tarea.fecha_vencimiento,
                        tarea.fecha_completada.isoformat() if tarea.fecha_completada else None,
                        tarea.actualizado_por, 
                        tarea.actualizado_en.isoformat() if tarea.actualizado_en else None,
                        tarea.usuario, tarea.id
                    ))
                
                conn.commit()
                return True
                
        except Exception as e:
            print(f"Error guardando tarea: {e}")
            return False
    
    def eliminar_tarea(self, tarea_id):
        """Elimina una tarea por ID."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM tareas WHERE id = ?', (tarea_id,))
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Error eliminando tarea: {e}")
            return False