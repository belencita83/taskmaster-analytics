# tui_app/screens/task_form.py
from textual.screen import Screen
from textual.widgets import Static, Button, Input, Select, Header, Footer
from textual.containers import Container, Vertical, Horizontal
from textual import on
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from tui_app.controllers.tarea_controller import TareaController

class TaskFormScreen(Screen):
    """Formulario para nuevas tareas con botones visibles"""
    
    CSS = """
    TaskFormScreen {
        align: center middle;
        background: #1A1B25;
    }
    
    .container {
        width: 80%;
        height: auto;
        border: double #06D6A0;
        background: #2A2B38;
        padding: 2;
    }
    
    .header {
        width: 100%;
        height: 3;
        content-align: center middle;
        background: #06D6A0;
        color: #1A1B25;
        text-style: bold;
        padding: 1;
    }
    
    .field-label {
        padding: 1 0 0 1;
        color: #B8B8D1;
    }
    
    .obligatorio {
        color: #E83E8C;
        text-style: bold;
    }
    
    Input {
        width: 100%;
        background: #2A2B38;
        color: #1A1B25;
    }
    
    Input:focus {
        border: tall #9B5DE5;
    }
    
    Select {
        width: 100%;
        background: #2A2B38;
        color: #1A1B25;
    }
    
    Select:focus {
        border: tall #FFD166;
    }
    
    .buttons {
        width: 100%;
        height: auto;
        align-horizontal: center;
        margin-top: 2;
    }
    
    #save {
        background: #E83E8C;
        color: #1A1B25;
    }
    
    #cancel {
        background: #FF9E64;
        color: #1A1B25;
    }
    
    # CLASES CSS PARA VALIDACIÓN
    .error-border {
        border: solid #EF476F;
    }
    
    .success-border {
        border: solid #06D6A0;
    }
    """

    def __init__(self):
        super().__init__()
        self.controller = TareaController()

    def compose(self):
        """Formulario con botones claramente visibles."""
        yield Header()
        yield Container(
            Static("🌞   NUEVA TAREA   🌞", classes="header"),
            Vertical(
                Static("Titulo de la tarea:*", classes="field-label obligatorio"),
                Input(placeholder="Ingrese el titulo aqui...", id="title"),
                
                Static("Descripcion:", classes="field-label"),
                Input(placeholder="Descripcion opcional...", id="description"),
                
                Static("Prioridad:*", classes="field-label obligatorio"),
                Select(
                    [("🔴 Alta", "alta"), ("🟡 Media", "media"), ("🟢 Baja", "baja")],
                    value="media",
                    id="priority",
                    allow_blank=False
                ),
                
                Static("Proyecto:", classes="field-label"),
                Input(placeholder="Proyecto opcional...", id="project"),
                
                Horizontal(
                    Button("GUARDAR", id="save", variant="primary"),
                    Button("CANCELAR", id="cancel", variant="error"),
                    classes="buttons"
                ),
                
                Static("* Campos obligatorios", classes="field-label"),
            ),
            classes="container"
        )
        yield Footer()

    @on(Button.Pressed, "#save")
    def save_task(self):
        """USA EL CONTROLADOR en lugar del Manager directo"""
        # 1. Obtener datos del formulario
        form_data = {
            'titulo': self.query_one("#title", Input).value.strip(),
            'descripcion': self.query_one("#description", Input).value.strip(),
            'prioridad': self.query_one("#priority", Select).value or "media",
            'proyecto': self.query_one("#project", Input).value.strip() or None,
            'usuario': 'tui_user'
        }
        
        # 2. USAR CONTROLADOR en lugar de Manager directo
        resultado = self.controller.crear_tarea(form_data)
        
        # 3. Manejar resultado
        if resultado['success']:
            self.notify(resultado['message'], severity="information")
            self.app.pop_screen()  # Volver al menú principal
        else:
            self.notify(resultado['message'], severity="error")
            # Enfocar campo de título si hay error
            self.query_one("#title", Input).focus()

    @on(Button.Pressed, "#cancel")
    def cancel(self):
        """Cancela y regresa al menu principal."""
        self.app.pop_screen()

    def on_mount(self):
        """Enfoca el campo titulo al cargar la pantalla."""
        self.query_one("#title", Input).focus()

    def on_key(self, event):
        """Maneja teclas especiales."""
        if event.key == "escape":
            self.app.pop_screen()

    @on(Input.Changed, "#title")
    def validate_title(self, event):
        """Valida el título en tiempo real."""
        if event is None:
            return
            
        title = event.value.strip()
        input_widget = self.query_one("#title")
        
        if not title:
            input_widget.add_class("error-border")
            input_widget.remove_class("success-border")
        else:
            input_widget.add_class("success-border")
            input_widget.remove_class("error-border")