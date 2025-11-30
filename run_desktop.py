#!/usr/bin/env python3
"""
Script ULTRA COMPACTO para ejecutar la aplicación desktop
"""
import sys
import os

def main():
    """Función principal para versión compacta."""
    print("Iniciando TaskMaster - VERSIÓN ULTRA COMPACTA")
    print("Optimizado para pantallas pequeñas")
    
    try:
        # Verificar dependencias
        import customtkinter
        print("customtkinter disponible")
        
        from desktop_app.app import TaskMasterDesktopApp
        app = TaskMasterDesktopApp()
        print("Aplicación compacta iniciada")
        print("Tamaño: 800x500 (centrado automático)")
        app.run()
        
    except ImportError as e:
        print(f"Error: {e}")
        print("Ejecuta: pip install customtkinter")
        input("Presiona Enter para salir...")
    except Exception as e:
        print(f"Error: {e}")
        input("Presiona Enter para salir...")

if __name__ == "__main__":
    main()