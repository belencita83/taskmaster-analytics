# tui_app/screens/analytics.py
from textual.screen import Screen
from textual.widgets import Static, Button, DataTable
from textual.containers import Container, Vertical, Horizontal
from textual import on
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from core.storage import GestorAlmacenamiento
from core.analytics import AnalyticsEngine
from core.managers import TareaManager

class AnalyticsScreen(Screen):
    """Pantalla para mostrar analytics y métricas - CORREGIDA"""
    
    CSS = """
    AnalyticsScreen {
        align: center middle;
    }
    
    .analytics-container {
        width: 85%;
        height: 85%;
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
    
    .buttons {
        width: 100%;
        height: auto;
        align-horizontal: center;
        padding: 1;
    }
    """
    
    def compose(self):
        """Compone la interfaz de analytics."""
        yield Container(
            Static("📊 Analytics y Métricas", classes="header"),
            
            Vertical(
                Static("Métricas de Productividad:"),
                DataTable(id="metrics_table"),
                
                Horizontal(
                    Button("🔄 Actualizar", id="refresh"),
                    Button("🔙 Atrás", id="back"),
                    classes="buttons"
                ),
            ),
            classes="analytics-container"
        )
    
    def on_mount(self):
        """Configura la pantalla al montarla."""
        self.load_metrics()
    
    def load_metrics(self):
        """Carga y muestra las métricas - CORREGIDO."""
        table = self.query_one(DataTable)
        table.clear()  # ⬅️ LIMPIAR ANTES DE CARGAR NUEVOS DATOS
        
        try:
            gestor = GestorAlmacenamiento("sqlite")
            manager = TareaManager(gestor)
            analytics = AnalyticsEngine(manager)
            
            # Generar matriz de métricas
            matriz = analytics.generar_matriz_metricas()
            
            # Configurar tabla de métricas
            table.add_columns("Métrica", "Valor", "Score")
            
            # Mostrar calificaciones principales
            calificaciones = matriz['calificaciones']
            table.add_row("🎯 Completitud", f"{calificaciones['completitud']}%", self._get_score_bar(calificaciones['completitud']))
            table.add_row("⏰ Puntualidad", f"{calificaciones['puntualidad']}%", self._get_score_bar(calificaciones['puntualidad']))
            table.add_row("📊 Priorización", f"{calificaciones['priorizacion']}%", self._get_score_bar(calificaciones['priorizacion']))
            table.add_row("📅 Consistencia", f"{calificaciones['consistencia']}%", self._get_score_bar(calificaciones['consistencia']))
            table.add_row("⚡ Velocidad", f"{calificaciones['velocidad']}%", self._get_score_bar(calificaciones['velocidad']))
            
            # Score final
            table.add_row("⭐ SCORE FINAL", f"{matriz['score_final']}/100", self._get_score_bar(matriz['score_final'], True))
            
        except Exception as e:
            self.notify(f"❌ Error cargando métricas: {e}")
            table.add_row("Error", str(e), "❌")
    
    def _get_score_bar(self, score, is_final=False):
        """Genera una barra de progreso visual."""
        bars = int(score / 10)
        bar = "█" * bars + " " * (10 - bars)
        
        if is_final:
            if score >= 90:
                return f"🎉 {bar}"
            elif score >= 70:
                return f"👍 {bar}"
            else:
                return f"🔧 {bar}"
        else:
            return bar
    
    @on(Button.Pressed, "#refresh")
    def refresh_metrics(self):
        """Actualiza las métricas."""
        self.load_metrics()  # ⬅️ Ahora limpiará y recargará correctamente
        self.notify("✅ Métricas actualizadas")
    
    @on(Button.Pressed, "#back")
    def go_back(self):
        """Regresa a la pantalla principal."""
        self.app.pop_screen()
