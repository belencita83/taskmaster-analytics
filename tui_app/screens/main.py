# tui_app/screens/main.py - MENÚ PRINCIPAL SIMPLIFICADO
from textual.screen import Screen
from textual.widgets import OptionList, Static, Header, Footer
from textual.containers import Container
from textual.widgets.option_list import Option

class MainScreen(Screen):
    """Pantalla principal simplificada"""
    
    CSS = """
    MainScreen {
        align: center middle;
        background: $surface;
    }
    
    .container {
        width: 60%;
        height: 70%;
        border: panel $accent;
        background: $panel;
    }
    
    .title {
        width: 100%;
        height: 3;
        content-align: center middle;
        background: $accent;
        color: $text;
        text-style: bold;
    }
    
    .subtitle {
        width: 100%;
        height: 2;
        content-align: center middle;
        color: $text-muted;
    }
    """

    def compose(self):
        """Interfaz simple del menú."""
        yield Header()
        yield Container(
            Static("TASKMASTER ANALYTICS", classes="title"),
            Static("Sistema de Gestion de Tareas", classes="subtitle"),
            OptionList(
                Option("Lista de Tareas", id="tasks"),
                Option("Nueva Tarea", id="new_task"),
                Option("Analytics", id="analytics"),
                Option("Salir", id="quit"),
                id="menu"
            ),
            classes="container"
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
        elif option_id == "quit":
            self.app.exit()