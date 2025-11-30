# desktop_app/views/main_window.py
import customtkinter as ctk
import tkinter.messagebox as messagebox
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from tui_app.controllers.tarea_controller import TareaController


class MainWindow:
    """Ventana principal - VERSIÓN ULTRA COMPACTA."""
    
    def __init__(self, root):
        self.root = root
        self.controller = TareaController()
        
        # Configurar interfaz
        self._setup_ui()
        
    def _setup_ui(self):
        """Configurar interfaz ULTRA COMPACTA."""
        # Frame principal con padding mínimo
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)  # Padding mínimo
        
        # Header COMPACTO
        self._create_compact_header()
        
        # Contenido principal COMPACTO
        self._create_compact_content()
        
        # Footer COMPACTO
        self._create_compact_footer()
    
    def _create_compact_header(self):
        """Crear encabezado COMPACTO."""
        header_frame = ctk.CTkFrame(self.main_frame, height=50)  # Muy compacto
        header_frame.pack(fill="x", pady=(0, 10))  # Padding mínimo
        header_frame.pack_propagate(False)
        
        # Título compacto
        title_label = ctk.CTkLabel(
            header_frame,
            text="TaskMaster",
            font=ctk.CTkFont(size=16, weight="bold")  # Más pequeño
        )
        title_label.pack(side="left", padx=10, pady=8)
        
        # Estadísticas compactas
        stats = self._load_quick_stats()
        stats_text = f"Total: {stats['total']} | Pend: {stats['pendientes']}"
        
        stats_label = ctk.CTkLabel(
            header_frame,
            text=stats_text,
            font=ctk.CTkFont(size=11)  # Más pequeño
        )
        stats_label.pack(side="right", padx=10, pady=8)
    
    def _create_compact_content(self):
        """Crear contenido principal ULTRA COMPACTO."""
        content_frame = ctk.CTkFrame(self.main_frame)
        content_frame.pack(fill="both", expand=True)
        
        # Grid compacto - 2 filas, 2 columnas para pantallas pequeñas
        content_frame.grid_columnconfigure((0, 1), weight=1)
        content_frame.grid_rowconfigure((0, 1), weight=1)
        
        # Botón 1: Nueva Tarea (COMPACTO)
        new_task_btn = ctk.CTkButton(
            content_frame,
            text="Nueva Tarea",
            command=self._open_task_form,
            height=70,  # Más compacto
            font=ctk.CTkFont(size=20, weight="bold"),
            fg_color="#E83E8C",
            hover_color="#C42D6E",
            corner_radius=8
        )
        new_task_btn.grid(row=0, column=0, padx=8, pady=8, sticky="nsew")  # Padding mínimo
        
        # Botón 2: Lista de Tareas (COMPACTO)
        task_list_btn = ctk.CTkButton(
            content_frame,
            text="Lista Tareas",
            command=self._open_task_list,
            height=70,  # Más compacto
            font=ctk.CTkFont(size=20, weight="bold"),
            fg_color="#06D6A0",
            hover_color="#04B486",
            corner_radius=8
        )
        task_list_btn.grid(row=0, column=1, padx=8, pady=8, sticky="nsew")
        
        # Botón 3: Analytics (COMPACTO)
        analytics_btn = ctk.CTkButton(
            content_frame,
            text="Analytics",
            command=self._open_analytics,
            height=70,  # Más compacto
            font=ctk.CTkFont(size=20, weight="bold"),
            fg_color="#9B5DE5",
            hover_color="#7B45C4",
            corner_radius=8
        )
        analytics_btn.grid(row=1, column=0, padx=8, pady=8, sticky="nsew")
        
        # Botón 4: Estadísticas Rápidas (COMPACTO)
        stats_btn = ctk.CTkButton(
            content_frame,
            text="Estadísticas",
            command=self._show_quick_stats,
            height=70,  # Más compacto
            font=ctk.CTkFont(size=20, weight="bold"),
            fg_color="#118AB2",
            hover_color="#0E7490",
            corner_radius=8
        )
        stats_btn.grid(row=1, column=1, padx=8, pady=8, sticky="nsew")
        
        # Info mínima
        info_frame = ctk.CTkFrame(content_frame, height=40)  # Muy compacto
        info_frame.grid(row=2, column=0, columnspan=2, padx=8, pady=8, sticky="nsew")
        info_frame.grid_propagate(False)
        
        info_label = ctk.CTkLabel(
            info_frame,
            text="Selecciona una opción para comenzar",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        info_label.pack(expand=True)
    
    def _create_compact_footer(self):
        """Crear pie de página COMPACTO."""
        footer_frame = ctk.CTkFrame(self.main_frame, height=30)  # Muy compacto
        footer_frame.pack(fill="x", pady=(10, 0))
        footer_frame.pack_propagate(False)
        
        footer_label = ctk.CTkLabel(
            footer_frame,
            text="© 2024 TaskMaster v1.0",
            font=ctk.CTkFont(size=10),  # Más pequeño
            text_color="gray"
        )
        footer_label.pack(side="right", padx=10, pady=5)
    
    def _show_quick_stats(self):
        """Mostrar estadísticas rápidas."""
        stats = self._load_quick_stats()
        messagebox.showinfo(
            "Estadísticas Rápidas", 
            f"Resumen de Tareas:\n\n"
            f"• Total: {stats['total']} tareas\n"
            f"• ⏳ Pendientes: {stats['pendientes']}\n"
            f"• ✅ Completadas: {stats['completadas']}\n"
            f"• 🎨 En progreso: {stats.get('en_progreso', 0)}"
        )
    
    def _load_quick_stats(self):
        """Cargar estadísticas rápidas para el header."""
        try:
            resultado = self.controller.obtener_estadisticas()
            if resultado['success']:
                data = resultado['data']
                return {
                    'total': data['total_tareas'],
                    'pendientes': data['por_estado']['pendiente'],
                    'completadas': data['por_estado']['completada'],
                    'en_progreso': data['por_estado']['en_progreso']
                }
        except Exception as e:
            print(f"Error cargando estadísticas: {e}")
        
        return {'total': 0, 'pendientes': 0, 'completadas': 0, 'en_progreso': 0}
    
    def _open_task_form(self):
        """Abrir formulario de nueva tarea."""
        try:
            from .task_form import TaskFormWindow
            TaskFormWindow(self.root, self.controller)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el formulario: {e}")
    
    def _open_task_list(self):
        """Abrir lista de tareas."""
        try:
            from .task_list import TaskListWindow
            TaskListWindow(self.root, self.controller)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir la lista: {e}")
    
    def _open_analytics(self):
        """Abrir panel de analytics."""
        try:
            from .analytics import AnalyticsWindow
            AnalyticsWindow(self.root, self.controller)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir analytics: {e}")