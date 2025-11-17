# tui_app/screens/task_form.py
from textual.screen import Screen
from textual.widgets import Static, Button, Input, Select, TextArea
from textual.containers import Container, Vertical, Horizontal
from textual import on
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from core.storage import GestorAlmacenamiento
from core.managers import TareaManager

class TaskFormScreen(Screen):
    """Pantalla para crear nuevas tareas."""
    
    CSS = """
    TaskFormScreen {
        align: center middle;
    }
    
    .form-container {
        width: 70%;
        height: 80%;
        border: solid $accent;
        padding: 1;
    }
    
    .header {
        width: 100%;
        content-align: center middle;
        padding: 1;
        background: $accent;
        color: $text;
        text-style: bold;
    }
    
    .form-field {
        height: auto;
        margin: 1 0;
    }
    
    .field-label {
        width: 100%;
        padding: 0 0 1 0;
        color: $text-muted;
    }
    
    .buttons {
        width: 100%;
        height: auto;
        align-horizontal: center;
        padding: 1;
        margin-top: 2;
    }
    """
    
    def compose(self):
        """Compone la interfaz del formulario."""
        yield Container(
            Static("📝 Crear Nueva Tarea", classes="header"),
            
            Vertical(
                Static("Título:", classes="field-label"),
                Input(placeholder="Ingresa el título de la tarea...", id="titulo"),
                
                Static("Descripción:", classes="field-label"),
                TextArea(placeholder="Descripción opcional...", id="descripcion"),
                
                Static("Prioridad:", classes="field-label"),
                Select(
                    [
                        ("🔴 Alta", "alta"),
                        ("🟡 Media", "media"), 
                        ("🔵 Baja", "baja")
                    ],
                    prompt="Selecciona prioridad...",
                    id="prioridad"
                ),
                
                Static("Proyecto:", classes="field-label"),
                Input(placeholder="Nombre del proyecto (opcional)...", id="proyecto"),
                
                Horizontal(
                    Button("💾 Guardar", id="save", variant="primary"),
                    Button("🗑️ Cancelar", id="cancel"),
                    classes="buttons"
                ),
            ),
            classes="form-container"
        )
    
    @on(Button.Pressed, "#save")
    def save_task(self):
        """Guarda la nueva tarea."""
        titulo = self.query_one("#titulo", Input).value.strip()
        descripcion = self.query_one("#descripcion", TextArea).text.strip()
        prioridad_select = self.query_one("#prioridad", Select)
        prioridad = prioridad_select.value if prioridad_select.value else "media"
        proyecto = self.query_one("#proyecto", Input).value.strip() or None
        
        if not titulo:
            self.notify("❌ El título es obligatorio")
            return
        
        try:
            gestor = GestorAlmacenamiento("sqlite")
            manager = TareaManager(gestor)
            
            nueva_tarea = manager.crear_tarea(
                titulo=titulo,
                descripcion=descripcion,
                prioridad=prioridad,
                proyecto=proyecto,
                usuario="tui_user"
            )
            
            self.notify(f"✅ Tarea '{titulo}' creada exitosamente!")
            self.app.pop_screen()
            
        except Exception as e:
            self.notify(f"❌ Error creando tarea: {e}")
    
    @on(Button.Pressed, "#cancel")
    def cancel(self):
        """Cancela y regresa."""
        self.app.pop_screen()
