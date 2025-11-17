# Abre el archivo en VS Code y pega ESTE contenido completo:

import sqlite3
from datetime import datetime
import os

class DatabaseManager:
    """Manager profesional para base de datos SQLite con auditoría."""
    
    def __init__(self, db_path="data/taskmaster.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self._init_database()
    
    def _init_database(self):
        """Inicializa la base de datos con tablas y campos de auditoría."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Tabla de tareas con campos de auditoría
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tareas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT NOT NULL,
                    descripcion TEXT,
                    estado TEXT DEFAULT 'pendiente',
                    prioridad TEXT DEFAULT 'media',
                    proyecto TEXT,
                    fecha_creacion TIMESTAMP,
                    fecha_vencimiento TIMESTAMP,
                    fecha_completada TIMESTAMP,
                    creado_por TEXT DEFAULT 'sistema',
                    actualizado_por TEXT DEFAULT 'sistema',
                    actualizado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    usuario TEXT DEFAULT 'sistema'
                )
            ''')
            
            # Tabla de proyectos (para escalabilidad futura)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS proyectos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL UNIQUE,
                    descripcion TEXT,
                    creado_por TEXT DEFAULT 'sistema',
                    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()