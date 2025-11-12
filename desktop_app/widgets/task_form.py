# desktop_app/widgets/task_form.py - FORMULARIO CORREGIDO
import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from core.storage import GestorAlmacenamiento
from core.managers import TareaManager

class TaskFormDialog:
    def __init__(self, parent):
        self.parent = parent
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Nueva Tarea")
        self.dialog.geometry("400x300")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.create_widgets()
        
    def create_widgets(self):
        """Crea el formulario."""
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        ttk.Label(main_frame, text="Nueva Tarea", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 15))
        
        # Campo título
        ttk.Label(main_frame, text="Título:*").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.title_entry = ttk.Entry(main_frame, width=40)
        self.title_entry.grid(row=1, column=1, sticky=tk.EW, pady=5, padx=(10, 0))
        
        # Campo descripción
        ttk.Label(main_frame, text="Descripción:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.desc_entry = ttk.Entry(main_frame, width=40)
        self.desc_entry.grid(row=2, column=1, sticky=tk.EW, pady=5, padx=(10, 0))
        
        # Campo prioridad
        ttk.Label(main_frame, text="Prioridad:*").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.priority_var = tk.StringVar(value="media")
        priority_frame = ttk.Frame(main_frame)
        priority_frame.grid(row=3, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        ttk.Radiobutton(priority_frame, text="Alta", variable=self.priority_var, value="alta").pack(side=tk.LEFT)
        ttk.Radiobutton(priority_frame, text="Media", variable=self.priority_var, value="media").pack(side=tk.LEFT)
        ttk.Radiobutton(priority_frame, text="Baja", variable=self.priority_var, value="baja").pack(side=tk.LEFT)
        
        # Campo proyecto
        ttk.Label(main_frame, text="Proyecto:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.project_entry = ttk.Entry(main_frame, width=40)
        self.project_entry.grid(row=4, column=1, sticky=tk.EW, pady=5, padx=(10, 0))
        
        # Botones
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Guardar", command=self.save_task).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Cancelar", command=self.dialog.destroy).pack(side=tk.LEFT)
        
        # Configurar grid weights
        main_frame.columnconfigure(1, weight=1)
        
        # Enfocar el campo título
        self.title_entry.focus()
        
    def save_task(self):
        """Guarda la nueva tarea."""
        title = self.title_entry.get().strip()
        description = self.desc_entry.get().strip()
        priority = self.priority_var.get()
        project = self.project_entry.get().strip() or None
        
        if not title:
            messagebox.showerror("Error", "El título es obligatorio")
            return
            
        try:
            gestor = GestorAlmacenamiento("sqlite")
            manager = TareaManager(gestor)
            
            tarea = manager.crear_tarea(
                titulo=title,
                descripcion=description,
                prioridad=priority,
                proyecto=project,
                usuario="desktop_user"
            )
            
            self.result = tarea
            messagebox.showinfo("Éxito", f"Tarea '{title}' creada correctamente")
            self.dialog.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo crear la tarea: {e}")