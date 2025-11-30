# desktop_app/views/task_list.py
import customtkinter as ctk
import tkinter.messagebox as messagebox
from tkinter import ttk
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

class TaskListWindow:
    """Ventana para mostrar y gestionar la lista de tareas con búsqueda y filtros avanzados."""
    
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.tareas = []
        self.filtered_tasks = []
        
        # Variables para filtros
        self.search_term = ""
        self.status_filter = "todos"
        self.priority_filter = "todos"
        self.project_filter = "todos"
        
        # Crear ventana
        self.window = ctk.CTkToplevel(parent)
        self.window.title("Lista de Tareas - Con Búsqueda Avanzada")
        self.window.geometry("900x670")
        self.window.minsize(800, 600)
        self.window.transient(parent)
        self.window.grab_set()
        
        # Centrar después de crear la UI
        self.window.after(100, self._center_window)
        
        # Configurar interfaz
        self._setup_ui()
        
        # Cargar tareas
        self._load_tasks()
    
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
        """Configurar la interfaz de la lista de tareas con filtros avanzados."""
        # Frame principal
        main_frame = ctk.CTkFrame(self.window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        self._create_header(main_frame)
        
        # Controles de búsqueda y filtros MEJORADOS
        self._create_advanced_controls(main_frame)
        
        # Tabla de tareas
        self._create_task_table(main_frame)
        
        # Botones de acción CON HABILITACIÓN/DESHABILITACIÓN
        self._create_action_buttons(main_frame)
    
    def _create_header(self, parent):
        """Crear encabezado de la ventana."""
        header_frame = ctk.CTkFrame(parent, height=60)
        header_frame.pack(fill="x", pady=(0, 20))
        header_frame.pack_propagate(False)
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="LISTA DE TAREAS - GESTIÓN COMPLETA",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(side="left", padx=20, pady=10)
        
        # Contador de tareas MEJORADO
        self.task_count_label = ctk.CTkLabel(
            header_frame,
            text="Cargando...",
            font=ctk.CTkFont(size=12)
        )
        self.task_count_label.pack(side="right", padx=20, pady=10)
    
    def _create_advanced_controls(self, parent):
        """Crear controles de búsqueda y filtros avanzados."""
        controls_frame = ctk.CTkFrame(parent)
        controls_frame.pack(fill="x", pady=(0, 15))
        
        # Fila 1: Búsqueda
        search_frame = ctk.CTkFrame(controls_frame)
        search_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(search_frame, text="Buscar:", font=ctk.CTkFont(weight="bold")).pack(side="left", padx=(0, 10))
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Buscar por título o descripción...",
            width=300
        )
        self.search_entry.pack(side="left", padx=(0, 20))
        self.search_entry.bind("<KeyRelease>", self._on_search_changed)
        
        # Botón limpiar filtros
        ctk.CTkButton(
            search_frame,
            text="🗑️ Limpiar Filtros",
            command=self._clear_filters,
            width=120,
            fg_color="#6C757D",
            hover_color="#5A6268"
        ).pack(side="right", padx=(10, 0))
        
        # Fila 2: Filtros múltiples
        filters_frame = ctk.CTkFrame(controls_frame)
        filters_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        # Filtro por estado
        ctk.CTkLabel(filters_frame, text="Estado:", font=ctk.CTkFont(weight="bold")).pack(side="left", padx=(0, 10))
        
        self.status_filter_combo = ctk.CTkComboBox(
            filters_frame,
            values=["Todos", "Pendiente", "En Progreso", "Completada"],
            width=120,
            command=self._on_filter_changed
        )
        self.status_filter_combo.set("Todos")
        self.status_filter_combo.pack(side="left", padx=(0, 20))
        
        # Filtro por prioridad
        ctk.CTkLabel(filters_frame, text="Prioridad:", font=ctk.CTkFont(weight="bold")).pack(side="left", padx=(0, 10))
        
        self.priority_filter_combo = ctk.CTkComboBox(
            filters_frame,
            values=["Todos", "Alta", "Media", "Baja"],
            width=120,
            command=self._on_filter_changed
        )
        self.priority_filter_combo.set("Todos")
        self.priority_filter_combo.pack(side="left", padx=(0, 20))
        
        # Filtro por proyecto
        ctk.CTkLabel(filters_frame, text="Proyecto:", font=ctk.CTkFont(weight="bold")).pack(side="left", padx=(0, 10))
        
        self.project_filter_combo = ctk.CTkComboBox(
            filters_frame,
            values=["Cargando..."],
            width=150,
            command=self._on_filter_changed
        )
        self.project_filter_combo.set("Todos")
        self.project_filter_combo.pack(side="left", padx=(0, 20))
        
        # Botón actualizar
        ctk.CTkButton(
            filters_frame,
            text="Actualizar",
            command=self._load_tasks,
            width=100
        ).pack(side="right")
    
    def _create_task_table(self, parent):
        """Crear tabla para mostrar las tareas."""
        # Frame para la tabla
        table_frame = ctk.CTkFrame(parent)
        table_frame.pack(fill="both", expand=True, pady=(0, 15))
        
        # Crear Treeview con más columnas
        columns = ("id", "titulo", "descripcion", "estado", "prioridad", "proyecto", "fecha")
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=12
        )
        
        # Configurar columnas
        self.tree.heading("id", text="ID")
        self.tree.heading("titulo", text="Título")
        self.tree.heading("descripcion", text="Descripción")
        self.tree.heading("estado", text="Estado")
        self.tree.heading("prioridad", text="Prioridad")
        self.tree.heading("proyecto", text="Proyecto")
        self.tree.heading("fecha", text="Fecha")
        
        self.tree.column("id", width=50)
        self.tree.column("titulo", width=200)
        self.tree.column("descripcion", width=250)
        self.tree.column("estado", width=100)
        self.tree.column("prioridad", width=80)
        self.tree.column("proyecto", width=120)
        self.tree.column("fecha", width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Empaquetar
        self.tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y", padx=(0, 10), pady=10)
        
        # Bind eventos
        self.tree.bind("<Double-1>", self._on_task_double_click)
        self.tree.bind("<<TreeviewSelect>>", self._on_selection_change)
    
    def _create_action_buttons(self, parent):
        """Crear botones de acción CON HABILITACIÓN/DESHABILITACIÓN."""
        button_frame = ctk.CTkFrame(parent)
        button_frame.pack(fill="x")
        
        # Botón Nueva Tarea (siempre activo)
        ctk.CTkButton(
            button_frame,
            text="Nueva Tarea",
            command=self._open_task_form,
            fg_color="#E83E8C",
            hover_color="#C42D6E",
            font=ctk.CTkFont(weight="bold"),
            height=35
        ).pack(side="left", padx=(0, 8), pady=8)
        
        # Botón Editar (inicialmente deshabilitado)
        self.edit_btn = ctk.CTkButton(
            button_frame,
            text="Editar",
            command=self._edit_task,
            fg_color="#FFD166",
            hover_color="#E6BC5C",
            height=35,
            state="disabled"
        )
        self.edit_btn.pack(side="left", padx=(0, 8), pady=8)
        
        # Botón Cambiar Estado (inicialmente deshabilitado)
        self.status_btn = ctk.CTkButton(
            button_frame,
            text="Estado",
            command=self._change_task_status,
            fg_color="#06D6A0",
            hover_color="#04B486",
            height=35,
            state="disabled"
        )
        self.status_btn.pack(side="left", padx=(0, 8), pady=8)
        
        # Botón Eliminar (inicialmente deshabilitado)
        self.delete_btn = ctk.CTkButton(
            button_frame,
            text="Eliminar",
            command=self._delete_task,
            fg_color="#EF476F",
            hover_color="#D43D63",
            height=35,
            state="disabled"
        )
        self.delete_btn.pack(side="left", padx=(0, 8), pady=8)
        
        # Botón Analytics (siempre activo)
        ctk.CTkButton(
            button_frame,
            text="Analytics",
            command=self._open_analytics,
            fg_color="#9B5DE5",
            hover_color="#7B45C4",
            height=35
        ).pack(side="left", padx=(0, 8), pady=8)
        
        # Botón Cerrar (siempre activo)
        ctk.CTkButton(
            button_frame,
            text="Cerrar",
            command=self.window.destroy,
            fg_color="#6C757D",
            hover_color="#5A6268",
            height=35
        ).pack(side="right", pady=8)
    
    def _on_selection_change(self, event=None):
        """Habilitar/deshabilitar botones según selección."""
        selection = self.tree.selection()
        if selection:
            # Habilitar botones cuando hay selección
            self.edit_btn.configure(state="normal")
            self.status_btn.configure(state="normal")
            self.delete_btn.configure(state="normal")
        else:
            # Deshabilitar botones cuando no hay selección
            self.edit_btn.configure(state="disabled")
            self.status_btn.configure(state="disabled")
            self.delete_btn.configure(state="disabled")
    
    def _load_tasks(self):
        """Cargar tareas desde el controlador."""
        try:
            resultado = self.controller.obtener_todas_tareas()
            
            if resultado['success']:
                self.tareas = resultado['data']
                self._update_project_filter()
                self._apply_filters()
            else:
                messagebox.showerror("Error", resultado['message'])
                
        except Exception as e:
            messagebox.showerror("Error", f"Error cargando tareas: {e}")
    
    def _update_project_filter(self):
        """Actualizar opciones del filtro de proyectos."""
        proyectos = set()
        for tarea in self.tareas:
            if tarea.get('proyecto'):
                proyectos.add(tarea['proyecto'])
        
        project_list = ["Todos"] + sorted(list(proyectos))
        self.project_filter_combo.configure(values=project_list)
        self.project_filter_combo.set("Todos")
    
    def _apply_filters(self):
        """Aplicar todos los filtros a las tareas."""
        self.filtered_tasks = []
        
        for tarea in self.tareas:
            # Filtro de búsqueda
            matches_search = True
            if self.search_term:
                search_lower = self.search_term.lower()
                title_match = search_lower in tarea['titulo'].lower()
                desc_match = tarea.get('descripcion', '') and search_lower in tarea['descripcion'].lower()
                matches_search = title_match or desc_match
            
            # Filtro de estado
            matches_status = True
            status_filter = self.status_filter_combo.get()
            if status_filter != "Todos":
                estado_traduccion = {
                    "Pendiente": "pendiente",
                    "En Progreso": "en_progreso", 
                    "Completada": "completada"
                }
                matches_status = tarea['estado'] == estado_traduccion.get(status_filter, status_filter.lower())
            
            # Filtro de prioridad
            matches_priority = True
            priority_filter = self.priority_filter_combo.get()
            if priority_filter != "Todos":
                matches_priority = tarea['prioridad'] == priority_filter.lower()
            
            # Filtro de proyecto
            matches_project = True
            project_filter = self.project_filter_combo.get()
            if project_filter != "Todos":
                proyecto_tarea = tarea.get('proyecto', 'Sin proyecto')
                matches_project = proyecto_tarea == project_filter
            
            if matches_search and matches_status and matches_priority and matches_project:
                self.filtered_tasks.append(tarea)
        
        self._update_task_table()
        self._update_task_count()
        # Deshabilitar botones después de aplicar filtros (ninguna selección)
        self._on_selection_change()
    
    def _update_task_table(self):
        """Actualizar la tabla con las tareas filtradas."""
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Agregar tareas filtradas
        for tarea in self.filtered_tasks:
            # Emojis para estado y prioridad
            estado_emoji = {
                "pendiente": "⏳",
                "en_progreso": "🎨", 
                "completada": "✅"
            }
            
            prioridad_emoji = {
                "alta": "🔴",
                "media": "🟡",
                "baja": "🟢"
            }
            
            estado_display = f"{estado_emoji.get(tarea['estado'], '❓')} {tarea['estado']}"
            prioridad_display = f"{prioridad_emoji.get(tarea['prioridad'], '⚪')} {tarea['prioridad']}"
            
            fecha = tarea.get('fecha_creacion', 'N/A')
            if hasattr(fecha, 'strftime'):
                fecha = fecha.strftime('%d/%m/%Y')
            
            descripcion = tarea.get('descripcion', '') or "Sin descripción"
            if len(descripcion) > 50:
                descripcion = descripcion[:47] + "..."
            
            proyecto = tarea.get('proyecto', 'Sin proyecto')
            
            self.tree.insert("", "end", values=(
                tarea['id'],
                tarea['titulo'],
                descripcion,
                estado_display,
                prioridad_display,
                proyecto,
                fecha
            ))
    
    def _update_task_count(self):
        """Actualizar contador de tareas."""
        total = len(self.tareas)
        filtered = len(self.filtered_tasks)
        
        if total == filtered:
            self.task_count_label.configure(
                text=f"Total: {total} tareas"
            )
        else:
            self.task_count_label.configure(
                text=f"Mostrando: {filtered} de {total} tareas"
            )
    
    def _on_search_changed(self, event=None):
        """Manejar cambio en la búsqueda."""
        self.search_term = self.search_entry.get().strip()
        self._apply_filters()
    
    def _on_filter_changed(self, event=None):
        """Manejar cambio en los filtros."""
        self._apply_filters()
    
    def _clear_filters(self):
        """Limpiar todos los filtros."""
        self.search_entry.delete(0, 'end')
        self.status_filter_combo.set("Todos")
        self.priority_filter_combo.set("Todos")
        self.project_filter_combo.set("Todos")
        self.search_term = ""
        self._apply_filters()
    
    def _on_task_double_click(self, event):
        """Manejar doble clic en una tarea."""
        selection = self.tree.selection()
        if selection:
            self._edit_task()
    
    def _get_selected_task(self):
        """Obtener la tarea seleccionada."""
        selection = self.tree.selection()
        if not selection:
            return None
        
        item = selection[0]
        task_id = self.tree.item(item)['values'][0]
        
        for tarea in self.tareas:
            if tarea['id'] == task_id:
                return tarea
        
        return None
    
    def _change_task_status(self):
        """Cambiar el estado de la tarea seleccionada."""
        tarea = self._get_selected_task()
        if not tarea:
            messagebox.showwarning("Advertencia", "Selecciona una tarea primero")
            return
        
        try:
            resultado = self.controller.cambiar_estado_tarea(tarea['id'])
            
            if resultado['success']:
                messagebox.showinfo("Éxito", resultado['message'])
                self._load_tasks()
            else:
                messagebox.showerror("Error", resultado['message'])
                
        except Exception as e:
            messagebox.showerror("Error", f"Error cambiando estado: {e}")
    
    def _edit_task(self):
        """Editar la tarea seleccionada - IMPLEMENTACIÓN CORREGIDA."""
        tarea = self._get_selected_task()
        if not tarea:
            messagebox.showwarning("Advertencia", "Selecciona una tarea primero")
            return
        
        # Crear ventana de edición
        edit_window = ctk.CTkToplevel(self.window)
        edit_window.title(f"Editar Tarea: {tarea['titulo']}")
        edit_window.geometry("500x550")
        edit_window.transient(self.window)
        edit_window.grab_set()
        
        # Centrar ventana de edición
        edit_window.update_idletasks()
        screen_width = edit_window.winfo_screenwidth()
        screen_height = edit_window.winfo_screenheight()
        x = (screen_width - 500) // 2
        y = (screen_height - 550) // 2
        edit_window.geometry(f"+{x}+{y}")
        
        # Frame principal
        main_frame = ctk.CTkFrame(edit_window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        title_label = ctk.CTkLabel(
            main_frame,
            text="EDITAR TAREA",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Formulario de edición
        form_frame = ctk.CTkFrame(main_frame)
        form_frame.pack(fill="both", expand=True, pady=10)
        
        # Campo: Título
        ctk.CTkLabel(form_frame, text="Título *:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", pady=(10, 5))
        title_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Título de la tarea...",
            width=400
        )
        title_entry.insert(0, tarea['titulo'])
        title_entry.pack(fill="x", pady=(0, 15))
        
        # Campo: Descripción
        ctk.CTkLabel(form_frame, text="Descripción:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", pady=(10, 5))
        desc_text = ctk.CTkTextbox(form_frame, height=80)
        desc_text.insert("1.0", tarea.get('descripcion', ''))
        desc_text.pack(fill="x", pady=(0, 15))
        
        # Campo: Prioridad
        ctk.CTkLabel(form_frame, text="Prioridad *:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", pady=(10, 5))
        priority_var = ctk.StringVar(value=tarea['prioridad'])
        priority_frame = ctk.CTkFrame(form_frame)
        priority_frame.pack(fill="x", pady=(0, 15))
        
        priorities = [
            ("🔴 Alta", "alta"),
            ("🟡 Media", "media"), 
            ("🟢 Baja", "baja")
        ]
        
        for text, value in priorities:
            ctk.CTkRadioButton(
                priority_frame,
                text=text,
                variable=priority_var,
                value=value
            ).pack(side="left", padx=10)
        
        # Campo: Proyecto
        ctk.CTkLabel(form_frame, text="Proyecto:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", pady=(10, 5))
        project_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Proyecto opcional...",
            width=400
        )
        project_entry.insert(0, tarea.get('proyecto', ''))
        project_entry.pack(fill="x", pady=(0, 25))
        
        # Botones
        button_frame = ctk.CTkFrame(form_frame)
        button_frame.pack(fill="x", pady=20)
        
        def guardar_cambios():
            """Guardar los cambios de la tarea."""
            nuevo_titulo = title_entry.get().strip()
            nueva_descripcion = desc_text.get("1.0", "end-1c").strip()
            nueva_prioridad = priority_var.get()
            nuevo_proyecto = project_entry.get().strip() or None
            
            if not nuevo_titulo:
                messagebox.showerror("Error", "El título es obligatorio")
                return
            
            # Verificar si hubo cambios
            cambios = False
            if (nuevo_titulo != tarea['titulo'] or 
                nueva_descripcion != tarea.get('descripcion', '') or
                nueva_prioridad != tarea['prioridad'] or
                nuevo_proyecto != tarea.get('proyecto')):
                cambios = True
            
            if not cambios:
                messagebox.showinfo("Información", "No se detectaron cambios para guardar")
                edit_window.destroy()
                return
            
            # Actualizar tarea
            datos_actualizados = {
                'titulo': nuevo_titulo,
                'descripcion': nueva_descripcion,
                'prioridad': nueva_prioridad,
                'proyecto': nuevo_proyecto
            }
            
            try:
                # Llamar al método actualizar_tarea del controller
                resultado = self.controller.actualizar_tarea(tarea['id'], datos_actualizados)
                
                if resultado['success']:
                    messagebox.showinfo("Éxito", resultado['message'])
                    edit_window.destroy()
                    self._load_tasks()  # Recargar lista
                else:
                    messagebox.showerror("Error", resultado['message'])
                    
            except Exception as e:
                messagebox.showerror("Error", f"Error actualizando tarea: {e}")
        
        ctk.CTkButton(
            button_frame,
            text="GUARDAR CAMBIOS",
            command=guardar_cambios,
            fg_color="#E83E8C",
            hover_color="#C42D6E",
            font=ctk.CTkFont(weight="bold")
        ).pack(side="right", padx=(10, 0))
        
        ctk.CTkButton(
            button_frame,
            text="CANCELAR",
            command=edit_window.destroy,
            fg_color="#6C757D",
            hover_color="#5A6268"
        ).pack(side="right")
        
        # Enfocar el campo título
        title_entry.focus()
        title_entry.select_range(0, 'end')
    
    def _delete_task(self):
        """Eliminar la tarea seleccionada - IMPLEMENTACIÓN CORREGIDA."""
        tarea = self._get_selected_task()
        if not tarea:
            messagebox.showwarning("Advertencia", "Selecciona una tarea primero")
            return
        
        confirm = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Estás seguro de que quieres ELIMINAR permanentemente la tarea?\n\n"
            f"Título: {tarea['titulo']}\n"
            f"Estado: {tarea['estado']}\n"
            f"Prioridad: {tarea['prioridad']}\n"
            f"Proyecto: {tarea.get('proyecto', 'Sin proyecto')}\n\n"
            f"Esta acción no se puede deshacer."
        )
        
        if confirm:
            try:
                # Llamar al método eliminar_tarea del controller
                resultado = self.controller.eliminar_tarea(tarea['id'])
                
                if resultado['success']:
                    messagebox.showinfo("Éxito", resultado['message'])
                    self._load_tasks()  # Recargar lista
                else:
                    messagebox.showerror("Error", resultado['message'])
                
            except Exception as e:
                messagebox.showerror("Error", f"Error eliminando tarea: {e}")
    
    def _open_task_form(self):
        """Abrir formulario de nueva tarea."""
        from .task_form import TaskFormWindow
        TaskFormWindow(self.parent, self.controller)
        # Recargar lista después de crear nueva tarea
        self.window.after(1000, self._load_tasks)
    
    def _open_analytics(self):
        """Abrir panel de analytics."""
        from .analytics import AnalyticsWindow
        AnalyticsWindow(self.parent, self.controller)