# tui_app/app_simple.py - TUI SIMPLE PERO IMPRESIONANTE
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from textual.app import App
from textual.widgets import Button, Static, DataTable
from textual.containers import Container, Grid
from textual import on

from core.storage import GestorAlmacenamiento
from core.analytics import AnalyticsEngine
from core.managers import TareaManager

class SimpleTUI(App):
    """TUI simple pero poderosa - Fácil de entender"""
    
    CSS = """
    /* CSS mínimo pero efectivo */
    Screen {
        background: #1e1e1e;
    }
    
    .title {
        text-align: center;
        color: #ff6b6b;
        text-style: bold;
        margin: 1;
    }
    
    .subtitle {
        text-align: center;
        color: #74b9ff;
        margin-bottom: 2;
    }
    
    .stats {
        text-align: center;
        color: #00cec9;
        margin: 1;
    }
    
    Button {
        width: 100%;
        margin: 1;
    }
    
    Button:hover {
        background: #74b9ff;
    }
    """
    
    def compose(self):
        """Interfaz simple con grid básico"""
        # Cargar datos para mostrar stats en tiempo real
        gestor = GestorAlmacenamiento("sqlite")
        tareas = gestor.cargar_tareas()
        total = len(tareas)
        completadas = sum(1 for t in tareas if t.estado == "completada")
        
        yield Container(
            Static("🎯 TASKMASTER ANALYTICS", classes="title"),
            Static("Gestión inteligente de tareas", classes="subtitle"),
            Static(f"📊 {total} tareas total • ✅ {completadas} completadas", classes="stats"),
            
            Grid(
                Button("📋 Ver todas las tareas", id="ver_tareas"),
                Button("➕ Crear nueva tarea", id="crear_tarea"), 
                Button("📈 Ver mis métricas", id="ver_metricas"),
                Button("🚪 Salir", id="salir", variant="error"),
                grid_columns="1fr",
                grid_gap=1,
            ),
            
            Static("\n💡 Tip: Usa el mouse o Tab para navegar", classes="subtitle"),
        )
    
    @on(Button.Pressed, "#ver_tareas")
    def ver_tareas(self):
        """Muestra pantalla simple de tareas"""
        self.push_screen(SimpleTasksScreen())
    
    @on(Button.Pressed, "#crear_tarea")  
    def crear_tarea(self):
        """Muestra formulario simple"""
        self.push_screen(SimpleFormScreen())
    
    @on(Button.Pressed, "#ver_metricas")
    def ver_metricas(self):
        """Muestra métricas simples"""
        self.push_screen(SimpleMetricsScreen())
    
    @on(Button.Pressed, "#salir")
    def salir(self):
        self.exit()

class SimpleTasksScreen(App):
    """Pantalla simple para ver tareas"""
    
    def compose(self):
        yield Container(
            Static("📋 TUS TAREAS", classes="title"),
            DataTable(id="tabla"),
            Button("🔙 Volver", id="volver"),
        )
    
    def on_mount(self):
        tabla = self.query_one(DataTable)
        tabla.add_columns("Tarea", "Estado", "Prioridad")
        
        gestor = GestorAlmacenamiento("sqlite")
        tareas = gestor.cargar_tareas()
        
        for tarea in tareas[:8]:  # Mostrar máximo 8
            estado = "✅" if tarea.estado == "completada" else "⏳"
            prioridad = {"alta": "🔴", "media": "🟡", "baja": "🔵"}.get(tarea.prioridad, "⚪")
            
            tabla.add_row(
                tarea.titulo[:25] + "..." if len(tarea.titulo) > 25 else tarea.titulo,
                estado,
                prioridad
            )
    
    @on(Button.Pressed, "#volver")
    def volver(self):
        self.exit()

class SimpleFormScreen(App):
    """Formulario simple para crear tareas"""
    
    def compose(self):
        yield Container(
            Static("➕ CREAR TAREA RÁPIDA", classes="title"),
            Static("Título:"),
            Static("[Aquí iría un Input simple]", classes="subtitle"),
            Static("Prioridad: 🔴 Alta 🟡 Media 🔵 Baja", classes="subtitle"),
            Static("\n🚧 Formulario en desarrollo...", classes="stats"),
            Button("🔙 Volver", id="volver"),
        )
    
    @on(Button.Pressed, "#volver")
    def volver(self):
        self.exit()

class SimpleMetricsScreen(App):
    """Pantalla simple para métricas"""
    
    def compose(self):
        yield Container(
            Static("📈 TUS MÉTRICAS", classes="title"),
            DataTable(id="metricas"),
            Button("🔙 Volver", id="volver"),
        )
    
    def on_mount(self):
        try:
            gestor = GestorAlmacenamiento("sqlite")
            manager = TareaManager(gestor)
            analytics = AnalyticsEngine(manager)
            
            matriz = analytics.generar_matriz_metricas()
            calificaciones = matriz['calificaciones']
            
            tabla = self.query_one(DataTable)
            tabla.add_columns("Área", "Puntaje", "Nivel")
            
            for nombre, valor in calificaciones.items():
                nivel = "😊 Excelente" if valor >= 80 else "👍 Bueno" if valor >= 60 else "💪 A mejorar"
                tabla.add_row(nombre.capitalize(), f"{valor}%", nivel)
            
            tabla.add_row("SCORE FINAL", f"{matriz['score_final']}%", "⭐")
            
        except Exception as e:
            self.query_one(DataTable).add_row("Error", str(e), "❌")
    
    @on(Button.Pressed, "#volver")
    def volver(self):
        self.exit()

if __name__ == "__main__":
    app = SimpleTUI()
    app.run()