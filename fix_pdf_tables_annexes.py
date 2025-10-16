#!/usr/bin/env python3
"""
Arregla el ancho de las columnas en las tablas y agrega los anexos financieros
"""

# 1. Arreglar las columnas de las tablas en pdf_ai_generator_completo.py
with open('utils/pdf_ai_generator_completo.py', 'r') as f:
    content = f.read()

# Arreglar matriz de riesgos - cambiar anchos de columnas
content = content.replace(
    "colWidths=[5*cm, 3*cm, 3*cm, 5*cm]",
    "colWidths=[4*cm, 2.5*cm, 2.5*cm, 7*cm]"  # Más espacio para mitigación
)

# Arreglar KPIs - cambiar anchos
content = content.replace(
    "colWidths=[5*cm, 4*cm, 3*cm, 4*cm]",
    "colWidths=[4*cm, 5*cm, 2.5*cm, 3.5*cm]"  # Más espacio para objetivo
)

# Guardar cambios
with open('utils/pdf_ai_generator_completo.py', 'w') as f:
    f.write(content)

print("✅ Anchos de columnas ajustados")

# 2. Arreglar la forma de pasar los anexos en app.py
with open('app.py', 'r') as f:
    lines = f.readlines()

# Buscar donde se prepara el PDF con IA (alrededor de línea 5355)
for i in range(5350, 5370):
    if "'pyl' in datos:" in lines[i]:
        # Reemplazar con la asignación correcta
        new_code = """                                            # Agregar datos reales para anexos
                                            datos['pyl'] = datos.get('pyl', None)
                                            datos['balance'] = datos.get('balance', None) 
                                            datos['fcf'] = datos.get('resultado_mckinsey', {}).get('fcf_proyectado', None)
                                            
"""
        lines[i:i+4] = [new_code]
        print(f"✅ Arreglada asignación de anexos en línea {i+1}")
        break

# Guardar app.py
with open('app.py', 'w') as f:
    f.writelines(lines)

print("\n✅ Problemas arreglados:")
print("  - Anchos de columnas ajustados para evitar cortes")
print("  - Anexos financieros correctamente asignados")
