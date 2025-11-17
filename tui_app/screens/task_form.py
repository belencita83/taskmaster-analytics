# tui_app/screens/task_form.py - FORMULARIO CORREGIDO CON BOTONES
from textual.screen import Screen
from textual.widgets import Static, Button, Input, Select, Header, Footer
from textual.containers import Container, Vertical, Horizontal
from textual import on
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from core.storage import GestorAlmacenamiento
from core.managers import TareaManager

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
        border: double #06D6A0;  /* Turquesa */
        background: #2A2B38;
        padding: 2;
    }
    
    .header {
        width: 100%;
        height: 3;
        content-align: center middle;
        background: #06D6A0;  /* Turquesa */
        color: #1A1B25;
        text-style: bold;
        padding: 1;
    }
    
    .field-label {
        padding: 1 0 0 1;
        color: #B8B8D1;
    }
    
    .obligatorio {
        color: #E83E8C;  /* Rosado */
        text-style: bold;
    }
    
    Input {
        width: 100%;
        background: #2A2B38;
        color: #1A1B25;
    }
    
    Input:focus {
        border: tall #9B5DE5;  /* Morado */
    }
    
    Select {
        width: 100%;
        background: #2A2B38;
        color: #1A1B25;
    }
    
    Select:focus {
        border: tall #FFD166;  /* Amarillo */
    }
    
    .buttons {
        width: 100%;
        height: auto;
        align-horizontal: center;
        margin-top: 2;
    }
    
    #save {
        background: #E83E8C;  /* Rosado */
        color: #1A1B25;
    }
    
    #cancel {
        background: #FF9E64;  /* Naranja */
        color: #1A1B25;
    }
    """

    def compose(self):
        """Formulario con botones claramente visibles."""
        yield Header()
        yield Container(
            Static("🌞   NUEVA TAREA   🌞", classes="header"),
            Vertical(
                # Campo título
                Static("Titulo de la tarea:*", classes="field-label obligatorio"),
                Input(placeholder="Ingrese el titulo aqui...", id="title"),
                
                # Campo descripción
                Static("Descripcion:", classes="field-label"),
                Input(placeholder="Descripcion opcional...", id="description"),
                
                # Campo prioridad
                Static("Prioridad:*", classes="field-label obligatorio"),
                Select(
                    [("🔴 Alta", "alta"), ("🟡 Media", "media"), ("🟢 Baja", "baja")],
                    value="media",
                    id="priority",
                    allow_blank=False
                ),
                
                # Campo proyecto
                Static("Proyecto:", classes="field-label"),
                Input(placeholder="Proyecto opcional...", id="project"),
                
                # Botones
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
        """Guarda la nueva tarea con mejor manejo de errores."""
        try:
            title_input = self.query_one("#title", Input)
            title = title_input.value.strip()
            
            # Validar campos obligatorios
            if not title:
                self.notify("ERROR: El titulo es obligatorio", severity="error")
                title_input.focus()
                return
            
            description = self.query_one("#description", Input).value.strip()
            priority_select = self.query_one("#priority", Select)
            project = self.query_one("#project", Input).value.strip() or None
            
            # Validar que se seleccionó una prioridad
            if not priority_select.value:
                self.notify("ERROR: Debe seleccionar una prioridad", severity="error")
                priority_select.focus()
                return
                
            priority = priority_select.value

            # Guardar en la base de datos
            try:
                gestor = GestorAlmacenamiento("sqlite")
                manager = TareaManager(gestor)
                
                nueva_tarea = manager.crear_tarea(
                    titulo=title,
                    descripcion=description or "",
                    prioridad=priority,
                    proyecto=project,
                    usuario="tui_user"
                )
                
                self.notify(f"ÉXITO: Tarea '{title}' creada", severity="information")
                self.app.pop_screen()
                
            except Exception as db_error:
                self.notify(f"ERROR en base de datos: {str(db_error)}", severity="error")
                
        except Exception as e:
            self.notify(f"ERROR inesperado: {str(e)}", severity="error")

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
    def validate_title(self, event: Input.Changed):
        """Valida el título en tiempo real."""
        if event is None:
            return
            
        title = event.value.strip()
        input_widget = self.query_one("#title")
        
        if not title:
            input_widget.remove_class("success-border")
            input_widget.add_class("error-border")
        else:
            input_widget.remove_class("error-border")
            input_widget.add_class("success-border")