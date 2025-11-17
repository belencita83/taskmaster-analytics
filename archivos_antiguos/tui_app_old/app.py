# tui_app/app.py - VERSIÓN FINAL OPCIÓN 1
import sys
import os
from textual.app import App
from textual.widgets import OptionList, Static, Footer
from textual.containers import Container
from textual.widgets.option_list import Option

class TaskMasterTUI(App):
    """Aplicación principal TUI - VERSIÓN FINAL."""
    
    CSS = """
    Screen {
        align: center middle;
        background: $surface;
    }
    
    .main-container {
        width: 60%;
        height: 70%;
        border: round $accent;
        background: $surface;
    }
    
    .title {
        width: 100%;
        content-align: center middle;
        padding: 1;
        background: $accent;
        color: $text;
        text-style: bold;
    }
    
    .subtitle {
        width: 100%;
        content-align: center middle;
        padding: 1;
        color: $text-muted;
    }
    """
    
    BINDINGS = [
        ("q", "quit", "Salir"),
        ("escape", "quit", "Salir"),
    ]

    def compose(self):
        """Interfaz principal."""
        yield Container(
            Static("🎯 TASKMASTER ANALYTICS", classes="title"),
            Static("Sistema de gestión de tareas con analytics", classes="subtitle"),
            OptionList(
                Option("📝 Lista de tareas", id="list_tasks"),
                Option("➕ Crear nueva tarea", id="create_task"),
                Option("📊 Dashboard de analytics", id="analytics"),
                Option("📤 Exportar reportes", id="export"),
                Option("ℹ️  Información del sistema", id="system_info"),
                Option("🚪 Salir", id="quit"),
                id="main_menu"
            ),
            classes="main-container"
        )
        yield Footer()

    def on_option_list_option_selected(self, event):
        """Navegación a otras pantallas."""
        option_id = event.option.id
        
        try:
            if option_id == "list_tasks":
                from tui_app.screens.task_list import TaskListScreen
                self.push_screen(TaskListScreen())
            elif option_id == "create_task":
                from tui_app.screens.task_form import TaskFormScreen
                self.push_screen(TaskFormScreen())
            elif option_id == "analytics":
                from tui_app.screens.analytics import AnalyticsScreen
                self.push_screen(AnalyticsScreen())
            elif option_id == "export":
                self.notify("📤 Exportando reportes... (próximamente)")
            elif option_id == "system_info":
                self.notify("ℹ️  Información del sistema... (próximamente)")
            elif option_id == "quit":
                self.exit()
        except Exception as e:
            self.notify(f"❌ Error cargando pantalla: {e}")

if __name__ == "__main__":
    app = TaskMasterTUI()
    app.run()