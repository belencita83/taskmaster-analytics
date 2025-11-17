# tui_app/screens/task_list.py
from textual.screen import Screen
from textual.widgets import DataTable, Static, Button, Header, Footer, OptionList, Input
from textual.containers import Container, Horizontal, Vertical
from textual import on
from textual.widgets.option_list import Option
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from core.storage import GestorAlmacenamiento

class TaskListScreen(Screen):
    """Pantalla de lista de tareas con menú funcional - CORREGIDO"""
    
    CSS = """
    TaskListScreen {
        align: center middle;
        background: #1A1B25;
    }
    
    .container {
        width: 70%;
        height: auto;
        border: round #9B5DE5;  /* Morado */
        background: #2A2B38;
    }
    
    .header {
        width: 100%;
        height: 3;
        content-align: center middle;
        background: #9B5DE5;  /* Morado */
        color: #FFFFFF;
        text-style: bold;
        padding: 1;
    }
    
    .instructions {
        width: 100%;
        height: 1;
        color: #FFD166;  /* Amarillo */
        background: #2A2B38;
        padding: 0;
        text-style: italic;
    }

    .search-label {
        width: 100%;
        height: 1;
        color: #FFD166;  /* Amarillo */
        background: #2A2B38;
        padding: 0;
    }
    
    .stats-label {
        width: 100%;
        height: 1;
        content-align: center middle;
        color: #FFD166;  /* Amarillo */
        background: #2A2B38;
        padding: 0;
        text-style: bold;
    }

    #stats_display {
        width: 100%;
        height: 1;
        content-align: center middle;
        color: #06D6A0;  /* Turquesa */
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
        border: solid #E83E8C;  /* Rosado */
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
        background: #FFD166;  /* Amarillo */
        color: #1A1B25;
    }
    
    #new {
        background: #E83E8C;  /* Rosado */
        color: #1A1B25;
    }
    
    #back {
        background: #FF9E64;  /* Naranja */
        color: #1A1B25;
    }
    """

    BINDINGS = [
        ("n", "new_task", "Nueva Tarea"),
        ("r", "refresh", "Actualizar"),
        ("escape", "go_back", "Atrás"),
    ]

    def compose(self):
        """Interfaz con menú de opciones."""
        yield Header()
        yield Container(
            Static("🫧   LISTA DE TAREAS   🫧", classes="header"),
            
            Static("Escribe para buscar:", classes="search-label"),
            Input(placeholder="Buscar por título...", id="search_input"),
            Static("Estadísticas rápidas:", classes="stats-label"),
            Static("Cargando...", id="stats_display"),
            
            Static(" Selecciona una tarea del menú para cambiar estado", classes="instructions"),
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
        """Carga las tareas al iniciar."""
        self.load_tasks()


    def load_tasks(self, search_term=None):
        menu = self.query_one(OptionList)
        menu.clear_options()
        
        try:
            gestor = GestorAlmacenamiento("sqlite")
            tareas = gestor.cargar_tareas()
            
            if search_term:
                tareas = [t for t in tareas if search_term.lower() in t.titulo.lower()]
            
            # Calcular estadísticas
            total = len(tareas)
            pendientes = sum(1 for t in tareas if t.estado == "pendiente")
            en_progreso = sum(1 for t in tareas if t.estado == "en_progreso")
            completadas = sum(1 for t in tareas if t.estado == "completada")
            
            # Actualizar display de estadísticas
            stats = self.query_one("#stats_display", Static)
            stats.update(f"⏳ {pendientes} 🎨 {en_progreso} 🎉 {completadas} | Total: {total}")
            
            if not tareas:
                menu.add_option(Option("No hay tareas", id="none"))
                return
                
            for tarea in tareas:
                if hasattr(tarea, 'id'):
                    estado = tarea.estado or "pendiente"
                    
                    estado_emoji = {
                        "pendiente": "⏳",
                        "en_progreso": "🎨",
                        "completada": "🎉"
                    }
                    
                    prioridad_emoji = {
                        "alta": "🔴",
                        "media": "🟡", 
                        "baja": "🟢"
                    }
                    
                    prioridad = tarea.prioridad or "media"
                    
                    texto = f"{tarea.id}. {tarea.titulo} - {estado_emoji.get(estado)} {estado} - {prioridad_emoji.get(prioridad)}"
                    menu.add_option(Option(texto, id=str(tarea.id)))
                    
        except Exception as e:
            menu.add_option(Option("Error cargando tareas", id="error"))

    @on(Input.Submitted, "#search_input")
    def on_search_submitted(self, event):
        """Buscar cuando se presiona Enter."""
        search_term = event.value.strip()
        self.load_tasks(search_term if search_term else None)

    @on(Input.Changed, "#search_input")  
    def on_search_changed(self, event):
        """Buscar en tiempo real mientras se escribe."""
        search_term = event.value.strip()
        if len(search_term) >= 2 or search_term == "":  # Buscar después de 2 caracteres o cuando se borra
            self.load_tasks(search_term if search_term else None)

    @on(OptionList.OptionSelected)
    def change_status(self, event):
        """Cambia el estado al seleccionar una tarea del menú."""
        if event.option.id != "none" and event.option.id != "error":
            task_id = int(event.option.id)
            
            try:
                gestor = GestorAlmacenamiento("sqlite")
                tareas = gestor.cargar_tareas()
                tarea = next((t for t in tareas if t.id == task_id), None)
                
                if tarea:
                    # Cambiar estado en ciclo
                    if tarea.estado == "pendiente":
                        new_status = "en_progreso"
                        emoji = "🎨"
                    elif tarea.estado == "en_progreso":
                        new_status = "completada"
                        emoji = "🎉"
                    else:
                        new_status = "pendiente"
                        emoji = "⏳"
                    
                    tarea.estado = new_status
                    gestor.guardar_tarea(tarea)
                    
                    self.notify(f"{emoji} Tarea {task_id} ahora está: {new_status}")
                    # Recargar manteniendo la búsqueda actual
                    search_input = self.query_one("#search_input", Input)
                    current_search = search_input.value.strip()
                    self.load_tasks(current_search if current_search else None)
                    
            except Exception as e:
                self.notify(f"Error: {e}")

    @on(Button.Pressed, "#refresh")
    def refresh_tasks(self):
        """Actualiza la lista."""
        search_input = self.query_one("#search_input", Input)
        search_input.value = ""  # Limpiar búsqueda
        self.load_tasks()
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
        """Abre formulario de nueva tarea."""
        self.action_new_task()

    @on(Button.Pressed, "#back")
    def go_back(self):
        """Regresa al menu."""
        self.action_go_back()