#!/usr/bin/env python3
"""
Arregla la integración del PDF profesional en las líneas correctas
"""

with open('app.py', 'r') as f:
    lines = f.readlines()

# Cambiar import en línea 5312
if 'from utils.pdf_ai_generator_completo import generate_complete_ai_pdf' in lines[5311]:
    lines[5311] = "                            from utils.pdf_valoracion_profesional import generate_professional_valuation_report\n"
    print("✅ Cambiado import en línea 5312")

# Cambiar llamada en línea 5375
if 'pdf_buffer = generate_complete_ai_pdf(datos, ai_analysis)' in lines[5374]:
    lines[5374] = "                                            pdf_buffer = generate_professional_valuation_report(datos, ai_analysis)\n"
    print("✅ Cambiada llamada en línea 5375")

# Guardar
with open('app.py', 'w') as f:
    f.writelines(lines)

print("\n✅ Integración corregida en las líneas correctas")
