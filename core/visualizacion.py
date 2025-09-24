# core/visualizacion.py
class VisualizadorMetricas:
    """Clase para visualizar la matriz de métricas de forma atractiva."""
    
    @staticmethod
    def mostrar_matriz_metricas(matriz):
        """Muestra la matriz de métricas en la consola."""
        print("\n" + "="*70)
        print("🎯 MATRIZ DE MÉTRICAS DE PRODUCTIVIDAD - TASKMASTER ANALYTICS")
        print("="*70)
        
        print(f"📅 Período de análisis: {matriz['periodo_analisis']}")
        print(f"👤 Usuario: {matriz['usuario']}")
        print(f"⭐ SCORE FINAL: {matriz['score_final']}/100")
        print()
        
        # CALIFICACIONES INDIVIDUALES
        print("📊 CALIFICACIONES POR CATEGORÍA:")
        print("-" * 50)
        calificaciones = matriz['calificaciones']
        
        for categoria, puntaje in calificaciones.items():
            barra = "█" * int(puntaje / 5) + " " * (20 - int(puntaje / 5))
            print(f"{categoria.capitalize():12} {puntaje:5.1f}/100 [{barra}]")
        
        print()
        
        # MATRIZ DE PRODUCTIVIDAD POR DÍA
        print("📅 PRODUCTIVIDAD POR DÍA DE LA SEMANA:")
        print("-" * 50)
        matriz_dias = matriz['matriz_productividad']
        
        for dia, datos in matriz_dias.items():
            print(f"{dia:10} | Creadas: {datos['creadas']:2d} | Completadas: {datos['completadas']:2d} | "
                  f"Ratio: {(datos['completadas']/datos['creadas']*100) if datos['creadas'] > 0 else 0:5.1f}%")
        
        print()
        
        # EFICIENCIA POR PROYECTO
        print("📂 EFICIENCIA POR PROYECTO:")
        print("-" * 50)
        eficiencia_proyectos = matriz['eficiencia_proyectos']
        
        for proyecto, datos in eficiencia_proyectos.items():
            if proyecto:  # Evitar proyectos None
                barra = "█" * int(datos['porcentaje_completado'] / 5) + " " * (20 - int(datos['porcentaje_completado'] / 5))
                print(f"{proyecto:15} | {datos['porcentaje_completado']:5.1f}% [{barra}] | "
                      f"Comp: {datos['completadas']}/{datos['total_tareas']}")
        
        # TENDENCIAS
        print("\n📈 TENDENCIA SEMANAL (últimas 4 semanas):")
        print("-" * 50)
        tendencias = list(matriz['analisis_temporal'].items())[-4:]  # Últimas 4 semanas
        
        for semana, datos in tendencias:
            semana_simple = semana.split('-')[1]  # Solo el número de semana
            ratio = (datos['completadas'] / datos['creadas'] * 100) if datos['creadas'] > 0 else 0
            print(f"Semana {semana_simple:2} | Creadas: {datos['creadas']:2d} | "
                  f"Completadas: {datos['completadas']:2d} | Ratio: {ratio:5.1f}%")
    
    @staticmethod
    def generar_recomendaciones(matriz):
        """Genera recomendaciones basadas en las métricas."""
        calificaciones = matriz['calificaciones']
        recomendaciones = []
        
        if calificaciones['completitud'] < 70:
            recomendaciones.append("💡 Enfócate en completar más tareas pendientes")
        
        if calificaciones['puntualidad'] < 80:
            recomendaciones.append("⏰ Mejora el cumplimiento de fechas límite")
        
        if calificaciones['priorizacion'] < 75:
            recomendaciones.append("🎯 Prioriza mejor las tareas de alta importancia")
        
        if calificaciones['consistencia'] < 60:
            recomendaciones.append("📅 Distribuye tu trabajo de manera más uniforme")
        
        if calificaciones['velocidad'] < 70:
            recomendaciones.append("⚡ Trabaja en completar tareas más rápidamente")
        
        if matriz['score_final'] >= 90:
            recomendaciones.append("🎉 ¡Excelente trabajo! Mantén este ritmo")
        elif matriz['score_final'] >= 70:
            recomendaciones.append("👍 Buen desempeño, hay áreas para mejorar")
        else:
            recomendaciones.append("🔧 Enfócate en mejorar tus procesos de trabajo")
        
        return recomendaciones