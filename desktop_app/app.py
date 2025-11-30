# desktop_app/app.py
#!/usr/bin/env python3
"""
Punto de entrada principal para la aplicación desktop de TaskMaster Analytics.
"""
import customtkinter as ctk
import sys
import os

# Agregar el directorio raíz al path para importaciones
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from desktop_app.views.main_window import MainWindow

class TaskMasterDesktopApp:
    """Aplicación desktop principal de TaskMaster Analytics."""
    
    def __init__(self):
        # Configurar apariencia
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")
        
        # Crear ventana principal
        self.root = ctk.CTk()
        self.root.title("TaskMaster Analytics - Desktop")
        self.root.geometry("1000x650")
        self.root.minsize(900, 550)
        
        # Centrar ventana
        self._center_window()
        
        # Inicializar ventana principal
        self.main_window = MainWindow(self.root)
        
    def _center_window(self):
        """Centrar la ventana en la pantalla."""
        self.root.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        x = (screen_width - 1000) // 2
        y = (screen_height - 650) // 2
        
        self.root.geometry(f"1000x650+{x}+{y}")
    
    def run(self):
        """Ejecutar la aplicación."""
        try:
            print("🚀 Iniciando TaskMaster Analytics Desktop...")
            self.root.mainloop()
        except Exception as e:
            print(f"❌ Error ejecutando aplicación: {e}")
            raise

def main():
    """Función principal para ejecutar la aplicación."""
    app = TaskMasterDesktopApp()
    app.run()

if __name__ == "__main__":
    main()