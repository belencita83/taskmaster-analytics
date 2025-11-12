# tui_app/screens/task_list.py - CORREGIDO
from textual.screen import Screen
from textual.widgets import DataTable, Static, Button, Header, Footer, OptionList
from textual.containers import Container, Horizontal
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
    }
    
    .container {
        width: 90%;
        height: 90%;
        border: panel $accent;
        background: $panel;
    }
    
    .header {
        width: 100%;
        height: 3;
        content-align: center middle;
        background: $accent;
        color: $text;
        text-style: bold;
    }
    
    .instructions {
        width: 100%;
        height: 2;
        content-align: center middle;
        color: $text-muted;
        padding: 1;
    }
    
    .buttons {
        width: 100%;
        height: auto;
        align-horizontal: center;
        padding: 1;
    }
    """

    def compose(self):
        """Interfaz con menú de opciones."""
        yield Header()
        yield Container(
            Static("LISTA DE TAREAS", classes="header"),
            Static("Selecciona una tarea del menú para cambiar estado", classes="instructions"),
            OptionList(id="tasks_menu"),
            Horizontal(
                Button("Actualizar", id="refresh", variant="primary"),
                Button("Nueva Tarea", id="new"),
                Button("Volver", id="back"),
                classes="buttons"
            ),
            classes="container"
        )
        yield Footer()

    def on_mount(self):
        """Carga las tareas al iniciar."""
        self.load_tasks()

    def load_tasks(self):
        """Carga tareas en el menú de opciones."""
        menu = self.query_one(OptionList)
        menu.clear_options()
        
        try:
            gestor = GestorAlmacenamiento("sqlite")
            tareas = gestor.cargar_tareas()
            
            if not tareas:
                menu.add_option(Option("No hay tareas", id="none"))
                return
                
            for tarea in tareas:
                if hasattr(tarea, 'id'):
                    estado = tarea.estado or "pendiente"
                    
                    # Emojis para mejor visualización
                    estado_emoji = {
                        "pendiente": "⏳",
                        "en_progreso": "🚧", 
                        "completada": "✅"
                    }
                    
                    texto = f"{tarea.id}. {tarea.titulo} - {estado_emoji.get(estado, '❓')} {estado}"
                    menu.add_option(Option(texto, id=str(tarea.id)))
                    
        except Exception as e:
            # Datos de ejemplo
            menu.add_option(Option("1. Presentación TUT - ⏳ pendiente", id="1"))
            menu.add_option(Option("2. Estudiar SIS 2420 - 🚧 en_progreso", id="2"))
            menu.add_option(Option("3. Revisar código - ✅ completada", id="3"))

    @on(OptionList.OptionSelected)
    def change_status(self, event):
        """Cambia el estado al seleccionar una tarea del menú."""
        if event.option.id != "none":
            task_id = int(event.option.id)
            
            try:
                gestor = GestorAlmacenamiento("sqlite")
                tareas = gestor.cargar_tareas()
                tarea = next((t for t in tareas if t.id == task_id), None)
                
                if tarea:
                    # Cambiar estado en ciclo
                    if tarea.estado == "pendiente":
                        new_status = "en_progreso"
                    elif tarea.estado == "en_progreso":
                        new_status = "completada"
                    else:
                        new_status = "pendiente"
                    
                    # CORREGIDO: usar guardar_tarea en lugar de actualizar_tarea
                    tarea.estado = new_status
                    gestor.guardar_tarea(tarea)  # ⬅️ ESTA LÍNEA CAMBIÓ
                    
                    self.notify(f"Tarea {task_id} ahora está: {new_status}")
                    self.load_tasks()  # Recargar menú
                    
            except Exception as e:
                self.notify(f"Error: {e}")

    @on(Button.Pressed, "#refresh")
    def refresh_tasks(self):
        """Actualiza la lista."""
        self.load_tasks()
        self.notify("Lista actualizada")

    @on(Button.Pressed, "#new")
    def new_task(self):
        """Abre formulario de nueva tarea."""
        from tui_app.screens.task_form import TaskFormScreen
        self.app.push_screen(TaskFormScreen())

    @on(Button.Pressed, "#back")
    def go_back(self):
        """Regresa al menu."""
        self.app.pop_screen()