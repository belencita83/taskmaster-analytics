import pytest
import sys
import os
from unittest.mock import Mock, MagicMock

# Agregar el directorio root al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def sample_tarea_data():
    """Datos de ejemplo para crear tareas."""
    return {
        'titulo': 'Tarea de prueba',
        'descripcion': 'Descripción de prueba',
        'prioridad': 'media',
        'proyecto': 'Proyecto Test',
        'usuario': 'test_user'
    }

@pytest.fixture
def mock_storage():
    """Mock del GestorAlmacenamiento para pruebas unitarias."""
    mock = Mock()
    mock.cargar_tareas.return_value = []
    mock.guardar_tarea.return_value = True
    return mock

@pytest.fixture
def sample_tareas():
    """Lista de tareas de ejemplo que coincida con el modelo real."""
    from core.models import Tarea
    
    tareas = [
        Tarea(titulo="Tarea 1", prioridad="alta", usuario="test_user"),
        Tarea(titulo="Tarea 2", prioridad="media", usuario="test_user"), 
        Tarea(titulo="Tarea 3", prioridad="baja", usuario="test_user"),
    ]
    
    # Configurar estados EXPLÍCITAMENTE y DIFERENTES
    tareas[0].estado = "completada"    # Solo esta debe aparecer en el filtro
    tareas[1].estado = "en_progreso"   # No debe aparecer
    tareas[2].estado = "pendiente"     # No debe aparecer
    
    return tareas