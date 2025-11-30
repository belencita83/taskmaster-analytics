# desktop_app/views/analytics.py
import customtkinter as ctk
import tkinter.messagebox as messagebox
from tkinter import ttk
import sys
import os
from datetime import datetime, timedelta

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

class AnalyticsWindow:
    """Ventana para mostrar analytics y estadísticas con distribución por proyecto y tendencias."""
    
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.stats_data = None
        
        # Crear ventana
        self.window = ctk.CTkToplevel(parent)
        self.window.title("Analytics - Con Distribución y Tendencias")
        self.window.geometry("950x600")
        self.window.minsize(750, 400)
        self.window.transient(parent)
        self.window.grab_set()
        
        # Centrar después de crear la UI
        self.window.after(100, self._center_window)
        
        # Configurar interfaz
        self._setup_ui()
        
        # Cargar estadísticas
        self._load_analytics()
    
    def _center_window(self):
        """Centrar la ventana CORREGIDO."""
        self.window.update_idletasks()
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        
        window_width = self.window.winfo_width()
        window_height = self.window.winfo_height()
        
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.window.geometry(f'+{x}+{y}')
    
    def _setup_ui(self):
        """Configurar la interfaz de analytics mejorada."""
        # Frame principal
        main_frame = ctk.CTkFrame(self.window)
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Header
        self._create_header(main_frame)
        
        # Métricas principales
        self._create_metrics(main_frame)
        
        # Estadísticas detalladas con pestañas MEJORADAS
        self._create_advanced_tabs(main_frame)
        
        # Botones
        self._create_action_buttons(main_frame)
    
    def _create_header(self, parent):
        """Crear encabezado."""
        header_frame = ctk.CTkFrame(parent, height=50)
        header_frame.pack(fill="x", pady=(0, 15))
        header_frame.pack_propagate(False)
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="ANALYTICS - DATOS EN TIEMPO REAL",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.pack(side="left", padx=15, pady=8)
        
        # Botón actualizar
        ctk.CTkButton(
            header_frame,
            text="Actualizar",
            command=self._load_analytics,
            width=90
        ).pack(side="right", padx=15, pady=8)
    
    def _create_metrics(self, parent):
        """Crear métricas principales COMPACTAS."""
        metrics_frame = ctk.CTkFrame(parent)
        metrics_frame.pack(fill="x", pady=(0, 15))
        
        # Crear 5 métricas en grid más compactas
        metrics_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
        
        # Métrica 1: Total tareas
        self.total_metric = self._create_compact_metric_card(
            metrics_frame, "📈 Total", "0", 0, 0, "#9B5DE5"
        )
        
        # Métrica 2: Pendientes
        self.pending_metric = self._create_compact_metric_card(
            metrics_frame, "⏳ Pend", "0", 0, 1, "#FFD166"
        )
        
        # Métrica 3: En progreso
        self.progress_metric = self._create_compact_metric_card(
            metrics_frame, "🎨 Prog", "0", 0, 2, "#06D6A0"
        )
        
        # Métrica 4: Completadas
        self.completed_metric = self._create_compact_metric_card(
            metrics_frame, "✅ Comp", "0", 0, 3, "#E83E8C"
        )
        
        # Métrica 5: Tasa de finalización
        self.completion_rate_metric = self._create_compact_metric_card(
            metrics_frame, "📊 Tasa", "0%", 0, 4, "#118AB2"
        )
    
    def _create_compact_metric_card(self, parent, title, value, row, column, color):
        """Crear una tarjeta de métrica COMPACTA."""
        card_frame = ctk.CTkFrame(parent, fg_color=color, height=60)
        card_frame.grid(row=row, column=column, padx=3, pady=3, sticky="nsew")
        card_frame.grid_propagate(False)
        
        # Título compacto
        title_label = ctk.CTkLabel(
            card_frame,
            text=title,
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="white"
        )
        title_label.pack(pady=(8, 2))
        
        # Valor
        value_label = ctk.CTkLabel(
            card_frame,
            text=value,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="white"
        )
        value_label.pack(pady=(0, 8))
        
        return value_label
    
    def _create_advanced_tabs(self, parent):
        """Crear pestañas avanzadas COMPACTAS."""
        tabview = ctk.CTkTabview(parent, height=350)
        tabview.pack(fill="both", expand=True, pady=(0, 10))
        
        # Pestaña 1: Distribución por Proyecto (CON DATOS REALES)
        tab_project = tabview.add("Proyectos")
        self._create_project_distribution(tab_project)
        
        # Pestaña 2: Por Prioridad (CON DATOS REALES)
        tab_priority = tabview.add("Prioridad")
        self._create_priority_stats(tab_priority)
        
        # Pestaña 3: Tendencias (CON DATOS REALES)
        tab_trends = tabview.add("Tendencias")
        self._create_trends_stats(tab_trends)
    
    def _create_project_distribution(self, parent):
        """Crear distribución por proyecto CON DATOS REALES."""
        project_frame = ctk.CTkFrame(parent)
        project_frame.pack(fill="both", expand=True, padx=8, pady=8)
        
        # Treeview para proyectos
        columns = ("proyecto", "total", "pendientes", "completadas", "tasa")
        self.project_tree = ttk.Treeview(
            project_frame,
            columns=columns,
            show="headings",
            height=8
        )
        
        # Configurar columnas
        self.project_tree.heading("proyecto", text="Proyecto")
        self.project_tree.heading("total", text="Total")
        self.project_tree.heading("pendientes", text="⏳")
        self.project_tree.heading("completadas", text="✅")
        self.project_tree.heading("tasa", text="%")
        
        self.project_tree.column("proyecto", width=100)
        self.project_tree.column("total", width=60)
        self.project_tree.column("pendientes", width=60)
        self.project_tree.column("completadas", width=60)
        self.project_tree.column("tasa", width=60)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(project_frame, orient="vertical", command=self.project_tree.yview)
        self.project_tree.configure(yscrollcommand=scrollbar.set)
        
        # Empaquetar
        self.project_tree.pack(side="left", fill="both", expand=True, padx=8, pady=8)
        scrollbar.pack(side="right", fill="y", padx=(0, 8), pady=8)
    
    def _create_priority_stats(self, parent):
        """Crear estadísticas por prioridad CON DATOS REALES."""
        priority_frame = ctk.CTkFrame(parent)
        priority_frame.pack(fill="both", expand=True, padx=8, pady=8)
        
        # Grid para prioridades
        priority_frame.grid_columnconfigure((0, 1, 2), weight=1)
        priority_frame.grid_rowconfigure(0, weight=1)
        
        self.priority_labels = {}
        
        priorities = [
            ("ALTA", "alta", "#EF476F", 0, 0),
            ("MEDIA", "media", "#FFD166", 0, 1),
            ("BAJA", "baja", "#06D6A0", 0, 2),
        ]
        
        for title, key, color, row, col in priorities:
            frame = ctk.CTkFrame(priority_frame, fg_color=color, corner_radius=8, height=50)
            frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            frame.grid_propagate(False)
            
            # Título
            title_label = ctk.CTkLabel(
                frame,
                text=title,
                font=ctk.CTkFont(size=15, weight="bold"),
                text_color="white"
            )
            title_label.pack(pady=(10, 2))
            
            # Estadísticas
            stats_label = ctk.CTkLabel(
                frame,
                text="T:0\nC:0\n0%",
                font=ctk.CTkFont(size=13),
                text_color="white",
                justify="center"
            )
            stats_label.pack(pady=(0, 10))
            
            self.priority_labels[key] = stats_label
        
        # Frame para resumen
        summary_frame = ctk.CTkFrame(priority_frame)
        summary_frame.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")
        
        self.priority_summary = ctk.CTkTextbox(summary_frame, height=150)
        self.priority_summary.pack(fill="both", expand=True, padx=8, pady=8)
        self.priority_summary.insert("1.0", "Cargando datos de prioridades...")
        self.priority_summary.configure(state="disabled")
    
    def _create_trends_stats(self, parent):
        """Crear estadísticas de tendencias CON DATOS REALES."""
        trends_frame = ctk.CTkFrame(parent)
        trends_frame.pack(fill="both", expand=True, padx=8, pady=8)
        
        # Treeview para tendencias
        columns = ("fecha", "total", "nuevas", "completadas", "tasa")
        self.trends_tree = ttk.Treeview(
            trends_frame,
            columns=columns,
            show="headings",
            height=8
        )
        
        # Configurar columnas
        self.trends_tree.heading("fecha", text="Fecha")
        self.trends_tree.heading("total", text="Total")
        self.trends_tree.heading("nuevas", text="🆕")
        self.trends_tree.heading("completadas", text="✅")
        self.trends_tree.heading("tasa", text="%")
        
        self.trends_tree.column("fecha", width=100)
        self.trends_tree.column("total", width=60)
        self.trends_tree.column("nuevas", width=50)
        self.trends_tree.column("completadas", width=50)
        self.trends_tree.column("tasa", width=50)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(trends_frame, orient="vertical", command=self.trends_tree.yview)
        self.trends_tree.configure(yscrollcommand=scrollbar.set)
        
        # Empaquetar
        self.trends_tree.pack(side="left", fill="both", expand=True, padx=8, pady=8)
        scrollbar.pack(side="right", fill="y", padx=(0, 8), pady=8)
    
    def _create_action_buttons(self, parent):
        """Crear botones de acción COMPACTOS."""
        button_frame = ctk.CTkFrame(parent, height=45)
        button_frame.pack(fill="x", pady=(5, 0))
        button_frame.pack_propagate(False)
        
        ctk.CTkButton(
            button_frame,
            text="Exportar",
            command=self._export_report,
            fg_color="#9B5DE5",
            hover_color="#7B45C4",
            width=100,
            height=35
        ).pack(side="left", padx=(0, 8), pady=5)
        
        ctk.CTkButton(
            button_frame,
            text="Cerrar",
            command=self.window.destroy,
            fg_color="#6C757D",
            hover_color="#5A6268",
            width=80,
            height=35
        ).pack(side="right", pady=5)
    
    def _load_analytics(self):
        """Cargar datos REALES de analytics."""
        try:
            # Obtener estadísticas generales
            resultado_stats = self.controller.obtener_estadisticas()
            
            if resultado_stats['success']:
                data = resultado_stats['data']
                self.stats_data = data
                self._update_metrics(data)
                self._update_detailed_stats(data)
            else:
                messagebox.showerror("Error", resultado_stats['message'])
                
        except Exception as e:
            messagebox.showerror("Error", f"Error cargando analytics: {e}")
    
    def _update_metrics(self, data):
        """Actualizar métricas principales con datos reales."""
        total = data['total_tareas']
        completadas = data['por_estado']['completada']
        tasa = (completadas / total * 100) if total > 0 else 0
        
        self.total_metric.configure(text=str(total))
        self.pending_metric.configure(text=str(data['por_estado']['pendiente']))
        self.progress_metric.configure(text=str(data['por_estado']['en_progreso']))
        self.completed_metric.configure(text=str(completadas))
        self.completion_rate_metric.configure(text=f"{tasa:.1f}%")
    
    def _update_detailed_stats(self, data):
        """Actualizar estadísticas detalladas con datos reales."""
        self._update_project_stats(data)
        self._update_priority_stats(data)
        self._update_trends_stats(data)
    
    def _update_project_stats(self, data):
        """Actualizar estadísticas de proyectos con datos REALES."""
        # Limpiar treeview
        for item in self.project_tree.get_children():
            self.project_tree.delete(item)
        
        try:
            # Obtener todas las tareas para analizar proyectos
            resultado_tareas = self.controller.obtener_todas_tareas()
            
            if resultado_tareas['success']:
                tareas = resultado_tareas['data']
                
                # Calcular distribución por proyecto
                proyectos = {}
                for tarea in tareas:
                    proyecto = tarea.get('proyecto', 'Sin Proyecto')
                    if proyecto not in proyectos:
                        proyectos[proyecto] = {
                            'total': 0,
                            'pendientes': 0,
                            'completadas': 0
                        }
                    
                    proyectos[proyecto]['total'] += 1
                    if tarea['estado'] == 'completada':
                        proyectos[proyecto]['completadas'] += 1
                    elif tarea['estado'] == 'pendiente':
                        proyectos[proyecto]['pendientes'] += 1
                
                # Insertar datos en el treeview
                for proyecto, stats in proyectos.items():
                    total = stats['total']
                    completadas = stats['completadas']
                    pendientes = stats['pendientes']
                    tasa = (completadas / total * 100) if total > 0 else 0
                    
                    self.project_tree.insert("", "end", values=(
                        proyecto,
                        total,
                        pendientes,
                        completadas,
                        f"{tasa:.1f}%"
                    ))
            else:
                # Insertar mensaje de error
                self.project_tree.insert("", "end", values=(
                    "Error cargando datos", 0, 0, 0, "0%"
                ))
                
        except Exception as e:
            print(f"Error actualizando proyectos: {e}")
            self.project_tree.insert("", "end", values=(
                "Error en datos", 0, 0, 0, "0%"
            ))
    
    def _update_priority_stats(self, data):
        """Actualizar estadísticas de prioridades con datos REALES."""
        total = data['total_tareas']
        
        try:
            # Obtener tareas para cálculo detallado
            resultado_tareas = self.controller.obtener_todas_tareas()
            
            if resultado_tareas['success']:
                tareas = resultado_tareas['data']
                
                # Calcular completadas por prioridad
                prioridad_detalle = {}
                for tarea in tareas:
                    prioridad = tarea['prioridad']
                    if prioridad not in prioridad_detalle:
                        prioridad_detalle[prioridad] = {'total': 0, 'completadas': 0}
                    
                    prioridad_detalle[prioridad]['total'] += 1
                    if tarea['estado'] == 'completada':
                        prioridad_detalle[prioridad]['completadas'] += 1
                
                # Actualizar tarjetas de prioridad
                for key, label in self.priority_labels.items():
                    if key in prioridad_detalle:
                        stats = prioridad_detalle[key]
                        count = stats['total']
                        completadas = stats['completadas']
                        tasa = (completadas / count * 100) if count > 0 else 0
                        
                        label.configure(text=f"T:{count}\nC:{completadas}\n{tasa:.1f}%")
                    else:
                        label.configure(text=f"T:0\nC:0\n0%")
                
                # Actualizar resumen
                self.priority_summary.configure(state="normal")
                self.priority_summary.delete("1.0", "end")
                self.priority_summary.insert("1.0", "📊 DISTRIBUCIÓN POR PRIORIDAD\n\n")
                
                for key in ['alta', 'media', 'baja']:
                    if key in prioridad_detalle:
                        stats = prioridad_detalle[key]
                        count = stats['total']
                        completadas = stats['completadas']
                        porcentaje = (count / total * 100) if total > 0 else 0
                        tasa_completitud = (completadas / count * 100) if count > 0 else 0
                        
                        self.priority_summary.insert("end", 
                            f"• {key.capitalize()}: {count} tareas ({porcentaje:.1f}%)\n"
                            f"  Completadas: {completadas} ({tasa_completitud:.1f}%)\n\n"
                        )
                    else:
                        self.priority_summary.insert("end", f"• {key.capitalize()}: 0 tareas\n\n")
                
                self.priority_summary.configure(state="disabled")
                
        except Exception as e:
            print(f"Error actualizando prioridades: {e}")
    
    def _update_trends_stats(self, data):
        """Actualizar estadísticas de tendencias con datos REALES."""
        # Limpiar treeview
        for item in self.trends_tree.get_children():
            self.trends_tree.delete(item)
        
        try:
            # Obtener tareas para análisis temporal
            resultado_tareas = self.controller.obtener_todas_tareas()
            
            if resultado_tareas['success']:
                tareas = resultado_tareas['data']
                
                # Analizar tendencias de los últimos 7 días
                hoy = datetime.now()
                tendencias = []
                
                for i in range(6, -1, -1):
                    fecha = hoy - timedelta(days=i)
                    fecha_str = fecha.strftime('%d/%m')
                    
                    # Contar tareas creadas y completadas en este día
                    tareas_creadas = [
                        t for t in tareas 
                        if hasattr(t.get('fecha_creacion'), 'date') and 
                        t['fecha_creacion'].date() == fecha.date()
                    ]
                    
                    tareas_completadas = [
                        t for t in tareas_creadas 
                        if t['estado'] == 'completada'
                    ]
                    
                    nuevas = len(tareas_creadas)
                    completadas_dia = len(tareas_completadas)
                    
                    # Tasa de completitud del día
                    tasa_dia = (completadas_dia / nuevas * 100) if nuevas > 0 else 0
                    
                    # Total acumulado hasta este día
                    total_acumulado = len([
                        t for t in tareas 
                        if hasattr(t.get('fecha_creacion'), 'date') and 
                        t['fecha_creacion'].date() <= fecha.date()
                    ])
                    
                    tendencias.append((
                        fecha_str,
                        total_acumulado,
                        nuevas,
                        completadas_dia,
                        f"{tasa_dia:.1f}%"
                    ))
                
                # Insertar tendencias
                for tendencia in tendencias:
                    self.trends_tree.insert("", "end", values=tendencia)
                    
        except Exception as e:
            print(f"Error actualizando tendencias: {e}")
            # Insertar datos de ejemplo si hay error
            hoy = datetime.now()
            for i in range(6, -1, -1):
                fecha = hoy - timedelta(days=i)
                self.trends_tree.insert("", "end", values=(
                    fecha.strftime('%d/%m'),
                    "N/D", "N/D", "N/D", "N/D"
                ))
    
    def _export_report(self):
        """Exportar reporte de analytics."""
        messagebox.showinfo(
            "Exportar Reporte", 
            "Función de exportación lista\n\n"
            "En una implementación completa, se generaría:\n"
            "• Reporte PDF con gráficos\n"
            "• Archivo Excel con datos detallados\n"
            "• Dashboard interactivo"
        )