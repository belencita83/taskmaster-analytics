# tui_app/screens/task_form_safe.py
from textual.screen import Screen
from textual.widgets import Static, Button, Input, Select
from textual.containers import Container, Vertical, Horizontal
from textual import on
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from core.storage import GestorAlmacenamiento
from core.managers import TareaManager

class TaskFormScreenSafe(Screen):
    """Formulario seguro para crear tareas."""
    
    BINDINGS = [("escape", "go_back", "Atrás")]
    
    def compose(self):
        yield Container(
            Static("📝 CREAR NUEVA TAREA"),
            Static("Presiona ESC para cancelar en cualquier momento"),
            
            Vertical(
                Static("Título (obligatorio):"),
                Input(placeholder="¿Qué necesitas hacer?", id="titulo"),
                
                Static("Prioridad:"),
                Select(
                    [("🔴 Alta", "alta"), ("🟡 Media", "media"), ("🔵 Baja", "baja")],
                    value="media",
                    id="prioridad"
                ),
                
                Static("Proyecto (opcional):"),
                Input(placeholder="Nombre del proyecto...", id="proyecto"),
                
                Horizontal(
                    Button("💾 Guardar Tarea", id="guardar", variant="primary"),
                    Button("❌ Cancelar", id="cancelar"),
                ),
            ),
        )
    
    @on(Button.Pressed, "#guardar")
    def guardar_tarea(self):
        """Guarda la nueva tarea de forma segura."""
        titulo = self.query_one("#titulo", Input).value.strip()
        prioridad = self.query_one("#prioridad", Select).value
        proyecto = self.query_one("#proyecto", Input).value.strip() or None
        
        if not titulo:
            self.notify("❌ El título es obligatorio")
            return
        
        try:
            gestor = GestorAlmacenamiento("sqlite")
            manager = TareaManager(gestor)
            
            nueva_tarea = manager.crear_tarea(
                titulo=titulo,
                descripcion="",  # Por ahora sin descripción
                prioridad=prioridad,
                proyecto=proyecto,
                usuario="tui_user"
            )
            
            self.notify(f"✅ Tarea '{titulo}' creada!")
            self.app.pop_screen()
            
        except Exception as e:
            self.notify(f"❌ Error: {str(e)}")
    
    @on(Button.Pressed, "#cancelar")
    def cancelar(self):
        """Cancela y regresa."""
        self.app.pop_screen()
    
    def action_go_back(self):
        """Volver con Escape."""
        self.app.pop_screen()