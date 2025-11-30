# tui_app/screens/task_list.py
from textual.screen import Screen
from textual.widgets import Static, Button, Header, Footer, OptionList, Input
from textual.containers import Container, Horizontal, Vertical
from textual import on
from textual.widgets.option_list import Option
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from tui_app.controllers.tarea_controller import TareaController

class TaskListScreen(Screen):
    """Pantalla de lista de tareas con menú funcional - USANDO CONTROLADOR"""
    
    # ... (tu CSS se mantiene igual)
    CSS = """
    TaskListScreen {
        align: center middle;
        background: #1A1B25;
    }
    
    .container {
        width: 70%;
        height: auto;
        border: round #9B5DE5;
        background: #2A2B38;
    }
    
    .header {
        width: 100%;
        height: 3;
        content-align: center middle;
        background: #9B5DE5;
        color: #FFFFFF;
        text-style: bold;
        padding: 1;
    }
    
    .instructions {
        width: 100%;
        height: 1;
        color: #FFD166;
        background: #2A2B38;
        padding: 0;
        text-style: italic;
    }

    .search-label {
        width: 100%;
        height: 1;
        color: #FFD166;
        background: #2A2B38;
        padding: 0;
    }
    
    .stats-label {
        width: 100%;
        height: 1;
        content-align: center middle;
        color: #FFD166;
        background: #2A2B38;
        padding: 0;
        text-style: bold;
    }

    #stats_display {
        width: 100%;
        height: 1;
        content-align: center middle;
        color: #06D6A0;
        background: #2A2B38;
        padding: 0;
    }
    
    #search_input {
        width: 100%;
        background: #2A2B38;
        color: #FFFFFF;
        border: solid #9B5DE5;
        margin: 1;
    }

    OptionList {
        background: #2A2B38;
        padding: 1;
        border: solid #E83E8C;
        margin: 1;
    }
    
    .buttons {
        width: 100%;
        height: auto;
        align-horizontal: center;
        padding: 1;
        background: #2A2B38;
    }
    
    #refresh {
        background: #FFD166;
        color: #1A1B25;
    }
    
    #new {
        background: #E83E8C;
        color: #1A1B25;
    }
    
    #back {
        background: #FF9E64;
        color: #1A1B25;
    }

    #debug {
        background: #FF9E64;
        color: #1A1B25;
    }
    """

    BINDINGS = [
        ("n", "new_task", "Nueva Tarea"),
        ("r", "refresh", "Actualizar"),
        ("escape", "go_back", "Atrás"),
    ]

    def __init__(self):
        super().__init__()
        self.controller = TareaController()
        self.tareas = []

    def compose(self):
        """Interfaz con menú de opciones."""
        yield Header()
        yield Container(
            Static("🫧     LISTA DE TAREAS    🫧", classes="header"),
            
            Static("Escribe para buscar:", classes="search-label"),
            Input(placeholder="Buscar por título...", id="search_input"),
            Static("Estadísticas rápidas:", classes="stats-label"),
            Static("Cargando...", id="stats_display"),
            
            Static("Selecciona una tarea del menú para cambiar estado", classes="instructions"),
            OptionList(id="tasks_menu"),
            Horizontal(
                Button("Actualizar", id="refresh", variant="warning"),
                Button("Nueva Tarea", id="new", variant="primary"),
                Button("Volver", id="back", variant="error"),
                classes="buttons"
            ),
            classes="container"
        )
        yield Footer()

    def on_mount(self):
        """USA EL CONTROLADOR para cargar tareas"""
        self.cargar_tareas()

    def cargar_tareas(self, search_term=None):
        """Carga tareas usando el Controlador"""
        if search_term:
            resultado = self.controller.buscar_tareas(search_term)
        else:
            resultado = self.controller.obtener_todas_tareas()
        
        if resultado['success']:
            self.tareas = resultado['data']
            self.actualizar_lista_tareas()
            self.actualizar_estadisticas()
        else:
            self.notify(resultado['message'], severity="error")

    def actualizar_lista_tareas(self):
        """Actualiza la lista visual de tareas."""
        menu = self.query_one("#tasks_menu", OptionList)
        menu.clear_options()
        
        if not self.tareas:
            menu.add_option(Option("📭 No hay tareas", id="none"))
            return
        
        for tarea in self.tareas:
            display_text = tarea['display_text']
            menu.add_option(Option(display_text, id=str(tarea['id'])))

    def actualizar_estadisticas(self):
        """Actualiza estadísticas usando el Controlador"""
        resultado = self.controller.obtener_estadisticas()
        
        if resultado['success']:
            data = resultado['data']
            stats_text = f"⏳ {data['por_estado']['pendiente']} 🎨 {data['por_estado']['en_progreso']} 🎉 {data['por_estado']['completada']} | Total: {data['total_tareas']}"
            self.query_one("#stats_display", Static).update(stats_text)

    @on(Input.Submitted, "#search_input")
    def on_search_submitted(self, event):
        """Buscar cuando se presiona Enter."""
        search_term = event.value.strip()
        self.cargar_tareas(search_term if search_term else None)

    @on(Input.Changed, "#search_input")  
    def on_search_changed(self, event):
        """Buscar en tiempo real mientras se escribe."""
        search_term = event.value.strip()
        if len(search_term) >= 2 or search_term == "":
            self.cargar_tareas(search_term if search_term else None)

    @on(OptionList.OptionSelected)
    def change_status(self, event):
        """Cambia estado usando el Controlador"""
        if event.option.id != "none" and event.option.id != "error":
            try:
                task_id = int(event.option.id)
                resultado = self.controller.cambiar_estado_tarea(task_id)
                
                if resultado['success']:
                    self.notify(resultado['message'], severity="information")
                    # Recargar manteniendo búsqueda actual
                    search_input = self.query_one("#search_input", Input)
                    current_search = search_input.value.strip()
                    self.cargar_tareas(current_search if current_search else None)
                else:
                    self.notify(resultado['message'], severity="error")
                    
            except Exception as e:
                self.notify(f"Error: {str(e)}", severity="error")

    @on(Button.Pressed, "#refresh")
    def refresh_tasks(self):
        """Actualiza la lista."""
        search_input = self.query_one("#search_input", Input)
        search_input.value = ""
        self.cargar_tareas()
        self.notify("Lista actualizada")

    def action_new_task(self):
        from tui_app.screens.task_form import TaskFormScreen
        self.app.push_screen(TaskFormScreen())

    def action_refresh(self):
        self.refresh_tasks()

    def action_go_back(self):
        self.app.pop_screen()

    @on(Button.Pressed, "#new")
    def new_task(self):
        self.action_new_task()

    @on(Button.Pressed, "#back")
    def go_back(self):
        self.action_go_back()