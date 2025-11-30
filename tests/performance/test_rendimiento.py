# tests/performance/test_rendimiento.py
import pytest
import time
from core.managers import TareaManager
from core.storage import GestorAlmacenamiento
from unittest.mock import Mock

class TestRendimiento:
    """Pruebas de rendimiento (opcionales)."""
    
    @pytest.mark.slow
    def test_rendimiento_creacion_multiples_tareas(self):
        """Test: Rendimiento al crear múltiples tareas."""
        mock_storage = Mock()
        manager = TareaManager(mock_storage)
        
        start_time = time.time()
        
        # Crear 100 tareas
        for i in range(100):
            manager.crear_tarea(
                titulo=f"Tarea de rendimiento {i}",
                prioridad="media",
                usuario="test_user"
            )
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Verificar que toma menos de 1 segundo
        assert execution_time < 1.0
        print(f"⏱ 100 tareas creadas en {execution_time:.2f} segundos")
    
    @pytest.mark.slow  
    def test_rendimiento_carga_tareas(self):
        """Test: Rendimiento al cargar muchas tareas."""
        # Crear mock con muchas tareas
        mock_tareas = [Mock(titulo=f"Tarea {i}") for i in range(1000)]
        mock_storage = Mock()
        mock_storage.cargar_tareas.return_value = mock_tareas
        
        manager = TareaManager(mock_storage)
        
        start_time = time.time()
        tareas = manager.obtener_tareas_por_estado("pendiente")
        end_time = time.time()
        
        execution_time = end_time - start_time
        
        # Verificar que es rápido incluso con muchas tareas
        assert execution_time < 0.1
        print(f"⏱ 1000 tareas filtradas en {execution_time:.3f} segundos")