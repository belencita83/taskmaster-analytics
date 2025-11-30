# tests/unit/test_edge_cases.py
import pytest
from core.managers import TareaManager
from core.models import Tarea
from unittest.mock import Mock

class TestCasosBorde:
    """Pruebas para casos borde y manejo de errores."""
    
    def test_titulo_muy_largo(self, mock_storage):
        """Test: Título extremadamente largo."""
        manager = TareaManager(mock_storage)
        
        titulo_largo = "A" * 1000  # Título muy largo
        
        # Esto debería manejarse gracefulmente
        tarea = manager.crear_tarea(titulo=titulo_largo, prioridad="media")
        
        assert len(tarea.titulo) == 1000
        # Depende de tus validaciones - podría truncarse o lanzar error
    
    def test_caracteres_especiales(self, mock_storage):
        """Test: Título con caracteres especiales."""
        manager = TareaManager(mock_storage)
        
        titulo_especial = "Tarea con ñ, áéíóú y símbolos! @#$%"
        
        tarea = manager.crear_tarea(titulo=titulo_especial, prioridad="media")
        
        assert tarea.titulo == titulo_especial
    
    def test_prioridad_case_sensitive(self, mock_storage):
        """Test: Las prioridades son case sensitive?"""
        manager = TareaManager(mock_storage)
        
        # Depende de tu implementación
        try:
            tarea = manager.crear_tarea(titulo="Test", prioridad="ALTA")  # Mayúsculas
            # Si no lanza error, verificar el valor
            assert tarea.prioridad == "ALTA" or tarea.prioridad == "alta"
        except ValueError:
            # Si lanza error, eso también es válido
            pass