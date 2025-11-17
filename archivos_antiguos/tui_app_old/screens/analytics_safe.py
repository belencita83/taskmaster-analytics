# tui_app/screens/analytics_safe.py
from textual.screen import Screen
from textual.widgets import Static, Button, DataTable
from textual.containers import Container, Vertical
from textual import on
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from core.storage import GestorAlmacenamiento
from core.analytics import AnalyticsEngine
from core.managers import TareaManager

class AnalyticsScreenSafe(Screen):
    """Pantalla segura para analytics."""
    
    BINDINGS = [("escape", "go_back", "Atrás")]
    
    def compose(self):
        yield Container(
            Static("📊 ANALYTICS Y MÉTRICAS"),
            
            Vertical(
                DataTable(id="metrics_table"),
                Button("🔄 Actualizar Métricas", id="actualizar"),
                Button("🔙 Volver al Menú", id="volver"),
            ),
        )
    
    def on_mount(self):
        self.cargar_metricas()
    
    def cargar_metricas(self):
        """Carga métricas de forma segura."""
        tabla = self.query_one(DataTable)
        tabla.clear()
        tabla.add_columns("Métrica", "Puntaje", "Barra")
        
        try:
            gestor = GestorAlmacenamiento("sqlite")
            manager = TareaManager(gestor)
            analytics = AnalyticsEngine(manager)
            
            matriz = analytics.generar_matriz_metricas()
            calificaciones = matriz['calificaciones']
            
            # Mostrar métricas principales
            for nombre, valor in calificaciones.items():
                barras = "█" * int(valor / 20)  # 5 barras máximo
                tabla.add_row(
                    nombre.capitalize(),
                    f"{valor:.1f}%",
                    barras
                )
            
            # Score final
            score_final = matriz['score_final']
            barras_final = "█" * int(score_final / 20)
            tabla.add_row(
                "SCORE FINAL",
                f"{score_final:.1f}/100",
                f"⭐ {barras_final}"
            )
            
        except Exception as e:
            self.notify(f"❌ Error cargando métricas: {e}")
    
    @on(Button.Pressed, "#actualizar")
    def actualizar_metricas(self):
        self.cargar_metricas()
        self.notify("✅ Métricas actualizadas")
    
    @on(Button.Pressed, "#volver")
    def volver(self):
        self.app.pop_screen()
    
    def action_go_back(self):
        self.app.pop_screen()