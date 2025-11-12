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
    }
    
    .container {
        width: 70%;
        height: auto;
        border: panel $accent;
        background: $panel;
        padding: 2;
    }
    
    .header {
        width: 100%;
        height: 3;
        content-align: center middle;
        background: $accent;
        color: $text;
        text-style: bold;
        margin-bottom: 1;
    }
    
    .field {
        margin: 1 0;
    }
    
    .label {
        padding: 0 0 1 0;
        color: $text-muted;
    }
    
    .buttons {
        width: 100%;
        height: auto;
        align-horizontal: center;
        margin-top: 2;
    }
    
    Input, Select {
        width: 100%;
    }
    
    #save {
        width: 48%;
    }
    
    #cancel {
        width: 48%;
    }
    """

    def compose(self):
        """Formulario con botones claramente visibles."""
        yield Header()
        yield Container(
            Static("NUEVA TAREA", classes="header"),
            Vertical(
                # Campo título
                Static("Titulo de la tarea:*", classes="label"),
                Input(placeholder="Ingrese el titulo aqui...", id="title"),
                
                # Campo descripción
                Static("Descripcion:", classes="label"),
                Input(placeholder="Descripcion opcional...", id="description"),
                
                # Campo prioridad
                Static("Prioridad:*", classes="label"),
                Select(
                    [("Alta", "alta"), ("Media", "media"), ("Baja", "baja")],
                    value="media",
                    id="priority",
                    allow_blank=False
                ),
                
                # Campo proyecto
                Static("Proyecto:", classes="label"),
                Input(placeholder="Proyecto opcional...", id="project"),
                
                # Botones - AHORA VISIBLES
                Horizontal(
                    Button("GUARDAR", id="save", variant="primary"),
                    Button("CANCELAR", id="cancel", variant="error"),
                    classes="buttons"
                ),
                
                Static("* Campos obligatorios", classes="label"),
            ),
            classes="container"
        )
        yield Footer()

    @on(Button.Pressed, "#save")
    def save_task(self):
        """Guarda la nueva tarea."""
        title = self.query_one("#title", Input).value.strip()
        description = self.query_one("#description", Input).value.strip()
        priority = self.query_one("#priority", Select).value or "media"
        project = self.query_one("#project", Input).value.strip() or None
        
        # Validar campos obligatorios
        if not title:
            self.notify("ERROR: El titulo es obligatorio")
            self.query_one("#title", Input).focus()
            return
            
        try:
            # Guardar en la base de datos
            gestor = GestorAlmacenamiento("sqlite")
            manager = TareaManager(gestor)
            
            nueva_tarea = manager.crear_tarea(
                titulo=title,
                descripcion=description,
                prioridad=priority,
                proyecto=project,
                usuario="tui_user"
            )
            
            self.notify(f"EXITO: Tarea '{title}' creada (ID: {nueva_tarea.id})")
            self.app.pop_screen()
            
        except Exception as e:
            self.notify(f"ERROR: No se pudo crear la tarea - {str(e)}")

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