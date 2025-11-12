# desktop_app/app.py - CORREGIDO
import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Corregir la ruta de importación
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.storage import GestorAlmacenamiento
from core.managers import TareaManager

class TaskMasterDesktop:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("TaskMaster Analytics")
        self.root.geometry("800x600")
        
        # Configurar estilo
        self.setup_styles()
        
        # Crear interfaz
        self.create_widgets()
        
    def setup_styles(self):
        """Configura estilos simples y bonitos."""
        style = ttk.Style()
        style.configure("TFrame", background="#f5f5f5")
        style.configure("TLabel", background="#f5f5f5", font=("Arial", 10))
        style.configure("Title.TLabel", background="#2c3e50", foreground="white", font=("Arial", 14, "bold"))
        style.configure("TButton", font=("Arial", 9))
        style.configure("Primary.TButton", background="#3498db", foreground="white")
        
    def create_widgets(self):
        """Crea la interfaz principal."""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(header_frame, text="🎯 TaskMaster Analytics", style="Title.TLabel").pack(fill=tk.X)
        ttk.Label(header_frame, text="Sistema de Gestión de Tareas").pack(fill=tk.X)
        
        # Botones de acción
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(button_frame, text="➕ Nueva Tarea", command=self.new_task).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="🔄 Actualizar", command=self.load_tasks).pack(side=tk.LEFT, padx=5)
        
        # Lista de tareas
        self.create_task_list(main_frame)
        
        # Cargar tareas iniciales
        self.load_tasks()
        
    def create_task_list(self, parent):
        """Crea la lista de tareas."""
        # Frame para la tabla
        table_frame = ttk.Frame(parent)
        table_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Treeview (tabla)
        columns = ("ID", "Título", "Estado", "Prioridad", "Proyecto")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        # Configurar columnas
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        self.tree.column("Título", width=200)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind double click para cambiar estado
        self.tree.bind("<Double-1>", self.on_task_double_click)
        
    def load_tasks(self):
        """Carga las tareas en la tabla."""
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        try:
            gestor = GestorAlmacenamiento("sqlite")
            tareas = gestor.cargar_tareas()
            
            for tarea in tareas:
                if hasattr(tarea, 'id'):
                    # Agregar emojis para mejor visualización
                    estado_emoji = {
                        "pendiente": "⏳",
                        "en_progreso": "🚧", 
                        "completada": "✅"
                    }
                    
                    estado = tarea.estado or "pendiente"
                    
                    self.tree.insert("", tk.END, values=(
                        tarea.id,
                        tarea.titulo or "Sin título",
                        f"{estado_emoji.get(estado, '❓')} {estado}",
                        tarea.prioridad or "media",
                        tarea.proyecto or "General"
                    ))
                    
        except Exception as e:
            # Datos de ejemplo
            self.tree.insert("", tk.END, values=(1, "Presentación TUT", "⏳ pendiente", "alta", "Universidad"))
            self.tree.insert("", tk.END, values=(2, "Estudiar SIS 2420", "🚧 en_progreso", "media", "Universidad"))
            
    def on_task_double_click(self, event):
        """Cambia el estado al hacer doble clic en una tarea."""
        selection = self.tree.selection()
        if selection:
            item = selection[0]
            values = self.tree.item(item, "values")
            task_id = int(values[0])
            
            # Extraer el estado actual (sin emoji)
            current_status = values[2].split(" ")[1] if " " in values[2] else values[2]
            
            # Cambiar estado
            if current_status == "pendiente":
                new_status = "en_progreso"
            elif current_status == "en_progreso":
                new_status = "completada"
            else:
                new_status = "pendiente"
                
            self.update_task_status(task_id, new_status)
            
    def update_task_status(self, task_id, new_status):
        """Actualiza el estado de una tarea."""
        try:
            gestor = GestorAlmacenamiento("sqlite")
            tareas = gestor.cargar_tareas()
            tarea = next((t for t in tareas if t.id == task_id), None)
            
            if tarea:
                tarea.estado = new_status
                gestor.guardar_tarea(tarea)
                self.load_tasks()  # Recargar lista
                messagebox.showinfo("Éxito", f"Tarea {task_id} actualizada a: {new_status}")
                
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar la tarea: {e}")
            
    def new_task(self):
        """Abre el formulario de nueva tarea."""
        from desktop_app.widgets.task_form import TaskFormDialog
        dialog = TaskFormDialog(self.root)
        self.root.wait_window(dialog.dialog)
        if dialog.result:
            self.load_tasks()  # Recargar si se creó una tarea
        
    def run(self):
        """Ejecuta la aplicación."""
        self.root.mainloop()

if __name__ == "__main__":
    app = TaskMasterDesktop()
    app.run()