# tui_app/app.py - APLICACIÓN PRINCIPAL SIMPLIFICADA
import os
import sys
from textual.app import App

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tui_app.screens.main import MainScreen

class TaskMasterApp(App):
    """Aplicación principal"""
    
    def on_mount(self):
        self.push_screen(MainScreen())

if __name__ == "__main__":
    app = TaskMasterApp()
    app.run()