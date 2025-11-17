# tui_app/screens/main_screen.py
from textual.screen import Screen
from textual.widgets import OptionList, Static
from textual.containers import Container
from textual.widgets.option_list import Option

class MainScreen(Screen):
    """Pantalla principal con menú de opciones."""
    
    # ⬇️⬇️⬇️ COMENTA O ELIMINA TODO EL BLOQUE CSS ⬇️⬇️⬇️
    # CSS = """
    # MainScreen {
    #     align: center middle;
    # }
    # 
    # .main-container {
    #     width: 60%;
    #     height: 70%;
    #     border: solid $accent;
    #     background: $surface;
    # }
    # 
    # .title {
    #     width: 100%;
    #     content-align: center middle;
    #     padding: 1;
    #     background: $accent;
    #     color: $text;
    #     text-style: bold;
    # }
    # 
    # .subtitle {
    #     width: 100%;
    #     content-align: center middle;
    #     padding: 1;
    #     color: $text-muted;
    # }
    # """
    
    def compose(self):
        """Compone la interfaz de la pantalla."""
        yield Container(
            Static("🎯 TaskMaster Analytics"),
            Static("Sistema de gestión de tareas con analytics"),
            OptionList(
                Option("📝 Lista de tareas", id="list_tasks"),
                Option("➕ Crear nueva tarea", id="create_task"),
                Option("📊 Dashboard de analytics", id="analytics"),
                Option("📤 Exportar reportes", id="export"),
                Option("⚙️  Información del sistema", id="system_info"),
                Option("🚪 Salir", id="quit"),
                id="main_menu"
            )
        )
    
    def on_option_list_option_selected(self, event):
        """Maneja la selección de opciones del menú."""
        option_id = event.option.id
        
        # Importar aquí para evitar importación circular
        if option_id == "list_tasks":
            from tui_app.screens.task_list import TaskListScreen
            self.app.push_screen(TaskListScreen())
        elif option_id == "create_task":
            from tui_app.screens.task_form import TaskFormScreen
            self.app.push_screen(TaskFormScreen())
        elif option_id == "analytics":
            from tui_app.screens.analytics import AnalyticsScreen
            self.app.push_screen(AnalyticsScreen())
        elif option_id == "export":
            self.notify("🚧 Función de exportación en desarrollo...")
        elif option_id == "system_info":
            self.notify("🚧 Información del sistema en desarrollo...")
        elif option_id == "quit":
            self.app.exit()
    
    def clear_screen(self):
        """Limpia la pantalla antes de mostrar contenido."""
        # Textual maneja el rendering, pero podemos forzar un refresh
        self.refresh()