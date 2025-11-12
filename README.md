# TaskMaster Analytics

Sistema profesional de gestión de tareas con análisis de productividad, desarrollado en Python con arquitectura por capas y múltiples interfaces.

## Características Principales

### Analytics Avanzado
- **Matriz de métricas** con sistema de calificación (0-100)
- **5 dimensiones** de evaluación: Completitud, Puntualidad, Priorización, Consistencia, Velocidad
- **Recomendaciones inteligentes** basadas en métricas
- **Dashboard interactivo** con visualizaciones

### Base de Datos
- **SQLite** con transacciones ACID
- **Campos de auditoría** (creado_por, actualizado_en, etc.)
- **Persistencia robusta** de datos
- **Compartida entre todas las interfaces**

### Sistema de Reportes
- **Exportación multi-formato**: CSV, JSON, TXT
- **Reportes ejecutivos** con estadísticas completas
- **Timestamps automáticos** en nombres de archivo

### Arquitectura Profesional
- **Patrón Managers** para separación de responsabilidades
- **Factory Pattern** para almacenamiento intercambiable
- **Models** con validaciones y lógica de negocio
- **Múltiples interfaces** compartiendo el mismo core

## Interfaces Disponibles

### 1. Console App
Interfaz de línea de comandos para uso rápido y scripts.

**Características:**
- Navegación por menús interactivos
- Gestión completa de tareas
- Exportación de reportes
- Rápida y ligera

**Ejecutar:**
```bash
python console_app/app.py
```

### 2. TUI (Text User Interface)
Interfaz textual elegante desarrollada con Textual.

**Características:**
- Menú principal con navegación intuitiva
- Lista de tareas con cambio de estados mediante selección
- Formulario de creación de nuevas tareas
- Dashboard de analytics con métricas en tiempo real
- Interfaz responsive y elegante

**Ejecutar:**
```bash
python tui_app/app.py
```

### 3. Desktop App
Interfaz gráfica tradicional desarrollada con Tkinter.

**Características:**
- Interfaz visual con tabla de tareas
- Cambio de estado con doble clic
- Formulario modal para nuevas tareas
- Diseño limpio y profesional
- Familiar para usuarios de aplicaciones desktop

**Ejecutar:**
```bash
python desktop_app/app.py
```

## Flujo de Trabajo

1. **Crear Tareas** - Usa cualquier interfaz para agregar nuevas tareas
2. **Seguimiento** - Cambia estados (pendiente → en progreso → completada)
3. **Análisis** - Consulta métricas de productividad en analytics
4. **Reportes** - Exporta datos para análisis externo

**Todas las interfaces comparten la misma base de datos**, por lo que puedes alternar entre ellas sin perder información.

## Tecnologías Utilizadas

- **Python 3.8+**
- **SQLite** - Base de datos embebida
- **Textual** - Framework para TUI
- **Tkinter** - Para interfaz desktop
- **Arquitectura por capas** - Models, Managers, Storage, Analytics

## Instalación

1. **Clonar repositorio:**
```bash
git clone https://github.com/tu_usuario/taskmaster-analytics.git
cd taskmaster-analytics
```

2. **Crear entorno virtual (recomendado):**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

## Estructura del Proyecto

```
taskmaster-analytics/
├── core/                 # Lógica de negocio compartida
│   ├── models.py         # Modelos de datos
│   ├── storage.py        # Gestión de base de datos
│   ├── managers.py       # Lógica de aplicación
│   └── analytics.py      # Motor de analytics
├── console_app/          # Interfaz de consola
├── tui_app/             # Interfaz textual (Textual)
│   ├── app.py
│   └── screens/
├── desktop_app/         # Interfaz gráfica (Tkinter)
│   ├── app.py
│   └── widgets/
├── data/                # Base de datos SQLite
├── reportes/            # Reportes exportados
└── requirements.txt     # Dependencias
```

## Uso Rápido

### Desde Consola:
```bash
python console_app/app.py
```

### Desde TUI (Recomendado):
```bash
python tui_app/app.py
```

### Desde Desktop:
```bash
python desktop_app/app.py
```

## Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

Distribuido bajo la Licencia MIT. Ver `LICENSE` para más información.

---

**¡TaskMaster Analytics - Gestiona tus tareas de forma inteligente desde cualquier interfaz!** 🚀
```