#!/usr/bin/env python3
"""
Agregar verificaciones de None para resultado_mckinsey
"""

with open("utils/pdf_mckinsey_generator.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

print("🔧 Agregando verificaciones de None...")

# Al inicio de la función generar_pdf_mckinsey, agregar validación
for i in range(len(lines)):
    if "def generar_pdf_mckinsey(" in lines[i]:
        # Buscar dónde termina el docstring
        j = i + 1
        while j < len(lines) and '"""' not in lines[j]:
            j += 1
        if j < len(lines):
            j += 1  # Pasar el cierre del docstring
            
            # Insertar validación
            validation = """
    # Validar parámetros para evitar errores NoneType
    if resultado_mckinsey is None:
        print("⚠️ resultado_mckinsey es None, usando valores por defecto")
        resultado_mckinsey = {
            'enterprise_value': 0,
            'equity_value': 0,
            'tir': 0,
            'wacc': 0,
            'roic_promedio': 0,
            'fcf_proyectados': [],
            'valor_terminal': 0,
            'pv_terminal': 0,
            'pv_fcf': 0,
            'deuda_neta': 0,
            'componentes_wacc': {}
        }
    
    if datos_empresa is None:
        datos_empresa = {}
    
    if pyl_df is None:
        pyl_df = pd.DataFrame()
    
    if balance_df is None:
        balance_df = pd.DataFrame()
    
    if fcf_df is None:
        fcf_df = pd.DataFrame()
    
    if analisis_ia is None:
        analisis_ia = {}
    
    if metricas is None:
        metricas = {}
    
"""
            lines.insert(j, validation)
            print(f"✅ Agregadas validaciones en línea {j+1}")
            break

# También arreglar líneas específicas que causan problemas
# Línea problemática en 339 y 1292: resultado_mckinsey['datos_empresa']
for i in range(len(lines)):
    if "resultado_mckinsey['datos_empresa']" in lines[i]:
        # Cambiar a acceso seguro
        lines[i] = lines[i].replace(
            "resultado_mckinsey['datos_empresa']",
            "resultado_mckinsey.get('datos_empresa', {})"
        )
        print(f"✅ Arreglada línea {i+1}: acceso seguro a datos_empresa")

# Línea problemática en 344: resultado_mckinsey['pyl']
for i in range(len(lines)):
    if "resultado_mckinsey['pyl']" in lines[i]:
        lines[i] = lines[i].replace(
            "resultado_mckinsey['pyl']",
            "resultado_mckinsey.get('pyl', [])"
        )
        print(f"✅ Arreglada línea {i+1}: acceso seguro a pyl")

# Guardar cambios
with open("utils/pdf_mckinsey_generator.py", "w", encoding="utf-8") as f:
    f.writelines(lines)

print("\n✅ Todas las verificaciones de None agregadas")
print("✅ Accesos inseguros corregidos")

