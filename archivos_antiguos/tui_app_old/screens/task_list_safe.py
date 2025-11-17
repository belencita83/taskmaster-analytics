# tui_app/screens/task_list_safe.py
from textual.screen import Screen
from textual.widgets import DataTable, Static, Button
from textual.containers import Container, Horizontal
from textual import on
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from core.storage import GestorAlmacenamiento

class TaskListScreenSafe(Screen):
    """Pantalla segura para listar tareas."""
    
    BINDINGS = [("escape", "go_back", "Atrás")]
    
    def compose(self):
        yield Container(
            Static("📋 LISTA DE TAREAS (Segura)"),
            Static("Presiona ESC para volver en cualquier momento"),
            DataTable(id="tasks_table"),
            Horizontal(
                Button("🔄 Actualizar", id="refresh"),
                Button("🔙 Volver al Menú", id="back"),
            ),
        )
    
    def on_mount(self):
        self.load_tasks()
    
    def load_tasks(self):
        """Carga tareas de forma segura."""
        table = self.query_one(DataTable)
        table.clear()
        table.add_columns("ID", "Título", "Estado", "Prioridad")
        
        try:
            gestor = GestorAlmacenamiento("sqlite")
            tareas = gestor.cargar_tareas()
            
            for tarea in tareas[:10]:  # Solo mostrar 10 para prueba
                estado_emoji = {"pendiente": "⏳", "completada": "✅"}
                prioridad_emoji = {"alta": "🔴", "media": "🟡", "baja": "🔵"}
                
                table.add_row(
                    str(tarea.id),
                    tarea.titulo[:20] + "..." if len(tarea.titulo) > 20 else tarea.titulo,
                    f"{estado_emoji.get(tarea.estado, '❓')}",
                    f"{prioridad_emoji.get(tarea.prioridad, '⚪')}"
                )
                
        except Exception as e:
            self.notify(f"❌ Error: {e}")
    
    @on(Button.Pressed, "#refresh")
    def refresh_tasks(self):
        self.load_tasks()
        self.notify("✅ Actualizado")
    
    @on(Button.Pressed, "#back")
    def go_back(self):
        self.app.pop_screen()
    
    def action_go_back(self):
        """Volver con Escape."""
        self.app.pop_screen()