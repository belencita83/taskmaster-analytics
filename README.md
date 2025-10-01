# TaskMaster Analytics 🎯

Sistema profesional de gestión de tareas con análisis de productividad, desarrollado en Python con arquitectura por capas.

## 🚀 Características Principales

### 🗃️ Base de Datos
- **SQLite** con transacciones ACID
- **Campos de auditoría** (creado_por, actualizado_en, etc.)
- **Persistencia robusta** de datos

### 📊 Analytics Avanzado
- **Matriz de métricas** con sistema de calificación (0-100)
- **5 dimensiones** de evaluación: Completitud, Puntualidad, Priorización, Consistencia, Velocidad
- **Recomendaciones inteligentes** basadas en métricas
- **Dashboard interactivo** con visualizaciones

### 📤 Sistema de Reportes
- **Exportación multi-formato**: CSV, JSON, TXT
- **Reportes ejecutivos** con estadísticas completas
- **Timestamps automáticos** en nombres de archivo

### 🏗️ Arquitectura Profesional
- **Patrón Managers** para separación de responsabilidades
- **Factory Pattern** para almacenamiento intercambiable
- **Models** con validaciones y lógica de negocio

## 🛠️ Tecnologías Utilizadas

- **Python 3.8+**
- **SQLite** - Base de datos embebida
- **Arquitectura por capas** - Models, Managers, Storage, Analytics
- **Sistema de import/export** con CSV, JSON

## 📦 Instalación y Ejecución

1. **Clonar repositorio:**
   ```bash
   git clone https://github.com/tu_usuario/taskmaster-analytics.git
   cd taskmaster-analytics