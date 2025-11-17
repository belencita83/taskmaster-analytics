# tui_app/app_safe.py
import sys
import os
import signal

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from textual.app import App
from textual.widgets import Header, Footer, Static, Button
from textual.containers import Container
from textual import events

class SafeTUI(App):
    """Versión segura de la TUI con múltiples salidas."""
    
    BINDINGS = [
        ("q", "quit", "Salir"),
        ("ctrl+c", "quit", "Salir"),
        ("ctrl+q", "quit", "Salir"), 
        ("escape", "quit", "Salir"),
        ("f1", "show_help", "Ayuda"),
    ]
    
    def __init__(self):
        super().__init__()
        # Manejar señales de sistema
        signal.signal(signal.SIGINT, self._emergency_exit)
    
    def _emergency_exit(self, signum, frame):
        """Salida de emergencia para Ctrl+C."""
        print("\n🚨 Salida de emergencia activada")
        self.exit()
    
    def compose(self):
        """Interfaz simple y segura."""
        yield Container(
            Static("🎯 TASKMASTER ANALYTICS - TUI SEGURA", classes="title"),
            Static("Esta versión es 100% segura de salir", classes="subtitle"),
            Static("Presiona CUALQUIER TECLA para ver ayuda de controles"),
            Button("📝 Ir a Lista de Tareas", id="tasks"),
            Button("🚪 Salir", id="quit"),
        )
    
    def on_key(self, event: events.Key) -> None:
        """Cualquier tecla muestra ayuda."""
        self.notify("🎮 Controles: q/Ctrl+C/Ctrl+Q/Escape = SALIR • F1 = Ayuda")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Maneja botones."""
        if event.button.id == "tasks":
            from tui_app.screens.task_list_safe import TaskListScreenSafe
            self.push_screen(TaskListScreenSafe())
        elif event.button.id == "quit":
            self.exit()
    
    def action_quit(self):
        """Acción de salir."""
        self.exit()
    
    def action_show_help(self):
        """Muestra ayuda completa."""
        self.notify("""
🎮 CONTROLES SEGUROS:
• q, Ctrl+C, Ctrl+Q, Escape = SALIR INMEDIATO
• F1 = Esta ayuda
• ↑↓←→ = Navegar
• Enter = Seleccionar
• Cualquier tecla = Recordatorio
        """)

if __name__ == "__main__":
    app = SafeTUI()
    app.run()