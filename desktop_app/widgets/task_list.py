# desktop_app/widgets/task_list.py - COMPONENTE DE LISTA
import tkinter as tk
from tkinter import ttk

class TaskList(ttk.Frame):
    def __init__(self, parent, on_task_select=None):
        super().__init__(parent)
        self.on_task_select = on_task_select
        self.create_widgets()
        
    def create_widgets(self):
        """Crea la lista de tareas."""
        # Treeview (tabla)
        columns = ("ID", "Título", "Estado", "Prioridad", "Proyecto")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=15)
        
        # Configurar columnas
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        self.tree.column("Título", width=200)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind events
        self.tree.bind("<Double-1>", self.on_double_click)
        
    def load_tasks(self, tasks):
        """Carga tareas en la lista."""
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        for tarea in tasks:
            if hasattr(tarea, 'id'):
                self.tree.insert("", tk.END, values=(
                    tarea.id,
                    tarea.titulo or "Sin título",
                    tarea.estado or "pendiente",
                    tarea.prioridad or "media",
                    tarea.proyecto or "General"
                ))
                
    def on_double_click(self, event):
        """Maneja doble clic en tarea."""
        if self.on_task_select:
            selection = self.tree.selection()
            if selection:
                item = selection[0]
                values = self.tree.item(item, "values")
                self.on_task_select(values[0])  # Pasar ID de la tarea