#!/usr/bin/env python3
"""
Ajusta los anchos de columna para evitar texto cortado
"""

with open('utils/pdf_ai_generator_completo.py', 'r') as f:
    content = f.read()

# Ajustar tabla de riesgos - dar más espacio para mitigación
content = content.replace(
    "colWidths=[4*cm, 2.5*cm, 2.5*cm, 6.5*cm]",
    "colWidths=[3.5*cm, 2*cm, 2*cm, 8.5*cm]"
)

# Ajustar tabla de KPIs - más espacio para objetivos
content = content.replace(
    "colWidths=[3.5*cm, 6*cm, 2.5*cm, 4*cm]",
    "colWidths=[3*cm, 7*cm, 2.5*cm, 3.5*cm]"
)

# Ajustar tabla de benchmarking
content = content.replace(
    "colWidths=[5*cm, 4*cm, 4*cm, 3*cm]",
    "colWidths=[4*cm, 4*cm, 5*cm, 3*cm]"
)

with open('utils/pdf_ai_generator_completo.py', 'w') as f:
    f.write(content)

print("✅ Anchos de tabla ajustados para mejor visualización")
