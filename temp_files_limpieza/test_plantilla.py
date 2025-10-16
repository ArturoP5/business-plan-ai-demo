#!/usr/bin/env python3
"""
Script de prueba para generar y revisar la plantilla Excel
"""

from utils.plantilla_excel_completa import crear_plantilla_completa
from datetime import datetime

print("🔄 Generando plantilla Excel de prueba...")

try:
    # Generar la plantilla
    excel_data = crear_plantilla_completa()
    
    # Guardar el archivo
    filename = f"TEST_plantilla_{datetime.now().strftime('%H%M%S')}.xlsx"
    with open(filename, 'wb') as f:
        f.write(excel_data.getvalue())
    
    print(f"✅ Plantilla generada exitosamente: {filename}")
    print("\n📋 La plantilla incluye:")
    print("  1. Información General (con descripción del negocio)")
    print("  2. Datos Históricos PYL")
    print("  3. Balance - Activo")
    print("  4. Balance - Pasivo")
    print("  5. Balance - Patrimonio")
    print("  6. Datos Laborales")
    print("  7. Líneas Financiación (con 9 nuevos tipos)")
    print("  8. Proyecciones y Parámetros")
    print("\n🎯 Características especiales:")
    print("  - Múltiples líneas del mismo tipo permitidas")
    print("  - Campos de descripción del negocio")
    print("  - 100% compatible con leer_excel_datos()")
    
except Exception as e:
    print(f"❌ Error: {e}")
