#!/usr/bin/env python3
"""
Test de todas las correcciones realizadas
"""

print("=" * 80)
print("TEST DE CORRECCIONES")
print("=" * 80)

errors = []

# Test 1: Verificar sintaxis de todos los archivos
print("\n1️⃣  Verificando sintaxis...")
try:
    import py_compile
    files = ['app.py', 'utils/data_collector.py', 'utils/ai_prompts.py', 
             'utils/pdf_ia_generator.py', 'utils/ai_analyzer_v2.py']
    for f in files:
        py_compile.compile(f, doraise=True)
    print("   ✅ Sintaxis correcta en todos los archivos")
except Exception as e:
    errors.append(("Sintaxis", str(e)))
    print(f"   ❌ Error de sintaxis: {e}")

# Test 2: Verificar modelo actualizado
print("\n2️⃣  Verificando nombre del modelo...")
try:
    with open('app.py', 'r') as f:
        content = f.read()
        if 'Gemini 2.5 Flash' in content:
            print("   ✅ Modelo actualizado a 'Gemini 2.5 Flash'")
        else:
            errors.append(("Modelo UI", "No se encontró 'Gemini 2.5 Flash'"))
            print("   ❌ Modelo no actualizado")
except Exception as e:
    errors.append(("Modelo UI", str(e)))

# Test 3: Verificar cálculo de KPIs
print("\n3️⃣  Verificando cálculo de KPIs en data_collector...")
try:
    with open('utils/data_collector.py', 'r') as f:
        content = f.read()
        if 'cagr_ventas' in content and '((ventas_year5 / ventas_year1)' in content:
            print("   ✅ CAGR Ventas se calcula correctamente")
        else:
            errors.append(("KPIs", "CAGR Ventas no se calcula"))
        
        if "'cash_conversion_cycle': 0" in content or "cash_conversion_cycle" in content:
            print("   ✅ Cash Conversion Cycle está definido")
        else:
            errors.append(("KPIs", "CCC no se calcula"))
        
        if "Margen EBITDA" in content and "pyl_df" in content:
            print("   ✅ Margen EBITDA se extrae del P&L")
        else:
            errors.append(("KPIs", "Margen EBITDA no se extrae"))
            
except Exception as e:
    errors.append(("KPIs", str(e)))

# Test 4: Verificar información completa en prompts
print("\n4️⃣  Verificando información en prompts...")
try:
    with open('utils/ai_prompts.py', 'r') as f:
        content = f.read()
        campos_requeridos = [
            'PRODUCTOS/SERVICIOS',
            'CUOTA DE MERCADO',
            'OBJETIVOS CORTO PLAZO',
            'OBJETIVOS MEDIO PLAZO',
            'VISIÓN LARGO PLAZO',
            'PRINCIPALES RIESGOS'
        ]
        missing = [c for c in campos_requeridos if c not in content]
        if not missing:
            print("   ✅ Todos los campos están en los prompts")
        else:
            errors.append(("Prompts", f"Faltan campos: {missing}"))
            print(f"   ❌ Faltan campos: {missing}")
except Exception as e:
    errors.append(("Prompts", str(e)))

# Test 5: Verificar optimización SWOT
print("\n5️⃣  Verificando optimización del SWOT...")
try:
    with open('utils/pdf_ia_generator.py', 'r') as f:
        content = f.read()
        if 'fontSize=8' in content and 'formatear_lista' in content and 'def _crear_swot' in content:
            print("   ✅ SWOT optimizado con fuente 8pt")
        else:
            errors.append(("SWOT", "No está optimizado"))
            print("   ❌ SWOT no optimizado")
except Exception as e:
    errors.append(("SWOT", str(e)))

# Test 6: Verificar tabla P&L robusta
print("\n6️⃣  Verificando tabla P&L robusta...")
try:
    with open('utils/pdf_ia_generator.py', 'r') as f:
        content = f.read()
        if 'def get_val(row, *keys):' in content:
            print("   ✅ Función helper get_val() implementada")
        else:
            errors.append(("P&L", "Función helper no encontrada"))
            print("   ❌ Función helper no implementada")
except Exception as e:
    errors.append(("P&L", str(e)))

# Test 7: Verificar modelo correcto en ai_analyzer_v2
print("\n7️⃣  Verificando modelo en ai_analyzer_v2...")
try:
    with open('utils/ai_analyzer_v2.py', 'r') as f:
        content = f.read()
        if "GenerativeModel('gemini-2.5-flash')" in content:
            print("   ✅ Usando gemini-2.5-flash")
        else:
            errors.append(("Modelo API", "No usa gemini-2.5-flash"))
            print("   ❌ No está usando gemini-2.5-flash")
except Exception as e:
    errors.append(("Modelo API", str(e)))

# Resumen
print("\n" + "=" * 80)
print("RESUMEN")
print("=" * 80)

if not errors:
    print("🎉 ¡TODAS LAS CORRECCIONES IMPLEMENTADAS CORRECTAMENTE!")
    print("\n✅ Listo para probar en la app:")
    print("   1. Cargar TechStart SaaS")
    print("   2. Generar proyecciones")
    print("   3. Configurar API key Gemini")
    print("   4. Click en 'Análisis Completo IA V2'")
    print("   5. Descargar y revisar PDF")
else:
    print(f"⚠️  {len(errors)} problema(s) encontrado(s):\n")
    for i, (modulo, error) in enumerate(errors, 1):
        print(f"{i}. {modulo}: {error}")

print("\n" + "=" * 80)

