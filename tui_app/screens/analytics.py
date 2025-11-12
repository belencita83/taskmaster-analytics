# tui_app/screens/analytics.py - ANALYTICS MEJORADO
from textual.screen import Screen
from textual.widgets import Static, Button, DataTable, Header, Footer
from textual.containers import Container, Vertical, Horizontal
from textual import on
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from core.storage import GestorAlmacenamiento
from core.analytics import AnalyticsEngine
from core.managers import TareaManager

class AnalyticsScreen(Screen):
    """Pantalla de analytics mejorada"""
    
    CSS = """
    AnalyticsScreen {
        align: center middle;
    }
    
    .container {
        width: 80%;
        height: 80%;
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
    }
    
    .buttons {
        width: 100%;
        height: auto;
        align-horizontal: center;
        padding: 1;
    }
    """

    def compose(self):
        """Interfaz simple de analytics."""
        yield Header()
        yield Container(
            Static("ANALYTICS - METRICAS", classes="header"),
            Vertical(
                DataTable(id="metrics_table"),
                
                Horizontal(
                    Button("Actualizar", id="refresh", variant="primary"),
                    Button("Volver", id="back"),
                    classes="buttons"
                ),
            ),
            classes="container"
        )
        yield Footer()

    def on_mount(self):
        """Carga metricas al iniciar."""
        self.load_metrics()

    def load_metrics(self):
        """Carga métricas útiles."""
        table = self.query_one(DataTable)
        table.clear()
        table.add_columns("Metrica", "Valor")
        
        try:
            gestor = GestorAlmacenamiento("sqlite")
            tareas = gestor.cargar_tareas()
            
            if not tareas:
                table.add_row("Total tareas", "0")
                table.add_row("Tareas pendientes", "0")
                table.add_row("Tareas completadas", "0")
                return
            
            total = len(tareas)
            pendientes = sum(1 for t in tareas if t.estado == "pendiente")
            en_progreso = sum(1 for t in tareas if t.estado == "en_progreso")
            completadas = sum(1 for t in tareas if t.estado == "completada")
            
            table.add_row("Total tareas", str(total))
            table.add_row("Tareas pendientes", str(pendientes))
            table.add_row("Tareas en progreso", str(en_progreso))
            table.add_row("Tareas completadas", str(completadas))
            table.add_row("Porcentaje completado", f"{(completadas/total)*100:.1f}%")
            
        except Exception as e:
            # Métricas básicas si hay error
            table.add_row("Total tareas", "0")
            table.add_row("Tareas pendientes", "0")
            table.add_row("Tareas completadas", "0")
            table.add_row("Porcentaje completado", "0%")

    @on(Button.Pressed, "#refresh")
    def refresh_metrics(self):
        """Actualiza metricas."""
        self.load_metrics()
        self.notify("Metricas actualizadas")

    @on(Button.Pressed, "#back")
    def go_back(self):
        """Regresa al menu."""
        self.app.pop_screen()