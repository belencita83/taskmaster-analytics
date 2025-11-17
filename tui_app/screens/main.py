# tui_app/screens/main.py - MENÚ PRINCIPAL SIMPLIFICADO
from textual.screen import Screen
from textual.widgets import OptionList, Static, Header, Footer, Button
from textual.containers import Container, Horizontal, Vertical
from textual.widgets.option_list import Option

class MainScreen(Screen):
    """Pantalla principal simplificada"""
    
    CSS = """
    MainScreen {
        align: center middle;
        background: #1A1B25;
    }
    
    .main-container {
        width: 50%;
        height: 60%;
        border: double #E83E8C;  /* Rosado */
        background: #2A2B38;
        padding: 0;
    }
    
    .title {
        width: 100%;
        height: 3;
        content-align: center middle;
        background: #E83E8C;  /* Rosado */
        color: #FFFFFF;
        text-style: bold;
        padding: 1;
    }
    
    .subtitle {
        width: 100%;
        height: 2;
        content-align: center middle;
        color: #FFD166;  /* Amarillo */
        background: #2A2B38;
        padding: 1;
        text-style: italic;
    }
    
    OptionList {
        background: #2A2B38;
        padding: 2;
    }
    
    OptionList:focus {
        background: #2A2B38;
    }
    
    Footer {
        background: #FFD166;  /* Amarillo */
        color: #1A1B25;
        text-style: bold;
    }

    .confirm-container {
        width: 50%;
        height: auto;
        border: double #EF476F;
        background: #2A2B38;
        padding: 2;
    }
    
    .confirm-buttons {
        width: 100%;
        height: auto;
        align-horizontal: center;
        margin-top: 2;
    }
    """

    BINDINGS = [
        ("ctrl+t", "show_tasks", "Tareas"),
        ("ctrl+n", "new_task", "Nueva"),
        ("ctrl+a", "show_analytics", "Analytics"),
        ("q", "quit", "Salir"),
    ]

    def compose(self):
        """Interfaz simple del menú."""
        yield Header()
        yield Container(
            Static("🌸   TASKMASTER ANALYTICS   🌸", classes="title"),
            Static("Sistema de Gestión de Tareas", classes="subtitle"),
            OptionList(
                Option("Lista de Tareas", id="tasks"),
                Option("Nueva Tarea", id="new_task"),
                Option("Analytics", id="analytics"),
                Option("Acerca de", id="about"),
                Option("Salir", id="quit"),
                id="menu"
            ),
            classes="main-container"
        )
        yield Footer()

    def on_option_list_option_selected(self, event):
        """Navegación simple."""
        option_id = event.option.id
        
        if option_id == "tasks":
            from tui_app.screens.task_list import TaskListScreen
            self.app.push_screen(TaskListScreen())
        elif option_id == "new_task":
            from tui_app.screens.task_form import TaskFormScreen
            self.app.push_screen(TaskFormScreen())
        elif option_id == "analytics":
            from tui_app.screens.analytics import AnalyticsScreen
            self.app.push_screen(AnalyticsScreen())
        elif option_id == "about":
            from tui_app.screens.about import AboutScreen
            self.app.push_screen(AboutScreen())
        elif option_id == "quit":
            self.app.exit()

    def action_show_tasks(self):
        from tui_app.screens.task_list import TaskListScreen
        self.app.push_screen(TaskListScreen())

    def action_new_task(self):
        from tui_app.screens.task_form import TaskFormScreen
        self.app.push_screen(TaskFormScreen())

    def action_show_analytics(self):
        from tui_app.screens.analytics import AnalyticsScreen
        self.app.push_screen(AnalyticsScreen())

    from textual.widgets import Button

    def action_quit(self):
        """Confirmar antes de salir."""
        self.app.push_screen(ConfirmScreen())

# Crear pantalla de confirmación simple
class ConfirmScreen(Screen):
    def compose(self):
        yield Container(
            Static("¿Estás seguro de que quieres salir?", classes="title"),
            Vertical(
                Static("Todos los cambios han sido guardados.", classes="subtitle"),
                Horizontal(
                    Button("Sí, salir", id="yes", variant="error"),
                    Button("No, cancelar", id="no", variant="primary"),
                    classes="confirm-buttons"
                ),
            ),
            classes="confirm-container"
        )
    
    def on_button_pressed(self, event):
        if event.button.id == "yes":
            self.app.exit()
        else:
            self.app.pop_screen()