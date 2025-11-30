import pytest
from datetime import datetime
from unittest.mock import Mock, patch
from core.managers import TareaManager
from core.models import Tarea

class TestTareaManager:
    """Pruebas unitarias para TareaManager."""
    
    def test_crear_tarea_exitosa(self, mock_storage, sample_tarea_data):
        """Test: Crear tarea exitosamente."""
        manager = TareaManager(mock_storage)
        
        # Configurar el mock para devolver una tarea simulada
        tarea_simulada = Tarea(**sample_tarea_data)
        tarea_simulada.id = 1
        mock_storage.guardar_tarea.return_value = True
        
        # Ejecutar
        tarea_creada = manager.crear_tarea(**sample_tarea_data)
        
        # Verificar
        assert tarea_creada.titulo == sample_tarea_data['titulo']
        assert tarea_creada.descripcion == sample_tarea_data['descripcion']
        assert tarea_creada.prioridad == sample_tarea_data['prioridad']
        assert tarea_creada.proyecto == sample_tarea_data['proyecto']
        assert tarea_creada.usuario == sample_tarea_data['usuario']
        assert isinstance(tarea_creada.fecha_creacion, datetime)
        mock_storage.guardar_tarea.assert_called_once()
    
    def test_crear_tarea_titulo_vacio(self, mock_storage):
        """Test: Error al crear tarea con título vacío."""
        manager = TareaManager(mock_storage)
        
        with pytest.raises(ValueError, match="El título de la tarea no puede estar vacío"):
            manager.crear_tarea(titulo="", prioridad="media")
        
        # Verificar que no se llamó a guardar
        mock_storage.guardar_tarea.assert_not_called()
    
    def test_crear_tarea_prioridad_invalida(self, mock_storage):
        """Test: Error al crear tarea con prioridad inválida."""
        manager = TareaManager(mock_storage)
        
        with pytest.raises(ValueError, match="Prioridad debe ser: baja, media o alta"):
            manager.crear_tarea(titulo="Tarea", prioridad="urgente")
        
        mock_storage.guardar_tarea.assert_not_called()
    
    # tests/unit/test_managers.py - CORREGIR ESTA PRUEBA
    def test_obtener_tareas_por_estado(self, mock_storage, sample_tareas):
        """Test: Obtener tareas filtradas por estado."""
        manager = TareaManager(mock_storage)
        
        # Configurar mock para devolver tareas de ejemplo
        mock_storage.cargar_tareas.return_value = sample_tareas
        
        # VERIFICAR LOS ESTADOS ACTUALES DE LAS TAREAS
        print(f"🔍 Estados de tareas: {[t.estado for t in sample_tareas]}")
        
        # Ejecutar - buscar tareas completadas
        tareas_completadas = manager.obtener_tareas_por_estado("completada")
        
        # Verificar - CONTAR CUÁNTAS TIENEN ESTADO "completada"
        tareas_completadas_count = sum(1 for t in sample_tareas if t.estado == "completada")
        assert len(tareas_completadas) == tareas_completadas_count
        
        # VERIFICAR QUE TODAS LAS TAREAS DEVUELTAS TIENEN EL ESTADO CORRECTO
        assert all(t.estado == "completada" for t in tareas_completadas)
        
        mock_storage.cargar_tareas.assert_called_once()
    
    def test_obtener_tareas_por_proyecto(self, mock_storage, sample_tareas):
        """Test: Obtener tareas filtradas por proyecto."""
        manager = TareaManager(mock_storage)
        
        # Configurar tareas con proyectos
        sample_tareas[0].proyecto = "Proyecto A"
        sample_tareas[1].proyecto = "Proyecto B"
        sample_tareas[2].proyecto = "Proyecto A"
        
        mock_storage.cargar_tareas.return_value = sample_tareas
        
        # Ejecutar
        tareas_proyecto_a = manager.obtener_tareas_por_proyecto("Proyecto A")
        
        # Verificar
        assert len(tareas_proyecto_a) == 2
        assert all(t.proyecto == "Proyecto A" for t in tareas_proyecto_a)
    
    def test_obtener_tareas_vencidas(self, mock_storage):
        """Test: Obtener tareas vencidas."""
        manager = TareaManager(mock_storage)
        
        from datetime import datetime, timedelta
        
        # Crear tareas de prueba con fechas
        tarea_vencida = Tarea(titulo="Vencida")
        tarea_vencida.estado = "pendiente"
        tarea_vencida.fecha_vencimiento = (datetime.now() - timedelta(days=1)).isoformat()
        
        tarea_no_vencida = Tarea(titulo="No vencida") 
        tarea_no_vencida.estado = "pendiente"
        tarea_no_vencida.fecha_vencimiento = (datetime.now() + timedelta(days=1)).isoformat()
        
        mock_storage.cargar_tareas.return_value = [tarea_vencida, tarea_no_vencida]
        
        # Ejecutar
        tareas_vencidas = manager.obtener_tareas_vencidas()
        
        # Verificar
        assert len(tareas_vencidas) == 1
        assert tareas_vencidas[0].titulo == "Vencida"
    
    def test_obtener_tareas_proximas_a_vencer(self, mock_storage):
        """Test: Obtener tareas próximas a vencer."""
        manager = TareaManager(mock_storage)
        
        from datetime import datetime, timedelta
        
        # Crear tareas de prueba
        tarea_proxima = Tarea(titulo="Próxima")
        tarea_proxima.estado = "pendiente"
        tarea_proxima.fecha_vencimiento = (datetime.now() + timedelta(days=2)).isoformat()
        
        tarea_lejana = Tarea(titulo="Lejana")
        tarea_lejana.estado = "pendiente" 
        tarea_lejana.fecha_vencimiento = (datetime.now() + timedelta(days=10)).isoformat()
        
        mock_storage.cargar_tareas.return_value = [tarea_proxima, tarea_lejana]
        
        # Ejecutar (buscar próximas 3 días)
        tareas_proximas = manager.obtener_tareas_proximas_a_vencer(dias=3)
        
        # Verificar
        assert len(tareas_proximas) == 1
        assert tareas_proximas[0].titulo == "Próxima"