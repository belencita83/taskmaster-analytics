# desktop_app/views/task_form.py
import customtkinter as ctk
import tkinter.messagebox as messagebox

class TaskFormWindow:
    """Ventana de formulario"""
    
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        
        # Crear ventana emergente COMPACTA
        self.window = ctk.CTkToplevel(parent)
        self.window.title("Nueva Tarea")
        self.window.geometry("500x550")  # MUCHO MÁS PEQUEÑO
        self.window.resizable(False, False)
        self.window.transient(parent)
        self.window.grab_set()
        
        # Centrar inmediatamente
        self._center_window()
        
        # Configurar interfaz COMPACTA
        self._setup_compact_ui()
    
    def _center_window(self):
        """Centrar ventana COMPACTA."""
        self.window.update_idletasks()
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        
        x = (screen_width - 500) // 2
        y = (screen_height - 550) // 2
        
        self.window.geometry(f"+{x}+{y}")
    
    def _setup_compact_ui(self):
        """Configurar interfaz ULTRA COMPACTA."""
        # Frame principal con padding mínimo
        main_frame = ctk.CTkFrame(self.window)
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Título compacto
        title_label = ctk.CTkLabel(
            main_frame,
            text="➕ NUEVA TAREA",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.pack(pady=(0, 15))
        
        # Formulario compacto
        form_frame = ctk.CTkFrame(main_frame)
        form_frame.pack(fill="both", expand=True)
        
        # Campo: Título compacto
        ctk.CTkLabel(form_frame, text="Título *:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", pady=(8, 3))
        self.title_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Título de la tarea...",
            height=30
        )
        self.title_entry.pack(fill="x", pady=(0, 10))
        
        # Campo: Descripción compacta
        ctk.CTkLabel(form_frame, text="Descripción:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", pady=(8, 3))
        self.desc_text = ctk.CTkTextbox(form_frame, height=60)  # Más compacto
        self.desc_text.pack(fill="x", pady=(0, 10))
        
        # Campo: Prioridad compacta
        ctk.CTkLabel(form_frame, text="Prioridad *:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", pady=(8, 3))
        self.priority_var = ctk.StringVar(value="media")
        priority_frame = ctk.CTkFrame(form_frame)
        priority_frame.pack(fill="x", pady=(0, 10))
        
        priorities = [
            ("🔴 Alta", "alta"),
            ("🟡 Media", "media"), 
            ("🟢 Baja", "baja")
        ]
        
        for text, value in priorities:
            ctk.CTkRadioButton(
                priority_frame,
                text=text,
                variable=self.priority_var,
                value=value,
                font=ctk.CTkFont(size=11)  # Más pequeño
            ).pack(side="left", padx=8, pady=5)
        
        # Campo: Proyecto compacto
        ctk.CTkLabel(form_frame, text="Proyecto:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", pady=(8, 3))
        self.project_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Proyecto opcional...",
            height=30
        )
        self.project_entry.pack(fill="x", pady=(0, 20))
        
        # Botones compactos
        button_frame = ctk.CTkFrame(form_frame)
        button_frame.pack(fill="x", pady=15)
        
        ctk.CTkButton(
            button_frame,
            text="💾 GUARDAR",
            command=self._save_task,
            fg_color="#E83E8C",
            hover_color="#C42D6E",
            font=ctk.CTkFont(weight="bold"),
            height=32
        ).pack(side="right", padx=(8, 0))
        
        ctk.CTkButton(
            button_frame,
            text="❌ CANCELAR",
            command=self.window.destroy,
            fg_color="#6C757D",
            hover_color="#5A6268",
            height=32
        ).pack(side="right")
        
        # Info compacta
        info_label = ctk.CTkLabel(
            form_frame,
            text="* Campos obligatorios",
            font=ctk.CTkFont(size=10, slant="italic"),
            text_color="gray"
        )
        info_label.pack(anchor="w", pady=(5, 0))
        
        # Enfocar campo título
        self.title_entry.focus()
    
    def _save_task(self):
        """Guardar la nueva tarea."""
        titulo = self.title_entry.get().strip()
        descripcion = self.desc_text.get("1.0", "end-1c").strip()
        prioridad = self.priority_var.get()
        proyecto = self.project_entry.get().strip() or None
        
        if not titulo:
            messagebox.showerror("Error", "El título es obligatorio")
            self.title_entry.focus()
            return
        
        form_data = {
            'titulo': titulo,
            'descripcion': descripcion,
            'prioridad': prioridad,
            'proyecto': proyecto,
            'usuario': 'desktop_user'
        }
        
        try:
            resultado = self.controller.crear_tarea(form_data)
            
            if resultado['success']:
                messagebox.showinfo("Éxito", "Tarea creada correctamente")
                self.window.destroy()
            else:
                messagebox.showerror("Error", resultado['message'])
                
        except Exception as e:
            messagebox.showerror("Error", f"Error guardando tarea: {e}")