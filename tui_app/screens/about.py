# tui_app/screens/about.py
from textual.screen import Screen
from textual.widgets import Static, Button, Header, Footer
from textual.containers import Container, Vertical, Horizontal
from textual import on

class AboutScreen(Screen):
    """Pantalla Acerca de"""
    
    CSS = """
    AboutScreen {
        align: center middle;
        background: #1A1B25;
    }
    
    .container {
        width: 60%;
        height: 70%;
        border: double #9B5DE5;
        background: #2A2B38;
        padding: 2;
    }
    
    .header {
        width: 100%;
        height: 3;
        content-align: center middle;
        background: #9B5DE5;
        color: #1A1B25;
        text-style: bold;
        padding: 1;
    }
    
    .info {
        width: 100%;
        content-align: center middle;
        color: #B8B8D1;
        padding: 0;
    }
    
    .buttons {
        width: 100%;
        height: auto;
        align-horizontal: center;
        padding: 1;
    }

    #back {
        background: #FF9E64;  /* Naranja */
        color: #1A1B25;
    }
    """

    def compose(self):
        yield Header()
        yield Container(
            Static("🎀 ACERCA DE 🎀", classes="header"),
            Vertical(
                Static("TaskMaster Analytics v1.0", classes="info"),
                Static("Sistema de gestión de tareas con analytics", classes="info"),
                Static("Desarrollado para SIS 2420 - Actualización Tecnológica", classes="info"),
                Static("✨ Interfaz TUI con Textual ✨", classes="info"),
                Static("", classes="info"),
                Static("Características:", classes="info"),
                Static("• Gestión completa de tareas", classes="info"),
                Static("• Analytics en tiempo real", classes="info"), 
                Static("• Múltiples interfaces", classes="info"),
                Static("• Base de datos SQLite", classes="info"),
                
                Horizontal(
                    Button("Volver", id="back"),
                    classes="buttons"
                ),
            ),
            classes="container"
        )
        yield Footer()

    @on(Button.Pressed, "#back")
    def go_back(self):
        """Regresa al menu."""
        self.app.pop_screen()