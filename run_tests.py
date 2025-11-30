#!/usr/bin/env python3
"""
Script para ejecutar todas las pruebas automáticamente.
"""
import subprocess
import sys

def run_tests():
    print("EJECUTANDO SUITE DE PRUEBAS COMPLETA")
    print("=" * 60)
    
    commands = [
        ("Pruebas unitarias básicas", ["pytest", "tests/unit/", "-v"]),
        ("Pruebas con cobertura", ["pytest", "--cov=core", "--cov=tui_app", "--cov-report=term-missing"]),
        ("Pruebas de integración", ["pytest", "tests/integration/", "-v", "-m", "integration"]),
        ("Pruebas de rendimiento", ["pytest", "tests/performance/", "-v", "-m", "slow"]),
    ]
    
    for name, cmd in commands:
        print(f"\n📋 EJECUTANDO: {name}")
        print("-" * 40)
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            print(result.stdout)
            if result.stderr:
                print("❌ ERRORES:", result.stderr)
        except Exception as e:
            print(f"❌ Error ejecutando {name}: {e}")
    
    print("=" * 60)
    print("🎉 SUITE DE PRUEBAS COMPLETADA")

if __name__ == "__main__":
    run_tests()