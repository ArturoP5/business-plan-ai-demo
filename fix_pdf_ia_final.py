#!/usr/bin/env python3
"""
Arregla definitivamente el PDF con IA:
1. Corrige el mapeo de resultado_mckinsey
2. Mejora formato de tablas
"""

with open('app.py', 'r') as f:
    lines = f.readlines()

# Buscar y corregir el mapeo de financial_data (alrededor de línea 5359)
for i in range(5355, 5365):
    if "'enterprise_value': datos.get('resultado_mck'" in lines[i]:
        # Cambiar resultado_mck por resultado_mckinsey
        lines[i] = "                                                'enterprise_value': datos.get('resultado_mckinsey', {}).get('enterprise_value', 0),\n"
        lines[i+1] = "                                                'wacc': datos.get('resultado_mckinsey', {}).get('wacc', 0),\n"
        lines[i+2] = "                                                'tir': datos.get('resultado_mckinsey', {}).get('tir_proyecto', 0),\n"
        lines[i+3] = "                                                'payback': datos.get('resultado_mckinsey', {}).get('payback_years', 0)\n"
        print("✅ Corregido mapeo: resultado_mck → resultado_mckinsey")
        break

with open('app.py', 'w') as f:
    f.writelines(lines)

# Ahora arreglar formato de tablas en el PDF
with open('utils/pdf_ai_generator_completo.py', 'r') as f:
    pdf_content = f.read()

# Cambiar anchos para matriz de riesgos (más espacio para mitigación)
pdf_content = pdf_content.replace(
    "colWidths=[5*cm, 2*cm, 2*cm, 7*cm]",
    "colWidths=[4*cm, 2.5*cm, 2.5*cm, 6.5*cm]"
)

# Cambiar anchos para KPIs (más espacio para objetivo)
pdf_content = pdf_content.replace(
    "colWidths=[4*cm, 5*cm, 2.5*cm, 3.5*cm]",
    "colWidths=[3.5*cm, 6*cm, 2.5*cm, 4*cm]"
)

# Reducir tamaño de fuente en estilos normales para que quepa más texto
pdf_content = pdf_content.replace(
    "fontSize=10,",
    "fontSize=9,"
)

with open('utils/pdf_ai_generator_completo.py', 'w') as f:
    f.write(pdf_content)

print("\n✅ Arreglos aplicados:")
print("  - Mapeo corregido: busca 'resultado_mckinsey' (nombre correcto)")
print("  - Anchos de columnas optimizados")
print("  - Tamaño de fuente ajustado")
