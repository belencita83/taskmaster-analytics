# ver_bd.py
import sqlite3
import os

def ver_base_datos():
    """Muestra el contenido de la base de datos usando Python."""
    
    db_path = "data/taskmaster.db"
    
    if not os.path.exists(db_path):
        print("❌ La base de datos no existe")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row  # Para acceder por nombre de columna
        cursor = conn.cursor()
        
        print("🗃️ BASE DE DATOS TASKMASTER")
        print("="*60)
        
        # Ver tablas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tablas = [tabla[0] for tabla in cursor.fetchall()]
        
        print("📊 TABLAS ENCONTRADAS:", ", ".join(tablas))
        print()
        
        # Mostrar contenido de tareas
        if 'tareas' in tablas:
            print("📋 CONTENIDO DE LA TABLA 'tareas':")
            print("-" * 60)
            
            cursor.execute("SELECT * FROM tareas ORDER BY id")
            tareas = cursor.fetchall()
            
            if tareas:
                # Mostrar columnas
                columnas = [desc[0] for desc in cursor.description]
                print("Columnas:", " | ".join(columnas))
                print("-" * 60)
                
                # Mostrar cada tarea
                for tarea in tareas:
                    print(f"ID: {tarea['id']} | {tarea['titulo']} | Estado: {tarea['estado']} | Prioridad: {tarea['prioridad']}")
                    if tarea['descripcion']:
                        print(f"   Descripción: {tarea['descripcion']}")
                    if tarea['proyecto']:
                        print(f"   Proyecto: {tarea['proyecto']}")
                    print(f"   Creado: {tarea['fecha_creacion']}")
                    print()
            else:
                print("No hay tareas en la base de datos")
        
        # Estadísticas
        print("📈 ESTADÍSTICAS:")
        print("-" * 30)
        cursor.execute("SELECT COUNT(*) as total, SUM(CASE WHEN estado='completada' THEN 1 ELSE 0 END) as completadas FROM tareas")
        stats = cursor.fetchone()
        print(f"Total tareas: {stats['total']}")
        print(f"Completadas: {stats['completadas']}")
        print(f"Pendientes: {stats['total'] - stats['completadas']}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    ver_base_datos()