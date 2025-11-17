from textual.screen import Screen
from textual.widgets import DataTable, Static, Button
from textual.containers import Container, Horizontal
from textual import on
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from core.storage import GestorAlmacenamiento

class TaskListScreen(Screen):
    """Pantalla para listar todas las tareas."""
    
    CSS = """
    TaskListScreen {
        align: center middle;
    }
    
    .table-container {
        width: 90%;
        height: 80%;
        border: solid $accent;
    }
    
    .header {
        width: 100%;
        content-align: center middle;
        padding: 1;
        background: $accent;
        color: $text;
        text-style: bold;
    }
    
    .buttons {
        width: 100%;
        height: auto;
        align-horizontal: center;
        padding: 1;
    }
    """
    
    def compose(self):
        """Compone la interfaz de la pantalla."""
        yield Container(
            Static("📋 Lista de Tareas", classes="header"),
            DataTable(id="tasks_table"),
            Horizontal(
                Button("🔄 Actualizar", id="refresh"),
                Button("➕ Nueva", id="new"),
                Button("🔙 Atrás", id="back"),
                classes="buttons"
            ),
            classes="table-container"
        )
    
    def on_mount(self):
        """Configura la pantalla al montarla."""
        self.load_tasks()
    
    def load_tasks(self):
        """Carga las tareas en la tabla."""
        table = self.query_one(DataTable)
        table.clear()
        table.add_columns("ID", "Título", "Estado", "Prioridad", "Proyecto", "Creado")
        
        try:
            gestor = GestorAlmacenamiento("sqlite")
            tareas = gestor.cargar_tareas()
            
            for tarea in tareas:
                estado_emoji = {"pendiente": "⏳", "en_progreso": "🚧", "completada": "✅"}
                prioridad_emoji = {"baja": "🔵", "media": "🟡", "alta": "🔴"}
                
                table.add_row(
                    str(tarea.id),
                    tarea.titulo,
                    f"{estado_emoji.get(tarea.estado, '❓')} {tarea.estado}",
                    f"{prioridad_emoji.get(tarea.prioridad, '⚪')} {tarea.prioridad}",
                    tarea.proyecto or "Sin proyecto",
                    tarea.fecha_creacion.strftime("%Y-%m-%d") if tarea.fecha_creacion else "N/A"
                )
        except Exception as e:
            self.notify(f"❌ Error cargando tareas: {e}")
    
    @on(Button.Pressed, "#refresh")
    def refresh_tasks(self):
        """Actualiza la lista de tareas."""
        self.load_tasks()
        self.notify("✅ Lista actualizada")
    
    @on(Button.Pressed, "#new")
    def new_task(self):
        """Abre el formulario para nueva tarea."""
        from tui_app.screens.task_form import TaskFormScreen
        self.app.push_screen(TaskFormScreen())
    
    @on(Button.Pressed, "#back")
    def go_back(self):
        """Regresa a la pantalla principal."""
        self.app.pop_screen()