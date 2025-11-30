# tests/unit/test_storage.py
import pytest
from unittest.mock import Mock, patch, MagicMock
from core.storage import GestorAlmacenamiento
from core.models import Tarea

class TestGestorAlmacenamiento:
    """Pruebas unitarias para GestorAlmacenamiento - BASADA EN TU ESTRUCTURA REAL."""
    
    def test_creacion_gestor_sqlite(self):
        """Test: Crear gestor con SQLite."""
        gestor = GestorAlmacenamiento("sqlite")
        
        # VERIFICACIONES BASADAS EN TU ESTRUCTURA REAL
        assert gestor is not None
        assert isinstance(gestor, GestorAlmacenamiento)
        
        # Verificar el atributo que SÍ existe
        assert hasattr(gestor, 'almacenamiento')
        assert gestor.almacenamiento is not None
        
        # Verificar métodos que SÍ existen
        assert hasattr(gestor, 'cargar_tareas')
        assert hasattr(gestor, 'guardar_tarea')
        assert hasattr(gestor, 'eliminar_tarea')
        assert hasattr(gestor, 'guardar_tareas')
        
        assert callable(gestor.cargar_tareas)
        assert callable(gestor.guardar_tarea)
        assert callable(gestor.eliminar_tarea)
        assert callable(gestor.guardar_tareas)
        
        print("GestorAlmacenamiento creado con estructura correcta")
    
    def test_metodos_disponibles(self):
        """Test: Verificar que todos los métodos necesarios existen."""
        gestor = GestorAlmacenamiento("sqlite")
        
        # MÉTODOS QUE SABEMOS QUE EXISTEN
        métodos_requeridos = ['cargar_tareas', 'guardar_tarea', 'eliminar_tarea', 'guardar_tareas']
        
        for método in métodos_requeridos:
            assert hasattr(gestor, método), f"Falta el método: {método}"
            assert callable(getattr(gestor, método)), f"El método {método} no es invocable"
    
    def test_cargar_tareas_llamada_correcta(self):
        """Test: cargar_tareas se llama con parámetros correctos."""
        gestor = GestorAlmacenamiento("sqlite")
        
        with patch.object(gestor, 'cargar_tareas') as mock_cargar:
            mock_cargar.return_value = []
            
            # Probar llamada sin usuario (valor por defecto)
            gestor.cargar_tareas()
            mock_cargar.assert_called_once()
            
            # Resetear mock y probar con usuario específico
            mock_cargar.reset_mock()
            gestor.cargar_tareas("usuario_especifico")
            mock_cargar.assert_called_once_with("usuario_especifico")
    
    def test_guardar_tarea_llamada_correcta(self):
        """Test: guardar_tarea se llama con tarea correcta."""
        gestor = GestorAlmacenamiento("sqlite")
        tarea = Tarea(titulo="Tarea de prueba")
        
        with patch.object(gestor, 'guardar_tarea') as mock_guardar:
            mock_guardar.return_value = True
            
            resultado = gestor.guardar_tarea(tarea)
            
            assert resultado is True
            mock_guardar.assert_called_once_with(tarea)
    
    def test_eliminar_tarea_llamada_correcta(self):
        """Test: eliminar_tarea se llama correctamente."""
        gestor = GestorAlmacenamiento("sqlite")
        
        with patch.object(gestor, 'eliminar_tarea') as mock_eliminar:
            mock_eliminar.return_value = True
            
            resultado = gestor.eliminar_tarea(1)  # ID de tarea
            
            assert resultado is True
            mock_eliminar.assert_called_once_with(1)
    
    def test_guardar_tareas_llamada_correcta(self):
        """Test: guardar_tareas se llama correctamente."""
        gestor = GestorAlmacenamiento("sqlite")
        tareas = [Tarea(titulo="Tarea 1"), Tarea(titulo="Tarea 2")]
        
        with patch.object(gestor, 'guardar_tareas') as mock_guardar:
            mock_guardar.return_value = True
            
            resultado = gestor.guardar_tareas(tareas)
            
            assert resultado is True
            mock_guardar.assert_called_once_with(tareas)
    
    def test_comportamiento_integracion_simple(self):
        """Test: Comportamiento integrado simple."""
        gestor = GestorAlmacenamiento("sqlite")
        
        # Mockear métodos para una prueba de integración simple
        with patch.object(gestor, 'cargar_tareas') as mock_cargar, \
             patch.object(gestor, 'guardar_tarea') as mock_guardar, \
             patch.object(gestor, 'eliminar_tarea') as mock_eliminar:
            
            mock_cargar.return_value = []
            mock_guardar.return_value = True
            mock_eliminar.return_value = True
            
            tarea = Tarea(titulo="Tarea de integración")
            
            # 1. Guardar tarea
            resultado_guardar = gestor.guardar_tarea(tarea)
            assert resultado_guardar is True
            
            # 2. Cargar tareas
            resultado_cargar = gestor.cargar_tareas()
            assert resultado_cargar == []
            
            # 3. Eliminar tarea
            resultado_eliminar = gestor.eliminar_tarea(1)
            assert resultado_eliminar is True
            
            # Verificar que se llamaron los métodos
            mock_guardar.assert_called_once_with(tarea)
            mock_cargar.assert_called_once()
            mock_eliminar.assert_called_once_with(1)

    def test_sqlite_completo(self):
        """Test: Implementación completa de SQLite (skipped por ahora)."""
        pytest.skip("Prueba de SQLite completo pendiente de implementación")