import pytest
from unittest.mock import Mock, patch, MagicMock
from tui_app.controllers.tarea_controller import TareaController

class TestTareaController:
    """Pruebas unitarias para TareaController."""
    
    @pytest.fixture
    def controller(self, mock_storage):
        """Fixture del controlador con storage mock."""
        with patch('tui_app.controllers.tarea_controller.GestorAlmacenamiento') as mock_gestor:
            with patch('tui_app.controllers.tarea_controller.TareaManager') as mock_manager:
                mock_gestor.return_value = mock_storage
                mock_manager.return_value = Mock()
                return TareaController()
    
    def test_crear_tarea_exitosa(self, controller, sample_tarea_data):
        """Test: Crear tarea exitosamente a través del controlador."""
        # Configurar mocks
        tarea_mock = Mock()
        tarea_mock.id = 1
        tarea_mock.titulo = sample_tarea_data['titulo']
        tarea_mock.prioridad = sample_tarea_data['prioridad']
        
        controller.manager.crear_tarea.return_value = tarea_mock
        
        # Ejecutar
        resultado = controller.crear_tarea(sample_tarea_data)
        
        # Verificar
        assert resultado['success'] is True
        assert "ÉXITO" in resultado['message']
        assert "creada" in resultado['message']
        assert resultado['data']['id'] == 1
        controller.manager.crear_tarea.assert_called_once()
    
    def test_crear_tarea_titulo_vacio(self, controller):
        """Test: Error al crear tarea con título vacío."""
        form_data = {
            'titulo': '',
            'prioridad': 'media'
        }
        
        resultado = controller.crear_tarea(form_data)
        
        assert resultado['success'] is False
        assert "obligatorio" in resultado['message']
        controller.manager.crear_tarea.assert_not_called()
    
    def test_crear_tarea_error_validacion(self, controller, sample_tarea_data):
        """Test: Error de validación del manager."""
        controller.manager.crear_tarea.side_effect = ValueError("Prioridad inválida")
        
        resultado = controller.crear_tarea(sample_tarea_data)
        
        assert resultado['success'] is False
        assert "Prioridad inválida" in resultado['message']
    
    def test_obtener_todas_tareas_exitoso(self, controller, sample_tareas):
        """Test: Obtener todas las tareas exitosamente."""
        controller.gestor.cargar_tareas.return_value = sample_tareas
        
        resultado = controller.obtener_todas_tareas()
        
        assert resultado['success'] is True
        assert len(resultado['data']) == len(sample_tareas)
        assert "Encontradas" in resultado['message']
        controller.gestor.cargar_tareas.assert_called_once()
    
    def test_obtener_todas_tareas_error(self, controller):
        """Test: Error al obtener tareas."""
        controller.gestor.cargar_tareas.side_effect = Exception("Error de base de datos")
        
        resultado = controller.obtener_todas_tareas()
        
        assert resultado['success'] is False
        assert "Error" in resultado['message']
        assert resultado['data'] == []
    
    def test_buscar_tareas(self, controller, sample_tareas):
        """Test: Buscar tareas por término."""
        controller.gestor.cargar_tareas.return_value = sample_tareas
        
        resultado = controller.buscar_tareas("Tarea 1")
        
        assert resultado['success'] is True
        # Debería encontrar solo la tarea que contiene "Tarea 1"
        assert any("Tarea 1" in tarea['titulo'] for tarea in resultado['data'])
    
    def test_cambiar_estado_tarea_exitoso(self, controller, sample_tareas):
        """Test: Cambiar estado de tarea exitosamente."""
        tarea = sample_tareas[0]
        tarea.id = 1
        tarea.titulo = "Tarea de prueba"
        tarea.estado = "pendiente"
        
        controller.gestor.cargar_tareas.return_value = sample_tareas
        
        resultado = controller.cambiar_estado_tarea(1)
        
        assert resultado['success'] is True
        assert "ahora está" in resultado['message']
        controller.gestor.guardar_tarea.assert_called_once()
    
    def test_cambiar_estado_tarea_no_encontrada(self, controller):
        """Test: Error al cambiar estado de tarea no encontrada."""
        controller.gestor.cargar_tareas.return_value = []
        
        resultado = controller.cambiar_estado_tarea(999)
        
        assert resultado['success'] is False
        assert "no encontrada" in resultado['message']